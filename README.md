# (Unofficial) UNIPD Careers API library and automation

Collection of libraries to interact with UNIPD Careers API. Contains automation tools (IFTTT) to receive notifications of events.

## Usage

### Careers API library

If you are interested in interacting with the Careers API via Python, you can use the functions available in the `careers.py` library.

#### `get_verification_status`

Parameters:

- `company_vat`: company VAT identification number.
- `auth`: authorization header line for HTTP request (eg. "Basic AAAA==").

You can browse the `careers.py` script file to see all available methods or use the `__all__` variable.

### Automation

If you are interested in automating the interaction with the Careers API, the `automation.py` CLI tool is your way to go.

To find all the available functions use `python automation.py --help`.
