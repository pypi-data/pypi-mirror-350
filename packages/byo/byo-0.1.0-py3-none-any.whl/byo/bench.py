import functools
import gc
import time
from atexit import register

from tabulate import tabulate

from .coroutines import Wrapper, stats


class bench:
  """
  Benchmarking decorator that records the number of calls and execution times
  which are passed to coroutines to compute statistics.

  Example:
    @bench
    def sleep():
      time.sleep(0.1)

  Atributes:
    _stats (dict): map of functions to coroutine tracking statistics
  """

  _stats = {}

  def __init__(self, fn):
    """
    Initialize our benchmarking decorator with the function
    to call and its name for logging
    """
    self.fn = fn
    self.name = fn.__name__

    # Add this function to the registry
    bench._stats[self.name] = Wrapper(stats())

  def __get__(self, instance, owner):
    """
    Bind self to the function call if on a class method
    """
    return functools.partial(self.__call__, instance)

  def __call__(self, *args, **kwargs):
    """
    Disable garbage collection and use perf counter
    to compute start and end time of function, then send to
    statistics coroutine
    """
    gc.disable()
    start = time.perf_counter_ns()
    result = self.fn(*args, **kwargs)
    end = time.perf_counter_ns()
    gc.enable()
    duration = end - start
    bench._stats[self.name].send(duration)
    return result

  @staticmethod
  def report_fn(name: str) -> None:
    """
    Pretty print report on all function calls for given function name
    """
    print("=== Report === ")
    headers = [
      "Function",
      "Calls",
      "Average (ms)",
      "Median (ms)",
      "Min (ms)",
      "Max (ms)",
    ]
    fn_stats = bench._stats[name]
    rows = [
      name,
      "Not found",
      "Not found",
      "Not found",
      "Not found",
      "Not found",
    ]
    if fn_stats:
      count, avg, median, mn, mx = fn_stats.value
      rows = [
        name,
        count,
        f"{avg / 10e6:.4f}" if avg else "N/A",
        f"{median / 10e6:.4f}" if median else "N/A",
        f"{mn / 10e6:.4f}" if mn else "N/A",
        f"{mx / 10e6:.4f}" if mx else "N/A",
      ]
    print(tabulate(rows, headers=headers, tablefmt="github"))

  @staticmethod
  @register
  def report() -> None:
    """
    Pretty print report on all function calls
    """
    print("=== Report === ")
    headers = [
      "Function",
      "Calls",
      "Average (ms)",
      "Median (ms)",
      "Min (ms)",
      "Max (ms)",
    ]
    rows = []
    for name, fn_stats in bench._stats.items():
      count, avg, median, mn, mx = fn_stats.value
      rows.append(
        [
          name,
          count,
          f"{avg / 10e6:.4f}" if avg else "N/A",
          f"{median / 10e6:.4f}" if median else "N/A",
          f"{mn / 10e6:.4f}" if mn else "N/A",
          f"{mx / 10e6:.4f}" if mx else "N/A",
        ]
      )
    print(tabulate(rows, headers=headers, tablefmt="github"))
