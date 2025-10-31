from flask import Blueprint, request, render_template
from models import db, stockOrder
from services.ocr_parser import parse_ocr_text
from datetime import date, datetime, timezone

stock_orders_bp = Blueprint('stockOrders', __name__ )

@stock_orders_bp.route("/add-stock-orders", methods = ["GET", "POST"])
def add_stock_order():
    if request.method == "POST":
        #generate id
        today_str = date.today().strftime("%m%d%Y")
        orders_today = stock_orders_bp.query.filter_by(order_date=date.today()).count()+1
        id = f"S{today_str}-{orders_today:03d}"

        brand = request.form["brand"]
        power = request.form["power"]
        cylinder = request.form["cylinder"]
        axis = request.form["axis"]
        add = request.form["add"]
        bc = request.form["bc"]

 
    return render_template("stockOrderForm.html")