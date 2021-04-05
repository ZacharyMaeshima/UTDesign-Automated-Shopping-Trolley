from flask import Flask, redirect, url_for, render_template, request
import BarcodeScanner

app = Flask(__name__)


@app.route("/", methods = ["GET", "POST"])
def home():
    return render_template("index.html")


@app.route("/scan", methods = ["GET","POST"])
def scan():
    return render_template("grid-barcode.html")

@app.route("/getbarcode", methods = ["GET"])
def getBarcode():
    return BarcodeScanner.UPC_lookup(BarcodeScanner.barcode_reader())


@app.route("/checkout", methods = ["GET", "POST"])
def checkout():
    return render_template("exit.html")

