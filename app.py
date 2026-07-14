from flask import Flask, render_template,request, redirect, url_for
from database import db
print("APP FILE LOADED")
app = Flask(__name__)

# ---------------- Database Configuration ----------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///courier.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "courier123"

# Initialize Database
db.init_app(app)

# Import models AFTER db initialization
from models import User, Shipment
import random

# ---------------- Home Page ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- Register Page ----------------
# ---------------- Register Page ----------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        password = request.form["password"]

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "<h3>Email already exists. Please Login.</h3>"

        # Create new user
        new_user = User(
            name=name,
            email=email,
            mobile=mobile,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

# ---------------- Login Page ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(
            email=email,
            password=password
        ).first()

        if user:
            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid Email or Password!"
        )

    return render_template("login.html")
# ---------------- User Dashboard ----------------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ---------------- Book Shipment ----------------
@app.route("/book", methods=["GET", "POST"])
def book():
    print("BOOK ROUTE EXECUTED")


    if request.method == "POST":

        sender_name = request.form.get("sender_name")
        receiver_name = request.form.get("receiver_name")
        source = request.form.get("source")
        destination = request.form.get("destination")
        weight = float(request.form.get("weight"))

        # Generate Tracking ID
        tracking_id = "TRK" + str(random.randint(100000, 999999))

        shipment = Shipment(
            sender_name=sender_name,
            receiver_name=receiver_name,
            source=source,
            destination=destination,
            weight=weight,
            tracking_id=tracking_id,
            status="Booked"
        )

        db.session.add(shipment)
        db.session.commit()

        return f"""
        <h2>✅ Shipment Booked Successfully!</h2>
        <h3>Your Tracking ID: {tracking_id}</h3>
        <br>
        <a href="/dashboard">Go to Dashboard</a>
        """

    return render_template("book.html")


# ---------------- Track Shipment ----------------
@app.route("/track", methods=["GET", "POST"])
def track():

    if request.method == "POST":

        tracking_id = request.form.get("tracking_id")

        shipment = Shipment.query.filter_by(
            tracking_id=tracking_id
        ).first()

        if shipment:
            return render_template(
                "track.html",
                shipment=shipment
            )

        return render_template(
            "track.html",
            error="Tracking ID not found!"
        )

    return render_template("track.html")


# ---------------- My Shipments ----------------

@app.route("/shipments")
def shipments():

    all_shipments = Shipment.query.all()

    return render_template(
        "shipments.html",
        shipments=all_shipments
    )


@app.route("/admin")
def admin():

    search = request.args.get("search")

    if search:

        shipments = Shipment.query.filter(
            Shipment.tracking_id.contains(search)
        ).all()

    else:

        shipments = Shipment.query.all()

    users = User.query.all()

    return render_template(
        "admin_dashboard.html",
        users=users,
        shipments=shipments
    )
@app.route("/update_status/<int:id>", methods=["POST"])
def update_status(id):

    shipment = Shipment.query.get_or_404(id)

    shipment.status = request.form.get("status")

    db.session.commit()

    return redirect(url_for("admin"))
# ---------------- Delete Shipment ----------------
@app.route("/delete_shipment/<int:id>")
def delete_shipment(id):

    shipment = Shipment.query.get_or_404(id)

    db.session.delete(shipment)
    db.session.commit()

    return redirect(url_for("admin"))
@app.route("/logout")
def logout():
    return redirect(url_for("login"))





# ---------------- Create Database ----------------
with app.app_context():
    db.create_all()



# ---------------- Run Application ----------------
if __name__ == "__main__":
    app.run(debug=True)