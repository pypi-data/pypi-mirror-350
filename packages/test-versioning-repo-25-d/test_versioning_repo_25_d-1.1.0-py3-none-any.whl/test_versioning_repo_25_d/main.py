# src/test_versioning_repo_25_d/main.py

"""Main."""

import asyncio
import logging

import test_versioning_repo_25_d.example
import test_versioning_repo_25_d

logger = logging.getLogger("main")


async def async_main() -> None:
  """Main entry point."""
  num_iters: int = 1000
  result: int = await test_versioning_repo_25_d.example.iterations(num_iters)
  logger.info(result)
  logger.info(test_versioning_repo_25_d.__version__)


def main() -> None:
  """Entry point for command line execution."""
  logging.basicConfig(level=logging.INFO)
  asyncio.run(async_main())


if __name__ == "__main__":
  main()
