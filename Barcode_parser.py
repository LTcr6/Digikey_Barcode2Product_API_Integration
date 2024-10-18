# Purpose:
# Receive a string from a Digikey barcode and change it into something that can be appended to a HTTPS address and then feed into the Digikey barcode 2 product API
# Digikey Barcode2Product API: https://developer.digikey.com/products/barcode/barcoding/product2dbarcode
#
# Credit to:
# Repo where the original implementation of this idea and most of the parsing comes from: https://github.com/alvarop/dkbc/tree/master
#

import urllib.parse
import argparse

def  main():

        parser = argparse.ArgumentParser()
        parser.add_argument("--outfile", help="CSV output file")
        parser.add_argument("--batch", action="store_true", help="Batch scan")
        parser.add_argument("--debug", action="store_true", help="Debug mode")

        parser.add_argument("--rs", help='Record separator. Default "{RS}"', default="{RS}")
        parser.add_argument("--gs", help='Group separator. Default "{GS}"', default="{GS}")
        parser.add_argument(
        "--eot", help='End of transmission. Default "{EOT}"', default="{EOT}"
        )
        
        barcode = input("Scan barcode:")
        args = parser.parse_args()

        barcode = barcode.replace(args.rs, "\x1e")
        barcode = barcode.replace(args.gs, "\x1d")
        barcode = barcode.replace(args.eot, "\x04")
        print(urllib.parse.quote(barcode, safe=''))

main()