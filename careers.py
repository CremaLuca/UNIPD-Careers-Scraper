"""
(Unofficial) UNIPD Careers API library.
"""

__version__ = "0.1"
__author__ = "Luca Crema"
__all__ = ["get_verification_status"]

import requests
from typing import List


def get_verification_status(company_vat: str, auth: str) -> bool:
    """
    Check existance and verification status of a company given its VAT code.

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
    if response.status_code != 200:
        raise ValueError(f"Invalid response code {response.status_code}")
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


def find_by_name(name: str, auth: str) -> List[str]:
    """
    Queries the list of companies containing the given name.

    Parameters:
        name : str
            Wanted name of the companies.
        auth : str
            Authorization header value, eg. "Basic AAAAA==".
    """
    response = requests.get(
        url=f"https://api.careers.unipd.it/api/v2/aziende/Cerca?ragioneSociale={name}",
        headers={
            "Authorization": auth,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    )
    if response.status_code != 200:
        raise ValueError(f"Invalid response code {response.status_code}")
    return response.json()
