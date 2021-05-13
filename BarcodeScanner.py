#!/usr/bin/python
import sys
import boto3
import evdev

tableName = "AutomatedShoppingTrolleyDB"
primaryColumn = "UPC"
REGION = "us-east-1"
# ACCESS_KEY, SECRET_KEY, AND TOKEN have to be replaced every 3 hours (limitation of AWS student account)
ACCESS_KEY = "blah"
SECRET_KEY = "blah"
TOKEN = "blah"

keys = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
}

barcodeDeviceName = "Logic Scanner"
barcodeDevicePath = ""

def findBarcodeInputDevice():
    devices = map(InputDevice, list_devices())
    for device in devices:
        if device.name == barcodeDeviceName:
            barcodeDevicePath = device.path
            return True
    return False

def barcode_reader():
    # dev = evdev.InputDevice('/dev/input/event2')
    dev = evdev.InputDevice(barcodeDevicePath)
    # print(dev)
    singleKey = 0
    barcode = ''
    while(len(barcode) < 12):
        event = dev.read_one()
        if event is not None:
            data = evdev.categorize(event)
            if event.type == evdev.ecodes.EV_KEY:
                if data.scancode == 28:
                    dev.close()
                    break
                if singleKey == 0:
                    # print("Scan code: " + str(data.scancode))
                    # print("Key: " + str(keys[data.scancode]))
                    barcode = barcode + str(keys[data.scancode])
                    singleKey = 1
                else:
                    singleKey = 0
    print("Barcode: " + barcode)
    return barcode


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
        print(formattedResponse)
        print("-----" * 5 + "\n")
        # return upc
        return formattedResponse
    
    except:
            print("Failed to get item from the DynamoDB Table")
            return "error"

# Looks for device path when imported
findBarcodeInputDevice()

if __name__ == '__main__':
    try:
        while True:
            UPC_lookup(barcode_reader())
    except KeyboardInterrupt:
        pass

