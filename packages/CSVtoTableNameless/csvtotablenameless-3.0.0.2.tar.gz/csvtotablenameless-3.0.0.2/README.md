# CSVtoTable

Simple command-line utility to convert CSV files to searchable and
sortable HTML table. Supports large datasets and horizontal scrolling
for large number of columns.

DISCLAIMER: This is NOT an official version, nor am I affiliated
with the original creator Vivek R \@vividvilla
<https://github.com/vividvilla> (Upstream Author) This version is mostly
for me, if you wanna use it too go ahead but I give no promises of
function. If you notice any errors or issues please tell me!

## Demo

[Here is a demo](<https://NanashiTheNameless.github.io/csvtotable/sample/goog.html>)
of [sample csv](<https://github.com/NanashiTheNameless/csvtotable/blob/master/sample/goog.csv>)
file converted to HTML table.

###### (You can use [https://NanashiTheNameless.github.io/csvtotable/sample/index.html](<https://NanashiTheNameless.github.io/csvtotable/sample/index.html>) to see all the example HTML pages.)

## Installation

Get the Latest

```sh
python3 -m pip install --upgrade 'CSVtoTableNameless @ git+https://github.com/NanashiTheNameless/csvtotable@master'
```

Or get from [PyPi](<https://pypi.org/project/CSVtoTableNameless/>) (not recommended, may be out of date)

```sh
python3 -m pip install --upgrade CSVtoTableNameless
```

## Get started

```sh
csvtotable --help
```

Convert `data.csv` file to `data.html` file

```sh
csvtotable data.csv data.html
```

Open output file in a web browser instead of writing to a file

```sh
csvtotable data.csv --serve
```

## Options

```text
csvtotable [OPTIONS] input_file [output_file]

CSVtoTable: Convert CSV files into searchable, sortable HTML tables.

Options:
  -h, --help            show this help message and exit
  --version             Show detailed version and metadata about the tool (alias for 'python3 -m pip show CSVtoTableNameless').
  input_file            Path to the input CSV file.
  output_file           Path to the output HTML file (optional if --serve is used).
  -c CAPTION, -t CAPTION, --caption CAPTION, --title CAPTION
                        Table caption and HTML title.
  -d DELIMITER, --delimiter DELIMITER
                        CSV delimiter (default: ',').
  -q QUOTECHAR, --quotechar QUOTECHAR
                        String used to quote fields containing special characters (default: '"').
  -dl DISPLAY_LENGTH, --display-length DISPLAY_LENGTH
                        Number of rows to show by default. Defaults to -1 (show all rows).
  -o, --overwrite       Overwrite the output file if it exists.
  -s, --serve           Open output HTML in a browser instead of writing to a file.
  -H HEIGHT, --height HEIGHT
                        Table height in px or as a percentage (e.g., 50%).
  -p, --pagination      Enable table pagination (enabled by default unless virtual scroll is active).
  -vs VIRTUAL_SCROLL, --virtual-scroll VIRTUAL_SCROLL
                        Enable virtual scroll for tables with more than the specified number of rows. Set to -1 to disable and 0 to always enable.
  -nh, --no-header      Disable displaying the first row as headers.
  -e, --disable-export  Disable export options for the table.
  -eo {copy,csv,json,print} [{copy,csv,json,print} ...], --export-options {copy,csv,json,print} [{copy,csv,json,print} ...]
                        Specify export options (default: all). For multiple options, use: -eo json csv.
  -ps, --preserve-sort  Preserve the default sorting order.
  --debug               Enable debug mode to show full tracebacks and advanced info with --help.
```

## Credits

[All Major Contributors](<CONTRIBUTORS.md>)

[All Other Contributors](<https://github.com/NanashiTheNameless/csvtotable/graphs/contributors>)

## External HTML Libraries used

[Datatables](<https://datatables.net>)

[jQuery](<https://jquery.com>)

[JSZip](<https://stuk.github.io/jszip>)

[PDFMake](<https://github.com/bpampuch/pdfmake>)

## External Python Libraries used

[argparse](<https://pypi.org/project/argparse>)

[colorama](<https://pypi.org/project/colorama>)

[hatchling](<https://pypi.org/project/hatchling>)

[jinja2](<https://pypi.org/project/Jinja2>)

[logging](<https://pypi.org/project/logging>)

[packaging](<https://pypi.org/project/packaging>)

[six](<https://pypi.org/project/six>)

[unicodecsv](<https://pypi.org/project/unicodecsv>)

[uuid](<https://pypi.org/project/uuid>)

[wheel](<https://pypi.org/project/wheel>)

## Other Misc Used Stuffs

[jburkardt's CSV Files](<https://people.sc.fsu.edu/~jburkardt/data/csv/csv.html>)
