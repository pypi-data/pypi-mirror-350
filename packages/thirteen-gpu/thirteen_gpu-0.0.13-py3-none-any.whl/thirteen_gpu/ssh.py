import paramiko
import os


class SSH(object):
    def __init__(self, ip, port, user):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(ip, port, user, timeout=10, banner_timeout=10, auth_timeout=10)

        self.ip = ip
        self.port = port
        self.user = user

    def ssh_exec_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdout.read().decode()

    def ssh_copy(self, src, dst):
        os.system(
            f"rsync -qrve 'ssh -p {self.port} -o StrictHostKeyChecking=no' --include='*/' --include=returns/*.pkl --include='*.sh' --include='*.py' --include='*.json' --exclude='*' {src}/ {self.user}@{self.ip}:{dst}"
        )

    def is_exists(self, path):
        out = self.ssh_exec_command(f"ls {path}")
        return out != ""
