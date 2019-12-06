import sys
import logging
import re
from collections import defaultdict

import requests

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

reg_ex_part = re.compile(r".*([0-9]{3}):.*\((.*),")
reg_ex_rest = re.compile(r"(.*),\).*")
reg_ex_complete = re.compile(r".*([0-9]{3}):.*\((.*)\),")

trantab = str.maketrans({"'": None, ",": None})


def add_meaning(status_codes, status_code, meanings):
    for meaning in meanings:
        value = meaning.translate(trantab)
        status_codes[status_code].append(value)
    


def main():
    status_codes = defaultdict(list)
    try:
        response = requests.get("https://raw.githubusercontent.com/psf/requests/master/requests/status_codes.py")
        consider_next_line = False
        last_status_code = None
        for line in response.text.split("\n"):
            if line:
                line = line.strip()
                meanings = None
                status_code = None
                if consider_next_line:
                    consider_next_line = False
                    ls = reg_ex_rest.search(line)
                    if ls:
                        status_code = last_status_code
                        meanings = ls.groups()[0].split()
                else:
                    ls = reg_ex_complete.search(line)
                    if ls:
                        status_code = ls.groups()[0]
                        meanings = ls.groups()[1].split()
                    else:
                        ls = reg_ex_part.search(line)
                        if ls:
                            consider_next_line = True
                            status_code = ls.groups()[0]
                            last_status_code = status_code
                            meanings = ls.groups()[1].split()
                if meanings and status_code:
                    add_meaning(status_codes=status_codes, status_code=status_code, meanings=meanings)

    except (Exception) as e:
        logger.error(f"Error '{str(e)}'.")
    
    for k, v in status_codes.items():
        print(k, v)


if __name__ == "__main__":
    sys.exit(main())
