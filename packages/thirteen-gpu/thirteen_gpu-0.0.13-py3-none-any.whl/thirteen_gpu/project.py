from glob import glob
import json
import os

from .definition import ProjectStatus
from .job import Job


class Project(object):
    def __init__(self, project_path, user, submit_at, executed_filename):
        self.status = ProjectStatus.LIVE

        self.path = project_path
        self.project_name = os.path.basename(project_path)
        self.user = user

        # assign current time
        self.submit_at = submit_at
        
        self.executed_filename = executed_filename

        # job 목록 초기화
        self.jobs = {}

        for config_path in sorted(glob(f"{self.path}/config/runs/*.json")):
            config_idx = config_path.split("/")[-1].split(".json")[0]

            job_name = f"job_{self.project_name}_{config_idx}"

            self.jobs[job_name] = Job(
                self.project_name, job_name, self.user, "/".join(config_path.split("/")[-3:]), id=config_idx, executed_filename=self.executed_filename
            )

    def delete(self):
        print(f"Delete project {self.project_name}...")

        if os.path.exists(self.path):
            os.system(f"rm -rf {self.path}")

        self.status = ProjectStatus.DEAD
