from dataclasses import field

from vajra._native.configs import CacheConfig as CacheConfig_C
from vajra.utils.dataclasses import frozen_dataclass


@frozen_dataclass
class CacheConfig:
    block_size: int = field(
        default=16, metadata={"help": "Size of a cache block in number of tokens."}
    )

    def __post_init__(self):
        # Create native handler
        self.native_handle = CacheConfig_C(
            self.block_size,
        )
