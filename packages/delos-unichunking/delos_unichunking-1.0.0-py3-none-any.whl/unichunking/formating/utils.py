"""Useful functions for handling SubChunks and Chunks."""

from uuid import uuid4

from llmax import tokens

from unichunking.types import Chunk, SubChunk


def subchunks_to_chunks(
    subchunks: list[SubChunk],
) -> list[Chunk]:
    """Convert a SubChunk object to a Chunk object with the same content."""
    return [
        Chunk(
            chunk_num=i + 1,
            content=subchunks[i].content,
            page_num=subchunks[i].page,
            positions=[subchunks[i].position.to_dict()],
            embedding=None,
            chunk_uid=uuid4(),
            num_tokens=tokens.count(subchunks[i].content),
        )
        for i in range(len(subchunks))
    ]
