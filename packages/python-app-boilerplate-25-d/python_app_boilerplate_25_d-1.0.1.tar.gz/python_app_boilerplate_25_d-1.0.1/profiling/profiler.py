# profiling/profiler.py

"""Profiling module."""

import logging
import pathlib
import time

import pyinstrument

import python_app_boilerplate_25_d.main

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("profiler")


def run_profiler() -> None:
  """Runs the application with pyinstrument."""
  profiler = pyinstrument.Profiler()
  profiler.start()

  # Place function to profile here
  python_app_boilerplate_25_d.main.main()

  profiler.stop()

  # Save report
  output_dir = pathlib.Path(__file__).parent / "reports"
  output_dir.mkdir(exist_ok=True)
  timestamp = time.strftime("%Y%m%d-%H%M%S")
  html_report_path = output_dir / f"{timestamp}_main_profile.html"

  with html_report_path.open("w") as f:
    f.write(profiler.output_html())

  result: str = f"Profiling report saved to: {html_report_path}"
  logger.info(result)


if __name__ == "__main__":
  run_profiler()
