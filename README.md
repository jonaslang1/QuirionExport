# QuirionExport

QuirionExport is a simple tool to automate data retrieval from the Quirion API.
It allows you to export your investment data into CSV files and download  documents from the postbox.

## Requirements

- Python 3.8 or higher
- Access to the Quirion API (credentials are required)

## Installation

Download the executable from the [releases](https://github.com/jonaslang1/QuirionExport/releases/latest) page or build it from source.

## Usage

1. Run the executable by double-clicking it or from the command line:
```bash
./dist/QuirionExport
```
2. Run the tool from the command line:
```bash
python src/main.py
```

### Output

The output will be saved in the [output](output) directory.
It generates a CSV file for each product in your Quirion account.
Use the [ImportVorlagen.dat](ImportVorlagen.dat) template file to import the import templates into your financial software to facilitate the import of the generated CSV files.
Additionally,
it can download the unread postbox documents and save them to the [output/documents](output/documents) directory.

### Options

#### Log Level

You can specify a loglevel for the output.
The default is `INFO`, but you can set it to either `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`.
```bash
python src/main.py --log-level DEBUG
```

## Contribute

1. Clone the repository:
   ```bash
   git clone https://github.com/jonaslang1/QuirionExport
   cd QuirionExport
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
Feel free to open issues, submit pull requests or fork the repository.

## Generate the Executable

1. To generate the executable, install `pyinstaller`:
   ```bash
   pip install -U pyinstaller
   ```
   
2. Then run:
   ```bash
   pyinstaller --onefile --specpath ./dist --name=QuirionExport src/main.py
   ```

The executable will be available in the [dist](dist) directory.

## Testing

To run the tests, run:
```bash
pytest
```
or, if you want to see the output in a more verbose format:
```bash
pytest -v
```
You can also run the tests with coverage:
```bash
pytest --cov --cov-report=html:target/coverage
```
This will generate an HTML report in the [target/coverage](target/coverage) directory.
Open the [index.html](target/coverage/index.html) file in your browser to view the coverage report.

## Linting

Install the `pylint` package:
```bash
pip install pylint
```

Lint all Python files:
```bash
pylint $(git ls-files '*.py')
```

Or only modified files:
```bash
pylint $(git ls-files -m '*.py')
```

## Troubleshooting & Support

If you encounter issues or have questions, please open an issue in the repository.

## License

This project is currently not licensed. All rights reserved.
