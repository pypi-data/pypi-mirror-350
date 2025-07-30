"""
Command-line interface for the Yearn Treasury exporter.

This module provides the `yearn-treasury` CLI, which connects to a Brownie network
based on the `--network` option (or the `BROWNIE_NETWORK_ID` environment variable),
periodically snapshots treasury balances via :func:`export_balances`, and
pushes metrics to Victoria Metrics.

Example:
    Run export every 12 hours on mainnet:

    .. code-block:: bash

        yearn-treasury run --network mainnet --interval 12h
"""

import asyncio
import os
from argparse import ArgumentParser
from pathlib import Path
from typing import Final, final

import brownie
import brownie.network
from eth_portfolio_scripts.balances import export_balances


parser = ArgumentParser(description="Treasury CLI")
subparsers = parser.add_subparsers(dest="command", required=True)

run_parser = subparsers.add_parser("run", help="Run the treasury export tool")
run_parser.add_argument(
    "--network",
    type=str,
    help="The brownie network identifier for the RPC to use. Overrides BROWNIE_NETWORK_ID env var if unset.",
    default="mainnet",
)
run_parser.add_argument(
    "--interval",
    type=str,
    help="The time interval between datapoints. Default: 12h",
    default="12h",
)
run_parser.add_argument(
    "--daemon",
    action="store_true",
    help="Run as a background daemon (currently unsupported).",
)
run_parser.add_argument(
    "--grafana-port",
    type=int,
    help="Port for the Grafana dashboard where you can view your data. Default: 3003",
    default=3003,
)
run_parser.add_argument(
    "--renderer-port",
    type=int,
    help="Port for the service that renders visual reports. Default: 8080",
    default=8080,
)
run_parser.add_argument(
    "--victoria-port",
    type=int,
    help="Port for the Victoria metrics reporting endpoint. Default: 8430",
    default=8430,
)
args = run_parser.parse_args()

# Set BROWNIE_NETWORK_ID from --network flag if not already set
os.environ.setdefault("BROWNIE_NETWORK_ID", args.network)
BROWNIE_NETWORK = os.environ["BROWNIE_NETWORK_ID"]


def export():
    """
    Brownie entrypoint for the treasury exporter script.

    This function is registered as a console script entrypoint under
    ``yearn-treasury`` and delegates execution to Brownie's script runner.
    """
    brownie.project.run(__file__)


# TODO: run forever arg
def main() -> None:
    """
    Connect to the configured Brownie network and start the export loop.

    Steps:
        1. Reads the ``BROWNIE_NETWORK_ID`` environment variable (populated from
           the ``--network`` option or existing env var).
        2. Connects to that Brownie network.
        3. Patches the global SHITCOINS mapping with local tokens.
        4. Constructs a frozen Args subclass to pass CLI parameters to
           :func:`export_balances`.
        5. Exports ports for external services into environment variables.
        6. Runs :func:`eth_portfolio_scripts.balances.export_balances` under asyncio.

    Raises:
        RuntimeError: If the Brownie network cannot be determined.
    """
    brownie.network.connect(BROWNIE_NETWORK)

    import eth_portfolio

    from . import constants, shitcoins

    # Merge local SHITCOINS into eth_portfolio's config to skip tokens we don't care about
    eth_portfolio.SHITCOINS[constants.CHAINID].update(shitcoins.SHITCOINS)  # type: ignore [index]

    @final
    class Args(constants.Args):
        """
        Immutable container of CLI arguments for :func:`~export_balances`.
        """

        network: Final[str] = args.network
        """Brownie network to connect to."""

        interval: Final[str] = args.interval
        """Time interval between snapshots."""

        grafana_port: Final[int] = args.grafana_port
        """Grafana port."""

        renderer_port: Final[int] = args.renderer_port
        """Report renderer port."""

        victoria_port: Final[int] = args.victoria_port
        """Victoria metrics port."""

        daemon: Final[bool] = args.daemon
        """Whether to run in daemon mode."""

        sort_rules: Final[Path] = Path(__file__).parent / "rules"
        """The path where the sort rules for dao-treasury are defined."""

    # Export ports for external services
    os.environ["GRAFANA_PORT"] = str(Args.grafana_port)
    os.environ["RENDERER_PORT"] = str(Args.renderer_port)
    os.environ["VICTORIA_PORT"] = str(Args.victoria_port)

    # Start the balance export routine
    asyncio.run(_main(Args))


async def _main(args) -> None:
    import dao_treasury.main

    # TODO: move this gather into dao-treasury
    await asyncio.gather(export_balances(args), dao_treasury.main.export(args))
