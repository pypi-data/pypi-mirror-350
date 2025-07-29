from .definition import JobStatus

class Job(object):
    def __init__(self, project_name, job_name, user, config_path, id=0, executed_filename="train.py"):
        
        self.status = JobStatus.PENDING
        self.project_name = project_name
        self.job_name = job_name
        self.config_path = config_path # config/runs/xxx.json
        self.user = user
        self.job_id = id        
        
        self.worker = None
        self.session_name = ""
        
        self.executed_filename = executed_filename
            
    def stop(self):
        self.worker.ssh.ssh_exec_command(
            f"tmux kill-session -t {self.session_name} && echo 'stopped' > {self.worker.home}/{self.project_name}/{self.job_name}.status"
        )
        
        self.status = JobStatus.STOPPED
        
    
