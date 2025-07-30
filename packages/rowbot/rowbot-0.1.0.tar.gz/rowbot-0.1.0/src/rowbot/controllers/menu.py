from pydantic import ValidationError

from rowbot.models.entry import Entry
from rowbot.services.commands import Commands
from rowbot.views.static import StaticTable


class Menu:
    """Perform actions into a JSON file, based on user input."""

    def __init__(self, commands: Commands) -> None:
        self.commands = commands

    def display(self) -> None:
        """
        Interactive menu for the user to select a given action and execute it in
        the JSON file.

        Whenever the user has entered a wrong input more than three times, the
        menu closes displaying an error message.
        """
        attempts = 0
        max_attempts = 3

        while attempts < max_attempts:
            print("\nSelect an action:")
            print("1. Add a command.")
            print("2. Remove a command.")
            print("3. Modify a command's description.")
            print("4. Exit without making any changes.")

            choice = input("\nEnter the number of your choice: ")

            if choice == "1":
                self.add()
                break

            if choice == "2":
                self.delete()
                break

            if choice == "3":
                self.modify()
                break

            if choice == "4":
                print("Exiting...")
                break

            print("Invalid choice. Please try again.")
            attempts += 1

        if attempts == max_attempts:
            print("")
            print("Max attempts reached. Exiting...")

    def add(self) -> None:
        """
        Prompt the user to enter a new command and its description, to add it in
        the JSON file, as long as it doesn't exist already there.

        Raises:
        -------
        - `ValueError`:
            Raised whenever the specified command already exists in the JSON file.
        """
        try:
            # Prompt the user to specify the command and description to add:
            command = input("Enter the new command: ")
            description = input("Enter the command's description: ")
            entry = Entry(command=command, description=description)

            # Prompt the user for confirmation:
            StaticTable.draw_table(entries=[entry])
            confirm = input("Type 'yes' to confirm these changes: ")

            # Adding the given command in the JSON file (if it doesn't exist yet).
            if confirm.lower() == "yes":
                self.commands.add(entry=entry)

        except ValidationError as validation_error:
            print(f"Invalid input: {validation_error.errors()}")
            raise validation_error

    def delete(self) -> None:
        """
        Prompt the user to delete a given command from the JSON file, as long as
        it does exist already there.

        Raises:
        -------
        - `ValueError`:
            Raised whenever the specified command doesn't exist in the JSON file.
        """
        # Prompt the user to specify the command to be deleted:
        command = input("Enter the command to remove: ")

        # Prompt the user for confirmation:
        confirm = input("Type 'yes' to confirm these changes: ")

        # Deleting the given command from the JSON file (if it exists already).
        if confirm.lower() == "yes":
            self.commands.delete(name=command)

    def modify(self) -> None:
        """
        Modify a given command's description, as long as the specified command
        does exist already in the JSON file.

        Raises:
        -------
        - `ValueError`:
            Raised whenever the specified command doesn't exist in the JSON file.
        """
        try:
            # Prompt the user to specify the command and description to add:
            command = input("Enter the new command: ")
            description = input("Enter the command's new description: ")
            entry = Entry(command=command, description=description)

            # Prompt the user for confirmation:
            StaticTable.draw_table(entries=[entry])
            confirm = input("Type 'yes' to confirm these changes: ")

            # Updating the command's description (if it exists already).
            if confirm.lower() == "yes":
                self.commands.modify(name=command, description=description)

        except ValidationError as validation_error:
            print(f"Invalid input: {validation_error.errors()}")
            raise validation_error
