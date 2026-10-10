#!/usr/bin/env python3
"""Render the shared domain lists as native, policy-neutral Quantumult X rules."""

import argparse
import ipaddress
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LIST_NAMES = ("whitelist", "ailist", "blacklist")
DOMAIN = re.compile(r"(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?")


def render(source: Path) -> str:
    rules = []
    seen = set()
    for number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
        entry = line.strip()
        if not entry or entry.startswith("#"):
            continue
        if not entry.startswith("+.") or not DOMAIN.fullmatch(entry[2:]):
            raise ValueError(f"{source.name}:{number}: expected +.lowercase-domain")
        domain = entry[2:]
        try:
            ipaddress.ip_address(domain)
        except ValueError:
            pass
        else:
            raise ValueError(f"{source.name}:{number}: IP addresses are not domain entries")
        if domain in seen:
            raise ValueError(f"{source.name}:{number}: duplicate domain {domain}")
        seen.add(domain)
        rules.append(f"host-suffix, {domain}, direct")
    return "\n".join([
        f"# Generated from lists/{source.name}; edit the source TXT instead.",
        "# Set force-policy in Quantumult X; direct below is only a placeholder.",
        *rules,
        "",
    ])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if generated files are stale")
    args = parser.parse_args()
    outputs = [(ROOT / "quantumult-x" / f"{name}.list", render(ROOT / "lists" / f"{name}.txt")) for name in LIST_NAMES]
    stale = []
    for destination, content in outputs:
        if args.check:
            if not destination.exists() or destination.read_text(encoding="utf-8") != content:
                stale.append(str(destination.relative_to(ROOT)))
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding="utf-8")
    if stale:
        parser.error("generated files are stale: " + ", ".join(stale))


if __name__ == "__main__":
    main()
