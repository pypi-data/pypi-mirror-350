from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network, ip_address

from elasticsearch import Elasticsearch


class NetFlowElasticsearch:
    def __init__(self, es_address: str, sampling_factor: int) -> None:
        self.es = Elasticsearch(es_address)
        self.sampling_factor = sampling_factor

    def get_top_by_network_bytes(
        self,
        size: int,
        excludes: set[IPv4Network | IPv6Network | IPv4Address | IPv6Address]
        | None = None,
        range_minutes: int = 5,
    ) -> list[dict]:
        excludes_set = excludes or set()

        query = {
            "bool": {
                "must": [],
                "filter": [
                    {"query_string": {"query": "*"}},
                    {"match_phrase": {"input.type": "netflow"}},
                    {
                        "range": {
                            "@timestamp": {
                                "gte": f"now-{range_minutes}m",
                            }
                        }
                    },
                ],
                "should": [],
                "must_not": [
                    {"term": {"destination.ip": str(i)}} for i in excludes_set
                ],
            }
        }

        aggs = {
            "0": {
                "terms": {
                    "field": "destination.ip",
                    "order": {"total_network_bytes": "desc"},
                    "size": size,
                    "shard_size": 1000,
                },
                "aggs": {"total_network_bytes": {"sum": {"field": "network.bytes"}}},
            }
        }

        indices = self.es.indices.get(index="filebeat-*", flat_settings=True)

        latest_index = max(
            indices, key=lambda i: indices[i]["settings"]["index.creation_date"]
        )
        resp = self.es.search(index=latest_index, query=query, aggs=aggs)

        range_seconds = range_minutes * 60

        return [
            {
                "ip": ip_address(b["key"]),
                "bitrate_mbps": (
                    (b["total_network_bytes"]["value"] * 8 * self.sampling_factor)
                    / (range_seconds)
                )
                / 1000
                / 1000,
            }
            for b in resp["aggregations"]["0"]["buckets"]
        ]
