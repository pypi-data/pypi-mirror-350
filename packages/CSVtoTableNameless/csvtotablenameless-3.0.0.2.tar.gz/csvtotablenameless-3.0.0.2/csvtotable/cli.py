import os
import sys
import argparse
import subprocess

from csvtotable.logger import logger
from csvtotable import convert

# Custom ArgumentParser to handle errors with logger
class CustomArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        self.debug_mode = False  # Track if --debug is set
        super().__init__(*args, **kwargs)

    def parse_known_args(self, args=None, namespace=None):
        # Check if --debug is in the arguments
        if "--debug" in (args or sys.argv):
            self.debug_mode = True
        return super().parse_known_args(args, namespace)

    def format_help(self):
        # Use detailed help if --debug is set
        if self.debug_mode:
            return super().format_help()

        # Simplified help format
        formatter = self._get_formatter()

        # Add the usage section
        formatter.add_usage("csvtotable [OPTIONS] input_file [output_file]", self._actions, self._mutually_exclusive_groups, "")

        # Add the description
        if self.description:
            formatter.add_text(self.description)

        # Add the options
        formatter.start_section("Options")
        for action in self._actions:
            if action.help != argparse.SUPPRESS:
                formatter.add_argument(action)
        formatter.end_section()

        return formatter.format_help()

    def error(self, message):
        """Override the default error method to customize error output."""
        logger.critical(message)
        logger.warning("Try 'csvtotable --help' for help.")
        sys.exit(2)


def prompt_overwrite(file_name):
    """Prompt the user to confirm overwriting a file."""
    if not os.path.exists(file_name):
        return True

    fmt = "File ({}) already exists. Do you want to overwrite? (y/n): "
    message = fmt.format(file_name)
    logger.warning(message)
    choice = input().strip().lower()

    return choice == "y"

def show_version():
    """Run 'python -m pip show CSVToTableNameless' and display its output."""
    try:
        # Run the pip show command
        result = subprocess.run(
            ["python", "-m", "pip", "show", "CSVtoTableNameless"],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving package information: {e}")
        sys.exit(1)
def main():
    # Use CustomArgumentParser
    parser = CustomArgumentParser(
        description="CSVtoTable: Convert CSV files into searchable, sortable HTML tables.",
    )

    # Add a --version flag to act as an alias for 'python -m pip show'
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show detailed version and metadata about the tool (alias for 'python -m pip show CSVtoTableNameless')."
    )

    # Positional arguments
    parser.add_argument(
        "input_file",
        type=str,
        nargs="?",
        help="Path to the input CSV file."
    )
    parser.add_argument(
        "output_file",
        type=str,
        nargs="?",
        help="Path to the output HTML file (optional if --serve is used).",
    )

    # Options
    parser.add_argument(
        "-c", "-t", "--caption", "--title",
        type=str,
        help="Table caption and HTML title."
    )
    parser.add_argument(
        "-d", "--delimiter",
        type=str,
        default=",",
        help="CSV delimiter (default: ',')."
    )
    parser.add_argument(
        "-q", "--quotechar",
        type=str,
        default='"',
        help="String used to quote fields containing special characters (default: '\"')."
    )
    parser.add_argument(
        "-dl", "--display-length",
        type=int,
        default=-1,
        help="Number of rows to show by default. Defaults to -1 (show all rows)."
    )
    parser.add_argument(
        "-o", "--overwrite",
        action="store_true",
        help="Overwrite the output file if it exists."
    )
    parser.add_argument(
        "-s", "--serve",
        action="store_true",
        help="Open output HTML in a browser instead of writing to a file."
    )
    parser.add_argument(
        "-H", "--height",
        type=str,
        help="Table height in px or as a percentage (e.g., 50%%)."
    )
    parser.add_argument(
    "-p", "--pagination",
    action="store_true",
    help="Enable table pagination (enabled by default unless virtual scroll is active)."
    )
    parser.add_argument(
        "-vs", "--virtual-scroll",
        type=int,
        default=1000,
        help="Enable virtual scroll for tables with more than the specified number of rows. Set to -1 to disable and 0 to always enable."
    )
    parser.add_argument(
        "-nh", "--no-header",
        action="store_true",
        help="Disable displaying the first row as headers."
    )
    parser.add_argument(
        "-e", "--disable-export",
        action="store_true",
        help="Disable export options for the table."
    )
    parser.add_argument(
        "-eo", "--export-options",
        choices=["copy", "csv", "json", "print"],
        nargs="+",
        help="Specify export options (default: all). For multiple options, use: -eo json csv."
    )
    parser.add_argument(
        "-ps", "--preserve-sort",
        action="store_true",
        help="Preserve the default sorting order."
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode to show full tracebacks and advanced info with --help."
    )

    # Parse arguments
    args = parser.parse_args()

    # Handle the --version flag
    if args.version:
        show_version()
        sys.exit(0)

    # Check for required input_file
    if not args.input_file:
        parser.error("the following arguments are required: input_file")

    try:
        # Convert the CSV
        content = convert.convert(
            args.input_file,
            caption=args.caption,
            delimiter=args.delimiter,
            quotechar=args.quotechar,
            display_length=args.display_length,
            height=args.height,
            pagination=args.pagination,
            virtual_scroll=args.virtual_scroll,
            no_header=args.no_header,
            disable_export=args.disable_export,
            export_options=args.export_options,
            preserve_sort=args.preserve_sort,
        )

        # Serve the file or write to output
        if args.serve:
            convert.serve(content)
        elif args.output_file:
            # Check overwrite conditions
            if not args.overwrite and os.path.exists(args.output_file):
                if not prompt_overwrite(args.output_file):
                    logger.warning("Operation aborted by user.")
                    sys.exit(0)
            convert.save(args.output_file, content)
            logger.info("File converted successfully: %s", args.output_file)
        else:
            raise ValueError("Missing argument: output_file or --serve.")

    except Exception as e:
        if args.debug:
            import traceback
            traceback.print_exc()
        logger.critical(f"{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
