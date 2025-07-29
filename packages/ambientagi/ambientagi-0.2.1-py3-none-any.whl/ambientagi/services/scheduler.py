import logging

from apscheduler.jobstores.base import JobLookupError  # type: ignore
from apscheduler.schedulers.background import BackgroundScheduler  # type: ignore


class AgentScheduler:
    def __init__(self):
        """
        Initialize the AgentScheduler with a background scheduler.
        """
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def add_job(self, job_id: str, func, trigger: str = "interval", **kwargs):
        """
        Add a job to the scheduler.

        :param job_id: A unique ID for the job.
        :param func: The function to schedule.
        :param trigger: The type of trigger ("interval", "cron", etc.).
        :param kwargs: Additional arguments for the trigger.
        """
        try:
            self.scheduler.add_job(
                func, trigger, id=job_id, replace_existing=True, **kwargs
            )
            self.logger.info(f"Job {job_id} added to the scheduler.")
        except Exception as e:
            self.logger.error(f"Failed to add job {job_id}: {e}")

    def remove_job(self, job_id: str):
        """
        Remove a job from the scheduler.

        :param job_id: The ID of the job to remove.
        """
        try:
            self.scheduler.remove_job(job_id)
            self.logger.info(f"Job {job_id} removed from the scheduler.")
        except JobLookupError:
            self.logger.error(f"Job {job_id} not found.")

    def shutdown(self):
        """
        Shutdown the scheduler.
        """
        self.scheduler.shutdown()
        self.logger.info("Scheduler shutdown successfully.")
