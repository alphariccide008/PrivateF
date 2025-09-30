import random,string,os
import json,requests
from functools import wraps

from flask import render_template,request,abort,redirect,flash,make_response,session,url_for,jsonify
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash


from pkg import app,csrf
from pkg.models import db,User,Admin,Information
from pkg.forms import *





#This is a decoratoer to help check if there is a user logged in
def login_required(f):
    @wraps(f)
    def login_check(*args,**kwargs):
        if session.get('admin') !=None:
            return f(*args,**kwargs)
        else:
            flash('Access Denied')
            flash('You must be logged in first')
            return redirect('/admin/')
    return login_check




@app.route("/admin/", methods=["GET", "POST"])
def admin():
    if request.method == "GET":
        return render_template("admin/adminlog.html")

    email = request.form.get("email")
    pwd = request.form.get("pwd")

    # Look up admin by email
    deets = db.session.query(Admin).filter(Admin.email == email).first()

    if deets and deets.password:  # ensure password exists
        if check_password_hash(deets.password, pwd):
            session["admin"] = deets.id
            flash("Login successful!", "success")
            return redirect(url_for("all_users"))
        else:
            flash("Invalid credentials, try again", "danger")
            return redirect(url_for("admin"))
    else:
        flash("Invalid credentials, try again", "danger")
        return redirect(url_for("admin"))

        



from sqlalchemy import desc  # Make sure this import is present

@app.route("/all_users/")
@login_required
def all_users():
    id = session.get("admin")
    admindeets = Admin.query.get_or_404(id)

    page = request.args.get("page", 1, type=int)

    pagination = (
        db.session.query(User, Information)
        .join(Information, User.id == Information.user_id)
        .order_by(desc(User.id))   # 👈 Sort by newest first (change to created_at if needed)
        .paginate(page=page, per_page=5, error_out=False)
    )

    deet = pagination.items

    return render_template(
        "admin/all_user.html",
        deet=deet,
        admindeets=admindeets,
        pagination=pagination,
    )



@app.route("/approved_applicants/")
@login_required
def approved():
    id = session.get("admin")
    admindeets = Admin.query.get_or_404(id)

    # Get current page number from query string (default = 1)
    page = request.args.get("page", 1, type=int)

    # Join User and Information, paginate with 10 per page
    pagination = (
        db.session.query(User, Information)
        .join(Information, User.id == Information.user_id).filter(User.approved=='approved')
        .paginate(page=page, per_page=5, error_out=False)
    )

    # pagination.items contains the actual records for this pageds
    deet = pagination.items

    return render_template(
        "admin/approved.html",
        deet=deet,
        admindeets=admindeets,
        pagination=pagination,
    )



@app.route('/user/<int:user_id>')
@login_required
def user_detail(user_id):
    # Correct way to get user or 404
    user = User.query.get_or_404(user_id)
    if user.status:
        user.status='clicked'
        db.session.commit()

    # Fetch related Information record
    information = Information.query.filter_by(user_id=user.id).first()


    return render_template('admin/user_detail.html', user=user, information=information)

@app.route('/approved/<int:user_id>')
@login_required
def approve_user(user_id):
    # Correct way to get user or 404
    user = User.query.get_or_404(user_id)
    if user.status:
        user.approved='approved'
        db.session.commit()
        flash('Applicant has been Approved successfully')
        return redirect(url_for('all_users'))


# @app.route('/edit_user_balance/')
# @login_required
# def edit_all_user():
#     id = session.get('admin')
#     admindeets = db.session.query(Adminreg).get_or_404(id)
#     userdeets = db.session.query(User).all()
    
#     return render_template('admin/edit_balance.html',userdeets=userdeets,admindeets=admindeets)



# @app.route("/All_transactions")
# @login_required
# def all_transaction():
#     id = session.get('admin')
#     admindeets = db.session.query(Adminreg).get_or_404(id)
#     userdeets = db.session.query(User,Transaction).join(Transaction, User.user_id==Transaction.trans_user_id).all()
#     deet = [{'user':user, 'trans': trans}for user ,trans in userdeets ]
#     return render_template('admin/transactions.html',admindeets=admindeets ,deets=deet)



# @app.route('/edit_balance/<di>', methods=['POST', 'GET'])
# @login_required
# def edit_balance(di):
#     user = db.session.query(User).filter_by(user_id=di).first()  # Ensure 'first()' is used to get a single result

#     if request.method == 'POST':
#         btc_balance = request.form.get('btcbalance')
#         eth_balance = request.form.get('ethbalance')
#         freezed_balance = request.form.get('freezed')

#         if user:
#             user.btc_balance = btc_balance
#             user.eth_balance = eth_balance
#             user.freezed_balance = freezed_balance
#             db.session.commit()
#             flash('Balance updated successfully', category='success')
#         else:
#             flash('User not found', category='error')

#         return redirect(url_for('edit_all_user'))

#     # Render template with 'user' (this will work whether 'POST' is submitted or not)
#     return render_template('admin/editbalance.html', user=user)




  
    
    





# @app.route("/admin/delete/<id>/" ,methods=['POST','GET'])
# def all_delete(id):
#     payment = db.session.query(User).get_or_404(id)
   
#     transaction =db.session.query(Transaction).filter_by(trans_user_id=id)
#     db.session.delete(payment)
   
#     db.session.commit()
#     flash('payments has been deleted Successfully',category='paymentmsg')
#     return redirect(url_for('all_users'))


# @app.route("/admin/confrim/<id>/")
# def confirm(id):
#     transaction =db.session.query(Transaction).get_or_404(id)
#     transaction.trans_status='Confirmed'
#     db.session.commit()
#     flash('Payment has been successfully confirmed',category='success')
#     return redirect(url_for('all_transaction'))



@app.route("/admin/logout")
def admin_logout():
    if session.get('admin')!= None:
        session.pop('admin',None)
        flash('you\'ve logged out successfully',"success")
    return redirect(url_for('admin'))