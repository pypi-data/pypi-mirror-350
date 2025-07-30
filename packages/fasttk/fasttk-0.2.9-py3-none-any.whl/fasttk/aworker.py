
import asyncio
import logging
import inspect
from uuid import uuid4 as random_uuid, UUID
from threading import Thread
from queue import Queue as TQueue, Empty
from typing import Coroutine, Callable, Any, Never
from tkinter import Tk

logger = logging.getLogger("FastTk.AsyncWorker")

class CallWrapper:

    _args: tuple[Any, ...]
    _kwargs: dict[str, Any]
    _func: Callable | Coroutine
    _method: Callable[[], Coroutine[Any, Any, Any]]

    def __init__(
        self,
        func: Callable | Coroutine,
        args: tuple[Any, ...] | None,
        kwargs: dict[str, Any] | None
    ):
        self._func = func
        if inspect.iscoroutine(func):
            self._method = self._coroutine_call
        elif callable(func):
            self._args = args or ()
            self._kwargs = kwargs or {}
            self._method = self._function_call
        else:
            self._method = self._fallback_call
    
    async def _function_call(self) -> Any:
        return await asyncio.to_thread(self._func, *self._args, **self._kwargs)

    async def _fallback_call(self) -> Never:
        raise TypeError("Task is neither a callable or coroutine.")

    async def _coroutine_call(self) -> Any:
        return await self._func

    def call(self) -> Coroutine[Any, Any, Any]:
        return self._method()


class AsyncWorker:
    
    _thread: Thread
    _queue: TQueue[tuple[CallWrapper, UUID] | None]
    _callback: TQueue[tuple[UUID, bool, Any] | None]
    _closed: bool
    _checker_id: str
    _root: Tk
    _mapping: dict[UUID, tuple[Callable, Callable]]

    def __init__(self, root: Tk):
        self._thread = Thread(target=self._entrance, name="fasttk.AsyncWorker")
        self._queue = TQueue()
        self._callback = TQueue()
        self._closed = False
        self._checker_id = root.after_idle(self.checker)
        self._root = root
        self._mapping = {}
    
    def checker(self) -> None:
        try:
            pack = self._callback.get_nowait()
            self._callback.task_done()
            if not pack:
                return None
            uuid, use_result, args = pack
            then, err = self._mapping.pop(uuid)
            if use_result:
                try:
                    then(args)
                except Exception as e:
                    err(e)
            else:
                err(args)
        except Empty:
            self._checker_id = self._root.after(1, self.checker)
        except Exception:
            logger.error(
                "Error occurred during AsyncWorker callback:",
                exc_info=True
            )
            self._checker_id = self._root.after_idle(self.checker)
        else:
            self._checker_id = self._root.after_idle(self.checker)

    async def _subtask_wrapper(self, pack: tuple[CallWrapper, UUID], cb: TQueue):
        task, uuid = pack
        try:
            result = await task.call()
            cb.put((uuid, True, result))
        except Exception as e:
            cb.put((uuid, False, e))

    async def _async_worker(self):
        while True:
            pack = await asyncio.to_thread(self._queue.get)
            self._queue.task_done()
            if not pack:
                break
            asyncio.create_task(self._subtask_wrapper(pack, self._callback))

    def _entrance(self):
        logger = logging.getLogger("FastTk.AsyncWorker.Thread")
        logger.info("Start asyncio thread.")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self._async_worker())
        finally:
            loop.stop()
            loop.close()
        logger.info("Asyncio thread exited.")
        
    
    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        if not self._closed:
            self._closed = True
            logger.info("Stopping AsyncWorker.")
            self._root.after_cancel(self._checker_id)
            self._queue.put(None)
            self._thread.join()

    def run(self, task: CallWrapper, then: Callable, error: Callable) -> None:
        uuid = random_uuid()
        self._mapping[uuid] = (then, error)
        self._queue.put((task, uuid))

