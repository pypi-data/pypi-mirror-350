# src/python_app_boilerplate_25_d/main.py

"""Main."""

import asyncio
import logging
import pathlib

import PIL
import PIL.Image

import python_app_boilerplate_25_d
import python_app_boilerplate_25_d.example

logger = logging.getLogger("main")


async def async_main() -> None:
  """Main entry point."""
  logger.info(python_app_boilerplate_25_d.__version__)

  resources_path = pathlib.Path(__file__).parent / "resources"
  img = PIL.Image.open(resources_path / "python-img.png")

  width = img.width
  height = img.height

  result_str: str = f"Sample Image dimensions: ({width}, {height})"
  logger.info(result_str)

  num_iters: int = 1000
  result: int = await python_app_boilerplate_25_d.example.iterations(num_iters)
  logger.info(result)


def main() -> None:
  """Entry point for command line execution."""
  logging.basicConfig(level=logging.INFO)
  asyncio.run(async_main())


if __name__ == "__main__":
  main()
