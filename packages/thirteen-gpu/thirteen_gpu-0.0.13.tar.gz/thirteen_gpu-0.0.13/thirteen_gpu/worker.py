from collections import defaultdict
from pprint import pprint
import json

from .definition import WORKSPACE_DIR, JobStatus, status_match_table
from .ssh import SSH


class GPU(object):
    def __init__(self, ip, port, user, gpu_id):
        self.ip = ip
        self.port = port
        self.user = user
        self.gpu_id = gpu_id


class Worker(object):

    def __init__(self, name, ip, port, user, n_gpus, home, owner):
        self.name = name
        self.ip = ip
        self.port = port
        self.user = user
        self.n_gpus = n_gpus
        self.home = home

        # print(f"Connecting to {name} ({user}@{ip}:{port})")
        import os, contextlib
        with contextlib.redirect_stderr(open(os.devnull, "w")):
            self.ssh = SSH(ip, port, user)

        print(f"[Success] Connection {name} ({user}@{ip}:{port})")

        self.owner = owner

        # user_setup.json에서 max_jobs_per_gpu 설정 읽기
        try:
            with open('thirteen_gpu/user_setup.json') as f:
                user_setup = json.load(f)
            self.max_jobs_per_gpus = defaultdict(lambda: 2, user_setup.get('max_jobs_per_gpus', {}))
        except Exception as e:
            print(f"user_setup.json 로드 실패: {e}")
            self.max_jobs_per_gpus = defaultdict(lambda: 2)
        self.max_jobs_per_gpu = self.max_jobs_per_gpus[self.owner]

    def get_available_gpus(self):
        """job 이 `max_jobs_per_gpu` 개 이하로 사용 중인 gpu 목록 반환한다"""

        gpu_usage = defaultdict(int)
        # gpu_usage = {gpu: 0 for gpu in range(self.n_gpus)}

        # tmux session 이름들을 가져오기
        try:
            sessions = self.ssh.ssh_exec_command(f"tmux ls | cut -d ':' -f 1")
        except:
            # ssh connection 이 끊어진 경우 -> GPU 를 사용할 수 없으므로 빈 리스트 반환
            return []

        # session 이름으로부터 사용중인 GPU 개수 카운팅
        for session_name in sessions.split("\n"):
            if session_name.startswith("gpu"):
                gpu_id = int(session_name.split("_")[0].replace("gpu", ""))
                gpu_usage[gpu_id] += 1

        # 사용 중인 gpu 제외하고 남은 gpu 반환
        available_gpus = []
        for gpu_id in range(self.n_gpus):
            for count in range(self.max_jobs_per_gpu - gpu_usage[gpu_id]):
                available_gpus.append(GPU(self.ip, self.port, self.user, gpu_id))

        return available_gpus

    def get_running_sessions(self):
        sessions = self.ssh.ssh_exec_command(f"tmux ls | cut -d ':' -f 1").split("\n")

        sessions = [session for session in sessions if session.startswith("gpu")]

        return sessions

    def update_job_status(self, projects: list):
        """Worker 안에서 실행되는 모든 프로젝트의 job 들의 상태를 업데이트한다"""

        project_names, job_names, status_values = [], [], []

        # read */*.status files with filename format: job_{job_name}.status
        # for line in self.ssh.ssh_exec_command("tail */*.status").split("\n"):
        for line in self.ssh.ssh_exec_command('for fname in */*.status; do echo \"==> $fname <==\"; tail \"$fname\"; done').split("\n"):

            if line.strip() == "":
                continue

            elif "==>" in line:
                line = line.split("==> ")[-1].split(" <==")[0]
                project, job = line.split("/")
                job = job.replace(".status", "")

            elif line.strip() in ["running", "finished", "failed", "stopped"]:
                # status 파일이 빈 경우가 있어서 (원인불명), ==> line 에서는 project, job 변수를 갱신만 해두고,
                # status value 가 정상적으로 읽히는 경우에만 append 를 해준다.
                try:
                    project_names.append(project)
                    job_names.append(job)
                    status_values.append(line)
                    print(f"{self.name=} {project=} {job=} {line=}")
                except Exception as e:
                    print(f"in update, 3, {line=}, {e=}")
                    raise ValueError(
                        f"status 에 적힌 로그가 이상합니다. {self.name=}, {line=}"
                    )

            else:
                raise ValueError(f"Unknown status contents: {line=}")

        for job, status_value in zip(job_names, status_values):
            for project in projects:
                if job in project.jobs:
                    # 이미 status 가 정해진 job 은 skip
                    if project.jobs[job].status in (
                        JobStatus.SUCCESS,
                        JobStatus.FAILED,
                        JobStatus.STOPPED,
                    ):
                        continue

                    if status_value in status_match_table:
                        project.jobs[job].status = status_match_table[status_value]
                    else:
                        project.jobs[job].status = JobStatus.UNKNOWN

    def run_jobs(self, jobs: list, gpus: list):
        if len(jobs) == 0 or len(gpus) == 0:
            return

        project_names = {job.project_name for job in jobs}

        for project_name in project_names:
            self.ssh.ssh_copy(
                src=f"{WORKSPACE_DIR}/{project_name}",
                dst=f"{self.home}/{project_name}/",
            )

        commands = []
        session_names = []

        for job, gpu in zip(jobs, gpus):
            REMOTE_WORKSPACE_DIR = f"{self.home}/{job.project_name}"
            command = (
                f"test -e {REMOTE_WORKSPACE_DIR}/data || ln -s /data {REMOTE_WORKSPACE_DIR}/ && "
                + f"mkdir -p {REMOTE_WORKSPACE_DIR}/.results && "
                + f"export AWS_ACCESS_KEY_ID=AKIAXCPLIY4KT76BUDF4 && "
                + f"export AWS_SECRET_ACCESS_KEY=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 && "
                + f"export AWS_S3_BUCKET=thirteen-ai && "
                + f"export CUDA_VISIBLE_DEVICES={gpu.gpu_id} && "
                + f"source $HOME/.miniconda3/bin/activate && "
                + f"cd {REMOTE_WORKSPACE_DIR} && "
                + f"echo 'running' > {REMOTE_WORKSPACE_DIR}/{job.job_name}.status && "
                + f"(python {job.executed_filename} {job.config_path} >> {REMOTE_WORKSPACE_DIR}/{job.job_name}.log 2>&1 && "
                + f"echo 'finished' > {REMOTE_WORKSPACE_DIR}/{job.job_name}.status) || "
                + f"echo 'failed' > {REMOTE_WORKSPACE_DIR}/{job.job_name}.status"
            )

            session_name = f"gpu{gpu.gpu_id}_{job.job_name}"
            session_names.append(session_name)

            command = f"tmux new-session -s {session_name} -d '{command}'"
            commands.append(command)

        ssh_command = " && ".join(commands)

        self.ssh.ssh_exec_command(ssh_command)

        pprint(f"{self.name} run {len(session_names)} Jobs: \n{session_names}")

        for job in jobs:
            job.status = JobStatus.RUNNING
            job.worker = self

    def get_hostname(self):
        try:
            hostname = self.ssh.ssh_exec_command("hostname").strip()
            return hostname
        except Exception as e:
            return f"Error: {e}"
