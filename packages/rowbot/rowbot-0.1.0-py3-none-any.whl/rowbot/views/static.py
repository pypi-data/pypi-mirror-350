from rowbot.models.entry import Entry


class StaticTable:
    """
    Calculate the table column's widths and render it statically (entirely) or
    any of the table's sections.
    """

    @staticmethod
    def calculate_widths(entries: list[Entry]) -> tuple[int, int]:
        """
        Parse all the JSON entries and determine the command and description
        with the highest length.

        Args:
        -----
        - entries (list):
            Array with all the JSON file's entries located inside the `entries`
            key.

        Returns:
        --------
        tuple[int, int]
            Tuple containing the command and the description column's width.
        """
        command_width = max(
            len("command"),
            max(len(e.command) for e in entries) if entries else 0,
        )
        description_width = max(
            len("description"),
            max(len(e.description) for e in entries) if entries else 0,
        )

        # Custom padding for style purposes:
        return command_width + 3, description_width + 3

    @staticmethod
    def render_top(command_width: int, description_width: int) -> str:
        """
        Render the table's top row, using the maximum width for the 'command'
        and the 'description' columns.

        Args:
        -----
        - command_width (int):
            Command column's maximum width.
        - description_width (int):
            Description column's maximum width.

        Returns:
        str
            Formatted table's top row.
        """
        return f"┌{'─' * command_width}┬{'─' * description_width}┐"

    @staticmethod
    def render_header(command_width: int, description_width: int) -> str:
        """
        Render the table's header row, using the maximum width for the 'command'
        and the 'description' columns.

        Args:
        -----
        - command_width (int):
            Command column's maximum width.
        - description_width (int):
            Description column's maximum width.

        Returns:
        str
            Formatted table's header row.
        """
        return f"│ {'Command'.ljust(command_width - 2)} │ {'Description'.ljust(description_width - 2)} │"

    @staticmethod
    def render_separator(command_width: int, description_width: int) -> str:
        """
        Render the table's separator row, using the maximum width for the 'command'
        and the 'description' columns.

        Args:
        -----
        - command_width (int):
            Command column's maximum width.
        - description_width (int):
            Description column's maximum width.

        Returns:
        str
            Formatted table's separator row.
        """
        return f"├{'─' * command_width}┼{'─' * description_width}┤"

    @staticmethod
    def render_row(
        command: str,
        command_width: int,
        description: str,
        description_width: int,
    ) -> str:
        """
        Render a table's row, using the maximum width for the 'command' and the
        'description' columns.

        Args:
        -----
        - command (str):
            Current row's command.
        - command_width (int):
            Command column's maximum width.
        - description (str):
            Current row's description.
        - description_width (int):
            Description column's maximum width.

        Returns:
        str
            Formatted table's row.
        """
        return f"│ {command.ljust(command_width - 2)} │ {description.ljust(description_width - 2)} │"

    @staticmethod
    def render_bottom(command_width: int, description_width: int) -> str:
        """
        Render the table's bottom row, using the maximum width for the 'command'
        and the 'description' columns.

        Args:
        -----
        - command_width (int):
            Command column's maximum width.
        - description_width (int):
            Description column's maximum width.

        Returns:
        str
            Formatted table's bottom row.
        """
        return f"└{'─' * command_width}┴{'─' * description_width}┘"

    @staticmethod
    def draw_table(entries: list[Entry]) -> None:
        """
        Render a formatted table with a 'commands' and a 'description' coumn in
        it, based on the maximum width these columns can have and an additional
        padding added to them.

        Args:
        -----
        - entries (list[Entry]):
            Array with all the 'Entry' instances (rows) the table has.
        """
        command_width, description_width = StaticTable.calculate_widths(
            entries=entries,
        )

        print(
            StaticTable.render_top(
                command_width=command_width,
                description_width=description_width,
            )
        )
        print(
            StaticTable.render_header(
                command_width=command_width,
                description_width=description_width,
            )
        )
        print(
            StaticTable.render_separator(
                command_width=command_width,
                description_width=description_width,
            )
        )

        for entry in entries:
            print(
                StaticTable.render_row(
                    command=entry.command,
                    command_width=command_width,
                    description=entry.description,
                    description_width=description_width,
                )
            )

        print(
            StaticTable.render_bottom(
                command_width=command_width,
                description_width=description_width,
            )
        )
