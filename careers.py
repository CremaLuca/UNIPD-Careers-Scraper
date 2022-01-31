"""
(Unofficial) UNIPD Careers API library.
"""

__version__ = "0.1"
__author__ = "Luca Crema"
__all__ = ["get_verification_status"]

import requests


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
