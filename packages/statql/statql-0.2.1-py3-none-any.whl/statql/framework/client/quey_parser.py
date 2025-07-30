import typing

from sqlglot import parse_one, expressions as sg, errors as sg_errors

from statql.common import FrozenModel
from ..common import (
    Term,
    ScalarFunction,
    AggregationFunction,
    TableColumn,
    AggregationFunctionNames,
    ScalarFunctionNames,
    Constant,
)
from ..logic import get_scalar_function_cls


class From(FrozenModel):
    catalog_name: str
    integration_name: str | None  # None -> all integrations of that catalog
    table_path: typing.Sequence[str]


class Where(FrozenModel):
    condition: Term


class OrderBy(FrozenModel):
    term: Term
    desc: bool


class ParsedQuery(FrozenModel):
    alias_to_term: typing.Mapping[str, Term]
    from_: From
    where: Term | None
    group_bys: typing.AbstractSet[Term]
    order_by: OrderBy | None
    limit: int | None


class QueryParser:
    @classmethod
    def parse(cls, *, sql: str) -> ParsedQuery:
        try:
            root_expression = parse_one(sql=sql)
        except sg_errors.ParseError as e:
            raise SyntaxError(f"Failed to parse SQL") from e

        if not isinstance(root_expression, sg.Select):
            raise SyntaxError(f"Unsupported root expression type: {type(root_expression).__name__}")

        cls._check_for_unsupported_expressions(root_expression=root_expression)

        from_expression = root_expression.args.get("from")

        if not isinstance(from_expression, sg.From):
            raise SyntaxError(f"Unexpected from expression type: {type(from_expression).__name__}")

        from_ = cls._parse_from(from_expression=from_expression)

        alias_to_selected_term: typing.Dict[str, Term] = {}
        unaliased_selected_terms: typing.Set[Term] = set()

        for select in root_expression.selects:
            if isinstance(select, sg.Alias):
                term = cls._resolve_term(exp=select.this, known_terms_by_alias={})
                alias_to_selected_term[select.alias] = term
            else:
                term = cls._resolve_term(exp=select, known_terms_by_alias={})
                unaliased_selected_terms.add(term)

        if where := root_expression.args.get("where"):
            where = cls._resolve_term(exp=where.this, known_terms_by_alias=alias_to_selected_term)
        else:
            where = None

        group_bys = set()

        if group_by_expressions := root_expression.args.get("group"):
            for group_by_exp in group_by_expressions:
                group_by_term = cls._resolve_term(exp=group_by_exp, known_terms_by_alias=alias_to_selected_term)
                group_bys.add(group_by_term)

        if order_by_exp := root_expression.args.get("order"):
            order_by = cls._parse_order_by(order_by=order_by_exp, known_terms_by_alias=alias_to_selected_term)
        else:
            order_by = None

        if limit := root_expression.args.get("limit"):
            limit = cls._parse_limit(limit=limit)
        else:
            limit = None

        return ParsedQuery(
            alias_to_term=alias_to_selected_term | {term.get_name(): term for term in unaliased_selected_terms},
            from_=from_,
            where=where,
            group_bys=group_bys,
            order_by=order_by,
            limit=limit,
        )

    @classmethod
    def _check_for_unsupported_expressions(cls, *, root_expression: sg.Select):
        # Checking for unsupported expressions
        if root_expression.args.get("joins"):
            raise SyntaxError(f"JOIN is not supported")

        if root_expression.args.get("having"):
            raise SyntaxError(f"HAVING is not supported")

    @classmethod
    def _parse_from(cls, *, from_expression: sg.From) -> From:
        target = from_expression.this

        if not isinstance(target, sg.Table):
            raise SyntaxError(f"Unexpected from expression target type: {type(target).__name__}")

        target_parts = target.sql().split(".")

        if len(target_parts) < 3:
            raise SyntaxError(f"Invalid target: {target.sql()}")

        catalog_name = target_parts[0]
        integration_name = target_parts[1]
        table_path = target_parts[2:]

        return From(
            catalog_name=catalog_name,
            integration_name=None if integration_name == "?" else integration_name,
            table_path=table_path,
        )

    @classmethod
    def _resolve_term(cls, *, exp: sg.Expression, known_terms_by_alias: typing.Mapping[str, Term]) -> Term:
        # TODO - stop this monstrosity, functions should be defined in one placed and parsed dynamically!
        if isinstance(exp, sg.Count):
            if exp.this:
                argument = cls._resolve_term(exp=exp.this, known_terms_by_alias=known_terms_by_alias)
                return AggregationFunction(func_name=AggregationFunctionNames.COUNT, argument=argument)
            else:
                return AggregationFunction(func_name=AggregationFunctionNames.COUNT, argument=None)

        elif isinstance(exp, sg.Sum):
            if not exp.this:
                raise SyntaxError("SUM must receive an argument")

            argument = cls._resolve_term(exp=exp.this, known_terms_by_alias=known_terms_by_alias)
            return AggregationFunction(func_name=AggregationFunctionNames.SUM, argument=argument)

        elif isinstance(exp, sg.Avg):
            if not exp.this:
                raise SyntaxError("AVG must receive an argument")

            argument = cls._resolve_term(exp=exp.this, known_terms_by_alias=known_terms_by_alias)
            return AggregationFunction(func_name=AggregationFunctionNames.AVG, argument=argument)

        elif isinstance(exp, sg.Binary):
            # Binary scalar functions (functions two operands)
            try:
                func_name = ScalarFunctionNames(exp.key)
            except ValueError as e:
                raise SyntaxError(f"Unknown scalar function: {exp.key}") from e

            left = cls._resolve_term(exp=exp.left, known_terms_by_alias=known_terms_by_alias)
            right = cls._resolve_term(exp=exp.right, known_terms_by_alias=known_terms_by_alias)
            return ScalarFunction(func_name=func_name, arguments=(left, right))

        elif isinstance(exp, sg.Split):
            to_split = exp.this
            split_by = exp.expression

            if not to_split or not split_by:
                raise SyntaxError("Split is missing arguments")

            return ScalarFunction(
                func_name=ScalarFunctionNames.SPLIT,
                arguments=(
                    cls._resolve_term(exp=to_split, known_terms_by_alias=known_terms_by_alias),
                    cls._resolve_term(exp=split_by, known_terms_by_alias=known_terms_by_alias),
                ),
            )

        elif isinstance(exp, sg.Concat):
            arguments = [cls._resolve_term(exp=arg_exp, known_terms_by_alias=known_terms_by_alias) for arg_exp in exp.expressions]
            return ScalarFunction(func_name=ScalarFunctionNames.CONCAT, arguments=tuple(arguments))

        elif isinstance(exp, sg.Anonymous):
            if not exp.this:
                raise ValueError(f"`Anonymous` is missing `this`")

            try:
                scalar_func_name = ScalarFunctionNames(exp.this)
            except ValueError as e:
                raise SyntaxError(f"Unknown scalar function: {exp.this}") from e

            scalar_func_cls = get_scalar_function_cls(func_name=scalar_func_name)

            if len(exp.expressions) != scalar_func_cls.num_args:
                raise SyntaxError(f"Scalar function {scalar_func_name} expects {scalar_func_cls.num_args} args")

            arguments = [cls._resolve_term(exp=arg_exp, known_terms_by_alias=known_terms_by_alias) for arg_exp in exp.expressions]
            return ScalarFunction(func_name=scalar_func_name, arguments=tuple(arguments))

        elif isinstance(exp, sg.Column):
            if exp.this.name in known_terms_by_alias:
                return known_terms_by_alias[exp.this.name]

            return TableColumn(column_name=exp.this.name)

        elif isinstance(exp, sg.Parameter):  # Columns that start with @
            if exp.sql() in known_terms_by_alias:
                return known_terms_by_alias[exp.sql()]

            return TableColumn(column_name=exp.sql())

        elif isinstance(exp, sg.Literal):
            val = exp.this

            try:
                val = int(val)
            except ValueError:
                pass

            return Constant(value=val)

        elif isinstance(exp, sg.Paren):
            return cls._resolve_term(exp=exp.this, known_terms_by_alias=known_terms_by_alias)

        else:
            raise SyntaxError(f"Unsupported expression type {type(exp).__name__}: {exp.sql()}")

    @classmethod
    def _parse_order_by(cls, *, order_by: sg.Order, known_terms_by_alias: typing.Mapping[str, Term]) -> OrderBy:
        if len(order_by.expressions) != 1:
            raise SyntaxError(f"Expected one order expression, got: {len(order_by.expressions)}")

        ordered = order_by.expressions[0]

        if not isinstance(ordered, sg.Ordered):
            raise TypeError(f"Unexpected order type: {type(ordered).__name__}")

        order_by_term = cls._resolve_term(exp=ordered.this, known_terms_by_alias=known_terms_by_alias)
        return OrderBy(term=order_by_term, desc=ordered.args.get("desc") or False)

    @classmethod
    def _parse_limit(cls, *, limit: sg.Limit) -> int:
        exp = limit.expression

        if not isinstance(exp, sg.Literal):
            raise SyntaxError(f"Unexpected limit expression type: {type(exp).__name__}")

        return int(exp.this)
