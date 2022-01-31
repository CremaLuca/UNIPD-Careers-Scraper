# (Unofficial) UNIPD Careers API library and automation

Collection of libraries to interact with UNIPD Careers API. Contains automation tools (IFTTT) to receive notifications of events.

## Usage

### Careers API library

If you are interested in interacting with the Careers API via Python, you can use the functions available in the `careers.py` library.

#### `get_verification_status`

Check existance and verification status of a company given its VAT code.

```py
Parameters:
    company_vat : str
        The VAT of the company you want to check.
    auth : str
        Authorization header value, eg. "Basic AAAAA==".
```

#### `find_by_name`

Queries the list of companies containing the given name.

```py
Parameters:
    name : str
        Wanted name of the companies.
    auth : str
        Authorization header value, eg. "Basic AAAAA==".
```

#### Other

You can browse the `careers.py` script file to see all available methods or use the `__all__` variable.

### Automation

If you are interested in automating the interaction with the Careers API, the `automation.py` CLI tool is your way to go.

To find all the available functions use `python automation.py --help`.
