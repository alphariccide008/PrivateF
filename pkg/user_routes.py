import random,string,os
import json,requests
from functools import wraps

from flask import render_template,request,abort,redirect,flash,make_response,session,url_for,jsonify
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


from pkg import app,csrf
from pkg.models import db,User,Information
from pkg.forms import *



#This is a decoratoer to help check if there is a user logged in
def login_required(f):
    @wraps(f)
    def login_check(*args,**kwargs):
        if session.get('user')!=None:
            return f(*args,**kwargs)
        else:
            flash("Access denied ,Login", "danger")
            return redirect('/login')
    return login_check 


def generate_string(howmany):#call this function as renerate_string(10)
    x = random.sample(string.digits,howmany)
    return ''.join(x)


app.config["UPLOAD_FOLDER"] = "uploads"  # 🔹 save directly into "upload/"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}




def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template('users/index.html')



@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        # Step 1: User details
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        age = request.form.get("age")
        level = request.form.get("level")
        school = request.form.get("school")
        phone = request.form.get("phone")
        guardian = request.form.get("guardian")
        occupation = request.form.get("occupation")

        # Save user
        new_user = User(
            fullname=fullname,
            email=email,
            age=age,
            level=level,
            school=school,
            phone=phone,
            guardian=guardian,
            occupation=occupation,
            status='new'
        )
        db.session.add(new_user)
        db.session.commit()

        # Step 2–5: Information
        financial = request.form.get("financial")
        intelligence = request.form.get("intelligence")
        grit = request.form.get("grit")
        growth = request.form.get("growth")
        giving_back = request.form.get("giving")

        # Handle File Uploads (save directly in "upload/")
        ALLOWED_EXTENSIONS = {'jpg', 'png', 'pdf', 'jpeg'}

# Upload folder
        UPLOAD_FOLDER = os.path.join("pkg", "static", "upload")
        os.makedirs(UPLOAD_FOLDER, exist_ok=True) 

        filesobj = request.files.get('waec')
        filesobj1 = request.files.get('jamb')

        if not filesobj or not filesobj1:
            flash('Please upload both Images', category='error')
            return

        filename = filesobj.filename
        filename1 = filesobj1.filename       

        if filename == '' or filename1 == '':
            flash('Please upload both Images', category='error')
            return

    # Extract extensions
        ext = filename.rsplit('.', 1)[-1].lower()
        ext1 = filename1.rsplit('.', 1)[-1].lower()

    # ✅ Correct validation
        if ext in ALLOWED_EXTENSIONS and ext1 in ALLOWED_EXTENSIONS:
        # Generate unique + safe filenames
            newname = f"{int(random.random()*10000000)}_{secure_filename(filename)}"
            newname1 = f"{int(random.random()*10000000)}_{secure_filename(filename1)}"

        # Full paths
        save_path = os.path.join(UPLOAD_FOLDER, newname)
        save_path1 = os.path.join(UPLOAD_FOLDER, newname1)

        # Save files
        filesobj.save(save_path)
        filesobj1.save(save_path1)
        # Save info
        new_info = Information(
            financial=financial,
            intelligence=intelligence,
            grit=grit,
            growth=growth,
            giving_back=giving_back,
            waec_file=newname,
            jamb_file=newname1,
           
            user_id=new_user.id,
        )
        db.session.add(new_info)
        db.session.commit()

        # Console log instead of return
        print(f"✅ User created: {new_user.fullname} ({new_user.school})")
        print(f"✅ Files: WAEC={filename}, JAMB={filename1}")
        print(f"✅ Files: Giving={giving_back}")

        return ("", 204)  # no page reload, frontend just continues

    return render_template('users/index.html')








    










@app.errorhandler(404)
def error_page(errors):
    return render_template("error 404")



# @app.after_request
# def after_request(response):
#     response.headers["cache-control"]="no-cache, no-store, must-revalidate"
#     return response





@app.errorhandler(500)
def server_error_page(errors):
    return render_template("Error")
 

@app.errorhandler(403)
def forbbiden_page(errors):
    return render_template("forbidden")













