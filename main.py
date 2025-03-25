from flask import Flask, render_template, redirect, request
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

# Configure the SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Avoids warnings
db.init_app(app)

# database
class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    phonenumber: Mapped[int] = mapped_column(Integer, nullable=False)

with app.app_context():
    db.create_all()

# ------------------------------------------------------------------

# this clears/deletes everything from the users table
with app.app_context():
    db.session.query(User).delete()
    db.session.commit()

# ------------------------------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        users = db.session.execute(db.select(User)).scalars().all()
        return render_template("index.html", users=users)
    else:
        user = User(
            name=request.form["name"], 
            email=request.form["email"], 
            phonenumber=request.form["phonenumber"]  # Corrected field name
        )
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    
# -------------
        
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_user(id):
    user = db.session.get(User, id)
    if not user:
        return "User not found", 404
    
    if request.method == "POST":
        user.name = request.form["name"]
        user.email = request.form["email"]
        user.phonenumber = request.form["phonenumber"]
        
        db.session.commit()
        return redirect("/")
    
    return render_template("index.html", user=user)

# ------------------------------------------------------------------------------------------


if __name__ == '__main__': 
    app.run(debug=True)

    



