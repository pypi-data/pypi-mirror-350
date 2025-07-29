import os
import base64
import re
import argparse
import shutil
import json
import time
import random
import boto3
from dotenv import load_dotenv
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
from datetime import datetime
from pathlib import Path

load_dotenv()
success_count = [0]  
error_count = [0]
full = []


bedrock_client = boto3.client("bedrock-runtime", region_name="ap-south-1")

def encode_image(image_path):
    """Encodes image to base64 format"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
        
    except Exception as e:
        print(f"❌ Error encoding image {image_path}: {str(e)}")
        return None

def convert_pdf_to_image(pdf_path, output_folder="temp"):
    """Converts the first two pages of a PDF into images"""
    
    os.makedirs(output_folder, exist_ok=True)
    global success_count, error_count
    global full
    
    try:
        pdf_reader = PdfReader(pdf_path)
        num_pages = len(pdf_reader.pages)
        

    except Exception as e:
        print(f"❌ Error reading PDF {pdf_path}: {str(e)}")
        return pdf_path

    try:
        
        images = convert_from_path(pdf_path, first_page=1, last_page=min(1, num_pages), dpi=300, thread_count=1)
        
        if not images:
            raise ValueError("No images generated")
        
        image_path = os.path.join(output_folder, os.path.basename(pdf_path).replace(".pdf", ".jpg"))
        images[0].save(image_path, "JPEG")
        
        return image_path
    
    except Exception as e:
        print(f"❌ Error converting {pdf_path} to images: {str(e)}")
        return None

def call_bedrock_api(image_path, invoice_number, party_name):
    """Calls the Bedrock API to extract invoice details from image"""

    base64_image = encode_image(image_path)
    
    if not base64_image:
        return None
    # print(f"Calling Bedrock API with image")
    
    prompt = (
        "You are an extremely strict and efficient Invoice Details Extractor. "
        "You will receive an image of an invoice. Your task is to extract exactly three fields: "
        
        "1. 'Invoice No' – Extract the invoice number using the command-line argument '" + invoice_number + "'. "
        "Search the PDF for the exact label '" + invoice_number + "' (case-insensitive). "
        "If found, extract the contiguous alphanumeric sequence that immediately follows '" + invoice_number + "'. "
        "Return that extracted sequence as the invoice number and STOP; do NOT apply any fallback rules. "
        "If the '" + party_name + "' is 'Platinum Industries Pvt Ltd' then the invoice number in the PDF will begin with 'Invoice No. PIPL.'"

        "If '" + invoice_number + "' is not found or has no following sequence, apply the fallback rules: "
        "  a. Search for 'Vch No.' and 'CIN No.' in the PDF. "
        "     - If only one is present, extract the number immediately following it. "
        "     - If both are present, extract the text that appears after 'Vch No.' and before 'CIN No.'. "
        "  b. If neither 'Vch No.' nor 'CIN No.' is found, search for 'Invoice No' and extract the number immediately following it. "
        "     - Invoice numbers often start with prefixes like 'CIL' or 'SRN'. "
        "     - Do NOT include any part that comes after a 'CIN No.' label. "

        "Examples of use: "
        "  - With invoice_number=\"CIN No\" → look for 'CIN No' first; if found, extract what follows. "
        "  - With invoice_number=\"Vch No\" or invoice_number=\"Invoice No\" → look for those labels accordingly. "
        "  - With invoice_number=\"Bill ID\" (or any other string) → look for 'Bill ID' first; if not found, fall back to the rules above. "
        ""

      """2. 'Invoice Dt' - Extract the invoice date only in the DD.MM.YYYY format The invoice date is usually preceded by the text 'Invoice Dt:', 'BILL.Date:', or similar variations. Extract the date that follows these keywords, ensuring you capture it accurately regardless of formatting or spacing. If multiple dates are present, prioritize the one closest to these keywords. Make sure to follow these rules: 
            - If the date is in DD/MM/YYYY format, convert it to DD.MM.YYYY. Add 20 before the year if it is in YY format.
            - If the year is in two-digit format (YY), assume it belongs to the 21st century (i.e., convert 'XX' to '20XX') explicitly convert it 
            - Always return the date as DD.MM.YYYY.
            - Make sure that the date is always in the format DD.MM.YYYY, and year is always in 4 digit format."""
        
      "3. 'Supplier Name' - The supplier's name must NEVER be '" + party_name + "'. "
        "If you encounter this name, immediately discard it and do NOT consider it as the supplier. "
        "Instead, look for another supplier name, which is typically found after labels such as 'Bill to:', 'Party:', 'Ship to:', or similar keywords. "
        "Ensure that the extracted supplier name is DISTINCT from '" + party_name + "' in every possible way, meaning: "
        "- It must NOT be a variation of '" + party_name + "' (for example with extra spaces, abbreviations, missing dots, or different punctuations). "
        "- It must NOT contain '" + party_name + "' as a substring or in any modified form. "
        "- It must NOT include any additional suffixes or prefixes that could make it seem different while still referring to '" + party_name + "'. "
        "If multiple supplier names are found, choose the most relevant one that is completely unrelated to '" + party_name + "'. "
        "Strictly ensure that the extracted supplier name is a proper business entity and NOT an address, description, or unrelated text. "
        "STOP extracting the name as soon as you encounter words like 'FLOOR', 'BUILDING', 'STREET', or other address-related terms to prevent errors."
       """for the 'Supplier Name' Extract only the party name that comes after Buyer (Bill to) Name from the invoice for the supplier's name in case both Buyer (Bill to) and Consignee (Ship to) exists in the pdf . - Ignore the Consignee (Ship to) section completely and ensure that you do not make the suppliers name as the name that comes near Consignee(Ship to) .  - Return only the name that is next to Buyer (Bill to) as the 'Supplier Name' name as it appears in the pdf image of the invoice.  
        - Ignore the following names and dont ever consider them to be the supplier name if they appear in the invoice, as they are NOT the supplier's name: 
           - SHAGUN GOLD 
           - JEWELLERS PRIVATE LIMITED 
           - M.V.S JEWELLERS PRIVATE LIMITED
           - SM GOLD 
           - TRISHUL JEWELLERS 
           - BAPON ROY 
           - SHUBH ORNAMENTS 
           - V P JEWELLERS 
           - SHREE NAKODA CREATION 
        - If any of these names are encountered,do not extract them nor consider them as the supplier's name. Instead, proceed further in the invoice image to locate the actual "Buyer (Bill to)" name which will be the supplier name. 
        - Strictly ignore the "Consignee (Ship to)" section and the party name that comes after 'Consignee (Ship to)' 
        - Consider the Buyer Name as the supplier name, not the Consignee Name as the supplier name
        - Return only the exact party name next to Buyer (Bill to) as written in the invoice sometimes the Buyer (Bill to) section is cramped up or sometimes it is really small pay utmost attention to extraction and ensure that you can correctly extract the party name that comes after Buyer(Bill to) as the 'Supplier Name'.   
           """  

        "Follow these rules strictly:\n"
        "- Output only a JSON object with exactly three keys: 'Invoice No', 'Invoice Dt', and 'Supplier Name'.\n"
        "- Do not include any additional text, explanations, or keys.\n"
        "- Strictly Make sure that you don't add the address in the 'Supplier Name'. It usually starts with FLOOR or FLOOR2 or FLOOR3 strictly make sure u stop extracting 'Supplier Name ' once u encounter these words\n"
        "- Strictly make sure that the 'Invoice No' always starts with actual invoice number and not anything else the actual 'Invoice no' is usually appended by Invoice No: "
        "-Always keep the 'Supplier Name' in capital letters even if it was extracted in small letters"
        "- If any required field is missing or uncertain, return an empty JSON object {}.\n"
        "Respond only with the JSON object without any markdown formatting or extra text."
    )



    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": base64_image}},
                    {"type": "text", "text": prompt}
                ]
            }
        ]
    }

    #print("payload: ", payload)
    
    retries = 3

    for attempt in range(retries):

        try:

            response = bedrock_client.invoke_model(
                modelId="anthropic.claude-3-haiku-20240307-v1:0",
                contentType="application/json",
                accept="application/json",
                body=json.dumps(payload)
            )

            response_body = json.loads(response["body"].read())

            #print("LLM response: ", response_body["usage"]["input_tokens"])
            #print("LLM response: ", response_body["usage"]["output_tokens"])
            #print("LLM response: ", response_body["usage"])
            #print("LLM response: ", response_body)

            return response_body["content"][0]["text"]
        
        except Exception as e:

            print(f"⚠️ Bedrock API error: {str(e)}. Retrying ({attempt+1}/{retries})...")
            time.sleep(2 ** attempt + random.uniform(0, 1))

    return None

def extract_invoice_details(extracted_text):
    """Extracts invoice details from JSON response"""
    try:
        
        data = json.loads(extracted_text)

        if not all(key in data for key in ["Invoice No", "Invoice Dt", "Supplier Name"]):
            return {}
        #print("Extracted data: ", data)
        
        return data
    
    except:
        return {}

def get_year_and_month(invoice_date):
    """Extracts year and month from the invoice date"""

    #print("Extracting year and month from invoice date: ", invoice_date)
    
    try:
        date_obj = datetime.strptime(invoice_date.strip(), "%d.%m.%Y")
        # print("Parsed date: ", date_obj)
        return date_obj.year, date_obj.strftime("%B").upper()

    except:
        return None, None

def sanitize_filename(filename):

    invalid_chars = r'[<>:"/\\|?*]'
    filename = re.sub(invalid_chars, ' ', filename)
    filename = re.sub(r'([a-z])([A-Z])', r'\1 \2', filename)

    #if filename.startswith BUYER then remove the BUYER 
    if filename.startswith("BUYER"):
        filename = filename[6:]
    # filename = filename.replace('-', ' ')
    
    return ' '.join(filename.split()).strip()

def process_subfolder(subfolder_path, invoice_number, party_name):
    """Processes all PDFs in a given subfolder"""

    pdf_files = [f for f in os.listdir(subfolder_path) if f.lower().endswith(".pdf")]
    print(f"🔍 Processing {len(pdf_files)} PDFs in {subfolder_path}...")

    error_pdfs = []
    global full, success_count, error_count

    for pdf_file in pdf_files:

        pdf_path = os.path.join(subfolder_path, pdf_file)
        try:

            # print('pdf path:',pdf_path)
            # Convert PDF to image
            image_path = convert_pdf_to_image(pdf_path)
            error_pdfs.append(image_path)
            # print("Error PDFs: ", error_pdfs)
        
            extracted_text = call_bedrock_api(image_path,invoice_number,party_name) if image_path else None
            invoice_details = extract_invoice_details(extracted_text) if extracted_text else {}

            # Extract invoice details
            invoice_no = invoice_details.get("Invoice No", "ERROR")
            invoice_dt = invoice_details.get("Invoice Dt", "01.01.2000")
            # if two digits are only present, convert to 4 digits
            if len(invoice_dt.split(".")[-1]) == 2:
                #print("Invoice Date: ", invoice_dt)
                invoice_dt = invoice_dt[:-2] + "20" + invoice_dt[-2:]
          
            supplier_name = invoice_details.get("Supplier Name", "ERROR")
            
            # Format extracted details  
            formatted_invoice_no = sanitize_filename(invoice_no.replace("/", "-").replace('"', '').replace(',', ''))

            #if formatted_invoice_no has CLI or GIL as first 3 characters then convert to 'CIL'
            if formatted_invoice_no[:3] == 'CLI' or formatted_invoice_no[:3] == 'GIL'  or formatted_invoice_no[:3] == 'CIN':
                formatted_invoice_no = 'CIL' + formatted_invoice_no[3:]
            
            #ensure that after the first 3 characters, there is a - character in the invoice number
            # if '-' not in formatted_invoice_no[3:]:
            #     formatted_invoice_no = formatted_invoice_no[:3] + '-' + formatted_invoice_no[3:]   
            
            #ensure that in the invoice number wherever there is 24-25 or any other sequence of number usually in '2X 2X' format make them '2X-2X'
            formatted_invoice_no = re.sub(r'\b(2\d)\s(2\d)\b', r'\1-\2', formatted_invoice_no)
            formatted_supplier = sanitize_filename(supplier_name)
            formatted_supplier = re.sub(r'^\b(Ms|Mr|M\.S|M\.R|M\s*S|M\s*R)\s*\.?\s*', '', formatted_supplier, flags=re.IGNORECASE)


            # Ensure filenames are within OS limits (truncate long supplier names)
            if len(formatted_supplier) > 50:
                formatted_supplier = formatted_supplier[:50]  # Trim to 50 characters

            # Extract year and month
            year, month = get_year_and_month(invoice_dt)
            # print("Year: ", year)
            # print("Month: ", month)
            if not year:
                year = 2000
            if not month:
                month = "UNKNOWN"

            # Define output paths
            output_parent_dir = os.path.join(subfolder_path, "Named")
            os.makedirs(output_parent_dir, exist_ok=True)

            output_dir = os.path.join(output_parent_dir, str(year), month)
            os.makedirs(output_dir, exist_ok=True)

            # Define new PDF file name
            # new_file_name = f"{formatted_invoice_no} {formatted_supplier}.pdf" if "ERROR" not in formatted_invoice_no else "error.pdf"
            # new_pdf_path = os.path.join(output_dir, new_file_name)
           
            base_name = f"{formatted_invoice_no} {formatted_supplier}"
            new_file_name = f"{base_name}.pdf"
            new_pdf_path = os.path.join(output_dir, new_file_name)

            # Check for duplicates and rename if needed
            counter = 1

            while os.path.exists(new_pdf_path):
                new_file_name = f"{base_name} ({counter}).pdf"
                new_pdf_path = os.path.join(output_dir, new_file_name)
                counter += 1

            # Copy original PDF to the new location
            shutil.copy(pdf_path, new_pdf_path)
            print(f"📂 Saved as {new_file_name} in {output_dir}")
            # success_count[0] += 1

            if "ERROR" in new_file_name:
                error_count[0] += 1  # Increment error count
                full.append(pdf_path) 
            
            else:
                success_count[0] += 1    

            # Cleanup temporary image file
            if image_path:
                os.remove(image_path)
                

        except Exception as e:

            print(f"❌ Error processing {pdf_file}: {str(e)}")
            
            # Log the error
            # with open("error_log.txt", "a") as log_file:
            with open("error_log.txt", "a", newline="") as log_file:

                log_file.write(f"{pdf_file}: {str(e)}\n")
            # error_count[0] += 1
            # Ensure the error file is saved no matter what
            year, month = 2000, "UNKNOWN"
            output_parent_dir = os.path.join(subfolder_path, "Named")
           
            os.makedirs(output_parent_dir, exist_ok=True)
            # output_dir = os.path.join(output_parent_dir, str(year), month)

            output_dir = Path(output_parent_dir) / str(year) / month
            output_dir.mkdir(parents=True, exist_ok=True)  # Ensures directory creation

            os.makedirs(output_dir, exist_ok=True)

            # Generate unique error filename to prevent overwriting
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            error_pdf_path = os.path.join(output_dir, f"error_{timestamp}.pdf")

            try:

                shutil.copy(pdf_path, error_pdf_path)
                print(f"⚠️ Error file saved as {error_pdf_path}")
                full.append(pdf_file)
                error_count[0] += 1

            except Exception as e:

                print(f"❌ Failed to save error file for {pdf_file}: {str(e)}")
                full.append(pdf_file)
                error_count[0] += 1


def process_main_folder(main_folder, invoice_number,party_name):
    """Processes all subfolders in the main folder"""

    global full 
    global success_count, error_count

    start_time = time.time()
    subfolders = [os.path.join(main_folder, f) for f in os.listdir(main_folder) if os.path.isdir(os.path.join(main_folder, f))]

    for subfolder in subfolders:
        # print("hello")
        print(f"📂 Processing subfolder: {subfolder}")
        process_subfolder(subfolder, invoice_number,party_name)

    end_time = time.time()
    total_time = end_time - start_time

    print(f"⏳ Total time taken: {total_time:.2f} seconds")    
    print("Processing complete.")
    print(f"✅ Total Successfully Processed PDFs: {success_count[0]}")
    print(f"❌ Total PDFs with Errors: {error_count[0]}")
    print("All PDFs with errors: ", full)

def main():

    parser = argparse.ArgumentParser(description="Extract invoice details from PDFs and organize them.")
    parser.add_argument("main_folder", type=str, nargs="?", default=os.getcwd(), help="Main folder containing subfolders with PDFs")
    parser.add_argument("invoice_number", type=str, nargs="?", default=None, help="Optional invoice number argument")
    parser.add_argument("party_name", type=str, nargs="?", default=None, help="Optional party name argument")
    args = parser.parse_args()

    process_main_folder(args.main_folder, args.invoice_number ,args.party_name)

if __name__ == "__main__":
    main()
