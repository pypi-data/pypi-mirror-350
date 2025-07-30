# DDAM

![Full solution architecture](doc/architecture.png "Architecture")

DDAM mitigates DDoS attacks by monitoring NetFlow data in an Elasticsearch
cluster (configured separately). It calculates per-IP throughput and announces
temporary blackhole routes via BGP when traffic exceeds a set threshold.
Blackhole duration will increase exponentially (up to 24h by default) for
repeat attacks to the same IP address.

## Example

Example Docker Compose configuration. Replace

- `<UPSTREAM-BGP-NEIGHBOR-IP>` with the upstream BGP neighbor IP,
- `<HOST-IP>` with the Docker host public IP,
- `<AS-NUMBER>` with your AS number,
- `<PEER-AS-NUMBER>` with the upstream BGP neighbor AS number,
- `<PEER-BLACKHOLE-COMMUNITY>` with the upstream blackhole community,
- `<ELASTICSEARCH-URL>` with the address of an Elasticsearch server NetFlow data is collected into.

`docker-compose.yml`:

```yaml
services:
  init-ddam-volume-permissions:
    image: "alikov/ddam"
    volumes:
      - "ddam-config:/etc/ddam"
      - "ddam-data:/var/lib/ddam"
      - "ddam-run:/run/exabgp"
    mem_limit: "32mb"
    read_only: true
    security_opt:
      - "no-new-privileges=true"
    user: root
    entrypoint: sh
    command:
      - -euc
      - 'chown -R nobody:root /etc/ddam /var/lib/ddam /run/exabgp'
    network_mode: none
  init-ddam-cidr-blocks:
    image: "alikov/ddam"
    volumes:
      - "ddam-config:/etc/ddam"
    mem_limit: "512mb"
    read_only: true
    cap_drop:
      - ALL
    security_opt:
      - "no-new-privileges=true"
    networks:
      backend:
        ipv4_address: "10.17.0.5"
    entrypoint: /opt/ddam/bin/get-as-cidr-blocks
    command:
      - --output-file
      - /etc/ddam/cidr-blocks.json
      - "<AS-NUMBER>"
    depends_on:
      init-ddam-volume-permissions:
        condition: service_completed_successfully
  init-ddam-exabgp-conf:
    image: "alikov/ddam"
    volumes:
      - "ddam-config:/etc/ddam"
      - "./neighbors.json:/etc/ddam/neighbors.json:ro"
    mem_limit: "128mb"
    read_only: true
    cap_drop:
      - ALL
    security_opt:
      - "no-new-privileges=true"
    network_mode: none
    entrypoint: /opt/ddam/bin/make-exabgp-conf
    command:
      - --neighbors-config-file
      - /etc/ddam/neighbors.json
      - --output-file
      - /etc/ddam/exabgp.conf
    depends_on:
      init-ddam-volume-permissions:
        condition: service_completed_successfully
  init-ddam-migrate:
    image: "alikov/ddam"
    environment:
      - DDAM_DB_FILE=/var/lib/ddam/ddam.db
    volumes:
      - "ddam-data:/var/lib/ddam"
    mem_limit: "128mb"
    read_only: true
    cap_drop:
      - ALL
    security_opt:
      - "no-new-privileges=true"
    network_mode: none
    entrypoint: /opt/ddam/bin/ddam
    command:
      - migrate
    depends_on:
      init-ddam-volume-permissions:
        condition: service_completed_successfully
  ddam:
    image: "alikov/ddam"
    environment:
      - DDAM_ES_ADDRESS=<ELASTICSEARCH-URL>
      - DDAM_DB_FILE=/var/lib/ddam/ddam.db
      - DDAM_NEIGHBORS_CONFIG_FILE=/etc/ddam/neighbors.json
      - DDAM_CIDR_BLOCKS_FILE=/etc/ddam/cidr-blocks.json
      - DDAM_DDOS_THRESHOLD_MBPS=1000
      - DDAM_EXPORTER_PORT=9998
      - exabgp.api.cli=true
      - exabgp.tcp.bind=0.0.0.0
      - exabgp.tcp.port=1790
    volumes:
      - "ddam-config:/etc/ddam"
      - "ddam-data:/var/lib/ddam"
      - "ddam-run:/run/exabgp"
      - "./neighbors.json:/etc/ddam/neighbors.json:ro"
    mem_limit: "1024mb"
    read_only: true
    cap_drop:
      - ALL
    security_opt:
      - "no-new-privileges=true"
    ports:
      - "9998:9998"
      - "179:1790"
    networks:
      backend:
        ipv4_address: "10.17.0.6"
    healthcheck:
      test:
        - CMD-SHELL
        - "/usr/bin/timeout 2 /usr/bin/nc -z 127.0.0.1 1790 || exit 1"
      interval: 30s
      timeout: 2s
      retries: 5
    command:
      - /opt/ddam/bin/exabgp
      - /etc/ddam/exabgp.conf
    restart: always
    depends_on:
      init-ddam-cidr-blocks:
        condition: service_completed_successfully
      init-ddam-exabgp-conf:
        condition: service_completed_successfully
      init-ddam-migrate:
        condition: service_completed_successfully
networks:
  backend:
    ipam:
      driver: default
      config:
        - subnet: "10.17.0.0/27"
          ip_range: "10.17.0.16/28"
volumes:
  ddam-config:
  ddam-data:
  ddam-run:
```

`neighbors.json`:

```json
{
  "<UPSTREAM-BGP-NEIGHBOR-IP>": {
    "description": "ddam-test-neighbor",
    "connect": 179,
    "local-address": "10.17.0.6",
    "router-id": "<HOST-IP>",
    "local-as": <AS-NUMBER>,
    "peer-as": <PEER-AS-NUMBER>,
    "communities": ["<PEER-BLACKHOLE-COMMUNITY>"]
  }
}
```

## Environment variables

| Name                                   | Default                 | Description                                                                    |
|----------------------------------------|-------------------------|--------------------------------------------------------------------------------|
| `DDAM_DB_FILE`                         | `ddam.db`               | Path to store the state SQLite DB in                                           |
| `DDAM_NEIGHBORS_CONFIG_FILE`           | `neighbors.json`        | BGP neighbor configuration JSON file (see example above)                       |
| `DDAM_CIDR_BLOCKS_FILE`                | `cidr-blocks.json`      | JSON list of CIDRs to protect from DDoS                                        |
| `DDAM_SAMPLING_FACTOR`                 | `10000`                 | Sampling factor used by the NetFlow collection system                          |
| `DDAM_ES_ADDRESS`                      | `http://localhost:9200` | Elasticsearch URL                                                              |
| `DDAM_EXCLUDES`                        |                         | Comma-separated list of IP addresses or CIDRs which should never be blackholed |
| `DDAM_DDOS_THRESHOLD_MBPS`             | `2000`                  | Throughput threshold in mbps to trigger blackholing                            |
| `DDAM_INTERVAL_MINUTES`                | `5`                     | Check interval in minutes                                                      |
| `DDAM_MAX_EXPIRATION_HOURS`            | `24`                    | Maximum duration for blackhole routes in hours                                 |
| `DDAM_EMAIL_ENABLE`                    | `0`                     | Set to `1` to enable email sending for blackhole/unblackhole events            |
| `DDAM_EMAIL_FROM`                      | `ddam`                  | From email address                                                             |
| `DDAM_EMAIL_RECIPIENTS`                |                         | Comma-separated list of recipient email addresses                              |
| `DDAM_SMTP_RELAY_ADDRESS`              | `127.0.0.1`             | Address of an SMTP relay                                                       |
| `DDAM_SMTP_PORT`                       | `25`                    | SMTP port                                                                      |
| `DDAM_SMTP_SSL`                        | `0`                     | Set to `1` to enable explicit SSL                                              |
| `DDAM_EXPORTER_PORT`                   | `9998`                  | Prometheus exporter port to listen on                                          |
| `DDAM_BLACKHOLE_EMAIL_TEMPLATE_FILE`   |                         | Optional path to a Jinja2 blackhole email template                             |
| `DDAM_UNBLACKHOLE_EMAIL_TEMPLATE_FILE` |                         | Optional path to a Jinja2 blackhole email template                             |

## Prometheus metrics

| Name                                | Type      | Description                                                       |
|-------------------------------------|-----------|-------------------------------------------------------------------|
| `ddam_blackholed_addresses_total`   | Counter   | Number of blackholed addresses                                    |
| `ddam_unblackholed_addresses_total` | Counter   | Number of unblackholed addresses                                  |
| `ddam_traffic_rate_mbps`            | Histogram | Traffic rate in mbps at blackhole time                            |
| `ddam_active_records_total`         | Gauge     | Number of active blackholes                                       |
| `ddam_max_recurring_attacks`        | Gauge     | Maximum number of attacks seen on an address within last 24 hours |
| `ddam_mailer_failures_total`        | Counter   | Number of times ddam failed to send notification email            |

## Developing

See [DEVELOPING.md](DEVELOPING.md) for local development setup instructions.

## Diagram icon attribution

- [Dot icons created by Bharat Icons - Flaticon](https://www.flaticon.com/free-icons/dot),
- [Network device icons created by SBTS2018 - Flaticon](https://www.flaticon.com/free-icons/network-device),
- [Wind icons created by Freepik - Flaticon](https://www.flaticon.com/free-icons/wind),
- [Cloud icons created by kosonicon - Flaticon](https://www.flaticon.com/free-icons/cloud),
- [Smtp icons created by Three musketeers - Flaticon](https://www.flaticon.com/free-icons/smtp).
