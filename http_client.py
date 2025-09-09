#!/usr/bin/env python3
import argparse
import json
import logging
from typing import Optional, Dict, Any

import requests

logging.basicConfig(
    filename='http.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def pretty_headers(headers: Dict[str, Any]) -> str:
    return "\n".join([f"{k}: {v}" for k, v in headers.items()])

def do_get(url: str, timeout: int = 10) -> None:
    logging.info(f"GET {url}")
    try:
        resp = requests.get(url, timeout=timeout)
        logging.info(f"Status: {resp.status_code}")
        print("=== GET RESPONSE HEADERS ===")
        print(pretty_headers(resp.headers))
        print("\n=== GET RESPONSE BODY ===")
        print(resp.text)
        resp.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"GET request failed: {e}")

def do_post(url: str, data: Optional[str], timeout: int = 10) -> None:
    logging.info(f"POST {url}")
    try:
        json_data = None
        form_data = None
        headers = {}
        if data:
            try:
                json_data = json.loads(data)
                headers['Content-Type'] = 'application/json'
            except json.JSONDecodeError:
                # assume key=value&key2=value2 format
                form_data = dict(
                    kv.split('=', 1) for kv in data.split('&') if '=' in kv
                )
        resp = requests.post(url, json=json_data, data=form_data, headers=headers, timeout=timeout)
        logging.info(f"Status: {resp.status_code}")
        print("=== POST RESPONSE HEADERS ===")
        print(pretty_headers(resp.headers))
        print("\n=== POST RESPONSE BODY ===")
        print(resp.text)
        resp.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"POST request failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="HTTP client for GET and POST with logging")
    parser.add_argument('--get-url', default='https://httpbin.org/get', help='URL for GET request')
    parser.add_argument('--post-url', default='https://httpbin.org/post', help='URL for POST request')
    parser.add_argument('--post-data', default='{"lab":"2","message":"Hello HTTP!"}', help='POST payload (JSON string or key=value&key2=value2)')
    parser.add_argument('--timeout', type=int, default=10, help='Timeout in seconds')
    args = parser.parse_args()

    do_get(args.get_url, timeout=args.timeout)
    print("\n" + "="*60 + "\n")
    do_post(args.post_url, data=args.post_data, timeout=args.timeout)

if __name__ == '__main__':
    main()
