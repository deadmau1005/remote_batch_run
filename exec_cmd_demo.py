import paramiko_clien
import os

from paramiko_clien import SUCCESS
from utils import *

SUCCESS = 0
FAIL = 1


if __name__ == '__main__':
    host_info_file = 'host_info.txt'
    host_info_list = parse_host_info(host_info_file)

    for host_info in host_info_list:
        node_name = host_info.split(' ')[0]
        node_ip = host_info.split(' ')[1]
        user = host_info.split(' ')[2]
        passwd = host_info.split(' ')[3]
        pkey = 'id_ed25519'
        node_info = NodeInfo(
            node_name=node_name,
            node_ip=node_ip,
            user=user,
            passwd=passwd,
            pkey=pkey
        )

        client = paramiko_clien.Client(
            node_name=node_info.node_name,
            node_ip=node_info.node_ip,
            user=node_info.user,
            passwd=node_info.passwd,
            pkey=node_info.pkey
        )

        client.connect_from_pkey()
        cmd = 'source ~/.bashrc;cd /home/dty;pwd;ls'
        ret_code = client.exec_cmd(cmd, timeout=3)
        if ret_code == FAIL:
            continue
        print(ret_code)
        client.close()

