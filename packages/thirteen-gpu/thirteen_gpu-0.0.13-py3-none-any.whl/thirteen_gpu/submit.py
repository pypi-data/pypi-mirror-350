import argparse
import os
from .ssh import SSH
from datetime import datetime, timezone, timedelta


parser = argparse.ArgumentParser()
parser.add_argument('--user', required=True)
parser.add_argument('--project', required=True)
parser.add_argument('--path', required=True, help='e.g) /path/to/neural-quant')
parser.add_argument("--alarm", action="store_true", default=False)

args = parser.parse_args()


def main():
    SCHEDULER_IP = "ip-172-31-1-4.tail58fd99.ts.net"
    SCHEDULER_USER = "seilna"
    SCHEDULER_PORT = 22

    os.system(f"ssh-copy-id -f {SCHEDULER_USER}@{SCHEDULER_IP} -p {SCHEDULER_PORT}")

    ssh = SSH(SCHEDULER_IP, SCHEDULER_PORT, SCHEDULER_USER)

    WORKSPACE_DIR = f"/home/{SCHEDULER_USER}/tmux_workspace"

    if ssh.is_exists(f"{WORKSPACE_DIR}/{args.project}"):
        print(f"Project {args.project} already exists.")
        exit(1)

    else:
        ssh.ssh_copy(args.path, f"{WORKSPACE_DIR}/{args.project}")
        ssh.ssh_exec_command(
            f"echo {args.user} > {WORKSPACE_DIR}/{args.project}/user.txt"
        )

        submit_at = datetime.now(timezone(timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')
        ssh.ssh_exec_command(
            f"echo {submit_at} > {WORKSPACE_DIR}/{args.project}/submit_at.txt"
        )

        if args.alarm:
            ssh.ssh_exec_command(
                f"echo {args.project} > {WORKSPACE_DIR}/{args.project}/alarm.txt"
            )

        print(f"[Submit Project] {args.project}")

if __name__ == '__main__':
    main()
