# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

import argparse
import asyncio
from signal import SIGINT

import agp_bindings


async def run_server(address: str, enable_opentelemetry: bool):
    # init tracing
    await agp_bindings.init_tracing(
        {
            "log_level": "debug",
            "opentelemetry": {
                "enabled": enable_opentelemetry,
                "grpc": {
                    "endpoint": "http://localhost:4317",
                },
            },
        }
    )

    global gateway
    # create new gateway object
    gateway = await agp_bindings.Gateway.new("cisco", "default", "gateway")

    # Run as server
    await gateway.run_server({"endpoint": address, "tls": {"insecure": True}})


async def main():
    parser = argparse.ArgumentParser(
        description="Command line client for gateway server."
    )
    parser.add_argument(
        "-g", "--gateway", type=str, help="Gateway address.", default="127.0.0.1:12345"
    )
    parser.add_argument(
        "--enable-opentelemetry",
        "-t",
        action="store_true",
        default=False,
        help="Enable OpenTelemetry tracing.",
    )

    args = parser.parse_args()

    # Create an asyncio event to keep the loop running until interrupted
    stop_event = asyncio.Event()

    # Define a shutdown handler to set the event when interrupted
    def shutdown():
        print("\nShutting down...")
        stop_event.set()

    # Register the shutdown handler for SIGINT
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(SIGINT, shutdown)

    # Run the client task
    client_task = asyncio.create_task(
        run_server(args.gateway, args.enable_opentelemetry)
    )

    # Wait until the stop event is set
    await stop_event.wait()

    # Cancel the client task
    client_task.cancel()
    try:
        await client_task
    except asyncio.CancelledError:
        pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program terminated by user.")
