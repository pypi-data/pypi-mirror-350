from __future__ import unicode_literals
import re
import os
import six
import uuid
import json
import time
import tempfile
import webbrowser
from io import open
import unicodecsv as csv
from jinja2 import Environment, FileSystemLoader, select_autoescape

from csvtotable.logger import logger

# File paths and Jinja2 environment setup
package_path = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(package_path, "templates")

env = Environment(
    loader=FileSystemLoader(templates_dir),
    autoescape=select_autoescape(["html", "xml", "j2"])
)
template = env.get_template("template.j2")

def convert(input_file_name, **kwargs):
    """Convert CSV file to HTML table"""
    delimiter = kwargs.get("delimiter") or ","
    quotechar = kwargs.get("quotechar") or "|"

    if six.PY2:
        delimiter = delimiter.encode("utf-8")
        quotechar = quotechar.encode("utf-8")

    # Read CSV and form a header and rows list
    with open(input_file_name, "rb") as input_file:
        reader = csv.reader(input_file,
                            encoding="utf-8",
                            delimiter=delimiter,
                            quotechar=quotechar)

        csv_headers = []
        if not kwargs.get("no_header"):
            # Read header from first line
            csv_headers = next(reader)

        csv_rows = [row for row in reader if row]

        # Set default column name if header is not present
        if not csv_headers and len(csv_rows) > 0:
            end = len(csv_rows[0]) + 1
            csv_headers = ["Column {}".format(n) for n in range(1, end)]

        # Render CSV to HTML
        html = render_template(csv_headers, csv_rows, **kwargs)

        # Return HTML
        return html


def save(file_name, content):
    """Save content to a file"""
    with open(file_name, "w", encoding="utf-8") as output_file:
        output_file.write(content)
    return output_file.name


def serve(content):
    """Write content to a temp file and serve it in browser"""
    temp_folder = tempfile.gettempdir()
    temp_file_name = tempfile.gettempprefix() + str(uuid.uuid4()) + ".html"
    # Generate a file path with a random name in temporary dir
    temp_file_path = os.path.join(temp_folder, temp_file_name)

    # save content to temp file
    save(temp_file_path, content)

    # Open templfile in a browser
    webbrowser.open("file://{}".format(temp_file_path))

    # Block the thread while content is served
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # cleanup the temp file
        os.remove(temp_file_path)


def render_template(table_headers, table_items, **options):
    """Render Jinja2 template."""
    caption = options.get("caption", "Table")
    display_length = options.get("display_length", -1)
    height = options.get("height", "70vh") or "70vh" # Ensure a valid default
    height = height.replace("%", "vh") # Adjust for 'vh'
    default_length_menu = [-1, 10, 25, 50]
    pagination = options.get("pagination", True)
    virtual_scroll_limit = options.get("virtual_scroll", 1000)
    preserve_sort = options.get("preserve_sort", False)

    # Determine if virtual scroll should be enabled
    virtual_scroll = False
    if virtual_scroll_limit != -1 and len(table_items) > virtual_scroll_limit:
        virtual_scroll = True
        display_length = -1  # Disable default display length for virtual scroll
        logger.warning(f"Virtual scroll is enabled since number of rows exceeds {virtual_scroll_limit}.")

    if not pagination and virtual_scroll:
        logger.warning("Pagination cannot be disabled in virtual scroll mode.")
        pagination = True  # Force pagination on

    # Data table options
    columns = [{"title": header} for header in table_headers]
    datatable_options = {
        "columns": columns,
        "data": table_items,
        "iDisplayLength": display_length,
        "sScrollX": "100%",
        "sScrollXInner": "100%",
        "paging": pagination,
        "scrollY": height,
    }

    if virtual_scroll:
        datatable_options.update({
            "scroller": True,
            "bPaginate": False,
            "deferRender": True,
            "bLengthChange": False,
        })

    if preserve_sort:
        datatable_options["order"] = []

    # Add export options if export is not explicitly disabled
    enable_export = not options.get("disable_export", False)
    if enable_export:
        allowed = options.get("export_options", ["copy", "csv", "json", "print"])
        if not isinstance(allowed, list):
            allowed = ["copy", "csv", "json", "print"]
        datatable_options.update({
            "dom": "Bfrtip",
            "buttons": allowed,
        })

    datatable_options_json = json.dumps(datatable_options, separators=(",", ":"))
    return template.render(
        caption=caption,
        datatable_options=datatable_options_json,
        virtual_scroll=virtual_scroll,
        enable_export=enable_export,
    )
