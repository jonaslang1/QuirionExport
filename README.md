# QuirionExport

This is a simple tool to export data from Quirion's API to a CSV file.

## Generate the executable

To generate the executable, you need to install `pyinstaller` and run the following command:
```bash
pip install -U pyinstaller
```

Then, you can run the following command:
```bash
pyinstaller --onefile --name=QuirionExport src/main.py
```