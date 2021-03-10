from flask import Flask, redirect, url_for, render_template, request
import BarcodeScanner

app = Flask(__name__)
api_key = "4CB6DEC567087909E1D57FBB985995D8"

@app.route("/", methods = ["POST", "GET"])
def home():
    return render_template("grid-barcode.html")

@app.route("/getbarcode", methods = ["GET"])
def getBarcode():
    return BarcodeScanner.UPC_lookup(api_key,BarcodeScanner.barcode_reader())