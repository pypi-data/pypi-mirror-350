from pydantic import BaseModel, ConfigDict, Field


class Entry(BaseModel):
    """Pydantic model for every entry inserted in the '.json' file."""

    model_config = ConfigDict(extra="forbid")

    command: str = Field(
        ..., min_length=1, description="Command cannot be empty."
    )
    description: str = Field(
        ..., min_length=1, description="Description cannot be empty."
    )
