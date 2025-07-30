import inspect
import logging
import os
import time
from collections.abc import Callable
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from typing import Literal, Optional, get_origin

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.server import Context
from mcp.server.fastmcp.tools.base import Tool
from mcp.server.fastmcp.utilities.func_metadata import _get_typed_signature

from .executor import executor_dict
from .storage import storage_dict
from .utils import get_metadata

logger = logging.getLogger(__name__)


def parse_uri(uri):
    scheme = urlparse(uri).scheme
    if scheme == "":
        key = uri
        scheme = "local"
    else:
        key = uri[len(scheme)+3:]
    return scheme, key


def init_storage(storage_config: Optional[dict] = None):
    if storage_config is None:
        storage_config = {"type": "local"}
    storage_config = storage_config.copy()
    storage_type = storage_config.pop("type")
    storage = storage_dict[storage_type](**storage_config)
    return storage_type, storage


def init_executor(executor_config: Optional[dict] = None):
    if executor_config is None:
        executor_config = {"type": "local"}
    executor_config = executor_config.copy()
    executor_type = executor_config.pop("type")
    return executor_dict[executor_type](**executor_config)


@contextmanager
def set_directory(workdir: str):
    cwd = os.getcwd()
    os.makedirs(workdir, exist_ok=True)
    try:
        os.chdir(workdir)
        yield
    finally:
        os.chdir(cwd)


def query_job_status(job_id: str, executor: Optional[dict] = None
                     ) -> Literal["Running", "Succeeded", "Failed"]:
    """
    Query status of a calculation job
    Args:
        job_id (str): The ID of the calculation job
    Returns:
        status (str): One of "Running", "Succeeded" or "Failed"
    """
    trace_id, exec_id = job_id.split("/")
    with set_directory(trace_id):
        executor = init_executor(executor)
        status = executor.query_status(exec_id)
        logger.info("Job %s status is %s" % (job_id, status))
    return status


def terminate_job(job_id: str, executor: Optional[dict] = None):
    """
    Terminate a calculation job
    Args:
        job_id (str): The ID of the calculation job
    """
    trace_id, exec_id = job_id.split("/")
    with set_directory(trace_id):
        executor = init_executor(executor)
        executor.terminate(exec_id)
        logger.info("Job %s is terminated" % job_id)


def get_job_results(job_id: str, executor: Optional[dict] = None,
                    storage: Optional[dict] = None) -> dict:
    """
    Get results of a calculation job
    Args:
        job_id (str): The ID of the calculation job
    Returns:
        results (dict): results of the calculation job
    """
    trace_id, exec_id = job_id.split("/")
    with set_directory(trace_id):
        storage_type, storage = init_storage(storage)
        executor = init_executor(executor)
        results = executor.get_results(exec_id)
        if isinstance(results, dict):
            for name in results:
                if isinstance(results[name], Path):
                    key = storage.upload("%s/outputs/%s" % (exec_id, name),
                                         results[name])
                    uri = storage_type + "://" + key
                    logger.info("Artifact %s uploaded to %s" % (
                        results[name], uri))
                    results[name] = uri
        logger.info("Job %s results is %s" % (job_id, results))
    return results


class CalculationMCPServer:
    def __init__(self, *args, preprocess_func=None, **kwargs):
        self.preprocess_func = preprocess_func
        self.mcp = FastMCP(*args, **kwargs)

    def add_patched_tool(self, fn, new_fn, name, is_async=False):
        # patch the metadata of the tool
        context_kwarg = None
        sig = inspect.signature(fn)
        for param_name, param in sig.parameters.items():
            if get_origin(param.annotation) is not None:
                continue
            if issubclass(param.annotation, Context):
                context_kwarg = param_name
                break
        # combine parameters
        parameters = []
        for param in _get_typed_signature(fn).parameters.values():
            if param.annotation is Path:
                parameters.append(inspect.Parameter(
                    name=param.name, default=param.default,
                    annotation=str, kind=param.kind))
            elif param.annotation is Optional[Path]:
                parameters.append(inspect.Parameter(
                    name=param.name, default=param.default,
                    annotation=Optional[str], kind=param.kind))
            else:
                parameters.append(param)
        for param in _get_typed_signature(new_fn).parameters.values():
            if param.name != "kwargs":
                parameters.append(param)
        func_arg_metadata = get_metadata(
            name,
            parameters=parameters,
            skip_names=[context_kwarg] if context_kwarg is not None else [],
            globalns=getattr(fn, "__globals__", {})
        )
        json_schema = func_arg_metadata.arg_model.model_json_schema()
        tool = Tool(
            fn=new_fn,
            name=name,
            description=fn.__doc__,
            parameters=json_schema,
            fn_metadata=func_arg_metadata,
            is_async=is_async,
            context_kwarg=context_kwarg,
            annotations=None,
        )
        self.mcp._tool_manager._tools[name] = tool

    def tool(self, preprocess_func=None):
        if preprocess_func is None:
            preprocess_func = self.preprocess_func

        def decorator(fn: Callable) -> Callable:
            def submit_job(executor: Optional[dict] = None,
                           storage: Optional[dict] = None, **kwargs):
                trace_id = datetime.today().strftime('%Y-%m-%d-%H:%M:%S.%f')
                logger.info("Job processing (Trace ID: %s)" % trace_id)
                with set_directory(trace_id):
                    if preprocess_func is not None:
                        executor, storage, kwargs = preprocess_func(
                            executor, storage, kwargs)
                    storage_type, storage = init_storage(storage)
                    sig = inspect.signature(fn)
                    for name, param in sig.parameters.items():
                        if param.annotation is Path or (
                            param.annotation is Optional[Path] and
                                kwargs.get(name) is not None):
                            uri = kwargs[name]
                            scheme, key = parse_uri(uri)
                            if scheme == storage_type:
                                s = storage
                            else:
                                s = storage_dict[scheme]()
                            path = s.download(key, "inputs/%s" % name)
                            logger.info("Artifact %s downloaded to %s" % (
                                uri, path))
                            kwargs[name] = Path(path)
                    executor = init_executor(executor)
                    res = executor.submit(fn, kwargs)
                    exec_id = res["job_id"]
                    job_id = "%s/%s" % (trace_id, exec_id)
                    logger.info("Job submitted (ID: %s)" % job_id)
                return {**res, "job_id": job_id}

            async def run_job(executor: Optional[dict] = None,
                              storage: Optional[dict] = None, **kwargs):
                context = self.mcp.get_context()
                res = submit_job(executor=executor, storage=storage, **kwargs)
                job_id = res["job_id"]
                await context.log(level="info", message="Job submitted "
                                  "(ID: %s)" % job_id)
                if res.get("extra_info"):
                    await context.log(level="info", message=res["extra_info"])
                while True:
                    status = query_job_status(job_id, executor=executor)
                    await context.log(level="info", message="Job status: %s"
                                      % status)
                    if status != "Running":
                        break
                    time.sleep(4)
                if status == "Succeeded":
                    await context.log(level="info", message="Job succeeded.")
                    return get_job_results(
                        job_id, executor=executor, storage=storage)
                elif status == "Failed":
                    await context.log(level="info", message="Job failed.")
                    raise RuntimeError("Job failed")

            self.add_patched_tool(fn, run_job, fn.__name__, is_async=True)
            # self.add_patched_tool(fn, submit_job, "submit_" + fn.__name__)
            # self.mcp.add_tool(query_job_status)
            # self.mcp.add_tool(terminate_job)
            # self.mcp.add_tool(get_job_results)
            return fn
        return decorator

    def run(self, **kwargs):
        if os.environ.get("DP_AGENT_RUNNING_MODE") in ["1", "true"]:
            return
        self.mcp.run(**kwargs)
