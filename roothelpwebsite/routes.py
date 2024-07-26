from roothelpwebsite import app
from flask import  render_template, url_for, request, flash, redirect

@app.route("/")
@app.route("/home")
def home():
    return render_template('Layout.html')