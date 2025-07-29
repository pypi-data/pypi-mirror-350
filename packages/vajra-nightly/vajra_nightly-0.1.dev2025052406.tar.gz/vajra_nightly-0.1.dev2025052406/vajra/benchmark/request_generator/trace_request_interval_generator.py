import logging
from typing import Optional

import pandas as pd

from vajra.benchmark.config import TraceRequestIntervalGeneratorConfig
from vajra.benchmark.request_generator.base_request_interval_generator import (
    BaseRequestIntervalGenerator,
)

logger = logging.getLogger(__name__)


class TraceRequestIntervalGenerator(BaseRequestIntervalGenerator):
    """
    Reads a trace csv file containing request arrival time, its prompt and completion token values to generate
    inter-request times, number of tokens.
    """

    def __init__(self, config: TraceRequestIntervalGeneratorConfig):
        super().__init__(config)

        # load into a pd dataframe
        self.trace_df: pd.DataFrame = pd.read_csv(config.trace_file)

        self.trace_df["arrival_time"] = pd.to_datetime(self.trace_df["arrival_time"])
        # restrict trace_df to be a subset of rows that have the same date
        self.trace_df = pd.DataFrame(
            self.trace_df[
                (self.trace_df["arrival_time"] > config.start_time)
                & (self.trace_df["arrival_time"] < config.end_time)
            ]
        )

        # change back to seconds
        self.trace_df["arrival_time"] = (
            self.trace_df["arrival_time"] - self.trace_df["arrival_time"].min()
        ) // pd.Timedelta("1s")

        # rescale the time to change QPS
        self.trace_df["arrival_time"] = (
            self.trace_df["arrival_time"] * config.time_scale_factor
        )

        # compute the inter-request time
        self.trace_df["inter_request_time"] = self.trace_df["arrival_time"].diff()

        self.next_request_idx = 1

        logger.info(
            f"Loaded interval trace file {config.trace_file} with {len(self.trace_df)} requests"
        )

    def get_next_inter_request_time(self) -> Optional[float]:
        if self.next_request_idx >= len(self.trace_df):
            return None

        inter_request_time = self.trace_df.iloc[self.next_request_idx][
            "inter_request_time"
        ].item()
        self.next_request_idx += 1

        return inter_request_time
