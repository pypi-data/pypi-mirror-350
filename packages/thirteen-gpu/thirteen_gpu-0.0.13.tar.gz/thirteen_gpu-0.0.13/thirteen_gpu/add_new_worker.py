import argparse
import re
import json
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--ssh_command", type=str, default=None)
parser.add_argument("--vast_id", type=str, required=True)
parser.add_argument("--user", type=str, required=True)
args = parser.parse_args()

if args.ssh_command is not None:
    _, _, new_port, user_ip, _, _ = args.ssh_command.split(" ")
    new_user, new_ip = user_ip.split("@")

elif args.vast_id is not None:
    instance = json.loads(
        subprocess.check_output(
            f"vastai show instance --raw {args.vast_id}", shell=True
        )
    )

    new_ip = instance["ssh_host"]
    new_port = instance["ssh_port"]
    new_user = "root"

home = "/home/seilna"
print(f"{new_ip=}, {new_port=}, {new_user=}")


hosts, ports = [], []

# 0. .ssh/config 에 추가
already_exists = False

new_machine_id = 0
with open(f"{home}/.ssh/config", "r") as f:
    for line in f.readlines():
        line = line.strip()

        if "hostname" in line:
            ip = line.split(" ")[-1]

        if "port" in line:
            port = line.split(" ")[-1]
            ports.append(port)

            if ip == new_ip and port == new_port:
                already_exists = True

        if "Host" in line:
            host = line.split(" ")[-1]
            hosts.append(host)

            machine_id = int(re.findall("(\d+)", line)[0])
            new_machine_id = max(machine_id + 1, new_machine_id)

new_host = f"v{new_machine_id}"

if already_exists:
    print(f"{new_ip=}, {new_port=}, {new_user=} already exists")
    exit()

else:
    hosts.append(new_host)
    ports.append(new_port)

    with open(f"{home}/.ssh/config", "a+") as f:
        f.write(f"Host {new_host}\n")
        f.write(f"    hostname {new_ip}\n")
        f.write(f"    user {new_user}\n")
        f.write(f"    port {new_port}\n")

    # # 1. gpustat web 에 추가
    with open(f"{home}/gpustat-web/gpustat_command.txt", "w") as f:
        command = f"python3 -m gpustat_web --port 2014 "
        for host, port in zip(hosts, ports):
            command += f"{host}:{port} "
        f.write(command)

    # 2. workers.json 에 추가
    from ssh import SSH

    ssh = SSH(new_ip, new_port, new_user)
    n_gpus = int(ssh.ssh_exec_command("nvidia-smi --list-gpus | wc -l").strip())

    workers = json.loads(open(f"thirteen_gpu/workers.json", "r").read())
    workers[new_host] = {
        "name": new_host,
        "ip": new_ip,
        "port": new_port,
        "user": new_user,
        "n_gpus": n_gpus,
        "home": f"/root",
        "owner": args.user,
    }

    json.dump(workers, open(f"thirteen_gpu/workers.json", "w"), indent=4)

    print(f"{new_host=}")

    import os

    # os.system("pkill -f run_scheduler.py && pkill -f gpustat_web")
