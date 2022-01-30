import argparse

import requests


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


def get_verification_status(company_vat: str, auth: str):
    """
    Performs a request to the UNIPD Careers API to check the given company verification status.

    Parameters:
        company_vat : str
            The VAT of the company you want to check.
        auth : str
            Authorization header value, eg. "Basic AAAAA==".
    """
    response = requests.get(
        url=f"https://api.careers.unipd.it/api/v2/aziende/Cerca?partitaIva={company_vat}",
        headers={
            "Authorization": auth,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    )
    # Check if response is valid
    if response.status_code != 200:
        raise ValueError(f"Invalid response code {response.status_code}")
    # Check if response is empty
    if response.json() == []:
        raise ValueError(f"Company {company_vat} not found")
    response_dict = response.json()
    if "num" not in response_dict:
        raise ValueError(f"Invalid response - missing 'num': {response_dict}")
    if response_dict["num"] != 1:
        raise ValueError(f"Invalid response - too many companies: {response_dict}")
    if "aziende" not in response_dict:
        raise ValueError(f"Invalid response - missing 'aziende': {response_dict}")
    if response_dict["aziende"] == []:
        raise ValueError(f"Invalid response - empty 'aziende': {response_dict}")
    if "convenzionata" not in response_dict["aziende"][0]:
        raise ValueError(f"Invalid response - missing 'convenzionata' in company details: {response_dict}")
    return response_dict["aziende"][0]["convenzionata"]


def main():
    parser = __make_parser()
    args = parser.parse_args()
    ifttt_payload = {}  # Content to be sent to IFTTT

    for vat in args.vats:
        company_verification_status = get_verification_status(vat, args.auth)
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
