#!/usr/bin/env python3
import argparse
import logging
from datetime import datetime

import dns.resolver
import dns.exception

logging.basicConfig(
    filename='dns.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def query_records(domain: str, rtype: str):
    try:
        answers = dns.resolver.resolve(domain, rtype)
        return [str(r) for r in answers]
    except dns.resolver.NoAnswer:
        return []
    except dns.resolver.NXDOMAIN:
        return ["NXDOMAIN"]
    except dns.exception.DNSException as e:
        return [f"Error: {e}"]

def main():
    parser = argparse.ArgumentParser(description="DNS client: resolve A, MX, and CNAME records and log results")
    parser.add_argument('--domain', required=True, help='Domain name to query (e.g., example.com)')
    args = parser.parse_args()

    domain = args.domain.strip()
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    log_filename = 'dns_log.txt'
    lines = [f"DNS Query Results for {domain} at {now}", "-"*48]

    for rtype in ['A', 'MX', 'CNAME']:
        results = query_records(domain, rtype)
        lines.append(f"{rtype} records:")
        if results:
            for r in results:
                lines.append(f"  - {r}")
        else:
            lines.append("  (no records)")
        lines.append("")

    output = "\n".join(lines)
    print(output)
    with open(log_filename, 'w', encoding='utf-8') as f:
        f.write(output + "\n")
    logging.info(f"Wrote DNS results to {log_filename}")

if __name__ == '__main__':
    main()
