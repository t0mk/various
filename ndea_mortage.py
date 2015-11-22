#!/usr/bin/env python3

# If you want details of Nordea mortage for 100000 EUR for 20 years with
# interest rate 1.4% call this as:
#
# $ ./ndea_mortage.py mortage -a 100000 -y 20 -i 1.4

import requests
import argparse
import argh
import json


URL = "http://www.nordea.fi/wemapp/api/housingloancalculator/calculatehousingloan/loantype/%s/loanamount/%s/years/%s/amortfree/0/periodicity/1/interest/%s"

def mortgage(amount='200000', years='20', interest='1.1', loantype='a2'):
    "Fetches Nordea mortage details with given parameters. Based on http://www.nordea.fi/en/personal-customers/loans/buying-a-home/loan-calculator.html"
    url = URL % (loantype, amount, years, interest)
    print(url)
    resp = requests.get(url, timeout=60)
    if resp.status_code != 200:
        print("Error while fetching %s:" % url)
        print(resp.text)
        return
    json_out = resp.json()
    # remove amortization calendar bullcrap
    del(json_out['payment'])
    del(json_out['paymentNr'])
    del(json_out['paymentList'])
    del(json_out['paymentAmortization'])
    print(json.dumps(json_out, sort_keys=True, indent=4))


if __name__ == "__main__":
    parser = argh.ArghParser()

    exposed = [mortgage]
    argh.assembling.set_default_command(parser, mortgage)

    parser.add_commands(exposed)

    parser.dispatch()

