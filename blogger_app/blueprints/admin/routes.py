from . import admin_bp
from flask import session, redirect, request, render_template, url_for

@admin_bp.route('/admin', methods=['POST','GET'])
def admin_login_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == 'admin@mail.com' and password == 'admin':
            session['is_login'] = True
            return redirect(url_for('blogger'))
    if session.get("is_login"):
        return redirect(url_for('blogger'))
    return render_template('admin/admin_login.html')

@admin_bp.route("/logout")
def logout():
    session.pop('is_login', None)
    return redirect(url_for('admin_login_page'))