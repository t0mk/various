#!/usr/bin/env python

import sys

def whole(amount, rate_pro, yrs):
    monthly_interest = rate_pro/(100 * 12)
    payments = yrs * 12
    m = amount * ( monthly_interest / (1 - (1 + monthly_interest) ** (- payments)))
    return (m, m*payments, (m*payments)-amount)

amount = int(sys.argv[1])
rate_pro = float(sys.argv[2])
yrs = int(sys.argv[3])

monthly, total, over = whole(amount, rate_pro, yrs)
print "montly: %.2f" % monthly
print "total: %.2f" % total
print "over: %.2f" % over



