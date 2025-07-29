import argparse
from .ssh import SSH

parser = argparse.ArgumentParser()
parser.add_argument('--user', required=True)
parser.add_argument('--project', required=True)

args = parser.parse_args()

def main():
    SCHEDULER_IP = "ip-172-31-1-4.tail58fd99.ts.net"
    SCHEDULER_USER = "seilna"
    SCHEDULER_PORT = 22

    ssh = SSH(SCHEDULER_IP, SCHEDULER_PORT, SCHEDULER_USER)
    
    WORKSPACE_DIR = f"/home/{SCHEDULER_USER}/tmux_workspace"
    
    if ssh.is_exists(f"{WORKSPACE_DIR}/{args.project}"):
        ssh.ssh_exec_command(
            f"rm -rf {WORKSPACE_DIR}/{args.project}"
        )
        print(f"[Delete Project] {args.project}")

    else:
        print(f"[Delete Project] {args.project} is not exists")

if __name__ == "__main__":
    main()
