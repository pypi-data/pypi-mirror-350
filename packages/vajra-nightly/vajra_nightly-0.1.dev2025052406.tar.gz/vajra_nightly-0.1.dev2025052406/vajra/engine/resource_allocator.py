from typing import List, Tuple

import ray

from vajra.datatypes import GlobalResourceMapping
from vajra.logger import init_logger
from vajra.utils import get_ip

logger = init_logger(__name__)


class ResourceAllocator:
    """Handles GPU resource allocation for replicas"""

    def __init__(self) -> None:
        ray.init(ignore_reinit_error=True)

    def validate_cluster_resources(self, num_replicas: int, world_size: int) -> None:
        """Validate that cluster has sufficient GPU resources"""
        num_gpus_required = num_replicas * world_size
        available_resources = ray.available_resources()

        assert (
            available_resources["GPU"] >= num_gpus_required
        ), f"Insufficient GPUs. Required: {num_gpus_required}, Available: {available_resources['GPU']}"

    def get_replicaset_resource_mapping(
        self, num_replicas: int, world_size: int
    ) -> GlobalResourceMapping:
        """Generate resource allocation mapping for all replicas
        Args:
            num_replicas: Number of replicas to allocate resources for
            world_size: Number of GPUs needed per replica
        Returns:
            GlobalResourceMapping: Mapping of resources allocated to all replicas
        """
        # First validate total resources needed
        self.validate_cluster_resources(num_replicas, world_size)

        # Get all available GPUs first to ensure fair distribution
        cluster_resources_keys = list(ray.available_resources().keys())
        ip_addresses = [
            x
            for x in cluster_resources_keys
            if x.startswith("node:") and x != "node:__internal_head__"
        ]

        runner_ip = f"node:{get_ip()}"
        if runner_ip in ip_addresses:
            ip_addresses.remove(runner_ip)
        ip_addresses.insert(0, runner_ip)

        # Pre-allocate all GPUs to ensure fair distribution across replicas
        available_gpus: List[Tuple[str, int]] = []
        for ip_address in ip_addresses:
            num_gpus_per_node = int(
                ray.available_resources()["GPU"] // len(ip_addresses)
            )
            for gpu_id in reversed(range(num_gpus_per_node)):
                available_gpus.append((ip_address, gpu_id))

        # Allocate resources for each replica
        resource_mapping: GlobalResourceMapping = {}
        for replica_id in range(num_replicas):
            devices = [available_gpus.pop(0) for _ in range(world_size)]
            resource_mapping[str(replica_id)] = devices

        return resource_mapping
