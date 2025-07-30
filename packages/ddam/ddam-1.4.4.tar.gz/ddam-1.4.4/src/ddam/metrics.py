from prometheus_client import Counter, Gauge, Histogram

BLACKHOLED_ADDRESSES = Counter(
    "ddam_blackholed_addresses_total", "Number of blackholed addresses", ["version"]
)
UNBLACKHOLED_ADDRESSES = Counter(
    "ddam_unblackholed_addresses_total", "Number of unblackholed addresses", ["version"]
)
TRAFFIC_RATE = Histogram(
    "ddam_traffic_rate_mbps",
    "Traffic rate in mbps at blackhole time",
    ["version"],
    buckets=(10, 20, 50, 100, 200, 500, 1000),
)
ACTIVE_RECORDS = Gauge("ddam_active_records_total", "Number of active blackholes")
MAX_RECURRING_ATTACKS = Gauge(
    "ddam_max_recurring_attacks",
    "Maximum number of attacks seen on an address within last 24 hours",
)

MAILER_FAILURES = Counter(
    "ddam_mailer_failures_total",
    "Number of times ddam failed to send notification email",
)
