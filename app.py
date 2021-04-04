from flask import Flask, redirect, url_for, render_template, request
import BarcodeScanner

app = Flask(__name__)


@app.route("/", methods = ["POST", "GET"])
def home:
    return render_template("index.html")


@app.route("/scan", methods = ["POST", "GET"])
def scan():
    return render_template("grid-barcode.html")

@app.route("/getbarcode", methods = ["GET"])
def getBarcode():
    return BarcodeScanner.UPC_lookup(BarcodeScanner.barcode_reader())