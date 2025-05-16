# QuirionExport

QuirionExport is a simple tool to automate data retrieval from the Quirion API.
It allows you to export your investment data into CSV files and download  documents from the postbox.

## Requirements

- Python 3.8 or higher
- Access to the Quirion API (API key or credentials if required)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jonaslang1/QuirionExport
   cd QuirionExport
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

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

## Usage

Run the tool from the command line:
```bash
python src/main.py
```
or, if built as an executable:
```bash
./dist/QuirionExport
```

The output will be saved in the [output](output) directory. 
It generates a CSV file for each product in your Quirion account.
Additionally,
it can download the unread postbox documents and save them to the [output/documents](output/documents) directory.

### Options

You can specify a loglevel for the output. 
The default is `INFO`, but you can set it to either `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`.
```bash
python src/main.py --log-level DEBUG
```

## Testing

To run the tests, run:
```bash
pytest
```
or, if you want to see the output in a more verbose format:
```bash
pytest -v
```

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
