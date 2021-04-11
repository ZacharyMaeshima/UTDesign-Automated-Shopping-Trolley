#!/usr/bin/python
import sys
import evdev


keys = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
}

table = [
    {
        "UPC": "037000962564",
        "ItemName": "Febreeze Air Freshener (Linen & Sky)",
        "ItemPrice": 3.49,
        "ItemTaxable": True,
        "ItemWeight": 250
    },
    {
        "UPC": "022592007014",
        "ItemName": "Ozarka Water Bottle (16.9 FL Oz)",
        "ItemPrice": 0.99,
        "ItemTaxable": False,
        "ItemWeight": 150
    },
    {
        "UPC": "038000138430",
        "ItemName": "Pringles (Sour Cream & Onion)",
        "ItemPrice": 1.99,
        "ItemTaxable": False,
        "ItemWeight": 150
    },
    {
        "UPC": "788521500109",
        "ItemName": "Hand Santizer",
        "ItemPrice": 3.99,
        "ItemTaxable": True,
        "ItemWeight": 600
    }
]

barcodeDeviceName = ""
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
                    barcode = barcode + str(keys[data.scancode])
                    singleKey = 1
                else:
                    singleKey = 0
    print("Barcode: " + barcode)
    return barcode



def UPC_lookup(upc):
    try :
        response = "error"
        for item in table:
            if item['UPC'] == upc:
                response = item
    
        print("-----" * 5)
        print(response)
        print("-----" * 5 + "\n")
        return response
    
    except:
            print("Error")
            return "error"

# Looks for device path when imported
findBarcodeInputDevice()



if __name__ == '__main__':
    try:
        while True:
            UPC_lookup(barcode_reader())
    except KeyboardInterrupt:
        pass

