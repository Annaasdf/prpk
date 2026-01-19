from flask import Blueprint, render_template, request, redirect
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from database import db
from models import User, Order, Allergy, Review, Product, PurchaseRequest

routes = Blueprint("routes", __name__)

# ---------- Проверка роли ----------
def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect("/login")
            if current_user.role != role:
                return redirect("/login")
            return func(*args, **kwargs)
        return wrapper
    return decorator


# ---------- Регистрация ----------
@routes.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(
            full_name=request.form["name"],
            email=request.form["email"],
            password=generate_password_hash(request.form["password"]),
            role=request.form["role"]
        )
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")


# ---------- Вход ----------
@routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(f"/{user.role}")
    return render_template("login.html")


# ---------- УЧЕНИК ----------
@routes.route("/student", methods=["GET", "POST"])
@login_required
@role_required("student")
def student():
    orders = Order.query.filter_by(student_id=current_user.id).all()
    allergy = Allergy.query.filter_by(student_id=current_user.id).first()

    if request.method == "POST":

        # оплата питания
        if "pay" in request.form:
            order = Order(
                student_id=current_user.id,
                meal_type=request.form["meal"],
                paid=True
            )
            db.session.add(order)

        # аллергии
        if "allergy" in request.form and request.form["allergy"]:
            if allergy:
                allergy.text = request.form["allergy"]
            else:
                db.session.add(Allergy(
                    student_id=current_user.id,
                    text=request.form["allergy"]
                ))

        # отзыв
        if "review" in request.form and request.form["review"]:
            db.session.add(Review(
                student_id=current_user.id,
                text=request.form["review"]
            ))

        db.session.commit()

    return render_template(
        "student.html",
        orders=orders,
        allergy=allergy
    )


# ---------- ПОВАР ----------
@routes.route("/cook", methods=["GET", "POST"])
@login_required
@role_required("cook")
def cook():
    orders = Order.query.filter_by(paid=True, received=False).all()
    products = Product.query.all()

    if request.method == "POST":

        # отметить выданное питание
        if "give" in request.form:
            order = Order.query.get(int(request.form["order_id"]))
            order.received = True

        # заявка на закупку
        if "request" in request.form:
            req = PurchaseRequest(
                cook_id=current_user.id,
                product=request.form["product"],
                quantity=int(request.form["quantity"])
            )
            db.session.add(req)

        db.session.commit()

    return render_template(
        "cook.html",
        orders=orders,
        products=products
    )


# ---------- АДМИНИСТРАТОР ----------
@routes.route("/admin", methods=["GET", "POST"])
@login_required
@role_required("admin")
def admin():
    requests = PurchaseRequest.query.all()
    paid_count = Order.query.filter_by(paid=True).count()
    visited_count = Order.query.filter_by(received=True).count()

    if request.method == "POST":
        req = PurchaseRequest.query.get(int(request.form["id"]))
        req.status = request.form["status"]
        db.session.commit()

    return render_template(
        "admin.html",
        requests=requests,
        paid_count=paid_count,
        visited_count=visited_count
    )


@routes.route("/logout")
def logout():
    logout_user()
    return redirect("/login")
