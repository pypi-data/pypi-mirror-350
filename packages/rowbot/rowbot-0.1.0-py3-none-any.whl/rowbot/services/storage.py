import json
import platform
import shutil
from abc import ABC, abstractmethod
from pathlib import Path

from pydantic import ValidationError

from rowbot.models.entry import Entry


class Storage(ABC):  # pylint: disable=C0115
    @abstractmethod
    def read(self) -> list[Entry]:  # pylint: disable=C0116
        ...

    @abstractmethod
    def write(self, entries: list[Entry]) -> None:  # pylint: disable=C0116
        ...


class JSONStorage(Storage):
    """
    Read from and write to a specific JSON file containing command entries in it
    and ensuring the data is properly managed.
    """

    def __init__(self, file: Path):
        self.file = Path(file)

    def read(self) -> list[Entry]:
        """
        Read the content of a JSON file, parsing all the existing entries within
        the `entries` key, returning an empty array if the key doesn't exist.

        Returns:
        --------
        list[Entry]
            Array of 'Entry' instances.

        Raises:
        -------
        - `json.JSONDecodeError`:
            Raised whenever the content of the JSON file has been corrupted and
            cannot be decoded.
        - `Exception`:
            Raised whenever an unexpected error occurs while decoding the file.
        """
        entries = []

        try:
            with open(file=self.file, mode="r", encoding="utf-8") as file:
                data = json.load(fp=file)

            for entry in data.get("entries", []):
                entries.append(Entry(**entry))

        except json.JSONDecodeError as decode_error:
            print(f"File's content has been corrupted: {self.file}")
            raise decode_error

        except ValidationError as validation_error:
            print(f"Incorrect data structure: {data}")
            raise validation_error

        except FileNotFoundError:
            # Creating the "commands.json" parent directory, in case it doesn't
            # exist yet:
            self.file.parent.mkdir(parents=True, exist_ok=True)

            # Determine the user's operative system, to select the os-specific
            # ".json" file which will be copied from the project's pre-defined
            # ".json" file:
            system = platform.system().lower()
            os = "win" if "windows" in system else "unix"
            src = Path(__file__).parent.parent / "configs" / f"cmds_{os}.json"
            shutil.copy(src=src, dst=self.file)

            with open(file=self.file, mode="r", encoding="utf-8") as file:
                data = json.load(fp=file)

            for entry in data.get("entries", []):
                entries.append(Entry(**entry))

        except Exception as error:
            print(f"Unexpected error while decoding JSON file: {error}")
            raise error

        return entries

    def write(self, entries: list[Entry]) -> None:
        """
        Insert an array of entries within a given JSON file.

        Args:
        -----
        - entries (list):
            Array of entries to be inserted in the file's `entries` key.
        """
        # Creating the JSON file's parent directory, if it doesn't exist yet:
        self.file.parent.mkdir(parents=True, exist_ok=True)

        with open(file=self.file, mode="w", encoding="utf-8") as file:
            json.dump(
                fp=file,
                indent=4,
                obj={"entries": [entry.model_dump() for entry in entries]},
            )
