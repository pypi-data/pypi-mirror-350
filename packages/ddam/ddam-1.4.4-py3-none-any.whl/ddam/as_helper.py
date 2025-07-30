import argparse
import json
import logging
import pathlib
from ipaddress import IPv4Network, IPv6Network, ip_network

import requests

logger = logging.getLogger(__name__)


def get_routes(as_numbers: list[int]) -> set[IPv4Network | IPv6Network]:
    result: set[IPv4Network | IPv6Network] = set()

    url = "https://rest.db.ripe.net/search.json"
    for asn in as_numbers:
        params = {
            "query-string": f"AS{asn}",
            "type-filter": ["route", "route6"],
            "inverse-attribute": "origin",
            "flags": "no-referenced",
        }

        response = requests.get(url, params=params).json()

        for obj in response["objects"]["object"]:
            if obj["type"] == "route":
                for attribute in obj["primary-key"]["attribute"]:
                    if attribute["name"] == "route":
                        result.add(IPv4Network(attribute["value"]))
            if obj["type"] == "route6":
                for attribute in obj["primary-key"]["attribute"]:
                    if attribute["name"] == "route6":
                        result.add(IPv6Network(attribute["value"]))

    # Remove subnets.
    networks_to_remove: set[IPv4Network | IPv6Network] = set()
    for candidate_network in result:
        for network in result - {candidate_network}:
            if type(candidate_network) is not type(network):
                continue
            if candidate_network.subnet_of(network):  # type: ignore
                networks_to_remove.add(candidate_network)
                break

    return result - networks_to_remove


def save_cidr_blocks(
    path: pathlib.Path, routes: set[IPv4Network | IPv6Network]
) -> None:
    with open(path, "w") as f:
        json.dump(sorted(str(r) for r in routes), f, indent=2, sort_keys=True)


def load_cidr_blocks(path: pathlib.Path) -> set[IPv4Network | IPv6Network]:
    with open(path) as f:
        cidrs = json.load(f)

    return {ip_network(cidr) for cidr in cidrs}


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "asn",
        type=int,
        nargs="+",
        help="AS number(s); can be specified multiple times",
    )
    parser.add_argument(
        "--output-file",
        type=pathlib.Path,
        default=pathlib.Path("cidr-blocks.json"),
        help="File path to write JSON output to",
    )

    args = parser.parse_args()

    routes = get_routes(args.asn)

    save_cidr_blocks(args.output_file, routes)

    logger.info("Saved CIDR blocks into %s", args.output_file)
