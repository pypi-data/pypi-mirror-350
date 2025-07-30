import asyncio
from functools import wraps, partial

async def async_parallel(func, args):
    # runs the function(s) in parallel
    return await asyncio.gather(*[func(arg) for arg in args])

async def async_serial(func, args):
    # runs the function(s) in serial order, 
    # awaiting for each iteration's completion before executing the next.
    return [await func(arg) for arg in args]

def async_wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, sem=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        
        # Partial function to be run in executor
        pfunc = partial(func, *args, **kwargs)
        
        # Check if semaphore is provided
        if sem is not None:
            async with sem:
                return await loop.run_in_executor(executor, pfunc)
        else:
            return await loop.run_in_executor(executor, pfunc)
        
    return run