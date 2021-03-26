#!/usr/bin/python
import sys
import boto3

tableName = "AutomatedShoppingTrolleyDB"
primaryColumn = "UPC"
REGION = "us-east-1"
# ACCESS_KEY, SECRET_KEY, AND TOKEN have to be replaced every 3 hours (limitation of AWS student account)
ACCESS_KEY = "blah"
SECRET_KEY = "blah"
TOKEN = "blah"

def barcode_reader():
    """Barcode code obtained from 'brechmos' 
    https://www.raspberrypi.org/forums/viewtopic.php?f=45&t=55100"""
    hid = {4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm',
           17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y',
           29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ',
           45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';', 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'}

    hid2 = {4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M',
            17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y',
            29: 'Z', 30: '!', 31: '@', 32: '#', 33: '$', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(', 39: ')', 44: ' ',
            45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':', 52: '"', 53: '~', 54: '<', 55: '>', 56: '?'}

    fp = open('/dev/hidraw0', 'rb')

    ss = ""
    shift = False

    done = False

    while not done:

        ## Get the character from the HID
        buffer = fp.read(8)
        for c in buffer:
            if c > 0:

                ##  40 is carriage return which signifies
                ##  we are done looking for characters
                if int(c) == 40:
                    done = True
                    break;

                ##  If we are shifted then we have to
                ##  use the hid2 characters.
                if shift:

                    ## If it is a '2' then it is the shift key
                    if int(c) == 2:
                        shift = True

                    ## if not a 2 then lookup the mapping
                    else:
                        ss += hid2[int(ord(c))]
                        shift = False

                ##  If we are not shifted then use
                ##  the hid characters

                else:

                    ## If it is a '2' then it is the shift key
                    if int(c)== 2:
                        shift = True

                    ## if not a 2 then lookup the mapping
                    else:
                        ss += hid[int(c)]
    return ss

def UPC_lookup(upc):
    db = boto3.resource('dynamodb',
                        aws_access_key_id = ACCESS_KEY,
                        aws_secret_access_key = SECRET_KEY,
                        aws_session_token = TOKEN,
                        region_name = REGION)
    table = db.Table(tableName)
    try :
        response = table.get_item(
            Key = {
                primaryColumn: upc
                })
        
        response = response['Item']
        formattedResponse = {
            "ItemName": response['ItemName'],
            "ItemPrice": float(response['ItemPrice']),
            "ItemTaxable": response['ItemTaxable'],
            "ItemWeight": float(response['ItemWeight'])}
    
        print("-----" * 5)
        print(upc)
        print(formattedResponse)
        print("-----" * 5 + "\n")
        # return upc
        return formattedResponse
    
    except:
            print("Failed to get item from the DynamoDB Table")
            return "error"

if __name__ == '__main__':
    try:
        while True:
            UPC_lookup(barcode_reader())
    except KeyboardInterrupt:
        pass

