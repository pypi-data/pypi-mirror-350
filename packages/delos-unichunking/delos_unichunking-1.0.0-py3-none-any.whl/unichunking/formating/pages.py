"""Page computing."""

import re
from typing import Any

from llmax import tokens

from unichunking.settings import unisettings
from unichunking.types import Chunk, StatusManager


def _strip_text(txt: str) -> str:
    image_description_pattern = r"@_@_@ IMAGE \d+ @_@_@"
    return (
        re.sub(image_description_pattern, "", txt)
        .replace("** Table : ", "")
        .replace(" ; End Of Table **", "")
        .replace("** Chart : ", "")
        .replace(" ; End Of Chart **", "")
        .replace(" ", "")
        .replace("\n", "")
        .replace("\xa0", "")
        .replace("-", "")
        .lower()
    )


def _positions_intersect(
    position1: dict[str, float],
    position2: dict[str, float],
) -> bool:
    return (
        (
            position1["x0"] <= position2["x0"] <= position1["x1"]
            and position1["y0"] <= position2["y0"] <= position1["y1"]
        )
        or (
            position1["x0"] <= position2["x1"] <= position1["x1"]
            and position1["y0"] <= position2["y0"] <= position1["y1"]
        )
        or (
            position1["x0"] <= position2["x0"] <= position1["x1"]
            and position1["y0"] <= position2["y1"] <= position1["y1"]
        )
        or (
            position1["x0"] <= position2["x1"] <= position1["x1"]
            and position1["y0"] <= position2["y1"] <= position1["y1"]
        )
    )


def _edit_chunk_positions(
    chunk: Chunk,
) -> None:
    different_positions: list[dict[str, float]] = []
    for position in chunk.positions:
        position["x0"] = max(0, position["x0"])
        position["y0"] = max(0, position["y0"])
        position["x1"] = min(1, position["x1"])
        position["y1"] = min(1, position["y1"])
        new = True
        for different_position in different_positions:
            if _positions_intersect(
                position,
                different_position,
            ) or _positions_intersect(different_position, position):
                different_position["x0"] = min(
                    different_position["x0"],
                    position["x0"],
                )
                different_position["y0"] = min(
                    different_position["y0"],
                    position["y0"],
                )
                different_position["x1"] = max(
                    different_position["x1"],
                    position["x1"],
                )
                different_position["y1"] = max(
                    different_position["y1"],
                    position["y1"],
                )
                new = False
                break
        if new:
            different_positions.append(position)
    chunk.positions = different_positions


def edit_positions_on_page(
    chunks_pages: list[list[Chunk]],
    extension: str,
) -> list[list[Chunk]]:
    """Adjusts the positions of subelements in Chunk objects to avoid overlaps.

    For DOCX : no highlighting because sourcing is not precise enough.

    Args:
        chunks_pages: A list of lists where chunks_pages[i][j] is Chunk j on page i.
        extension: File extension.

    Returns:
        The same list of lists of Chunk objects, whoses positions where adjusted.
    """
    if extension == "docx":
        for page in chunks_pages:
            for chunk in page:
                chunk.positions = [{"x0": 0.0, "y0": 0.0, "x1": 0.0, "y1": 0.0}]

    else:
        for page in chunks_pages:
            for chunk in page:
                _edit_chunk_positions(chunk)

    return chunks_pages


async def compute_pages(
    chunks: list[Chunk],
    status_manager: Any = None,
) -> tuple[list[Chunk], int]:
    """Corrects the pagination of DOCX chunks by comparing the text to the converted PDF.

    Args:
        path: Path to the local file.
        chunks: List of Chunk objects.
        num_pages: Number of pages originally found through Page Breaks.
        status_manager: Optional, special object to manage task progress.
        increment_reach: Boolean value (True by default) indicating whether or not to increase the page reach when accumulating chunks on the same page.

    Returns:
        A tuple containing an int and a list:
        - The actual number of pages in the document.
        - A list containing the Chunk objects, updated with the correct page numbers.
    """
    if not status_manager:
        status_manager = StatusManager(task="Page computing")

    curr_page = 0
    page_content_token = 0

    for chunk_idx in range(len(chunks)):
        if chunk_idx % int(len(chunks) / 30 + 1) == 0:
            page_progress = int((chunk_idx + 1) / len(chunks) * 100)
            await status_manager.update_status(
                progress=page_progress,
                start=status_manager.start,
                end=status_manager.end,
            )

        chunk = chunks[chunk_idx]
        stripped_chunk = _strip_text(chunk.content)

        page_content_token += tokens.count(stripped_chunk)

        if page_content_token > unisettings.chunking.MAX_TOKENS_PAGE:
            curr_page += 1
            page_content_token = 0

        chunk.page_num = curr_page + 1

    return chunks, curr_page + 1
