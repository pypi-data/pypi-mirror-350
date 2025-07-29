"""coroutines.py: Utilities for implementing coroutines and built-in coroutines

This module provides a convenience decorator and wrapper for coroutines.

It also provides `average`, `median`, `minimum`, and `maximum` coroutines for streaming statistics
and a convenience `stats` coroutine to process all statistics.
"""

import heapq


def coroutine(fn):
  """
  Convenience decorator for coroutines that primes the coroutine
  """

  def start(*args, **kwargs):
    cr = fn(*args, **kwargs)
    next(cr)
    return cr

  return start


class Wrapper:
  """
  Wrapper class around coroutines that allows associating data with that coroutine

  Specifically this is used to track the final value of the coroutine
  """

  def __init__(self, gen):
    self._gen = gen
    self.value = None

  def send(self, value):
    self.value = self._gen.send(value)

  def close(self):
    self._gen.close()


@coroutine
def average():
  """
  Coroutine for streaming average
  """
  total = 0
  count = 0
  avg = None
  while True:
    time = yield avg
    total += time
    count += 1
    avg = total / count


@coroutine
def median():
  """
  Coroutine for streaming median
  """
  left, right = [], []
  median = None
  while True:
    time = yield median
    heapq.heappush(left, -time)
    heapq.heappush(right, -heapq.heappop(left))
    if len(right) > len(left):
      heapq.heappush(left, -heapq.heappop(right))
    median = -left[0] if len(left) > len(right) else (-left[0] + right[0]) / 2


@coroutine
def maximum():
  """
  Coroutine for streaming maximum
  """
  mx = None
  while True:
    time = yield mx
    mx = time if not mx else max(mx, time)


@coroutine
def minimum():
  """
  Coroutine for streaming min
  """
  mn = None
  while True:
    time = yield mn
    mn = time if not mn else min(mn, time)


@coroutine
def stats():
  """
  Coroutine for streaming statistics
  """
  avg = average()
  med = median()
  mn = minimum()
  mx = maximum()
  curr_count = 0
  curr_avg = None
  curr_median = None
  curr_min = None
  curr_max = None
  while True:
    # Receive the time
    time = yield (curr_count, curr_avg, curr_median, curr_min, curr_max)
    curr_count += 1
    curr_avg = avg.send(time)
    curr_median = med.send(time)
    curr_min = mn.send(time)
    curr_max = mx.send(time)
