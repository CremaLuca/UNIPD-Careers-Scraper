import argparse

import requests
import careers


def __make_parser():
    parser = argparse.ArgumentParser(
        description='Checks verification status from the UNIPD Careers API and sends it to a IFTTT webhook',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--vats', nargs="+", type=str, help='List of companies VATs.', required=True)
    parser.add_argument('--auth', help='Authorization token, eg. "Basic AAA===".', required=True)
    parser.add_argument('--event', type=str, default='verification_update', help='Event name.', required=False)
    parser.add_argument('--key', type=str, help='IFTTT key.', required=True)
    return parser


def main():
    parser = __make_parser()
    args = parser.parse_args()
    ifttt_payload = {}  # Content to be sent to IFTTT

    for vat in args.vats:
        company_verification_status = careers.get_verification_status(vat, args.auth)
        print(f"{vat}: {company_verification_status}")
        ifttt_payload[vat] = company_verification_status

    # Send payload to IFTTT
    requests.post(
        url=f"https://maker.ifttt.com/trigger/{args.event}/json/with/key/{args.key}",
        headers={
            "Content-Type": "application/json"
        },
        json=ifttt_payload
    )


if __name__ == "__main__":
    main()
