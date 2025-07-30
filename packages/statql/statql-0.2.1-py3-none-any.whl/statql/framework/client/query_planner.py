from __future__ import annotations

import typing
from dataclasses import dataclass

from statql.common import invert_map, IConnector, IAsyncConnector, IntegrationIdentifier
from .quey_parser import ParsedQuery
from ..common import (
    IPlanNode,
    Term,
    TableColumn,
    AggregationFunction,
    ScalarFunction,
    PopulationPipelineBatch,
    AggregationPipelineBatch,
    Constant,
    StatQLContext,
)
from ..logic import Aggregate, Filter, Limit, Materialize, Order, Project, SampleReservoir, Scan, Reservoir, UpdateReservoir


@dataclass
class ExecutionPlan:
    population_plan: IPlanNode[PopulationPipelineBatch]
    aggregation_plan: IPlanNode[AggregationPipelineBatch]


class Planner:
    @classmethod
    def plan(cls, *, ctx: StatQLContext, parsed_query: ParsedQuery) -> ExecutionPlan:
        all_terms = cls._get_all_terms(parsed_query=parsed_query)

        # ------------- Population Plan -------------
        integration_id_to_connector = cls._get_relevant_connectors(
            catalog_name=parsed_query.from_.catalog_name,
            integration_name=parsed_query.from_.integration_name,
            connectors=ctx.connectors,
        )

        population_plan = Scan(
            integration_id_to_connector=integration_id_to_connector,
            table_path=parsed_query.from_.table_path,
            columns={term for term in all_terms if isinstance(term, TableColumn)},
        )

        if parsed_query.where:
            # If WHERE statement uses scalar function, need to add a projection so that this scalar function will be defined
            if parsed_query.where not in population_plan.get_output_terms():
                # Validating that term is scalar func / constant, otherwise it is not supported in Project
                if not isinstance(parsed_query.where, (ScalarFunction, Constant)):
                    raise RuntimeError(f"Unable to resolve WHERE statement: {type(parsed_query.where).__name__}")

                population_plan = Project(input=population_plan, new_terms={parsed_query.where})

            population_plan = Filter(input=population_plan, condition=parsed_query.where)

        # The reservoir is the thing that connects the population plan and the aggregation plan.
        # Population plan is for populating the reservoir, and aggregation plan is for calculating results based on the reservoir.
        reservoir = Reservoir(table_reservoir_max_size=10_000, terms=population_plan.get_output_terms())  # TODO: configurable
        population_plan = UpdateReservoir(input=population_plan, reservoir=reservoir)

        # ------------- Aggregation Plan -------------
        aggregation_plan = SampleReservoir(reservoir=reservoir)

        aggregation_func_terms = {term for term in all_terms if isinstance(term, AggregationFunction)}

        if not aggregation_func_terms:
            raise SyntaxError("Only aggregation queries are supported (use an aggregation function like COUNT)")

        terms_introduced_in_aggregation_funcs = set()

        for agg_func_term in aggregation_func_terms:
            for agg_func_arg in agg_func_term.get_args():
                if agg_func_arg not in aggregation_plan.get_output_terms():
                    # Validating that term is scalar func / constant, otherwise it is not supported in Project
                    if not isinstance(agg_func_arg, (ScalarFunction, Constant)):
                        raise RuntimeError(f"Unable to resolve aggregation function argument: {agg_func_arg}")

                    terms_introduced_in_aggregation_funcs.add(agg_func_arg)

        terms_introduced_in_group_bys = set()

        for group_by_term in parsed_query.group_bys:
            if group_by_term not in aggregation_plan.get_output_terms():
                # Validating that term is scalar func / constant, otherwise it is not supported in Project
                if not isinstance(group_by_term, (ScalarFunction, Constant)):
                    raise RuntimeError(f"Unable to resolve GROUP BY term: {group_by_term}")

                terms_introduced_in_group_bys.add(group_by_term)

        # If aggregation step relies on scalar function terms that are not available already, add a projection
        if terms_introduced_in_aggregation_funcs or terms_introduced_in_group_bys:
            aggregation_plan = Project(input=aggregation_plan, new_terms=terms_introduced_in_aggregation_funcs | terms_introduced_in_group_bys)

        # Make sure all group by terms are defined
        if unknown_group_bys := parsed_query.group_bys - aggregation_plan.get_output_terms():
            raise SyntaxError(f"Cannot group by unknown terms: {unknown_group_bys}")

        aggregation_plan = Aggregate(input=aggregation_plan, group_bys=parsed_query.group_bys, aggregations=aggregation_func_terms)

        if parsed_query.order_by:
            # If order by relies on scalar function terms that are not available already, add a projection
            if parsed_query.order_by.term not in aggregation_plan.get_output_terms():
                # Validating that term is scalar func / constant, otherwise it is not supported in Project
                if not isinstance(parsed_query.order_by.term, (ScalarFunction, Constant)):
                    raise RuntimeError(f"Unable to resolve ORDER BY term: {parsed_query.order_by.term}")

                aggregation_plan = Project(input=aggregation_plan, new_terms={parsed_query.order_by.term})

            aggregation_plan = Order(input=aggregation_plan, term=parsed_query.order_by.term, desc=parsed_query.order_by.desc)

        if parsed_query.limit is not None:
            if parsed_query.limit < 1:
                raise SyntaxError("Limit must be greater than 0")

            aggregation_plan = Limit(input=aggregation_plan, limit=parsed_query.limit)

        terms_introduced_in_final_selects = set()

        # Check that all terms are either in the group by or are aggregation functions
        for final_term in parsed_query.alias_to_term.values():
            if final_term not in aggregation_plan.get_output_terms():
                # Validating that term is scalar func / constant, otherwise it is not supported in Project
                if not isinstance(final_term, (ScalarFunction, Constant)):
                    raise SyntaxError(f"Unable to resolve SELECT term: {final_term} - is it missing from GROUP BY?")

                terms_introduced_in_final_selects.add(final_term)

        if terms_introduced_in_final_selects:
            aggregation_plan = Project(input=aggregation_plan, new_terms=terms_introduced_in_final_selects)

        aggregation_plan = Materialize(input=aggregation_plan, term_to_alias=invert_map(parsed_query.alias_to_term))

        return ExecutionPlan(population_plan=population_plan, aggregation_plan=aggregation_plan)

    @classmethod
    def _get_relevant_connectors(
        cls, *, catalog_name: str, integration_name: str | None, connectors: typing.Mapping[IntegrationIdentifier, IConnector | IAsyncConnector]
    ) -> typing.Dict[IntegrationIdentifier, IConnector | IAsyncConnector]:
        # First, narrow down by catalog name
        relevant_connectors = {identifier: connector for identifier, connector in connectors.items() if identifier.catalog_name == catalog_name}

        if not relevant_connectors:
            raise SyntaxError(f"Unknown catalog: {catalog_name}")

        if integration_name is not None:
            # Then, if specific integration name is specified, narrow down by integration name
            relevant_connectors = {
                identifier: connector for identifier, connector in relevant_connectors.items()
                if identifier.integration_name == integration_name
            }

            if not relevant_connectors:
                raise SyntaxError(f"Unknown integration: {integration_name}")

        return relevant_connectors

    @classmethod
    def _get_all_terms(cls, *, parsed_query: ParsedQuery) -> typing.Set[Term]:
        stack = []

        stack += list(parsed_query.alias_to_term.values())

        stack += parsed_query.group_bys

        if parsed_query.where:
            stack.append(parsed_query.where)

        all_terms = set()

        while stack:
            curr_term = stack.pop()
            all_terms.add(curr_term)
            stack += curr_term.get_args()

        return all_terms
