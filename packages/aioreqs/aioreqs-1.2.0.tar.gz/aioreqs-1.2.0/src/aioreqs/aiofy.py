import typing
import asyncio
import functools
import concurrent.futures

# ==------------------------------------------------------------== #
# Global and static variables, constants                           #
# ==------------------------------------------------------------== #
__default_thread_pool: concurrent.futures.ThreadPoolExecutor | None = None


# ==------------------------------------------------------------== #
# Decorators                                                       #
# ==------------------------------------------------------------== #
def awaitable(func: typing.Callable = None, *, thread_pool: concurrent.futures.ThreadPoolExecutor | None = None):
    """Decorates synchronous function and makes it awaitable by executing it in thread pool to prevent IO-bounds blocks.

    Important notes:
    - Don't use this decorator for CPU-intensive tasks, use `@parallel` (not implemented now) instead to prevent event loop blocks.
    - Preferably no more than one workers in thread pool.

    Usecases:
    - File I/O operations (e.g., reading/writing files, especially large ones)
    - Any blocking network and socket operations
    - External services interactions
    """

    def outer_wrapper(wrapped_func: typing.Callable):

        @functools.wraps(wrapped_func)
        async def inner_wrapper(*args, **kwargs):

            # If thread pool type is inbvalid
            if thread_pool is not None and type(thread_pool) not in [concurrent.futures.ThreadPoolExecutor]:
                raise Exception("Argument `thread_pool` have to be `ThreadPoolExecutor` type or `None`.")

            # If no thread pool defined in decorator argument - use default
            if thread_pool is None:

                # If deafult thrad pool executor defined
                if __default_thread_pool is not None:
                    return await asyncio.get_event_loop().run_in_executor(__default_thread_pool, lambda: wrapped_func(*args, **kwargs))

                return await asyncio.to_thread(wrapped_func, *args, **kwargs)

            # Executing function in defined thraed pool
            return await asyncio.get_event_loop().run_in_executor(thread_pool, lambda: wrapped_func(*args, **kwargs))

        # Return wrapped function
        return inner_wrapper

    # If decorator gets arguments
    if func is None:
        return outer_wrapper

    return outer_wrapper(func)


# ==------------------------------------------------------------== #
# Functions                                                        #
# ==------------------------------------------------------------== #
def create_thread_pool(max_threads: int = 32, thread_name_prefix: str = "thread") -> concurrent.futures.ThreadPoolExecutor:
    """Wrapper-function for simple creating of `ThreadPoolExecutor` instance."""

    return concurrent.futures.ThreadPoolExecutor(max_workers=max_threads, thread_name_prefix=thread_name_prefix)


def set_default_thread_pool_executor(thread_pool: concurrent.futures.ThreadPoolExecutor | None = None) -> None:
    """Sets given thread pool as default to make function decorated with `@awaitable` executes at this thread pool if `thread_pool` argument not defined in decorator."""

    if thread_pool is not None and type(thread_pool) not in [concurrent.futures.ThreadPoolExecutor]:
        raise Exception("Argument `thread_pool` have to be `ThreadPoolExecutor` type or `None`.")

    global __default_thread_pool

    __default_thread_pool = thread_pool
