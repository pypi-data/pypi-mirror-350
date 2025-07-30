# Global Command Tool

This is a Python CLI tool that helps you extract invoice details from PDFs and organize them into folders based on the year and month.

## Installation

To install the `global_cmd` tool, use `pip3`:

```sh
pip3 install global_cmd
This will install all the necessary dependencies for the tool to work.

How to Run the Script
After installing the tool, you can run the script from the command line by providing the folder path containing the PDFs you want to process.

Example:
global_cmd /path/to/pdf_folder

Where to Put the PDF Folder:
The pdf_folder argument should point to a directory containing PDF files that you want to process.
The tool will scan all .pdf files in this folder, extract invoice details, and organize them into directories by year and month.
The folder containing the PDFs should be accessible to the script from the command line.
Example:
global_cmd /Users/mustafa.mohammed/Automation/pdfs
Expected Output:
The tool will:

Extract the Invoice No, Invoice Date, and Supplier Name from the PDF files.
Create directories based on the year and month from the invoice date.
Copy the PDFs into the corresponding year and month folder, renaming them based on the Invoice No and Supplier Name.
Notes:
The .env file must contain the OpenAI API key as openaiprem for text extraction to work.
Ensure that the PDFs in the folder follow the expected format for the tool to extract details successfully.

