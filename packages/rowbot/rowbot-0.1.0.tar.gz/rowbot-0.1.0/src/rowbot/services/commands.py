from rowbot.models.entry import Entry
from rowbot.services.storage import JSONStorage


class Commands:
    """
    Manage the commands entries in a JSON file, handling specific business cases
    and ensuring a successful commands management.
    """

    def __init__(self, storage: JSONStorage):
        self.storage = storage

    def add(self, entry: Entry) -> None:
        """
        Add a new entry of a command/description into the JSON file, ensuring it
        doesn't exist already.

        Args:
        -----
        - entry (Entry):
            'Entry' instance, expected to be added in the JSON file, if it
            doesn't exist yet.

        Raises:
        -------
        - `ValueError`:
            Raised whenever the specified **command** already exists in the JSON
            file.
        """
        commands = self.storage.read()

        if any(cmd.command == entry.command for cmd in commands):
            print(f"Command '{entry.command}' already exists.")
            raise ValueError(f"Command '{entry.command}' already exists.")

        commands.append(entry)
        commands.sort(key=lambda x: x.command)

        self.storage.write(entries=commands)

    def delete(self, name: str) -> None:
        """
        Remove an entry from the JSON file by using the command's name, ensuring
        it exists already.

        Args:
        -----
        - name (str):
            Command's name to be deleted.

        Raises:
        -------
        - `ValueError`:
            Raised whenever the specified command doesn't exist yet.
        """
        commands = self.storage.read()
        updated = [cmd for cmd in commands if cmd.command != name]

        if len(updated) == len(commands):
            print(f"Command '{name}' not found.")
            raise ValueError(f"Command '{name}' not found.")

        self.storage.write(entries=updated)

    def modify(self, name: str, description: str) -> None:
        """
        Update an entry's description, ensuring the specified command does exist
        already in the JSON file.

        Args:
        -----
        - name (str):
            Command's name.
        - description (str):
            Command's new description.

        Raises:
        -------
        - `ValueError`:
            Raised whenever the specified command doesn't exist yet.
        """
        commands = self.storage.read()

        for i, cmd in enumerate(commands):
            if cmd.command == name:
                commands[i] = Entry(command=name, description=description)
                self.storage.write(entries=commands)
                return

        print(f"Command '{name}' not found for modification.")
        raise ValueError(f"Command '{name}' not found for modification.")

    def list(self) -> list[Entry]:
        """
        Retrieve all the existing entries in the JSON `entries` key.

        Returns:
        list[Entry]
            All the JSON file's entries within its `entries` key.
        """
        return self.storage.read()
