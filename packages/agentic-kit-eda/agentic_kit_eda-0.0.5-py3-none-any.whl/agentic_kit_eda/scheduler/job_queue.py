import datetime
import threading
from abc import ABC, abstractmethod

from agentic_kit_core.base.job import Job, JobStatusEnum


class JobQueue(ABC):
    """
    job队列
    调度流转：
    READY -> RUNNING -> SUSPENDED -> RUNNING
                     -> TERMINATED
    """

    @abstractmethod
    def enqueue(self, thread_id: str, job: Job):
        raise NotImplemented

    @abstractmethod
    def start(self, thread_id: str):
        raise NotImplemented

    @abstractmethod
    def suspend(self, thread_id: str):
        raise NotImplemented

    @abstractmethod
    def resume(self, thread_id: str):
        raise NotImplemented

    @abstractmethod
    def terminate(self, thread_id: str):
        raise NotImplemented

    @abstractmethod
    def get(self, thread_id: str):
        raise NotImplemented

    @abstractmethod
    def get_by_status(self, status: str):
        raise NotImplemented

    @abstractmethod
    def pop_by_status_and_thread_id(self, thread_id: str, status: str):
        raise NotImplemented


class JobQueueInMemory(JobQueue):
    """
    job队列，基于内存
    调度流转：
    READY -> RUNNING -> SUSPENDED -> RUNNING
                     -> TERMINATED
    """

    __ready_queue: dict[str, Job] = {}

    __running_queue: dict[str, Job] = {}

    __suspended_queue: dict[str, Job] = {}

    __terminated_queue: dict[str, Job] = {}
    # todo: 终止态的，持久化以后就丢弃

    # 创建可重入锁对象，可重入锁，允许同一个线程多次获取锁
    rlock = threading.RLock()

    def __init__(self):
        pass

    def get(self, thread_id: str):
        if thread_id in self.__ready_queue:
            return self.__ready_queue.get(thread_id, None)
        elif thread_id in self.__running_queue:
            return self.__running_queue.get(thread_id, None)
        elif thread_id in self.__suspended_queue:
            return self.__suspended_queue.get(thread_id, None)
        elif thread_id in self.__terminated_queue:
            return self.__terminated_queue.get(thread_id, None)
        else:
            return None

    def get_by_status(self, status: str):
        if status == JobStatusEnum.READY:
            return self.__ready_queue.values()
        elif status == JobStatusEnum.RUNNING:
            return self.__running_queue.values()
        elif status == JobStatusEnum.SUSPENDED:
            return self.__suspended_queue.values()
        elif status == JobStatusEnum.TERMINATED:
            return self.__terminated_queue.values()
        else:
            return None

    def pop_by_status_and_thread_id(self, thread_id: str, status: str):
        if status == JobStatusEnum.READY:
            return self.__ready_queue.pop(thread_id)
        elif status == JobStatusEnum.RUNNING:
            return self.__running_queue.pop(thread_id)
        elif status == JobStatusEnum.SUSPENDED:
            return self.__suspended_queue.pop(thread_id)
        elif status == JobStatusEnum.TERMINATED:
            return self.__terminated_queue.pop(thread_id)
        else:
            return None

    def __check_job_terminated(self, thread_id: str):
        job = self.__terminated_queue.get(thread_id, None)
        if job:
            raise Exception(f'{thread_id}: 终止态，不可继续操作')

    def enqueue(self, thread_id: str, job: Job):
        """将job加入到queue中, job必须是ready状态"""
        with self.rlock:
            self.__check_job_terminated(thread_id)

            if job.status != JobStatusEnum.READY:
                raise RuntimeError(f'{thread_id}：只能将ready状态到job加入到队列中')
            if thread_id in self.__ready_queue \
                or thread_id in self.__running_queue \
                or thread_id in self.__suspended_queue \
                or thread_id in self.__terminated_queue:
                raise RuntimeError(f'{thread_id}: 不可重复调度enqueue')

            self.__ready_queue[thread_id] = job

    def start(self, thread_id: str):
        """当job开始运行，或者被event唤醒时，调用start将job加入running队列"""
        with self.rlock:
            self.__check_job_terminated(thread_id)

            # 如果是ready状态
            ready_job = self.__ready_queue.get(thread_id, None)
            if ready_job:
                ready_job.status = JobStatusEnum.RUNNING
                self.__ready_queue.pop(thread_id)
                self.__running_queue[thread_id] = ready_job
                return ready_job

            # 如果是suspended状态
            suspended_job = self.__suspended_queue.get(thread_id, None)
            if suspended_job:
                suspended_job.status = JobStatusEnum.RUNNING
                self.__suspended_queue.pop(thread_id)
                self.__running_queue[thread_id] = suspended_job
                return suspended_job

    def suspend(self, thread_id: str):
        """挂起job，等待event事件resume"""
        with self.rlock:
            self.__check_job_terminated(thread_id)

            running_job = self.__running_queue.get(thread_id, None)
            if not running_job:
                raise RuntimeError(f'{thread_id}：未处在running队列中')

            running_job.status = JobStatusEnum.SUSPENDED
            self.__running_queue.pop(thread_id)
            self.__suspended_queue[thread_id] = running_job
            return running_job

    def resume(self, thread_id: str):
        """event事件唤醒job"""
        with self.rlock:
            self.__check_job_terminated(thread_id)

            suspended_job = self.__suspended_queue.get(thread_id, None)
            if not suspended_job:
                raise RuntimeError(f'{thread_id}：未处在suspended队列中')

            suspended_job.status = JobStatusEnum.RUNNING
            self.__suspended_queue.pop(thread_id)
            self.__running_queue[thread_id] = suspended_job
            return suspended_job

    def terminate(self, thread_id: str):
        """正常运行结束或停止job，终止态"""

        def __set_job_terminated(_job: Job):
            _job.status = JobStatusEnum.TERMINATED
            _job.end_time = datetime.datetime.now()
            self.__terminated_queue[thread_id] = _job

        with self.rlock:
            self.__check_job_terminated(thread_id)

            ready_job = self.__ready_queue.get(thread_id, None)
            if ready_job:
                self.__ready_queue.pop(thread_id)
                __set_job_terminated(ready_job)

            running_job = self.__running_queue.get(thread_id, None)
            if running_job:
                self.__running_queue.pop(thread_id)
                __set_job_terminated(running_job)

            suspended_job = self.__suspended_queue.get(thread_id, None)
            if suspended_job:
                self.__suspended_queue.pop(thread_id)
                __set_job_terminated(suspended_job)

    def dump(self, dump_only=True):
        print('---ready---')
        print(self.__ready_queue)
        print('---running---')
        print(self.__running_queue)
        print('---suspended---')
        print(self.__suspended_queue)
        print('---terminated---')
        print(self.__terminated_queue)

        if not dump_only:
            return {
                'ready': [item.dump() for item in self.__ready_queue.values()],
                'running': [item.dump() for item in self.__running_queue.values()],
                'suspended': [item.dump() for item in self.__suspended_queue.values()],
                'terminated': [item.dump() for item in self.__terminated_queue.values()],
            }
