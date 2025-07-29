# lv
Utils to slurp stuff

To install:	```pip install lv```

## Overview
The `lv` package provides utilities to automate web interactions, particularly for logging into websites and downloading content. The primary functionality is encapsulated in the `slurp_with_login_and_pwd` function. This function uses the `mechanize` library to handle web requests, manage cookies, and parse forms, allowing users to log into sites and access resources that require authentication.

## Functionality
### `slurp_with_login_and_pwd`
This function automates the process of:
1. Opening a web page with a login form (currently hardcoded to Yahoo's login page).
2. Filling out and submitting the login form with user credentials.
3. Navigating to a subsequent URL (currently hardcoded to a specific Coursera lecture video) after logging in.
4. Downloading content from the final URL.

The function uses `mechanize.Browser` to simulate a web browser, which handles cookies and user-agent headers to maintain session and appear as a regular browser to web services.

## Usage
### Basic Example
Below is an example of how you might use the `slurp_with_login_and_pwd` function within a Python script. Note that you will need to replace `'yahoo-user-id'` and `'password'` with your actual Yahoo credentials, and the URL with the resource you wish to access after logging in.

```python
from lv import slurp_with_login_and_pwd

# Ensure you replace the credentials and URL with your specific details
slurp_with_login_and_pwd()
```

### Important Notes
- The function is currently tailored specifically for Yahoo and a Coursera course video. To use it for other websites or resources, modifications to the function are required.
- Ensure that your use of this function complies with the terms of service of the website you are interacting with.

## Dependencies
- `mechanize`: Used for handling HTTP requests, forms, cookies, and more.

## Installation
To use the `lv` package, you will need to install the required dependencies:
```bash
pip install mechanize
```

Then, you can install the `lv` package itself:
```bash
pip install lv
```

## Disclaimer
This tool is intended for educational and legitimate purposes only. Ensure that you have the right to access and download content from the website, and always respect the terms of service of the website.