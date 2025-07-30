from agentic_kit_eda.infrastructure.queue.redis_hash import RedisHash
from agentic_kit_eda.infrastructure.queue.schema import RedisQueueConfig


class BreakpointManager:
    """
    管理breakpoint与graph.thread_id的关系，在恢复graph时需要
    graph执行toolcall时，tool_call_id作为breakpoint.id
    """
    breakpoints: RedisHash

    def __init__(self, config: RedisQueueConfig):
        self.breakpoints = RedisHash(key_prefix='breakpoint_manager:', config=config, is_json=False)

    def push(self, breakpoint_id: str, thread_id: str):
        """保存breakpoint_id映射thread_id"""
        _thread_id = self.breakpoints.get(breakpoint_id)
        if _thread_id is None:
            return self.breakpoints.add(breakpoint_id, thread_id)

    def pop(self, breakpoint_id: str):
        return self.breakpoints.delete(breakpoint_id)

    def get(self, breakpoint_id: str):
        """通过breakpoint_id获取thread_id"""
        return self.breakpoints.get(breakpoint_id)
