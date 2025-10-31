from flask import Blueprint, request, redirect, render_template, url_for, flash
from models import db, PatientOrder, Patient, Doctor, Logs
from datetime import date, datetime, timezone
from sqlalchemy.exc import IntegrityError, OperationalError


pt_orders_bp = Blueprint('ptOrders', __name__)


# Route to handle the form submission
@pt_orders_bp.route("/add_patient_order", methods=["GET", "POST"])
def add_patient_order():
    if request.method == "POST":
        #generate ID
        today_str = date.today().strftime("%m%d%Y")
        orders_today = PatientOrder.query.filter_by(order_date=date.today()).count()+1
        #P10142025-001
        oid = f"P{today_str}-{orders_today:03d}"

        #Create better error handling here
        # ISSUES: If no cyl or axis, it will throw error. 
        # Consider limiting values based off brand or type of lens
        patient_name = request.form["patient_name"]
        patient_dob = datetime.strptime(request.form["dob"], "%Y-%m-%d").date()
        doctor_name = request.form["doctor"]
        brand = request.form["brand"]
        notes = request.form.get("notes", None)
        order_date = datetime.now(timezone.utc).date()
        
        try: 
            power = float(request.form["power"])
            axis = int(request.form.get("axis", None))
            cyl = float(request.form.get("cylinder", None))
            add = float(request.form.get("add", None))
            bc = float(request.form["base_curve"])
            diameter = float(request.form["diameter"])
            quantity = int(request.form.get("quantity", None))
        except ValueError:
            return "Invalid input. Please check your data and try again.", 400
        
        # 1. Check if patient exists, else create
        patient = Patient.query.filter_by(name=patient_name, date_of_birth=patient_dob).first()
        if not patient:
            patient = Patient(name=patient_name, date_of_birth=patient_dob)
            db.session.add(patient)
            db.session.commit()  # Assigns an id without committing
        
        # Check doctor exists
        doctor = Doctor.query.filter_by(name=doctor_name).first()
        if not doctor:
            doctor = Doctor(name=doctor_name)
            db.session.add(patient)
            db.session.commit()


        # create new pt order in order table
        new_order = PatientOrder(id = oid,
                                patient = patient,
                                doctor = doctor,
                                order_date=order_date,
                                brand=brand, 
                                power=power,
                                axis=axis,
                                add = add,
                                cylinder=cyl,
                                bc=bc,
                                diameter=diameter,
                                quantity=quantity,
                                notes=notes
                                )
        
        try:
            db.session.add(new_order)
            db.session.commit()
            flash("Order was added successfully", "Success")
        except IntegrityError:
            db.session.rollback()
            flash("Order not added. Order ID already exists.", "Error")
        except OperationalError:
            db.session.rollback()
            flash("Database connection failed!", "Error")

        total_logs = Logs.query.filter_by(order_id =oid).count()+1
        log_id = f"{oid}-{total_logs:03d}"
        action = f"Order created"
        order = new_order

        new_log = Logs(id = log_id,
                       action = action,
                       order = order)
        db.session.add(new_log)
        db.session.commit()
        

        # Redirect to the orders page
        return redirect(url_for('ptOrders.get_patient_orders'))
    return render_template("ptOrderForm.html")

@pt_orders_bp.route("/pt-orders",methods=["GET"])
def get_patient_orders():
    orders = PatientOrder.query.order_by(PatientOrder.order_date.desc()).all()
    return render_template("orders.html", orders=orders) 


@pt_orders_bp.route("/pt-orders/<order_id>/remove", methods = ["POST"])
def remove_pt_order(order_id):
    order = PatientOrder.query.get(order_id)
    orders = PatientOrder.query.order_by(PatientOrder.order_date.desc()).all()

    if not order:
        flash("Order not found", "Error")
        return render_template("orders.html", orders = orders)
    else:
        #Remove order from order list
        db.session.delete(order)
        db.session.commit()
        return render_template("orders.html", orders = orders)
    
@pt_orders_bp.route("/pt-orders/<order_id>/more-info", methods = ["GET"])
def order_info(order_id):
    order = PatientOrder.query.get(order_id)
    orders = PatientOrder.query.order_by(PatientOrder.order_date.desc()).all()

    if not order:
        flash("Order not found", "Error")
        return render_template("orders.html", orders = orders)
    else:
        return render_template("order-info.html", order = order)

@pt_orders_bp.route("/pt-orders/<order_id>/change-status", methods=["GET", "POST"])
def change_order_status(order_id):

    if request.method == "POST":
        order = PatientOrder.query.get(order_id)
        orders = PatientOrder.query.order_by(PatientOrder.order_date.desc()).all()
        if not order:
            return render_template("orders.html", orders = orders)
        # Mark order arrived with date
        status = request.form.get("status", None)
        order.order_status = status
        order.arrival_date = datetime.now(timezone.utc).date()
        db.session.commit()

        #Log status change
        total_logs = Logs.query.filter_by(order_id =order_id).count()+1
        log_id = f"{order_id}-{total_logs:03d}"
        action = f"Order status changed to {status}"

        new_log = Logs(id = log_id,
                        action = action,
                        order = order)
        
        db.session.add(new_log)
        db.session.commit() 
    
    return redirect(url_for("ptOrders.order_info", order_id = order_id))





# @pt_orders_bp.route("/pt-orders/<order_id>/update-patient", methods = ["GET", "POST"])
        



    

    


