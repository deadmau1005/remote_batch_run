import paramiko
import os
import re

SUCCESS = 0
FAIL = 1

class Client(paramiko.SSHClient):
    def __init__(self, node_name, node_ip, user, port=22, passwd=None, pkey=None):
        super().__init__()
        self.node_name = node_name
        self.node_ip = node_ip
        self.user = user
        self.port = port
        self.passwd = passwd
        self.pkey = pkey
        self.sftp = None
        super().set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.passwd is None and self.pkey is None:
            print('password and pkey is None')
            raise 1

    def connect_from_passwd(self, timeout=3):
        try:
            super().connect(
                hostname=self.node_ip,
                port=self.port,
                username=self.user,
                password=self.passwd,
                timeout=timeout,
            )
            return SUCCESS
        except Exception as e:
            print(f'connect to {self.node_ip} fail, {e}')
            return FAIL

    def connect_from_pkey(self, timeout=3):
        try:
            pkey = paramiko.Ed25519Key.from_private_key_file(self.pkey)
            super().connect(
                hostname=self.node_ip,
                port=self.port,
                username=self.user,
                pkey=pkey,
                timeout=timeout,
            )
            return SUCCESS
        except Exception as e:
            print(f'connect to {self.node_ip} fail,{type(e)} {e}')
            return FAIL

    def exec_cmd(self, cmd, timeout=3):
        try:
            if isinstance(cmd, str):
                stdin, stdout, stderr = super().exec_command(command=cmd,
                                                             timeout=timeout)
                return stdout.read().decode('utf-8')
            elif isinstance(cmd, list):
                res = []
                for _cmd in cmd:
                    stdin, stdout, stderr = super().exec_command(command=_cmd,
                                                                 timeout=timeout)
                    res.append(stdout.read().decode('utf-8'))
                return res
        except Exception as e:
            print(f'command exec fail, {e}')
            return FAIL


    def open_sftp_client(self):
        self.sftp = super().open_sftp()


    def sftp_get(self, remote_path, local_path):
        try:
            self.sftp.get(remote_path, local_path)
            return SUCCESS
        except Exception as e:
            print(f'get file from remote fail, {e}')
            return FAIL


    def sftp_put(self, local_path, remote_path):
        try:
            self.sftp.put(local_path, remote_path)
            return SUCCESS
        except Exception as e:
            print(f'put file to remote fail, {e}')
            return FAIL


    def sftp_put_dir(self, local_path, remote_path):
        try:
            root_dir_name = os.path.basename(local_path)
            for root, dir_list, file_list in os.walk(root_dir_name):
                for dir_name in dir_list:
                    _remote_dir = os.path.join(remote_path, root, dir_name).replace('\\', '/')
                    self.exec_cmd(f"mkdir -p {_remote_dir}")
                for file_name in file_list:
                    _local_path = os.path.join(root, file_name)
                    _remote_path = os.path.join(remote_path, _local_path).replace('\\', '/')
                    self.sftp_put(_local_path, _remote_path)
            return SUCCESS
        except Exception as e:
            print(f'put dir to remote fail, {e}')
            return FAIL

