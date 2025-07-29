from collections import defaultdict
from datetime import datetime, timedelta
from glob import glob
import json
import threading
import os
from pprint import pprint
from time import sleep

from .definition import JobStatus, ProjectStatus, WORKSPACE_DIR, status_match_table
from .worker import Worker
from .project import Project


def execute_by_threads(threads: list):
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def get_available_gpus(worker, results):
    gpus = worker.get_available_gpus()
    results[worker.name] = gpus
    print(f"Get Available GPUs for {worker.name}, {[g.gpu_id for g in gpus]}")


def dispatch_jobs(worker: Worker, jobs, available_gpus):
    worker.run_jobs(jobs, available_gpus)


def connect_worker(worker_info, workers):
    try:
        worker = Worker(**worker_info)
        workers[worker.name] = worker
    except:
        return None


def main():
    print("start")
    # workers 정보 가져오기
    workers_info = json.load(open("thirteen_gpu/workers.json"))

    projects = []

    first_iteration = True
    worker_pool_last_update = datetime.now() - timedelta(days=999)

    for loop in range(5):
        print(f"loop: {loop}")

        """각 worker 에 connection 을 test 하여, 정상적으로 연결되어 있는 worker 를 active workers 로 정의한다"""
        if datetime.now() - worker_pool_last_update >= timedelta(seconds=10):
            workers_dict = {}
            
            # 각 worker 서버에 연결 시도
            threads = [
                threading.Thread(
                    target=connect_worker,
                    args=(
                        worker_info,
                        workers_dict,
                    ),
                )
                for worker_info in workers_info.values()
            ]

            execute_by_threads(threads)

            workers = [
                workers_dict[worker_name] for worker_name in sorted(workers_dict.keys())
            ]
            worker_pool = defaultdict(list)
            for worker in workers:
                worker_pool[worker.owner].append(worker.name)
            with open("thirteen_gpu/worker_pool_names.txt", "w") as f:
                f.write(str(json.dumps(dict(worker_pool), indent=4)))

        sleep(1)

        """ 유저가 제출한 프로젝트 목록 가져오기 (시간 순 정렬) """
        new_projects = []
        for project_path in glob(f"{WORKSPACE_DIR}/*"):
            user = open(f"{project_path}/user.txt").read().strip()
            submit_at = open(f"{project_path}/submit_at.txt").read().strip()

            if os.path.exists(f"{project_path}/command.json"):
                with open(f"{project_path}/command.json", "r") as file:
                    executed_filename = json.load(file).get("command", "train.py")
            else:
                executed_filename = "train.py"

            new_projects.append(
                Project(project_path, user, submit_at, executed_filename)
            )

        new_projects = sorted(new_projects, key=lambda x: x.submit_at)
        # 추가된 project
        for new_project in new_projects:
            if new_project.project_name not in [project.project_name for project in projects]:
                projects.append(new_project)

        deleted_jobs = []

        """ 각 worker 들에서 job status 정보를 읽어와서 메모리에 업데이트 한다 """
        # Warning: 간혹 어떤 worker 와의 connection 이 불안정하여, 해당 worker 가 돌렸던 job status 를 못 읽어오는 경우가 있음
        # 이러한 경우, 현재 코드에서는 job 이 안 돌아가는 것으로 간주함 (pending 상태로 잘못 판단)
        if first_iteration:
            first_iteration = False

            # 각 worker 들에 존재하는 *.status 파일들을 읽어와서, project / job / status 로 파싱하여 저장
            project_names, job_names, status_values = [], [], []
            for worker in workers:
                for line in worker.ssh.ssh_exec_command("tail */*.status").split("\n"):
                    if line.strip() == "":
                        continue

                    elif "==>" in line:
                        line = line.split("==> ")[-1].split(" <==")[0]
                        project, job = line.split("/")
                        job = job.replace(".status", "")

                    elif line.strip() in ["running", "finished", "failed", "stopped"]:
                        # status 파일이 빈 경우가 있어서 (원인불명), ==> line 에서는 project, job 변수를 갱신만 해두고,
                        # status value 가 정상적으로 읽히는 경우에만 append 를 해준다.
                        project_names.append(project)
                        job_names.append(job)
                        status_values.append(line)

                    else:
                        raise ValueError(f"Unknown status contents: {line=}")

            # 각 job 에 대한 status 를 project.jobs.status 에 할당
            for project_name, job, status_value in zip(
                project_names, job_names, status_values
            ):
                assign_status = False

                for project in projects:
                    if project.project_name == project_name and job in project.jobs:
                        if status_value in status_match_table:
                            project.jobs[job].status = status_match_table[status_value]
                        else:
                            project.jobs[job].status = JobStatus.UNKNOWN

                        assign_status = True
                        break

                # status 가 알 수없는 값이라면, 해당 job 을 삭제 대상에 추가한다
                if assign_status is False:
                    deleted_jobs.append(job)

        # 메모리로 관리하는 projects 가 있는데, 디스크에는 없으면 삭제된 것으로 간주함
        deleted_projects = []
        for project in projects:
            if project.status == ProjectStatus.DEAD:
                continue

            if project.project_name not in [new_project.project_name for new_project in new_projects]:
                deleted_projects.append(project)

        deleted_jobs += [
            job.job_name
            for project in deleted_projects
            for job in project.jobs.values()
        ]

        print(f"projects: {[project.project_name for project in projects]}")
        print(f"{deleted_projects=}")

        """ 중지해야 하는 프로젝트 목록을 받아와서 각 worker 들에서 job 들을 kill 한다 """
        if len(deleted_projects) > 0 or len(deleted_jobs) > 0:
            # worker 마다 deleted job 에 해당하는 container 중지
            def delete_jobs_in_worker(worker: Worker):
                # running jobs 목록 가져오기
                running_sessions = worker.get_running_sessions()

                # Running 중인 Job 인데, deleted project 목록에 있으면 stop
                stopping_sessions = []
                for session in running_sessions:
                    # session_name -> gpuX_jobname
                    # job_name -> jobname
                    job_name = "_".join(session.split("_")[1:])
                    if job_name in deleted_jobs:
                        stopping_sessions.append(session)

                if len(stopping_sessions) > 0:
                    pprint(f"{worker.name} 에서 중지할 job: {stopping_sessions}")
                    command = ""
                    for session in stopping_sessions:
                        command += f"tmux kill-session -t {session};"
                    worker.ssh.ssh_exec_command(command)

            threads = [
                threading.Thread(target=delete_jobs_in_worker, args=(worker,))
                for worker in workers
            ]
            execute_by_threads(threads)

            # Canceled project 와 Finished Project 는 둘 다 디스크에서 프로젝트가 삭제되는데,
            # 이 2개를 구분하지 않고  모두 Job Status 를 STOPPED 로 변경하고 있음...
            for project in deleted_projects:
                project.delete()

                for job in project.jobs.values():
                    job.status = JobStatus.STOPPED

        """ pending 상태인 job 들을 각 worker 에 dispatch 한다 """
        # projects 를 job 단위로 분리
        jobs = []
        for project in projects:
            if project.status.value != ProjectStatus.LIVE.value:
                continue

            for job in project.jobs.values():
                if job.status.value == JobStatus.PENDING.value:
                    jobs.append(job)

        print(f"pending jobs: {[job.job_name for job in jobs]}")

        # 각 서버마다 available GPUs 목록을 받아온다
        available_gpus = {}
        threads = [
            threading.Thread(target=get_available_gpus, args=(worker, available_gpus))
            for worker in workers
        ]
        execute_by_threads(threads)

        n_job_slots = sum([len(gpus) for gpus in available_gpus.values()])
        n_job_slots_per_user = defaultdict(int)
        for worker_name, gpus in available_gpus.items():
            for worker in workers:
                if worker.name == worker_name:
                    n_job_slots_per_user[worker.owner] += len(gpus)
                    break

        job_dispatch_args = []

        for worker in workers:
            gpus = available_gpus[worker.name]
            if len(gpus) == 0:
                continue

            """ 현재 worker 에 뿌릴 pending jobs 목록 가져오기: job 의 user 가 현재 worker 의 owner 인 경우로 제한함 """
            pending_jobs_for_user = [job for job in jobs if job.user == worker.owner]

            job_dispatch_args.append((worker, pending_jobs_for_user[: len(gpus)], gpus))

            jobs = [
                job for job in jobs if job not in pending_jobs_for_user[: len(gpus)]
            ]

            print(
                f"{worker.name} 에 뿌릴 pending jobs: {[job.job_name for job in pending_jobs_for_user[: len(gpus)]]}"
            )

            # jobs = jobs[len(gpus) :]

        # 현재 pending 중인 job 들을 각 서버에 dispatch 한다.
        print("1")
        threads = [
            threading.Thread(target=dispatch_jobs, args=job_dispatch_arg)
            for job_dispatch_arg in job_dispatch_args
        ]
        execute_by_threads(threads)
        print("2")

        with open("thirteen_gpu/available_job_slots.txt", "w") as f:
            # f.write(str(n_job_slots))
            f.write(str(dict(n_job_slots_per_user)))

        # Job status 업데이트 -> Thread 로 하면 원인불명의 에러가 나서, 메인 프로세스에서 직접 업데이트
        for worker in workers:
            print(f"update job status for {worker.name}")
            worker.update_job_status(projects=projects)
            print(f"update job status for {worker.name} done")
        print("3")
        # Job status 를 디스크에 저장하여, 대시보드에서 읽어올 수 있도록 함
        with open(f"thirteen_gpu/status.json", "w") as f:
            status = defaultdict(lambda: defaultdict(int))

            for project in projects:
                # initialize status dict (dict of dict of int)
                status[project.project_name]["user"] = project.user
                status[project.project_name]["submit_at"] = project.submit_at
                status[project.project_name]["status"] = defaultdict(int)

                for job in project.jobs.values():
                    status[project.project_name]["status"][job.status.name] += 1

            # dump to json file
            json.dump(status, f, indent=4)
        print("4")
        # 특정 Project 의 모든 Job 이 끝난 상태면, Project 폴더 삭제
        for project in projects:
            if project.status.value == ProjectStatus.DEAD.value:
                continue

            if all(
                [
                    job.status
                    in (
                        JobStatus.SUCCESS,
                        JobStatus.FAILED,
                        JobStatus.CRASHED,
                        JobStatus.STOPPED,
                        JobStatus.UNKNOWN,
                    )
                    for job in project.jobs.values()
                ]
            ):
                print(f"Delete project {project.project_name}")
                project.delete()

                if os.path.exists(f"{project.project_path}/alarm.txt"):
                    from utils.slack import slack_alarm

                    slack_alarm(
                        message=f"✅ 스케줄러 프로젝트 `{project.project_name}` 가 완료되었습니다. ✅",
                        tag_user=project.user,
                    )

        print("-" * 80)
