import sys
import logging
import re
from collections import defaultdict

import requests

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

reg_ex = re.compile("[ ]*([0-9]{3}): \('(\w)'\)")
reg_ex = re.compile("[ ]*([0-9]{3}): \('(\w)'\)[.]*")
reg_ex_part = re.compile(r".*([0-9]{3}):.*\((.*),")
reg_ex_rest = re.compile(r"(.*),\).*")
# reg_ex = re.compile(r".*([0-9]{3}):([.]*)")
reg_ex_complete = re.compile(r".*([0-9]{3}):.*\((.*)\),")
# reg_ex = re.compile(r"^.*([0-9]{3}):.*$")
# reg_ex = re.compile(r"^.*([0-9]{3}):.*,$")


def main():
    status_codes = defaultdict(list)
    try:
        response = requests.get("https://raw.githubusercontent.com/psf/requests/master/requests/status_codes.py")
        consider_next_line = False
        last_status_code = None
        for line in response.text.split("\n"):
            if line:
                line = line.strip()
                if consider_next_line:
                    consider_next_line = False
                    ls = reg_ex_rest.search(line.strip())
                    if ls:
                        meanings = ls.groups()[0].split()
                        for meaning in meanings:
                            trantab = str.maketrans({"'": None, ",": None})
                            value = meaning.translate(trantab)
                            status_codes[last_status_code].append(value)

                else:
                    ls = reg_ex_complete.search(line.strip())
                    if ls:
                        meanings = ls.groups()[1].split()
                        for meaning in meanings:
                            trantab = str.maketrans({"'": None, ",": None})
                            value = meaning.translate(trantab)
                            status_codes[ls.groups()[0]].append(value)
                    else:
                        ls = reg_ex_part.search(line.strip())
                        if ls:
                            consider_next_line = True
                            last_status_code = ls.groups()[0]
                            meanings = ls.groups()[1].split()
                            for meaning in meanings:
                                trantab = str.maketrans({"'": None, ",": None})
                                value = meaning.translate(trantab)
                                status_codes[ls.groups()[0]].append(value)

    except (Exception) as e:
        logger.error(f"Error '{str(e)}'.")
    
    for k, v in status_codes.items():
        print(k, v)


if __name__ == "__main__":
    sys.exit(main())
