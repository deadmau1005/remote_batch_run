import os
import sys
import re


class NodeInfo:
    def __init__(self, node_name, node_ip, user, passwd=None, pkey=None):
        self.node_name = node_name
        self.node_ip = node_ip
        self.user = user
        self.passwd = passwd
        self.pkey = pkey

def parse_host_info(file_name):
    file_pointer = open(file_name, 'r')
    filter_str = ''
    host_info = []
    if len(sys.argv) == 1:
        filter_str = ''
    elif len(sys.argv) == 2:
        filter_str = sys.argv[1]
    for line in file_pointer.readlines():
        if line.startswith('#'):
            continue
        if re.search(filter_str, line):
            host_info.append(line)
    return host_info

