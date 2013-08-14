#!/usr/bin/env python

# Script getting ads on lyyra.fi for listed postal codes. it will collect
# add the relevant ads and sedn it by email in nice format - you'll be only
# one click away from seeing the location and you'll see description,
# publication date and avaiability date, and also a link on the ad.
# It also stored the read links in pickle file, so that you will only be
# shown the new ones in each script run. If you want to see all, just
# delete the pickle file.

# Things you want to modify:
# - list of the postal codes you want to see (POSTAL_CODES)
# - filename for the pickle storage of read ads (READ_LINKS_STORAGE)
# - the credentials in function sendmail - you need to specify destination
#   email, and an account to send the email from. I suggest to create a
#   dummy gmail account, as you need to store the password in this script

# Bonne chance!!

import urllib2
import urllib
import datetime
import re
import os
import sys
import pickle
import smtplib
import email.mime.text

# need to isntall python-mechanize and python-beautifulsoup
import mechanize
import BeautifulSoup


READ_LINKS_STORAGE = '/home/tomk/readlyyra.pi'

# areas around Otaniemi
POSTAL_CODES = ["02100",
      "02101",
      "02110",
      "02120",
      "02130",
      "02131",
      "02140",
      "02150",
      "02151",
      "02160",
      "02170",
      "02171",
      "02180"]

#POSTAL_CODES = ["02100"]

def getLinksForArea(code):
    br = mechanize.Browser()
    br.open('https://www.lyyra.fi/browse_lyyrarentals.php')
    forms = br.forms()
    br.select_form("browse_lyyrarentals")
    post = br.form.find_control('field_27')
    post.value = code
    print "submitting search"
    resp = br.submit()
    ls = []
    for link in br.links(url_regex='asunnot/ilmoitus', text_regex="Lis"):
        ls.append(link.url)
    return ls


def gatherLinksForCodes(codes_list):
    r = {}
    for n in codes_list:
        print "getting links for postal code %s" % n
        r[n] = getLinksForArea(n)
    return r


def getAdData(ad):

    def getField(soup, fieldname):
        preceeding_field = soup.find(text=re.compile(fieldname))
        if preceeding_field:
            the_field = preceeding_field.findParent().findNextSibling(name='td')
            return the_field.renderContents().strip()
        else:
            return None
    resp = urllib2.urlopen(ad)
    s = BeautifulSoup.BeautifulSoup(resp.read())

    desc = getField(s, 'Kuvaus:')
    ddate = getField(s, 'Ilmoitus j')
    avail = getField(s, 'Saatavuus:')
    addr = getField(s, 'Osoite:')
    return (desc, ddate, avail, addr)


def resolveCity(li, di):
    for pn in di:
        if li in di[pn]:
            if pn.startswith("02"):
                return "Espoo"
            elif pn.startswith("00"):
                return "Helsinki"
    raise Exception("unknown city for link %s, with dict %s" % li, di)


def sendmail(txt_par):
    m = email.mime.text.MIMEText(txt_par)
    destination = '__your_email_@gmail.com'
    frommail = '_from_email__t@gmail.com'
    m['To'] = destination
    m['Subject'] = 'New ads ' + datetime.datetime.now().__str__()[:19]
    m['from'] = frommail
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.login(frommail, '_password__')
    s.sendmail(destination, [destination], m.as_string())
    s.quit()


def getReadLinks():
    if os.path.isfile(READ_LINKS_STORAGE):
        rl = pickle.load(open(READ_LINKS_STORAGE,"rb"))
    else:
        rl = []
    return rl


def saveLinks(old, current):
    print "Adding sent links to read set"
    to_save = list(set(old) | set(current))
    pickle.dump(to_save, open(READ_LINKS_STORAGE, "wb" ) )


def compileEmail(ads_dict, ads_by_code):
    txt = ""
    for link in ads_dict:
        d, p, a, addr = ads_dict[link]
        d = d.replace("<br />","\n")
        addr = addr.replace("<br />","").strip()
        city = resolveCity(link, ads_by_code)
        addr = addr.replace(" ", "%20")
        maps_addr = "https://maps.google.fi/maps?q=%s,%s" % (addr, city)
        txt += ("%s:\nDESCRIPTION: %s\nPUBLISHED: %s\nAVAILABLE: %s\n"
                "ADDRESS: %s\n" % (link,d,p,a, maps_addr))
        txt += "-" * 80
        txt += "\n\n"
    return txt


links_by_code = gatherLinksForCodes(POSTAL_CODES)
current_links = sum(links_by_code.values(), [])
read_links = getReadLinks()

ads_to_send = {a: getAdData(a) for a in set(read_links) ^ set(current_links)}

if not ads_to_send:
    print "no new ads. not sending any email"
    sys.exit(0)

msg = compileEmail(ads_to_send, links_by_code)

sendmail(msg)

saveLinks(read_links, current_links)


