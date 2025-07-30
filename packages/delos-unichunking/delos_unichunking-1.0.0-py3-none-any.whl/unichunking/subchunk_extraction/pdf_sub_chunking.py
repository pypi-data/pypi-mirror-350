"""Extract subchunks from PDF file."""

import asyncio
import base64
import operator
from collections.abc import Awaitable
from functools import reduce
from pathlib import Path
from typing import Any, Callable

import fitz
import pymupdf

from unichunking.types import ChunkPosition, SubChunk

MIN_PIXELS: int = 128


def _handle_line(
    line: Any,
    width: float,
    height: float,
    subchunk_idx: int,
    page_num: int,
    file_name: str,
) -> tuple[list[SubChunk], int]:
    line_chunks: list[SubChunk] = []
    for span in line["spans"]:
        text = str(span["text"].replace("�", " ").strip())
        font: Any = span["font"]
        bbox: Any = span["bbox"]
        if "bold" in font.lower():
            text = f"**{text}**"
        if text:
            x0, y0, x1, y1 = bbox
            position = ChunkPosition(
                x0=x0 / width,
                y0=y0 / height,
                x1=x1 / width,
                y1=y1 / height,
            )
            line_chunks.append(
                SubChunk(
                    subchunk_id=subchunk_idx,
                    content=text,
                    page=page_num,
                    position=position,
                    file_name=file_name,
                ),
            )
            subchunk_idx += 1

    return line_chunks, subchunk_idx


async def _retrieve_subchunks(
    path: Path,
    status_manager: Any,
    function: Callable[[str], Awaitable[str]],
) -> tuple[list[list[list[list[SubChunk]]]], list[SubChunk], int]:
    chunks: list[list[list[list[SubChunk]]]] = []
    images_chunks: list[SubChunk] = []
    idx = 0
    image_idx = 0
    images_jobs: list[dict[str, str | int]] = []

    async def handle_image(
        base64_image: str,
        image_idx: int,
        page_num: int,
        semaphore: asyncio.Semaphore,
    ) -> None:
        """Make the async call to describe the image."""
        async with semaphore:
            image_description = await function(base64_image)
            if image_description:
                image_chunk = SubChunk(
                    subchunk_id=7_700_000 + image_idx,
                    content=image_description,
                    page=page_num,
                    position=ChunkPosition(
                        x0=0,
                        y0=0,
                        x1=1,
                        y1=1,
                    ),
                    file_name=path.name,
                    content_type="image",
                )
                images_chunks.append(image_chunk)

    with pymupdf.Document(path) as doc:
        num_pages: Any = doc.page_count  # type: ignore
        for page_num in range(num_pages):
            # text
            if page_num % int(num_pages / 17 + 1) == 0:
                page_progress = int((page_num + 1) / num_pages * 75)
                await status_manager.update_status(
                    progress=page_progress,
                    start=status_manager.start,
                    end=status_manager.end,
                )
            page_chunks: list[list[list[SubChunk]]] = []
            textpage: Any = doc.load_page(page_num).get_textpage()  # type: ignore
            page = textpage.extractDICT(sort=False)
            width, height = page["width"], page["height"]
            blocks = page["blocks"]

            for block in blocks:
                block_chunks: list[list[SubChunk]] = []
                lines = block["lines"]
                for line in lines:
                    line_chunks, idx = _handle_line(
                        line=line,
                        width=width,
                        height=height,
                        subchunk_idx=idx,
                        page_num=page_num,
                        file_name=path.name,
                    )
                    if line_chunks:
                        block_chunks.append(line_chunks)
                if block_chunks:
                    page_chunks.append(block_chunks)
            if page_chunks:
                chunks.append(page_chunks)

            zoom = 1.0  # Modifier le facteur de zoom pour une meilleure qualité
            mat = fitz.Matrix(zoom, zoom)

            # Convertir la page en image pixmap
            page = doc.load_page(page_num)  # type: ignore
            pix = page.get_pixmap(matrix=mat)  # type: ignore
            image_bytes = pix.tobytes()  # type: ignore

            base64_image = base64.b64encode(image_bytes).decode("utf-8")  # type: ignore

            images_jobs.append(
                {
                    "base64": base64_image,
                    "page_num": page_num,
                    "image_idx": image_idx,
                },
            )
            image_idx += 1

    # Do the tasks in //
    semaphore = asyncio.Semaphore(5)
    tasks = [
        handle_image(
            str(res["base64"]),
            int(res["page_num"]),
            int(res["image_idx"]),
            semaphore,
        )
        for res in images_jobs
    ]
    await asyncio.gather(*tasks)

    return chunks, images_chunks, num_pages


def _filter_subchunks(
    chunks: list[list[list[list[SubChunk]]]],
) -> list[SubChunk]:
    flattened_chunks: list[SubChunk] = []

    for page_chunks in chunks:
        for block_chunks in page_chunks:
            for line_chunks in block_chunks:
                if line_chunks:
                    filtered_line_chunks = reduce(operator.add, line_chunks)
                    flattened_chunks.append(filtered_line_chunks)

    return flattened_chunks


async def extract_subchunks_pdf(
    path: Path,
    status_manager: Any,
    function: Callable[[str], Awaitable[str]],
) -> tuple[list[SubChunk], int]:
    """Filetype-specific function : extracts subchunks from a PDF file.

    Args:
        path: Path to the local file.
        status_manager: Optional, special object to manage task progress.
        function: Function to handle images.

    Returns:
        A list of SubChunk objects.
    """
    chunks, images_chunks, num_pages = await _retrieve_subchunks(
        path=path,
        status_manager=status_manager,
        function=function,
    )

    if len(images_chunks) > 0:
        flattened_chunks = images_chunks
    else:
        flattened_chunks = _filter_subchunks(chunks)

    progress = 100
    await status_manager.update_status(
        progress=progress,
        start=status_manager.start,
        end=status_manager.end,
    )

    return flattened_chunks, num_pages
