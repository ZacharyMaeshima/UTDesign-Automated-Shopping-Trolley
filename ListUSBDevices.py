#!/usr/bin/python
import evdev

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

for device in devices:
    print(device.path, device.name, device.phys)
    
# Look for the device that is named something weird like "Info..."
# That is the barcode scanner. Write that name into variable <barcodeDeviceName>
# in BarcodeScanner.py and BarcodeScanner-noDB.py