import csv
import mimetypes
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import mysql.connector
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "HINDALCO_IT_RPD"

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="it_employee"
)

# CSV FILE
file = "csv/temp.csv"


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/user_login", methods=["POST"])
def user_login():
    return render_template("user/user_login.html")


@app.route("/login_user", methods=["POST"])
def login_user():
    username = request.form.get("username")
    password = request.form.get("password")

    # Username and Password From Database
    mycursor = mydb.cursor()
    sql = "SELECT * FROM user_login WHERE username = %s AND password = %s"
    values = (username, password,)
    mycursor.execute(sql, values)
    myresult = mycursor.fetchone()
    if myresult is not None:
        dbusername = myresult[0]
        dbpassword = myresult[1]

    if myresult == None:
        return render_template("user/user_login.html", message="Wrong E-Mail ID OR Password")

    if username == dbusername and password == dbpassword:
        session['username'] = username
        return render_template("user/user-dashboard.html", username=session['username'])
    else:
        return render_template("user/user_login.html", message="Wrong E-Mail ID OR Password")


@app.route("/admin_login", methods=['POST'])
def admin_login():
    return render_template("admin/admin_login.html")


@app.route("/login_admin", methods=["POST"])
def login_admin():
    username = request.form.get("username")
    password = request.form.get("password")

    # Username and Password From Database
    mycursor = mydb.cursor()
    sql = "SELECT it_employee.admin.username, it_employee.user_login.password FROM it_employee.admin, it_employee.user_login WHERE admin.username = user_login.username AND admin.username = %s AND user_login.password = %s;"
    values = (username, password,)
    mycursor.execute(sql, values)
    myresult = mycursor.fetchone()
    if myresult != None:
        dbusername = myresult[0]
        dbpassword = myresult[1]

    if username == "admin" and password == "admin":
        session['username'] = username
        return render_template("admin/admin-dashboard.html", username=session['username'])

    if myresult == None:
        return render_template("admin/admin_login.html", message="Wrong Admin ID OR Password")

    if username == dbusername and password == dbpassword:
        session['username'] = username
        return render_template("admin/depart_admin_dashboard.html", username=session['username'])
    else:
        return render_template("admin/admin_login.html", message="Wrong E-Mail ID OR Password")


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    return render_template("index.html")


@app.route("/depart_add_user", methods=["POST"])
def depart_add_user():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT username FROM user_login")
    myresult = mycursor.fetchall()
    users = []
    for x in myresult:
        users.append(x[0])

    mycursor = mydb.cursor()
    sql = "SELECT * FROM user WHERE owner = %s;"
    val = (session["username"],)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    exists = []
    for x in myresult:
        exists.append(x[1])

    return render_template("admin/depart_add_user.html", username=session['username'],
                           users=users, exists=exists)


@app.route("/depart_add_user_list", methods=["POST"])
def depart_add_user_list():
    owner = session["username"]
    user = request.form.get("user")
    # print(owner, user)

    mycursor = mydb.cursor()
    sql = "SELECT * FROM user WHERE owner = %s AND username = %s;"
    values = (owner, user,)
    mycursor.execute(sql, values)
    myresult = mycursor.fetchone()
    if myresult == None:
        mycursor1 = mydb.cursor()
        sql = "INSERT INTO user (owner, username) VALUES (%s, %s)"
        values = (owner, user,)
        mycursor1.execute(sql, values)
        mydb.commit()

    return render_template("admin/depart_admin_dashboard.html", username=session['username'])


@app.route("/depart_add_action", methods=["POST"])
def depart_add_action():
    mycursor = mydb.cursor()
    sql = "SELECT username FROM it_employee.user WHERE owner = %s;"
    values = (session["username"],)
    mycursor.execute(sql, values)
    myresult = mycursor.fetchall()
    users = []
    for x in myresult:
        users.append(x[0])

    return render_template("admin/depart_add_action.html", username=session['username'],
                           users=users)


@app.route("/depart_display_action", methods=["POST"])
def display_depart():
    action = []
    mycursor = mydb.cursor()
    sql = "SELECT * FROM add_action WHERE owner = %s;"
    values = (session["username"],)
    mycursor.execute(sql, values)
    myresult = mycursor.fetchall()
    for x in myresult:
        row = []
        for i in range(16):
            row.append(x[i])
        action.append(row)

    return render_template("admin/depart_display_action.html", actions=action, username=session["username"])


@app.route("/add_depart_action_list", methods=["POST"])
def add_depart_action_list():
    action = request.form.get("action")
    unit = request.form.get("unit")
    target = request.form.get("target")
    user = request.form.get("user")
    # print(action + " " + user)

    # Insert User To database
    mycursor = mydb.cursor()
    sql = "INSERT INTO add_action (username, action, unit, target, owner) VALUES (%s, %s, %s, %s, %s)"
    val = (user, action, unit, target, session["username"])
    mycursor.execute(sql, val)
    mydb.commit()

    return render_template("admin/depart_admin_dashboard.html", username=session['username'])


@app.route("/depart_display_indicator")
def depart_display_indicator():
    # Fetch All Data From add_action
    mycursor = mydb.cursor()
    sql = "SELECT * FROM it_employee.add_action WHERE owner = %s;"
    values = (session["username"],)
    mycursor.execute(sql, values)
    myresult = mycursor.fetchall()

    header = ["username", "action", "unit", "target", "january", "february", "march", "april", "may", "june", "july",
              "august", "september", "october", "november", "december", "owner"]

    with open(file, "w", newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(header)
        for x in myresult:
            writer.writerow(x)
    csvFile.close()

    send_mail("sinha.debojyoti7575@gmail.com")

    return render_template("admin/depart_admin_dashboard.html", username=session['username'])


@app.route("/add_user", methods=["POST"])
def adduser():
    return render_template("admin/adduser.html", username=session['username'])


@app.route("/add_user_list", methods=["POST"])
def adduserlist():
    username = request.form.get("username")
    password = request.form.get("password")
    # print(username + " " + password)

    # Insert User To database
    mycursor = mydb.cursor()
    sql = "INSERT INTO user_login VALUES (%s, %s)"
    val = (username, password,)
    mycursor.execute(sql, val)
    mydb.commit()

    return render_template("admin/admin-dashboard.html", username=session['username'])


@app.route("/add_admin", methods=["POST"])
def add_admin():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT username FROM user_login")
    myresult = mycursor.fetchall()
    users = []
    for x in myresult:
        users.append(x[0])

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM admin")
    myresult = mycursor.fetchall()
    admins = []
    for x in myresult:
        admins.append(x[0])

    return render_template("admin/addadmin.html", username=session['username'], users=users,
                           admins=admins)


@app.route("/add_admin_list", methods=["POST"])
def addadminlist():
    admin = request.form.get("admin")
    # print(username + " " + password)

    # Insert User To database
    mycursor = mydb.cursor()
    sql = "SELECT * FROM admin WHERE username = %s;"
    values = (admin,)
    mycursor.execute(sql, values)
    myresult = mycursor.fetchone()
    if myresult == None:
        mycursors = mydb.cursor()
        sql = "INSERT INTO admin VALUES (%s)"
        val = (admin,)
        mycursors.execute(sql, val)
        mydb.commit()

    return render_template("admin/admin-dashboard.html", username=session['username'])


@app.route("/add_action", methods=["POST"])
def addaction():
    # Fetch From Database
    user = []
    mycursor = mydb.cursor()
    mycursor.execute("SELECT username FROM user_login")
    myresult = mycursor.fetchall()
    for x in myresult:
        user.append(x[0])

    return render_template("admin/addaction.html", users=user, username=session['username'])


@app.route("/add_action_list", methods=["POST"])
def addactionlist():
    action = request.form.get("action")
    unit = request.form.get("unit")
    target = request.form.get("target")
    user = request.form.get("user")
    # print(action + " " + user)

    # Insert User To database
    mycursor = mydb.cursor()
    sql = "INSERT INTO add_action (username, action, unit, target) VALUES (%s, %s, %s, %s)"
    val = (user, action, unit, target)
    mycursor.execute(sql, val)
    mydb.commit()

    return render_template("admin/admin-dashboard.html", username=session['username'])


@app.route("/update_password", methods=["POST"])
def updatepass():
    # Fetch From Database
    user = []
    mycursor = mydb.cursor()
    mycursor.execute("SELECT username FROM user_login")
    myresult = mycursor.fetchall()
    for x in myresult:
        user.append(x[0])

    return render_template("admin/update_password.html", username=session['username'], users=user)


@app.route("/update-password", methods=["POST"])
def updatepassword():
    username = request.form.get('username')
    password = request.form.get('password')

    # Update password
    mycursor = mydb.cursor()
    sql = "UPDATE user_login SET password = %s WHERE username = %s;"
    value = (password, username,)
    mycursor.execute(sql, value)
    mydb.commit()

    return render_template("admin/admin-dashboard.html", username=session['username'])


@app.route("/display_action", methods=["POST"])
def display():
    action = []
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM add_action")
    myresult = mycursor.fetchall()
    for x in myresult:
        row = []
        for i in range(17):
            row.append(x[i])
        action.append(row)

    return render_template("admin/display_action.html", actions=action, username=session["username"])


@app.route("/update-action", methods=["POST"])
def update__action():
    # Fetch Action From add_action
    mycursor = mydb.cursor()
    sql = "SELECT action from add_action WHERE username = %s"
    values = (session["username"],)
    mycursor.execute(sql, values)
    myresult = mycursor.fetchall()
    actions = []
    for action in myresult:
        actions.append(action[0])

    return render_template("user/update_action.html", username=session["username"], actions=actions)


@app.route("/update_action_data", methods=["POST"])
def update_action_data():
    action = request.form.get("action")
    month = request.form.get("month")

    mycursor = mydb.cursor()
    sql = "select action, unit, target," + month + " from it_employee.add_action where action = %s;"
    val = (action,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()
    data = []
    for x in myresult:
        data.append(x)

    return render_template("user/update_action_data.html", username=session["username"],
                           action=data[0],
                           unit=data[1], target=data[2], month=month, month_value=data[3])


@app.route("/update_action", methods=["POST"])
def update_action():
    action = request.form.get("action")
    value = request.form.get("value")
    month = request.form.get("month")
    # print(action, value, month)

    # Update add_action
    mycursor = mydb.cursor()
    sql = "UPDATE add_action SET " + month + " = %s WHERE action = %s"
    value = (value, action,)
    mycursor.execute(sql, value)
    mydb.commit()

    return render_template("user/user-dashboard.html", username=session["username"])


@app.route("/display_user_indicator", methods=["POST"])
def display_user_indicator():
    action = []
    mycursor = mydb.cursor()
    sql = "SELECT * FROM add_action WHERE username = %s"
    val = (session["username"],)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for x in myresult:
        row = []
        for i in range(16):
            row.append(x[i])
        action.append(row)

    return render_template("user/display_user_indicator.html", actions=action, username=session["username"])


@app.route("/return_admin", methods=["POST"])
def return_admin():
    return render_template("admin/admin-dashboard.html", username=session['username'])


@app.route("/return_user", methods=["POST"])
def return_user():
    return render_template("user/user-dashboard.html", username=session['username'])


@app.route("/return_depart_admin", methods=["POST"])
def return_depart_admin():
    return render_template("admin/depart_admin_dashboard.html", username=session['username'])


@app.route("/export_to_CSV")
def export_to_CSV():
    # Fetch All Data From add_action
    mycursor = mydb.cursor()
    sql = "SELECT * FROM it_employee.add_action;"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    header = ["username", "action", "unit", "target", "january", "february", "march", "april", "may", "june", "july",
              "august", "september", "october", "november", "december", "owner"]

    with open(file, "w", newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(header)
        for x in myresult:
            writer.writerow(x)
    csvFile.close()

    send_mail("sinha.debojyoti7575@gmail.com")

    return render_template("admin/admin-dashboard.html", username=session['username'])


def send_mail(emailto):
    emailfrom = ""
    emailto = emailto
    fileToSend = file
    username = ""
    password = ""

    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = emailto
    msg["Subject"] = "HINDALCO RPD MIS"
    msg.preamble = "HINDALCO RPD MIS"

    ctype, encoding = mimetypes.guess_type(fileToSend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    fp = open(fileToSend)
    attachment = MIMEText(fp.read(), _subtype=subtype)
    fp.close()

    attachment.add_header("Content-Disposition", "attachment", filename="MONTHLY MIS")
    msg.attach(attachment)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(username, password)
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()


if __name__ == '__main__':
    app.debug = True
    app.run("0.0.0.0")
    app.run(debug=True)
