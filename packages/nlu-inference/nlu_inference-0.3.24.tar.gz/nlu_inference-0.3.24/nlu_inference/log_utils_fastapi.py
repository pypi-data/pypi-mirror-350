# -*- coding: utf-8 -*-
import os
import sys
import json
import inspect
import logging
from datetime import datetime
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from contextvars import ContextVar


# 初始化 ContextVar
request_context: ContextVar[dict] = ContextVar("request_context", default={})


# 自定义中间件
class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 设置请求上下文
        token = request_context.set({
            "headers": dict(request.headers),
            "path": request.url.path,
            "method": request.method
        })
        try:
            # 调用后续处理
            response = await call_next(request)
        finally:
            # 请求结束后重置 ContextVar
            request_context.reset(token)
        return response
    


class FastApiMDCLogger:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def _log(self, level: int, msg: str):
        # 获取调用位置信息
        frame = inspect.currentframe()
        # 向上查找直到找到非日志相关的调用帧
        file_path = 'unknown'
        line_no = 0
        while frame:
            if frame.f_code.co_filename != __file__:
                file_path = frame.f_code.co_filename
                line_no = frame.f_lineno
                break
            frame = frame.f_back
        if file_path != 'unknown':
            file_path = os.path.basename(file_path)
        # 格式化时间
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        # 获取pid
        pid = os.getpid()
        # 从flask请求中解析MDC数据
        ending_id = "sys#0"
        session_id = ""
        utt_id = ""
        log_mark = "LOGIC"
        headers = request_context.get().get("headers", {})
        if headers.get('mdc-passing') is not None:
            mdc_header = headers.get('mdc-passing')
            if mdc_header is not None:
                try:
                    mdc_values = json.mdc_header()
                    ending_id = mdc_values.get("endingId", "sys#0"),
                    session_id = mdc_values.get("sessionId", ""),
                    utt_id = mdc_values.get("uttId", ""),
                    log_mark = mdc_values.get("logMark", "LOGIC")
                except:
                    pass
        # 构建日志消息
        log_msg = (
            f"[{current_time}]"
            f"[{file_path}]"
            f"[{line_no}]"
            f"[pid{pid}]"
            f"[{logging.getLevelName(level)}]"
            f"[{ending_id}]"
            f"[{session_id}]"
            f"[{utt_id}]"
            f"[{log_mark}] - "
            f"{msg}"
        )
        self.logger.log(level, log_msg)

    def debug(self, msg: str):
        self._log(logging.DEBUG, msg)

    def info(self, msg: str):
        self._log(logging.INFO, msg)

    def warning(self, msg: str):
        self._log(logging.WARNING, msg)

    def error(self, msg: str):
        self._log(logging.ERROR, msg)

    def critical(self, msg: str):
        self._log(logging.CRITICAL, msg)


def setup_logging(name):
    """配置基础日志"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(message)s',
        stream=sys.stdout
    )
    return FastApiMDCLogger(logging.getLogger(name))


def get_logger():
    return setup_logging("model")


##### 使用说明 #####
# 
# 要支持传递MDC值，需要在FastAPI应用中添加中间件
#
# app.add_middleware(RequestContextMiddleware)
#
# 要在开展异步任务的时候传递MDC信息，需要手动传递contextVars
# 
# 首先增加依赖
# from contextvars import copy_context
# 
# 然后在代码中调用
#    context = copy_context()
#    await asyncio.create_task(context.run(async_task))
#