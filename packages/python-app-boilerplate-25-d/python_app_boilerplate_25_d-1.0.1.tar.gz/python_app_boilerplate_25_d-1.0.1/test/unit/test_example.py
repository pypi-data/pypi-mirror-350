# test/unit/test_example.py

"""Example unit test."""

import pytest
import pytest_mock

import python_app_boilerplate_25_d.example


@pytest.mark.asyncio
async def test_example_iterations_100() -> None:
  """Example iterations."""
  num_iters: int = 1000
  result: int = await python_app_boilerplate_25_d.example.iterations(num_iters=num_iters)
  assert result == num_iters


@pytest.mark.asyncio
async def test_mock_example_iterations_100(mocker: pytest_mock.MockFixture) -> None:
  """Example mock iterations."""
  num_iters: int = 100
  mock_response: int = -1
  mocker.patch(
    "python_app_boilerplate_25_d.example.iterations",
    pytest_mock.AsyncMockType(return_value=mock_response),
  )
  result: int = await python_app_boilerplate_25_d.example.iterations(num_iters=num_iters)
  assert result == mock_response
