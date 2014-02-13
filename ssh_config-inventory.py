#!/usr/bin/env python

# Ansible dynamic inventory which lets you use aliases from ~/.ssh/config.

import paramiko
import argparse
import os.path
import sys

DOCUMENTATION = '''
---
inventory: ssh_config
short_description: inventory from OpenSSH client user config
description: |
    Prints inventory based on parsed ~/.ssh/config. You can refer to hosts
    with their alias, rather than with the IP or hostname. It takes advantage
    of the ansible_ssh_{host,port,user,private_key_file}.

    If you have in your .ssh/config:

        Host git
            HostName git.domain.org
            User tkarasek
            IdentityFile /home/tomk/keys/thekey

    You can do
        $ ansible git -m ping

author: Tomas Karasek
examples:
    - description: List hosts from .ssh/config
      code: ssh_config-inventory --list
    - description: Show hosts properties
      code: ssh_config-inventory --host INSTANCE_IP
'''


try:
    import json
except:
    import simplejson as json

_key = 'ssh_config'

ssh_to_ansible = [('user', 'ansible_ssh_user'),
                  ('hostname', 'ansible_ssh_host'),
                  ('identityfile', 'ansible_ssh_private_key_file'),
                  ('port', 'ansible_ssh_port')]


def checkDoc():
    # check if DOCUMENTATION is valid yaml
    # python-yaml should be installed anyway for ansible
    import yaml
    d = yaml.load(DOCUMENTATION)
    print d['description']

def getConfig():
    with open(os.path.expanduser('~/.ssh/config')) as f:
        cfg = paramiko.SSHConfig()
        cfg.parse(f)
        ret_dict = {}
        for d in cfg._config:
            _copy = dict(d)
            del _copy['host']
            ret_dict[d['host']] = _copy
        return ret_dict


def print_list():
    cfg = getConfig()
    meta = {'hostvars': {}}
    for alias, attributes in cfg.items():
        tmp_dict = {}
        for ssh_opt, ans_opt in ssh_to_ansible:
            if ssh_opt in attributes:
                tmp_dict[ans_opt] = attributes[ssh_opt]
        if tmp_dict:
            meta['hostvars'][alias] = tmp_dict

    print json.dumps({_key: list(set(meta['hostvars'].keys())), '_meta': meta})


def print_host(host):
    cfg = getConfig()
    print json.dumps(cfg[host])


def get_args(args_list):
    parser = argparse.ArgumentParser(
            description='ansible inventory script parsing .ssh/config')
    mutex_group = parser.add_mutually_exclusive_group(required=True)
    help_list = 'list all hosts from .ssh/config inventory'
    mutex_group.add_argument('--list', action='store_true', help=help_list)
    help_host = 'display variables for a host'
    mutex_group.add_argument('--host', help=help_host)
    help_check_doc = 'Check that DOCUMENTATION is valid yaml'
    mutex_group.add_argument('--check_doc', action='store_true',
                             help=help_check_doc)
    return parser.parse_args(args_list)


def main(args_list):

    args = get_args(args_list)
    if args.list:
        print_list()
    if args.host:
        print_host(args.host)
    if args.check_doc:
        checkDoc()


if __name__ == '__main__':
    main(sys.argv[1:])
