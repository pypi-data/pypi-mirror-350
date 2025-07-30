import datetime
import threading
import time
from typing import Any

from langgraph.types import Command

from agentic_kit_core.base.job import Job, JobStatusEnum
from agentic_kit_core.base.schema import Breakpoint
from agentic_kit_eda.infrastructure.queue.redis_hash import RedisHash
from agentic_kit_eda.infrastructure.queue.schema import RedisQueueConfig
from .breakpoint_manager import BreakpointManager
from .job_queue import JobQueue, JobQueueInMemory


# TODO:
# 1. 是否需要优化清理线程，在fastapi onstartup启动清理线程


class Scheduler:

    breakpoint_manager: BreakpointManager
    '''breakpoint_id->thread_id管理'''

    job_queue: JobQueue
    '''任务队列'''

    cleaner_thread: threading.Thread
    CLEANER_THREAD_INTERNAL: int = 30
    '''清理线程运行间隔'''

    terminated_job_queue: RedisHash
    '''terminated job持久化'''

    # 创建可重入锁对象，可重入锁，允许同一个线程多次获取锁
    rlock = threading.RLock()

    @classmethod
    def create(cls):
        manager = cls()
        return manager

    def __init__(self, job_queue: JobQueue = None, terminated_job_queue_config: RedisQueueConfig = None, breakpoint_config: RedisQueueConfig = None):
        if breakpoint_config is None:
            breakpoint_config = terminated_job_queue_config = RedisQueueConfig(host='localhost', port=6379, db=0)
        self.breakpoint_manager = BreakpointManager(config=breakpoint_config)

        if job_queue is None:
            # note: 默认基于内存的job queue
            self.job_queue = JobQueueInMemory()

        if terminated_job_queue_config is None:
            terminated_job_queue_config = RedisQueueConfig(host='localhost', port=6379, db=0)
        self.terminated_job_queue = RedisHash(key_prefix='terminated_job_queue:', config=terminated_job_queue_config, is_json=True)

        # note: 开启job清理线程
        self.cleaner_thread = threading.Thread(target=self.__clean_terminated_jobs)
        self.cleaner_thread.start()

    def __clean_terminated_jobs(self):
        while True:
            time.sleep(self.CLEANER_THREAD_INTERNAL)
            with self.rlock:
                breakpoint_ids = []
                terminated_thread_ids = []
                running_jobs = self.job_queue.get_by_status(status=JobStatusEnum.RUNNING)
                # note: 遍历running jobs，如果已经执行结束，则terminate
                for running_job in running_jobs:
                    _state = running_job.runnable.get_state(running_job.thread_config)
                    if _state.next is None or len(_state.next) == 0 or _state.next == '':
                        terminated_thread_ids.append(running_job.thread_id)

                        breakpoints = _state.values.get('breakpoints', None)
                        if breakpoints:
                            for bk in breakpoints.values():
                                breakpoint_ids.append(bk.id)
                # 转移到terminate
                for terminated_thread_id in terminated_thread_ids:
                    self.job_queue.terminate(terminated_thread_id)

                # 清理breakpoint
                for breakpoint_id in breakpoint_ids:
                    self.breakpoint_manager.pop(breakpoint_id=breakpoint_id)

                # print('__clean_terminated_jobs')
                terminated_thread_ids = []
                jobs = self.job_queue.get_by_status(status=JobStatusEnum.TERMINATED)
                if jobs: # note: 持久化，放入redis
                    for job in jobs:
                        terminated_thread_ids.append(job.thread_id)
                        self.terminated_job_queue.add(job.thread_id, job.dump(dump_only=False, dump_runnable=False))

                for terminated_thread_id in terminated_thread_ids:
                    self.job_queue.pop_by_status_and_thread_id(thread_id=terminated_thread_id, status=JobStatusEnum.TERMINATED)

    def enqueue(self, thread_id: str, job: Job, auto_start=True, **kwargs):
        """将job加入到queue中, job必须是ready状态"""
        with self.rlock:
            self.job_queue.enqueue(thread_id=thread_id, job=job)

            # 自动执行
            if auto_start and job.init_state:
                self.start(thread_id=thread_id)
                if job.is_stream:
                    return job.runnable.astream(job.init_state, job.thread_config, stream_mode=job.stream_mode, **kwargs)
                else:
                    return job.runnable.invoke(job.init_state, job.thread_config, stream_mode=job.stream_mode, **kwargs)

            return job

    def start(self, thread_id: str):
        """当job开始运行，或者被event唤醒时，调用start将job加入running队列"""
        with self.rlock:
            self.job_queue.start(thread_id=thread_id)

    def suspend(self, thread_id: str, breakpoint_id: str, task: Any = None):
        """挂起job，等待event事件resume"""
        # note: 如果有断点信息，写入context
        with self.rlock:
            job = self.job_queue.suspend(thread_id=thread_id)

            # resume时需要
            self.breakpoint_manager.push(breakpoint_id=breakpoint_id, thread_id=thread_id)

            # todo: subgraph参数是否需要True？获得所有subgraph的状态？
            _state = job.runnable.get_state(job.thread_config)
            _breakpoints = _state.values.get('breakpoints', None)
            if _breakpoints is None:
                _breakpoints = {}
            _breakpoint = Breakpoint.create(status=0, task=task, id=breakpoint_id, thread_id=thread_id)
            _breakpoints[breakpoint_id] = _breakpoint

            job.runnable.update_state(job.thread_config, {'breakpoints': _breakpoints})
            # print('--------suspend 1')
            # print(job.runnable.get_state(job.thread_config))
            # print('--------suspend 2')
        return job, _breakpoint

    def resume(self, data: dict, breakpoint_id: str = None, auto_start: bool = False):
        """event事件唤醒job"""
        if breakpoint_id is None and 'breakpoint_id' in data:
            breakpoint_id = data['breakpoint_id']
        if breakpoint_id is None and 'tool_call_id' in data:
            breakpoint_id = data['tool_call_id']
        if not breakpoint_id:
            raise Exception('data [%s] does not contain breakpoint_id' % data)

        thread_id = self.breakpoint_manager.get(breakpoint_id=breakpoint_id)
        if not thread_id:
            raise Exception('data [%s] does not contain thread_id' % data)

        with self.rlock:
            job = self.job_queue.resume(thread_id=thread_id)
            if not job:
                raise Exception('job not in queue: %s' % thread_id)

            _state = job.runnable.get_state(job.thread_config)
            _breakpoints = _state.values.get('breakpoints', None)
            if _breakpoints is None:
                raise Exception('job [%s] does not contain breakpoints' % thread_id)

            _breakpoint = _breakpoints.get(breakpoint_id, None)
            if _breakpoint is None:
                raise Exception(f'job [{thread_id}] does not contain breakpoint [{breakpoint_id}]')

            _breakpoint.status = 1
            _breakpoint.result = data
            _breakpoint.end_time = datetime.datetime.now().timestamp()

            # 更新graph的state
            job.runnable.update_state(job.thread_config, {'breakpoints': _breakpoints})

        # 恢复执行
        if auto_start:
            print(f'恢复执行[{thread_id}] with data: [{data}]')
            if job.is_stream:
                return job.runnable.astream(
                    Command(resume=data),
                    job.thread_config,
                    stream_mode=job.stream_mode
                )
            else:
                return job.runnable.invoke(Command(resume=data), job.thread_config, stream_mode=job.stream_mode)
        else:
            return job

    def terminate(self, thread_id: str):
        """正常运行结束或停止job，终止态"""
        with self.rlock:
            self.job_queue.terminate(thread_id=thread_id)
