from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Chunk(BaseModel):
    """Represents one text chunk from a source document."""

    model_config = ConfigDict(extra="forbid")

    id: str
    source: str
    position: int = Field(ge=0)
    text: str
    word_count: int = Field(ge=0)


class Settings(BaseModel):
    """Configuration for document chunking."""

    model_config = ConfigDict(extra="forbid")

    size: int = Field(default=200, gt=0)
    overlap: int = Field(default=40, ge=0)

    @model_validator(mode="after")
    def validate_overlap(self) -> Self:
        if self.overlap >= self.size:
            raise ValueError("Overlap must be smaller than chunk size.")

        return self
