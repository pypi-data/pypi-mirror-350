"""Converts files to Office format or PDF."""

import asyncio
import subprocess
from pathlib import Path
from typing import Literal

from unichunking.utils import logger


async def convert_file(
    input_path: Path,
    extension: Literal["docx", "xlsx", "pptx", "pdf"],
    max_attempts: int = 5,
) -> Path | None:
    """Converts DOC/XLS/PPT and ODT/ODS/ODP to DOCX/XLSX/PPTX or PDF.

    Args:
        input_path: Path to the local file to convert.
        extension: Output format.
        max_attempts: maximun sttemps before failing

    Returns:
        The path to the local converted file.
    """
    attempt = 0

    while attempt < max_attempts:
        try:

            def run_subprocess() -> None:
                subprocess.run(  # noqa: S603
                    [
                        Path("soffice"),
                        "--headless",
                        "--convert-to",
                        extension,
                        input_path,
                        "--outdir",
                        input_path.parent,
                    ],
                    check=True,
                )

            await asyncio.to_thread(run_subprocess)
            return input_path.with_suffix(f".{extension}")

        except subprocess.CalledProcessError:  # noqa: PERF203
            attempt += 1
            logger.error(
                f"Attempt {attempt}: Couldn't convert the file to {extension}",
            )

    logger.error(
        f"Failed to convert the file to {extension} after {max_attempts} attempts",
    )
    return None
