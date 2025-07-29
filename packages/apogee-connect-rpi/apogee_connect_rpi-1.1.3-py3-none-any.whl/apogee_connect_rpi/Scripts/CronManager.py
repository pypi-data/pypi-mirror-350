from crontab import CronTab
import os
import subprocess
from apogee_connect_rpi.Scripts.AppConfig import AppConfig

class CronManager:
    def __init__(self):
        self.cron = CronTab(user=True)

    async def setup_crontab_command_if_needed(self):
        # Make sure we don't create duplicate commands
        if self.check_for_existing_job():
            return

        collection_frequency = AppConfig().get_collection_frequency()
        command = self.get_cron_job_command()
        job = self.cron.new(command=command)
        job.minute.every(collection_frequency)
        self.cron.write()

    def get_cron_job_command(self):
        home_dir = os.path.expanduser("~")
        log_dir = os.path.join(home_dir, "Apogee", "apogee_connect_rpi", "logs")
        os.makedirs(log_dir, exist_ok=True)

        executable_path = self.get_executable("apogee", home_dir)

        command = f"{executable_path} run-data-collection >> {log_dir}/ac_rpi_log.log 2>&1"
        return command

    def remove_crontab_job(self):
        print("Removing scheduled data collection task")
        job = self.check_for_existing_job()
        if job:
            self.cron.remove(job)
            self.cron.write()

    def check_for_existing_job(self):
        for job in self.cron:
            if f"apogee run-data-collection" in job.command:
                return job
        return None
    
    def get_executable(self, command_name, home_dir) -> str:
        # Most likely location
        executable_path = f"{home_dir}/.local/bin/apogee"

        if not os.path.isfile(executable_path):
            # Second most likely location
            executable_path = f"{home_dir}/.local/pipx/bin/apogee"

        if not os.path.isfile(executable_path):
            # Try to check for the location programmatically
            result = subprocess.run(['which', command_name], capture_output=True, text=True)
            if result.returncode == 0:
                executable_path = result.stdout.strip()
            else:
                raise RuntimeError(f"Could not find executable location. Please make sure 'apogee' executable is located at: {home_dir}/.local/bin/apogee or is part of $PATH") 

        return executable_path

    def update_cron_interval(self, interval):
        job = self.check_for_existing_job()
        if job:
            print("Updating scheduled collection interval")
            job.minute.every(interval)
            self.cron.write()