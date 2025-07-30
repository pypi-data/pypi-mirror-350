import argparse
import json
import logging
import pathlib
from ipaddress import ip_address

import jinja2

logger = logging.getLogger(__name__)


def load_neighbors(path: pathlib.Path) -> dict:
    neighbors = {}

    with open(path) as f:
        config = json.load(f)

    for neighbor_ip_str, neighbor_config in config.items():
        ip = ip_address(neighbor_ip_str)
        neighbors[ip] = {
            "local-address": ip_address(neighbor_config["local-address"]),
            "router-id": neighbor_config["router-id"],
            "local-as": neighbor_config["local-as"],
            "peer-as": neighbor_config["peer-as"],
            "communities": neighbor_config["communities"],
        }
        if "description" in neighbor_config:
            neighbors[ip]["description"] = neighbor_config["description"]

        if "connect" in neighbor_config:
            neighbors[ip]["connect"] = int(neighbor_config["connect"])

    return neighbors


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--output-file",
        type=pathlib.Path,
        default=pathlib.Path("exabgp.conf"),
        help="File path to write output ExaBGP config to",
    )

    parser.add_argument(
        "--neighbors-config-file",
        type=pathlib.Path,
        default=pathlib.Path("neighbors.json"),
        help="File path to neighbors JSON config",
    )

    args = parser.parse_args()

    neighbors = load_neighbors(args.neighbors_config_file)

    jinja_env = jinja2.Environment(
        loader=jinja2.PackageLoader("ddam"), autoescape=False
    )

    template = jinja_env.get_template("exabgp.conf.j2")

    with open(args.output_file, "w") as f:
        f.write(template.render(neighbors=neighbors))
