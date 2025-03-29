# QuirionExport

This is a simple tool to export data from Quirion's API to a CSV file.

## Generate the executable

To generate the executable, you need to install `pyinstaller` and run the following command:
```bash
pip install -U pyinstaller
```

Then, you can run the following command:
```bash
pyinstaller --onefile --specpath ./dist --name=QuirionExport src/main.py
```

## Linting

Install the `pylint` package:
```bash
pip install pylint
```

Then, you can line all python files the following command:
Or only new files:
```bash
pylint $(git ls-files '*.py')
```