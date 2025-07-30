from celery import shared_task
from langchain_community.utilities.requests import JsonRequestsWrapper

from agentic_kit_eda.infrastructure.event_driven.pub_sub.redis_publish import tool_call_publish_wrapper
from agentic_kit_eda.infrastructure.event_driven.pub_sub.redis_pubsub_manager import tool_call_publisher


@shared_task(name='celery_app.build_in.http_get_async')
@tool_call_publish_wrapper(publisher=tool_call_publisher)
def http_get_async(
    url: str,
    params: dict,
    tool_call_id: str
):
    print('=====celery_app.build_in.http_get_async=======')
    print(f'http_get_async: {url} : {params}')
    http_requests_wrapper = JsonRequestsWrapper()
    data = http_requests_wrapper.get(url, **{'params': params})
    return {
        'type': 'tool',
        'artifact': data,
        'content': data,
        'status': 'success',
        'tool_call_id': tool_call_id,
    }


@shared_task(name='celery_app.build_in.http_post_async')
@tool_call_publish_wrapper(publisher=tool_call_publisher)
def http_post_async(
        url: str,
        params: dict,
        tool_call_id: str
):
    print('=====celery_app.build_in.http_post_async=======')
    print(f'http_post_async: {url} : {params}')
    http_requests_wrapper = JsonRequestsWrapper()
    data = http_requests_wrapper.post(url, data=params)
    return {
        'type': 'tool',
        'artifact': data,
        'content': data,
        'status': 'success',
        'tool_call_id': tool_call_id,
    }


@shared_task(name='celery_app.build_in.http_patch_async')
@tool_call_publish_wrapper(publisher=tool_call_publisher)
def http_patch_async(
        url: str,
        params: dict,
        tool_call_id: str
):
    print('=====celery_app.build_in.http_patch_async=======')
    print(f'http_patch_async: {url} : {params}')
    http_requests_wrapper = JsonRequestsWrapper()
    data = http_requests_wrapper.patch(url, data=params)
    return {
        'type': 'tool',
        'artifact': data,
        'content': data,
        'status': 'success',
        'tool_call_id': tool_call_id,
    }


@shared_task(name='celery_app.build_in.http_put_async')
@tool_call_publish_wrapper(publisher=tool_call_publisher)
def http_put_async(
        url: str,
        params: dict,
        tool_call_id: str
):
    print('=====celery_app.build_in.http_put_async=======')
    print(f'http_put_async: {url} : {params}')
    http_requests_wrapper = JsonRequestsWrapper()
    data = http_requests_wrapper.put(url, data=params)
    return {
        'type': 'tool',
        'artifact': data,
        'content': data,
        'status': 'success',
        'tool_call_id': tool_call_id,
    }


@shared_task(name='celery_app.build_in.http_delete_async')
@tool_call_publish_wrapper(publisher=tool_call_publisher)
def http_delete_async(
    url: str,
    params: dict,
    tool_call_id: str
):
    print('=====celery_app.build_in.http_delete_async=======')
    print(f'http_delete_async: {url} : {params}')
    http_requests_wrapper = JsonRequestsWrapper()
    data = http_requests_wrapper.delete(url, **{'params': params})
    return {
        'type': 'tool',
        'artifact': data,
        'content': data,
        'status': 'success',
        'tool_call_id': tool_call_id,
    }
