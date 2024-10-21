# Purpose:
# Receive a string from a Digikey barcode and change it into something that can be appended to a HTTPS address and then feed into the Digikey barcode 2 product API
# Digikey Barcode2Product API: https://developer.digikey.com/products/barcode/barcoding/product2dbarcode
#
# Credit to:
# Repo where the original implementation of this idea and most of the parsing comes from: https://github.com/alvarop/dkbc/tree/master
#
#------------------------------------------------------------------------------------------------------------------------------------------------------------------
import urllib.parse
import argparse
import os
import requests
#------------------------------------------------------------------------------------------------------------------------------------------------------------------
def  Barcode_Parser(Barcode_List):

        #barcode = input('Scan barcode:')
        URLizedBarcode = []  
        
        for barcode in Barcode_List:
                
                parser = argparse.ArgumentParser()
                parser.add_argument("--outfile", help='CSV output file')
                parser.add_argument("--batch", action='store_true', help='Batch scan')
                parser.add_argument("--debug", action='store_true', help='Debug mode')
                parser.add_argument("--rs", help='Record separator. Default "{RS}"', default="{RS}")
                parser.add_argument("--gs", help='Group separator. Default "{GS}"', default="{GS}")
                parser.add_argument("--eot", help='End of transmission. Default "{EOT}"', default="{EOT}")
                args = parser.parse_args()

                barcode = barcode.replace(args.rs,  '\x1e') 
                barcode = barcode.replace(args.gs,  '\x1d') 
                barcode = barcode.replace(args.eot, '\x04')

                URLizedBarcode.append(urllib.parse.quote(barcode, safe='')) 

        return URLizedBarcode
#------------------------------------------------------------------------------------------------------------------------------------------------------------------
def line_reader(filepath):

        with open(filepath) as f:
                Barcode_List = f.readlines()

        return Barcode_List
#------------------------------------------------------------------------------------------------------------------------------------------------------------------
def make_and_send_cURL_Command(URLizedBarcode):

        Client_ID = 'Put a value or linked variable here'#To-do make me a variable
        Auth_Token = 'Put a value or linked variable here'   #To-do make me a variable
        url = 'https://api.digikey.com/Barcoding/v3/Product2DBarcodes/' + URLizedBarcode[0]
        headers = {
        'accept': 'application/json',
        "content-type": "application/json",
        'Authorization': 'Bearer ' + Auth_Token,
        'x-DIGIKEY-client-id': Client_ID,
        }


        response = requests.get(url, headers=headers)
        print(response.json)
        print('\n')
        # Check if the response contains valid JSON
        try:
                json_response = response.json()  # Parse JSON from the response
                print("JSON Response:", json_response)  # Print the parsed JSON response
                print('\n')
        except ValueError:
                print("Response is not in JSON format")

                # Construct the equivalent cURL command
        
        cURL_Command = f"curl -X GET '{url}' " + " ".join([f"-H '{k}: {v}'" for k, v in headers.items()])
        return cURL_Command
#------------------------------------------------------------------------------------------------------------------------------------------------------------------
filepath = os.path.join('Part_Barcode_CSVs', 'Tapes_2.csv')
Barcode_List = line_reader(filepath)

URLizedBarcode = Barcode_Parser(Barcode_List)
#print(URLizedBarcode)
#print('\n')

cURL_Command = make_and_send_cURL_Command(URLizedBarcode)
#print(cURL_Command)
#print('\n')