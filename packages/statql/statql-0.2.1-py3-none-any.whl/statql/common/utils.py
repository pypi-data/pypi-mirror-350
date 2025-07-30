import asyncio
import contextlib
import itertools
import math
import random
import time
import typing
from logging import getLogger

from pydantic import BaseModel, ConfigDict

logger = getLogger(__name__)


class Model(BaseModel):
    model_config = ConfigDict(extra="forbid")

    def __init__(self, **kwargs):
        self.transform(obj=kwargs)
        super().__init__(**kwargs)

    @classmethod
    def transform(cls, obj: typing.MutableMapping) -> None:
        pass


class FrozenModel(Model):
    model_config = ConfigDict(frozen=True)


def chunkify[T](*, iterator: typing.Iterator[T], size: int) -> typing.Generator[typing.List[T], None, None]:
    while True:
        chunk = list(itertools.islice(iterator, size))
        if not chunk:
            break

        yield chunk


def roundrobin[T](*iterables: typing.Iterable[T]) -> typing.Generator[T, None, None]:
    # Copied from https://docs.python.org/3/library/itertools.html
    iterators = map(iter, iterables)
    for num_active in range(len(iterables), 0, -1):
        iterators = itertools.cycle(itertools.islice(iterators, num_active))
        yield from map(next, iterators)


def invert_map[K: typing.Hashable, V: typing.Hashable](mapping: typing.Mapping[K, V]) -> typing.Dict[V, K]:
    inverted = {}

    for k, v in mapping.items():
        if k in inverted:
            raise ValueError(f"Cannot invert - value is not unique: {v}")

        inverted[v] = k

    return inverted


def async_gen_to_sync_gen[T](*, async_gen: typing.AsyncGenerator[T, None], loop: asyncio.AbstractEventLoop) -> typing.Generator[T, None, None]:
    # Create a new event loop for running the async generator.
    while True:
        try:
            # Run until the next item is available.
            value = asyncio.run_coroutine_threadsafe(async_gen.__anext__(), loop=loop).result()
            yield value
        except GeneratorExit:  # If cancelled from outside
            asyncio.run_coroutine_threadsafe(async_gen.aclose(), loop=loop).result()
            raise
        except StopAsyncIteration:  # If generator is finished naturally
            break


@contextlib.contextmanager
def timer(name: str) -> typing.ContextManager[None]:
    enter_time = time.perf_counter()

    try:
        yield
    finally:
        logger.debug(f"{name} took {time.perf_counter() - enter_time} seconds")


async def safe_wait(tasks: typing.Iterable[asyncio.Task], *, return_when: str) -> typing.Tuple[typing.Set[asyncio.Task], typing.Set[asyncio.Task]]:
    try:
        done, pending = await asyncio.wait(tasks, return_when=return_when)

    except asyncio.CancelledError as e:
        # CancelledError either came from caller of this func, or from the table scan tasks.
        # Either way, we cancel the tasks and wait for them to finish, just in case CancelledError came from the caller.
        for task in tasks:
            task.cancel(str(e))

        await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)

        raise

    else:
        if pending and return_when == asyncio.ALL_COMPLETED:
            raise RuntimeError(f"wait() has exited while some tasks are pending: {pending}")

        try:
            for task in done:
                if exc := task.exception():
                    raise exc

        except Exception:
            for task in pending:
                task.cancel()

            raise

        return done, pending


def scale_sequence[T](*, seq: typing.Sequence[T], factor: float) -> typing.List[T]:
    """
    Scales an iterable by replicating its elements so that the final list has
    approximately factor * (original number of elements) items.

    For a list of length 100 and a scaling factor of 5.5:
      - Each element is replicated floor(5.5)=5 times, giving 500 items.
      - An extra round(0.5 * 100)=50 items are randomly added from the list,
        yielding a total of 550 items.

    Args:
        seq (list): The original sequence.
        factor (float): The scaling factor.

    Returns:
        list: A new list with the replicated elements.
    """
    n = len(seq)
    if n == 0:
        return []

    base_rep = int(math.floor(factor))
    base_total = base_rep * n
    desired_total = int(round(factor * n))
    extra_count = desired_total - base_total

    # Replicate each element base_rep times.
    scaled = [item for item in seq for _ in range(base_rep)]

    # Sample extra_count items randomly (sampling with replacement).
    if extra_count > 0:
        extra_items = random.choices(seq, k=extra_count)
        scaled.extend(extra_items)

    return scaled
