import math

from .utils import FrozenModel


class SamplingConfig(FrozenModel):
    stop_on_population_coverage: float = 0.99
    sample_ratio: float = 0.01

    def get_amount_of_samples(self) -> int:
        """
        The probability of a certain row to be sampled in one sample:           self.sample_ratio
        The probability of a certain row to not be sampled in one sample:       1 - self.sample_ratio
        The probability of a certain row to not be sampled after K samples:    (1 - self.sample_ratio) ^ K
        The expected fraction of rows that will be sampled after K samples:     1 - (1 - self.sample_ratio) ^ K
        We need to ensure that this fraction is larger than self.stop_on_population_coverage. So:

        1 - (1 - self.sample_ratio) ^ K >= self.stop_on_population_coverage

        After developing this equation:

        K >= ln(1 - self.stop_on_population_coverage) / ln(1 - self.sample_ratio)
        """
        return math.ceil(math.log(1 - self.stop_on_population_coverage) / math.log(1 - self.sample_ratio))

    def is_worth_sampling(self, *, population_size: int, sample_size: int) -> bool:
        """
        Population is worth sampling of the self.sample_ratio * population_size >= sample_size, otherwise it is considered a small population
        """
        return self.sample_ratio * population_size >= sample_size
