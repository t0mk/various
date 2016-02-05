#!/usr/bin/env python

import datetime
import sys

def decode(code):

    if code[0] != "4":
        raise Exception("Unsupported version")
    iban = "FI" + code[1:17]
    print "IBAN:", iban
    eur = int(code[17:25].lstrip('0')) / 100.0
    print "Amount EUR:", eur
    refnum = code[25:48].lstrip('0')
    print "Reference:", refnum
    date = datetime.datetime.strptime(code[48:54], "%y%m%d")
    print date
    

# example code
c = '496166030002156010004444900050150680530540910699150623'

if len(sys.argv) > 1:
    c = sys.argv[1]

decode(c)
