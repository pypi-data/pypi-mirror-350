# src/python_app_boilerplate_25_d/example.py

"""Example."""


async def iterations(num_iters: int) -> int:
  """Sum one to zero num_iters times.

  Args:
      num_iters (int): Number of iterations.

  Returns:
      int: num_iters * 1
  """
  result: int = 0
  for _ in range(num_iters):
    result += 1
  return result
