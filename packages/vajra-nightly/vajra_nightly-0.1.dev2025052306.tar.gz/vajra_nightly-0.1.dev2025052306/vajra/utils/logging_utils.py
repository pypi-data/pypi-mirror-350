from rich.console import Console
from rich.table import Table
from rich.text import Text

from vajra.datatypes import GlobalResourceMapping
from vajra.logger import init_logger

logger = init_logger(__name__)


def log_table(rich_table: Table) -> None:
    """Generate an ascii formatted presentation of a Rich table
    Eliminates any column styling
    """
    console = Console(width=150)
    with console.capture() as capture:
        console.print(rich_table)
    text = Text.from_ansi(capture.get())
    logger.info(text, extra={"markup": True})


def print_vajra_banner() -> None:
    """
    Print a stylized VAJRA logo with a jagged, golden thunderbolt for the 'J'.
    """
    # Explanation of ANSI sequences:
    #   \033[3m         => Start italics
    #   \033[38;5;220m  => Switch to color index 220 (a golden color)
    #   \033[39m        => Revert to default foreground color (but keep italic)
    #   \033[0m         => Reset all formatting (end italics, color, etc.)
    #

    logo = (
        "\033[3m"  # Start italic
        "\n\033[38;5;214m                 ⚡⚡⚡⚡⚡\033[39m"
        "\n\033[38;5;214m                    ⚡⚡\033[39m"
        "\n\033[1m\033[38;5;39m██╗   ██╗ █████╗ \033[39m  \033[38;5;214m ⚡⚡\033[39m  \033[38;5;39m██████╗  █████╗\033[39m"
        "\n\033[38;5;39m██║   ██║██╔══██╗\033[39m   \033[38;5;214m⚡⚡\033[39m  \033[38;5;39m██╔══██╗██╔══██╗\033[39m"
        "\n\033[38;5;39m██║   ██║███████║\033[39m   \033[38;5;214m⚡⚡\033[39m  \033[38;5;39m██████╔╝███████║\033[39m"
        "\n\033[38;5;39m╚██╗ ██╔╝██╔══██║\033[39m   \033[38;5;214m⚡⚡\033[39m  \033[38;5;39m██╔══██╗██╔══██║\033[39m"
        "\n\033[38;5;39m ╚████╔╝ ██║  ██║\033[39m   \033[38;5;214m⚡⚡\033[39m  \033[38;5;39m██║  ██║██║  ██║\033[39m"
        "\n\033[38;5;39m  ╚═══╝  ╚═╝  ╚═╝\033[39m   \033[38;5;214m⚡\033[39m    \033[38;5;39m╚═╝  ╚═╝╚═╝  ╚═╝\033[39m\033[0m"
        "\n\033[38;5;214m                  ⚡⚡\033[39m"
        "\n\033[38;5;214m                  ⚡\033[39m"
        "\n\033[0m"  # Reset everything
    )
    print(logo)


def print_resource_mapping(resource_mapping: GlobalResourceMapping) -> None:
    """Print a formatted table of resource allocations for all replicas using Rich

    Args:
        resource_mapping: GlobalResourceMapping mapping replica IDs to lists of (node_ip, device_id) tuples
    """

    if not resource_mapping:
        logger.info("No resources allocated.")
        return

    # Create a Rich table
    table = Table(title="Resource Allocation")

    # Add columns
    table.add_column("Replica ID", style="cyan", no_wrap=True)
    table.add_column("Node IP", style="green")
    table.add_column("GPU IDs", style="yellow")

    # Add rows for each replica's resources
    for replica_id, devices in sorted(resource_mapping.items()):
        # Group devices by node for better readability
        nodes_dict = {}
        for node_ip, gpu_id in devices:
            if node_ip not in nodes_dict:
                nodes_dict[node_ip] = []
            nodes_dict[node_ip].append(gpu_id)

        # Add first node to the table with replica ID
        first_node = list(nodes_dict.keys())[0]
        gpu_str = ", ".join(str(gpu_id) for gpu_id in nodes_dict[first_node])
        table.add_row(str(replica_id), first_node, gpu_str)

        # Add remaining nodes if any (with empty replica ID cell)
        for node_ip in list(nodes_dict.keys())[1:]:
            gpu_str = ", ".join(str(gpu_id) for gpu_id in nodes_dict[node_ip])
            table.add_row("", node_ip, gpu_str)

    log_table(table)
