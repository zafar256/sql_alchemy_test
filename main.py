from flask import Flask, render_template, redirect, request

app = Flask(__name__)


@app.route("/", methods = ["GET", "POST"])
def home():

    if request.method == "GET":
        cur.execute("select * from testform;")
        mytestform = cur.fetchall()
        return render_template("index.html", mytestform=mytestform)
    else:
        name = request.form["name"]
        email = request.form["email"]
        phonenumber = request.form["phonenumber"]

        queryinsert = "insert into testform(name,email,phonenumber)"\
            "values('{}','{}',{})".format(name,
                                           email, phonenumber)
        

        cur.execute(queryinsert)
        conn.commit()
        return redirect('/')  
    

if __name__ == '__main__': 
    app.run(debug=True)