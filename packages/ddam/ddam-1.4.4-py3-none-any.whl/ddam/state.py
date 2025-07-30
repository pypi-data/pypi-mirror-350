import datetime
import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from ipaddress import IPv4Address, IPv6Address, ip_address


class DB:
    def __init__(self, db_file: str, max_hours: int = 24):
        self.db_file = db_file
        self.max_hours = max_hours

    @contextmanager
    def get_con(self) -> Generator[sqlite3.Connection, None, None]:
        con = sqlite3.connect(self.db_file, autocommit=False)
        try:
            with con:
                yield con
        finally:
            con.close()

    def migrate(self):
        sql = """CREATE TABLE IF NOT EXISTS targets (
ip TEXT PRIMARY KEY,
updated INTEGER,
active INTEGER,
counter INTEGER)"""
        with self.get_con() as con:
            con.execute(sql)

    def add(self, ip: IPv4Address | IPv6Address) -> dict:
        """
        Add an IP.
        If the IP is already present - set it to active and
        increment the counter
        """

        sql = """INSERT INTO targets(ip, updated, active, counter)
VALUES (:ip, unixepoch(), 1, 0)
ON CONFLICT(ip) DO UPDATE
SET updated=unixepoch(), active=1, counter=counter+1
RETURNING ip, updated, counter, min(unixepoch() + (pow(2, counter) * 60 * 60), unixepoch() + :max_hours * 60 * 60)"""  # noqa: E501
        with self.get_con() as con:
            c = con.execute(sql, {"ip": str(ip), "max_hours": self.max_hours})
            ip, updated, counter, expiration = c.fetchone()
            return {
                "ip": ip_address(ip),
                "updated": datetime.datetime.fromtimestamp(
                    updated, datetime.timezone.utc
                ),
                "counter": counter,
                "expiration": datetime.datetime.fromtimestamp(
                    expiration, datetime.timezone.utc
                ),
            }

    def get_expired(self) -> list[dict]:
        """
        Return expired records.
        Record expiration is progressive depending on the counter,
        so the first time it expires in 1 hour, then 2, 4, 8, and
        so on.
        Maximum expiration time is capped by max_hours which is
        one day by default.
        """

        result = []
        sql = """SELECT ip, updated, counter FROM targets
WHERE active=1
AND updated < max(unixepoch() - (pow(2, counter) * 60 * 60), unixepoch() - :max_hours * 60 * 60)"""  # noqa: E501
        with self.get_con() as con:
            for row in con.execute(sql, {"max_hours": self.max_hours}):
                ip, updated, counter = row
                result.append(
                    {
                        "ip": ip_address(ip),
                        "updated": datetime.datetime.fromtimestamp(
                            updated, datetime.timezone.utc
                        ),
                        "counter": counter,
                    }
                )

        return result

    def deactivate(self, ip: IPv4Address | IPv6Address) -> None:
        with self.get_con() as con:
            con.execute(
                "UPDATE targets SET active=0, updated=unixepoch() WHERE ip=:ip",
                {"ip": str(ip)},
            )

    def ip_is_blackholed(self, ip: IPv4Address | IPv6Address) -> bool:
        sql = "SELECT COUNT(ip) FROM targets WHERE ip=:ip AND active=1"
        with self.get_con() as con:
            c = con.execute(sql, {"ip": str(ip)})
            count = c.fetchone()[0]

        return count > 0

    def get_active(self) -> list[dict]:
        result = []
        sql = """SELECT ip, updated, counter FROM targets
WHERE active=1
AND updated >= min(unixepoch() - (pow(2, counter) * 60 * 60), unixepoch() - :max_hours * 60 * 60)"""  # noqa: E501
        with self.get_con() as con:
            for row in con.execute(sql, {"max_hours": self.max_hours}):
                ip, updated, counter = row
                result.append(
                    {
                        "ip": ip_address(ip),
                        "updated": datetime.datetime.fromtimestamp(
                            updated, datetime.timezone.utc
                        ),
                        "counter": counter,
                    }
                )

        return result

    def prune(self) -> None:
        """
        Delete all inactive records older than max_hours
        """

        sql = """DELETE FROM targets
WHERE active=0
AND (updated < unixepoch() - (:max_hours * 60 * 60))"""

        with self.get_con() as con:
            con.execute(sql, {"max_hours": self.max_hours})
