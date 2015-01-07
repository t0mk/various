#!/usr/bin/env python

# lists forks of a github repo sorted by time of latest push
# call as
# $ forks.py <github http[s] repo url> | <user|org> <repo>
# for example
# $ forks.py github.com/ansible/ansible
# or
# $ forks.py ansible ansible

import requests
import sys
import dateutil.parser

def usage():
    print "%s <repo_url> | <username> <repo>" % (sys.argv[0])
    sys.exit(1)

def from_iso8601(when=None):
    _when = dateutil.parser.parse(when)
    return _when

if len(sys.argv) not in [2,3]:
    usage()

if len(sys.argv) == 2:
    user, repo = sys.argv[1].split('/')[-2:]

if len(sys.argv) == 3:
    user = sys.argv[1]
    repo = sys.argv[2]

print "getting list of all the forks ..."
allforks_url = ("https://api.github.com/repos/%s/%s/forks?per_page=100" %
                 (user, repo))
resp = requests.get(allforks_url)
forks = resp.json()
if type(forks) is not list:
    print 'not list returned:'
    print forks
    sys.exit(1)


while 'next' in resp.links:
    new_url = resp.links['next']['url']
    print 'there is more than last page, getting it:'
    print new_url, '...'
    resp = requests.get(new_url)
    forks.extend(resp.json())

forks.sort(key=lambda x: from_iso8601(x['pushed_at']))

for f in forks:
    print "-------------------"
    print f['html_url']
    print f['pushed_at']

