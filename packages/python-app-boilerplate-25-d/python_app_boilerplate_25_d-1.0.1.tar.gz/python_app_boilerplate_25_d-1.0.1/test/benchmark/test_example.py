# test/benchmark/test_example.py

"""Example benchmark test."""

import pytest
import pytest_benchmark.fixture  # type: ignore[]

import python_app_boilerplate_25_d.example


@pytest.mark.asyncio
async def test_benchmark_service_simple_compute_1000_iterations(  # type: ignore[no-any-unimported]
  benchmark: pytest_benchmark.fixture.BenchmarkFixture,
) -> None:
  """Service simple compute."""
  iterations: int = 1000
  await benchmark.pedantic(  # type: ignore[]
    target=python_app_boilerplate_25_d.example.iterations, args=[iterations]
  )
