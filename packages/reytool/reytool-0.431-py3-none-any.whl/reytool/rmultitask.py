# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-19 20:06:20
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Multi task methods.
"""


from __future__ import annotations
from typing import Any, List, Tuple, Dict, Optional, Literal, Iterable, Callable, Generator, Coroutine, Union, Type
from threading import RLock as TRLock, get_ident as threading_get_ident
from concurrent.futures import ThreadPoolExecutor, Future as CFuture, as_completed as concurrent_as_completed
from asyncio import (
    Future as AFuture,
    Queue as AQueue,
    Lock as ALock,
    run as asyncio_run,
    gather as asyncio_gather,
    iscoroutine
)
from asyncio.queues import QueueEmpty
from aiohttp import ClientSession, ClientResponse

from .rexception import throw, check_most_one, check_response_code
from .rtime import sleep, RTimeMark
from .rwrap import wrap_thread


__all__ = (
    "async_run",
    "async_request",
    "RThreadLock",
    "RAsyncLock",
    "RThreadPool",
    "RAsyncPool"
)


def async_run(*coroutines: Coroutine) -> List:
    """
    Asynchronous run `Coroutine` instances.

    Parameters
    ----------
    coroutines : `Coroutine` instances.

    Returns
    -------
    Run result list.
    """


    # Define.
    async def gather_coroutine() -> AFuture:
        """
        Get `Future` instance.

        Returns
        -------
        Future instance.
        """

        # Gather.
        future = await asyncio_gather(*coroutines)

        return future


    # Run.
    result = asyncio_run(gather_coroutine())

    return result


async def async_request(
    url: str,
    params: Optional[Dict] = None,
    data: Optional[Union[Dict, str, bytes]] = None,
    json: Optional[Dict] = None,
    headers: Dict[str, str] = {},
    timeout: Optional[float] = None,
    proxy: Optional[str] = None,
    method: Optional[Literal["get", "post", "put", "patch", "delete", "options", "head"]] = None,
    check: Union[bool, int, Iterable[int]] = False,
    handler: Optional[Union[str, Tuple[str], Callable[[ClientResponse], Union[Coroutine, Any]]]] = None
) -> Any:
    """
    Get asynchronous `Coroutine` instance of send request.

    Parameters
    ----------
    url : Request URL.
    params : Request URL add parameters.
    data : Request body data. Conflict with parameter `json`.
        - `Dict` : Convert to `key=value&...` format bytes.
            Automatic set `Content-Type` to `application/x-www-form-urlencoded`.
        - `Dict and a certain value is 'bytes' type` : Key is parameter name and file name, value is file data.
            Automatic set `Content-Type` to `multipart/form-data`.
        - `str` : File path to read file bytes data.
            Automatic set `Content-Type` to file media type, and `filename` to file name.
        - `bytes` : File bytes data.
            Automatic set `Content-Type` to file media type.

    json : Request body data, convert to `JSON` format. Conflict with parameter `data`.
        Automatic set `Content-Type` to `application/json`.

    headers : Request header data.
    timeout : Request maximun waiting time.
    proxy : Proxy URL.
    method : Request method.
        - `None` : Automatic judge.
            * When parameter `data` or `json` not has value, then request method is `get`.
            * When parameter `data` or `json` has value, then request method is `post`.
        - `Literal['get', 'post', 'put', 'patch', 'delete', 'options', 'head']` : Use this request method.

    check : Check response code, and throw exception.
        - `Literal[False]`: Not check.
        - `Literal[True]`: Check if is between 200 and 299.
        - `int` : Check if is this value.
        - `Iterable` : Check if is in sequence.

    handler: Response handler.
        - `None` : Automatic handle.
            * `Response 'Content-Type' is 'application/json'` : Use `ClientResponse.json` method.
            * `Response 'Content-Type' is 'text/plain; charset=utf-8'` : Use `ClientResponse.text` method.
            * `Other` : Use `ClientResponse.read` method.
        - `str` : Get this attribute.
            * `Callable` : Execute this method. When return `Coroutine`, then use `await` syntax execute `Coroutine`.
            * `Any` : Return this value.
        - `Tuple[str]` : Get these attribute.
            * `Callable` : Execute this method. When return `Coroutine`, then use `await` syntax execute `Coroutine`.
            * `Any` : Return this value.
        - `Callable` : Execute this method. When return `Coroutine`, then use `await` syntax execute `Coroutine`.

    Returns
    -------
    Response handler result.
    """

    # Check.
    check_most_one(data, json)

    # Handle parameter.
    if method is None:
        if data is None and json is None:
            method = "get"
        else:
            method = "post"

    # Session.
    async with ClientSession() as session:

        # Request.
        async with session.request(
            method,
            url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            timeout=timeout,
            proxy=proxy
        ) as response:

            # Check code.
            if check is not False:
                if check is True:
                    range_ = None
                else:
                    range_ = check
                check_response_code(response.status, range_)

            # Receive.
                
            ## Auto.
            if handler is None:
                if response.content_type == "application/json":
                    result = await response.json()
                elif response.content_type == "text/plain; charset=utf-8":

                    # Set encode type.
                    if response.get_encoding() == "ISO-8859-1":
                        encoding = "utf-8"
                    else:
                        encoding = None

                    result = await response.text(encoding=encoding)
                else:
                    result = await response.read()

            ## Attribute.
            elif handler.__class__ == str:
                result = getattr(response, handler)

                ### Method.
                if callable(result):
                    result = result()

                    #### Coroutine.
                    if iscoroutine(result):
                        result = await result

            ## Attributes.
            elif handler.__class__ == tuple:
                result = []
                for key in handler:
                    result_element = getattr(response, key)

                    ### Method.
                    if callable(result_element):
                        result_element = result_element()

                        #### Coroutine.
                        if iscoroutine(result_element):
                            result_element = await result_element

                    result.append(result_element)

            ## Method.
            elif callable(handler):
                result = handler(response)

                ### Coroutine.
                if iscoroutine(result):
                    result = await result

            ## Throw exception.
            else:
                throw(TypeError, handler)

            return result


class RThreadLock():
    """
    Rey's `thread lock` type.
    """


    def __init__(self) -> None:
        """
        Build `thread lock` instance.
        """

        # Set attribute.
        self.lock = TRLock()
        self.acquire_thread_id: Optional[int] = None


    def acquire(
        self,
        timeout: float = None
    ) -> bool:
        """
        Wait and acquire thread lock.

        Parameters
        ----------
        timeout : Maximum wait seconds.
            - `None` : Not limit.
            - `float` : Use this value.

        Returns
        -------
        Whether acquire success.
        """

        # Handle parameter.
        if timeout is None:
            timeout = -1

        # Acquire.
        result = self.lock.acquire(timeout=timeout)

        # Update attribute.
        if result:
            thread_id = threading_get_ident()
            self.acquire_thread_id = thread_id

        return result


    def release(self) -> None:
        """
        Release thread lock.
        """

        # Release.
        self.lock.release()

        # Update attribute.
        self.acquire_thread_id = None


    def __call__(self) -> None:
        """
        Automatic judge, wait and acquire thread lock, or release thread lock.
        """

        # Release.
        thread_id = threading_get_ident()
        if thread_id == self.acquire_thread_id:
            self.release()

        # Acquire.
        else:
            self.acquire()


class RAsyncLock():
    """
    Rey's `asynchronous lock` type.
    """


    def __init__(self) -> None:
        """
        Build `asynchronous lock` instance.
        """

        # Set attribute.
        self.lock = ALock()


    def acquire(
        self,
        timeout: float = None
    ) -> bool:
        """
        Wait and acquire thread lock.

        Parameters
        ----------
        timeout : Maximum wait seconds.
            - `None` : Not limit.
            - `float` : Use this value.

        Returns
        -------
        Whether acquire success.
        """

        # Handle parameter.
        if timeout is None:
            timeout = -1

        # Acquire.
        result = self.lock.acquire()

        return result


    def release(self) -> None:
        """
        Release thread lock.
        """

        # Release.
        self.lock.release()


class RThreadPool(object):
    """
    Rey's `thread pool` type.
    """


    def __init__(
        self,
        task: Callable,
        *args: Any,
        _max_workers: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        """
        Build `thread pool` instance.

        Parameters
        ----------
        task : Thread task.
        args : Task default position arguments.
        _max_workers : Maximum number of threads.
            - `None` : Number of CPU + 4, 32 maximum.
            - `int` : Use this value, no maximum limit.

        kwargs : Task default keyword arguments.
        """

        # Set attribute.
        self.task = task
        self.args = args
        self.kwargs = kwargs
        self.thread_pool = ThreadPoolExecutor(
            _max_workers,
            task.__name__
        )
        self.futures: List[CFuture] = []


    def one(
        self,
        *args: Any,
        **kwargs: Any
    ) -> CFuture:
        """
        Add and start a task to the thread pool.

        Parameters
        ----------
        args : Task position arguments, after default position arguments.
        kwargs : Task keyword arguments, after default keyword arguments.

        Returns
        -------
        Task instance.
        """

        # Set parameter.
        func_args = (
            *self.args,
            *args
        )
        func_kwargs = {
            **self.kwargs,
            **kwargs
        }

        # Submit.
        future = self.thread_pool.submit(
            self.task,
            *func_args,
            **func_kwargs
        )

        # Save.
        self.futures.append(future)

        return future


    def batch(
        self,
        *args: Tuple,
        **kwargs: Tuple
    ) -> List[CFuture]:
        """
        Add and start a batch of tasks to the thread pool.
        parameters sequence will combine one by one, and discard excess parameters.

        Parameters
        ----------
        args : Sequence of task position arguments, after default position arguments.
        kwargs : Sequence of task keyword arguments, after default keyword arguments.

        Returns
        -------
        Task instance list.

        Examples
        --------
        >>> func = lambda *args, **kwargs: print(args, kwargs)
        >>> a = (1, 2)
        >>> b = (3, 4, 5)
        >>> c = (11, 12)
        >>> d = (13, 14, 15)
        >>> thread_pool = RThreadPool(func, 0, z=0)
        >>> thread_pool.batch(a, b, c=c, d=d)
        (0, 1, 3) {'z': 0, 'c': 11, 'd': 13}
        (0, 2, 4) {'z': 0, 'c': 12, 'd': 14}
        """

        # Combine.
        args_zip = zip(*args)
        kwargs_zip = zip(
            *[
                [
                    (key, value)
                    for value in values
                ]
                for key, values in kwargs.items()
            ]
        )
        params_zip = zip(args_zip, kwargs_zip)

        # Batch submit.
        futures = [
            self.one(*args_, **dict(kwargs_))
            for args_, kwargs_ in params_zip
        ]

        # Save.
        self.futures.extend(futures)

        return futures


    def generate(
        self,
        timeout: Optional[float] = None
    ) -> Generator[CFuture]:
        """
        Return the generator of added task instance.

        Parameters
        ----------
        timeout : Call generator maximum waiting seconds, timeout throw exception.
            - `None` : Infinite.
            - `float` : Set this seconds.

        Returns
        -------
        Generator of added task instance.
        """

        # Get parameter.
        self.futures, futures = [], self.futures

        # Build.
        generator = concurrent_as_completed(
            futures,
            timeout
        )

        return generator


    def repeat(
        self,
        number: int
    ) -> List[CFuture]:
        """
        Add and start a batch of tasks to the thread pool, and only with default parameters.

        Parameters
        ----------
        number : Number of add.

        Returns
        -------
        Task instance list.
        """

        # Batch submit.
        futures = [
            self.one()
            for _ in range(number)
        ]

        # Save.
        self.futures.extend(futures)

        return futures


    def join(self) -> None:
        """
        Block until all tasks are done.
        """

        # Generator.
        generator = self.generate()

        # Wait.
        for _ in generator:
            pass


    def __iter__(self) -> Generator:
        """
        Return the generator of task result.

        Returns
        -------
        Generator of task result.
        """

        # Generator.
        generator = self.generate()

        # Generate.
        for future in generator:
            yield future.result()


    __call__ = one


    __mul__ = repeat


class RAsyncPool(object):
    """
    Rey's `asynchronous pool` type.
    """


    def __init__(
        self,
        async_func: Callable[..., Coroutine],
        *args: Any,
        _max_async: int = 10,
        _exc_handler: Optional[Callable] = None,
        **kwargs: Any
    ) -> None:
        """
        Build `asynchronous pool` instance.

        Parameters
        ----------
        async_func : Function of create asynchronous `Coroutine`.
        args : Function default position arguments.
        _max_async : Maximum number of asynchronous.
        _exc_handler : `Coroutine` execution exception handler, will return value.
        kwargs : Function default keyword arguments.
        """

        # Set attribute.
        self.async_func = async_func
        self.args = args
        self.kwargs = kwargs
        self.exc_handler = _exc_handler
        self.queue_input: AQueue[Tuple[Tuple, Dict]] = AQueue()
        self.queue_output = AQueue()
        self.queue_count = 0

        # Start.
        self._start_workers(_max_async)


    @wrap_thread
    def _start_workers(
        self,
        worker_n: int
    ) -> None:
        """
        Start workers of execute asynchronous `Coroutine`.

        Parameters
        ----------
        worker_n : Number of execute asynchronous `Coroutine` workers.
        """


        # Define.
        async def async_worker() -> None:
            """
            Worker of execute asynchronous `Coroutine`.
            """

            # Loop.
            while True:

                # Get parameter.
                args, kwargs = await self.queue_input.get()

                # Execute.
                try:
                    result = await self.async_func(*args, **kwargs)

                # Handle exception.
                except:
                    if self.exc_handler is not None:
                        result = self.exc_handler()
                        await self.queue_output.put(result)

                    ## Count.
                    else:
                        self.queue_count -= 1

                else:
                    await self.queue_output.put(result)


        # Create.
        coroutines = [
            async_worker()
            for _ in range(worker_n)
        ]

        # Start.
        async_run(*coroutines)


    def one(
        self,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """
        Add and start a task to the pool.

        Parameters
        ----------
        args : Function position arguments, after default position arguments.
        kwargs : Function keyword arguments, after default keyword arguments.
        """

        # Set parameter.
        func_args = (
            *self.args,
            *args
        )
        func_kwargs = {
            **self.kwargs,
            **kwargs
        }
        item = (
            func_args,
            func_kwargs
        )

        # Count.
        self.queue_count += 1

        # Put.
        self.queue_input.put_nowait(item)


    def batch(
        self,
        *args: Tuple,
        **kwargs: Tuple
    ) -> None:
        """
        Add and start a batch of tasks to the pool.
        parameters sequence will combine one by one, and discard excess parameters.

        Parameters
        ----------
        args : Sequence of function position arguments, after default position arguments.
        kwargs : Sequence of function keyword arguments, after default keyword arguments.

        Examples
        --------
        >>> async def func(*args, **kwargs):
        ...     print(args, kwargs)
        >>> a = (1, 2)
        >>> b = (3, 4, 5)
        >>> c = (11, 12)
        >>> d = (13, 14, 15)
        >>> async_pool = RAsyncPool(func, 0, z=0)
        >>> async_pool.batch(a, b, c=c, d=d)
        (0, 1, 3) {'z': 0, 'c': 11, 'd': 13}
        (0, 2, 4) {'z': 0, 'c': 12, 'd': 14}
        """

        # Combine.
        args_zip = zip(*args)
        kwargs_zip = zip(
            *[
                [
                    (key, value)
                    for value in values
                ]
                for key, values in kwargs.items()
            ]
        )
        params_zip = zip(args_zip, kwargs_zip)

        # Batch submit.
        for args_, kwargs_ in params_zip:
            self.one(*args_, **dict(kwargs_))


    def repeat(
        self,
        number: int
    ) -> List[CFuture]:
        """
        Add and start a batch of tasks to the pool, and only with default parameters.

        Parameters
        ----------
        number : Number of add.
        """

        # Batch submit.
        for _ in range(number):
            self.one()


    def get(
        self,
        timeout: Optional[float] = None
    ) -> Any:
        """
        Get one execution result of asynchronous `Coroutine`, will block.

        Parameters
        ----------
        timeout : Maximum seconds of block.

        Returns
        -------
        One execution result.
        """

        # Set parameter.
        if timeout is not None:
            rtm = RTimeMark()
            rtm()

        # Loop.
        while True:

            # Judge.
            if not self.queue_output.empty():

                # Get.
                try:
                    result = self.queue_output.get_nowait()
                except QueueEmpty:
                    pass
                else:

                    # Count.
                    self.queue_count -= 1

                    return result

            # Timeout.
            if timeout is not None:
                rtm()
                if rtm.total_spend > timeout:
                    throw(TimeoutError, timeout)

            # Sleep.
            sleep(0.01)


    def join(self) -> None:
        """
        Block until all asynchronous `Coroutine` are done.
        """

        # Generate.
        while True:

            # Break.
            if self.queue_count == 0:
                break

            self.get()


    def __iter__(self) -> Generator:
        """
        Return the generator of result of asynchronous `Coroutine`.

        Returns
        -------
        Generator of result of asynchronous `Coroutine`.
        """

        # Generate.
        while True:

            # Break.
            if self.queue_count == 0:
                break

            result = self.get()
            yield result


    __call__ = one


    __mul__ = repeat