from flask import Flask, render_template, request, url_for,redirect
from flask_mail import Mail, Message
from pymongo import MongoClient
import os
import random
import string
def random_alphanumeric_string(length):
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=length
        )
    )
app = Flask(__name__)
client=MongoClient('mongodb://localhost:27017')
db=client['cafe']
collection=db['book']
@app.route('/',methods=['GET','POST'])
def index():
 return render_template('index.html')
@app.route('/returnie')
def returnie():
    return render_template('index.html')   
@app.route('/messagee')
def message():
 dataa = collection.find().limit(1).sort([('$natural',-1)])
 return render_template('message.html',data=[i for i in dataa])
@app.route('/addmin')
def admin():
    return render_template('admin.html')
@app.route('/dashie',methods=["GET","POST"])
def dashie():
    if request.method=="POST":
        data1 = collection.find()
        return render_template('dashboard.html',data=[i for i in data1])  
    else:
        data1 = collection.find()
        return render_template('dashboard.html',data=[i for i in data1])  
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '--EMAILID--'
app.config['MAIL_PASSWORD'] = '--PASSWORD--'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


@app.route("/emailie",methods=['GET','POST'])
def email():
    if request.method=="POST":
        ac=request.form.get("action")
        eid=request.form.get("eid")
        if ac=="yes":
            return redirect(url_for("confirm",email=eid))
        else:
            return redirect(url_for("cancel",email=eid))
            
@app.route("/coemail",methods=['GET','POST'])
def confirm():
    if request.method=="POST":
        tik=request.form.get("tik")
        data=collection.find_one({"ticket":tik})
        eid=data["email"]
        filter = { "ticket":tik }
        newvalues = { "$set": { 'status': "confirmed" } }
        collection.update_one(filter, newvalues)
        msg = Message("booking confirmed", sender='--EMAILID--', recipients=[eid])
        msg.body = "Thank you for booking! Your reservation  is confirmed!"
        mail.send(msg)
    return redirect(url_for("dashie"))
            
@app.route("/caemail",methods=['GET','POST'])
def cancel():
    if request.method=="POST":
        tik=request.form.get("tik")
        data=collection.find_one({"ticket":tik})
        eid=data["email"]
        msg = Message("booking cancelled", sender='--EMAILID--', recipients=[eid])
        msg.body ="Sorry we had to cancel your reservastion due to excessive booking, Thank you for choosing us!"
        mail.send(msg)
        collection.delete_many({'ticket':tik})
    return redirect(url_for("dashie"))

@app.route("/messy",methods=["GET","POST"])
def messy():
    if request.method=="POST":
        cus_name = request.form.get("cus_name")
        email=request.form.get("cus_email")
        cus_seats = request.form.get("cus_seats")
        time = request.form.get("time")
        pho_num = request.form.get("pho_num")
        tik=random_alphanumeric_string(5)     
        collection.insert_one({'cus_name':cus_name,"email":email,"cus_seats":cus_seats,"time":time,'pho_num':pho_num,'ticket':tik,'status':"pending"})
        return redirect(url_for('message'))
    
    
@app.route("/cancy",methods=["GET","POST"])
def cancy():
    if request.method=="POST":
        tik = request.form.get("ticket")
        collection.delete_many({'ticket':tik})
    return redirect(url_for('index'))
@app.route("/goback",methods=["GET","POST"])
def goback():
    return redirect(url_for('index'))
if __name__=='__main__':
    app.run(host='0.0.0.0',port='8888',debug=True) 
    
