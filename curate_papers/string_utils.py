import re

def green(content):
    return "\033[92m{}\033[0m".format(content)

def red(content):
    return "\033[91m{}\033[0m".format(content)

def orange(content):
    return "\033[93m{}\033[0m".format(content)

def sanitise_string(string):
    return re.sub(r'[^A-Za-z0-9\\.]+', ' ', string).strip().replace(" ", "-").lower()

def get_uppercase_characters(string):
    return ''.join(c for c in string if c.isupper())
