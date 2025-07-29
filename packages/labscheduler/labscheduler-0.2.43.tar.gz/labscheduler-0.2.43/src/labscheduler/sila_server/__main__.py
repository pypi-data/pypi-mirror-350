# Generating by sila2.code_generator; sila2.__version__: 0.7.3
import contextlib
import logging
from argparse import ArgumentParser
from uuid import UUID

from .server import Server

logger = logging.getLogger(__name__)


def parse_args():
    parser = ArgumentParser(prog="scheduler_server", description="Start this SiLA 2 server")
    parser.add_argument("-a", "--ip-address", default="127.0.0.1", help="The IP address (default: '127.0.0.1')")
    parser.add_argument("-p", "--port", type=int, default=50052, help="The port (default: 50052)")
    parser.add_argument("--server-uuid", type=UUID, default=None, help="The server UUID (default: create random UUID)")
    parser.add_argument("--disable-discovery", action="store_true", help="Disable SiLA Server Discovery")

    parser.add_argument("--insecure", action="store_true", help="Start without encryption")
    parser.add_argument("-k", "--private-key-file", default=None, help="Private key file (e.g. 'server-key.pem')")
    parser.add_argument("-c", "--cert-file", default=None, help="Certificate file (e.g. 'server-cert.pem')")
    parser.add_argument(
        "--ca-export-file",
        default=None,
        help="When using a self-signed certificate, write the generated CA to this file",
    )

    log_level_group = parser.add_mutually_exclusive_group()
    log_level_group.add_argument("-q", "--quiet", action="store_true", help="Only log errors")
    log_level_group.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    log_level_group.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")

    return parser.parse_args()


def run_server(args):
    # prepare args
    insecure: bool = args.insecure
    ca_export_file: str | None = args.ca_export_file
    address: str = args.ip_address
    port: int = args.port
    enable_discovery: bool = not args.disable_discovery
    server_uuid: UUID | None = args.server_uuid

    if args.cert_file:
        with open(args.cert_file, "rb") as f:
            cert = f.read()
    else:
        cert = None
    if args.private_key_file:
        with open(args.private_key_file, "rb") as f:
            private_key = f.read()
    else:
        private_key = None

    if (insecure or ca_export_file is not None) and (cert is not None or private_key is not None):
        msg = "Cannot use --insecure or --ca-export-file with --private-key-file or --cert-file"
        raise ValueError(msg)
    if sum(par is None for par in (cert, private_key)) not in {0, 2}:
        msg = "Either provide both --private-key-file and --cert-file, or none of them"
        raise ValueError(msg)
    if insecure and ca_export_file is not None:
        msg = "Cannot use --export-ca-file with --insecure"
        raise ValueError(msg)

    # run server
    server = Server(server_uuid=server_uuid)
    try:  # FIXME: create a context manager for the server instead of using try-finally. Re-use in test modules?
        if insecure:
            server.start_insecure(address, port, enable_discovery=enable_discovery)
        else:
            server.start(address, port, cert_chain=cert, private_key=private_key, enable_discovery=enable_discovery)
            if ca_export_file is not None:
                with open(ca_export_file, "wb") as fp:
                    fp.write(server.generated_ca)
                print(f"Wrote generated CA to '{ca_export_file}'")  # noqa: T201
        print("Server startup complete, press Enter to stop")  # noqa: T201

        with contextlib.suppress(KeyboardInterrupt):
            input()
    finally:
        server.stop()
        print("Stopped server")  # noqa: T201


def setup_basic_logging(args):
    level = logging.WARNING
    if args.verbose:
        level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    if args.quiet:
        level = logging.ERROR

    logging.basicConfig(level=level, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")


def main():
    args = parse_args()
    setup_basic_logging(args)
    run_server(args)


if __name__ == "__main__":
    main()
