# third party imports
from flask import render_template, redirect, url_for, flash, request
from flask import current_app as app
from flask_login import login_required, login_user, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
import datetime 

# local imports
from . import auth 
from .forms import RegisterForm, LoginForm, EmailForm, PasswordForm
from ...models import  User
from ...extensions import db, mail

def send_mail(to, subject, template):
    msg = Message(subject, recipients=[to], html=template, sender= app.config['MAIL_DEFAULT_SENDER'])
    mail.send(msg)

# send confirmation email
def send_confirmation(user_email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    confirm_url = url_for('.confirm_email', 
            token=serializer.dumps(user_email, salt='confirm-email'), 
            _external=True)
    html = render_template('auth/confirm.html', confirm_url=confirm_url)

    send_mail(user_email,'Equip Youth Africa. Please confirm your email', html)

#send password reset
def send_password_reset(user_email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    password_reset_url = url_for('.reset_password_token', 
            token=serializer.dumps(user_email, salt='reset-password'),
            _external=True)
    html = render_template('auth/email_password_reset.html', password_reset_url=password_reset_url)

    send_mail(user_email, 'Password reset requested', html)
    


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        send_confirmation(form.email.data)
        flash('A confirmation link has been sent to your email address', 'success')
        return redirect(url_for('main.index'))

    return render_template('auth/register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('You are logged in', 'success')
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invaild Credienials or Password', 'danger')

    form.email.data = ''
    form.password.data= ''


    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out', 'warning')
    return redirect(url_for('main.index'))

@auth.route('/confirm/<token>')
def confirm_email(token):
    try:
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = serializer.loads(token, salt='confirm-email', max_age=3600)
    except:
        flash('The confirmation link is invalid', 'danger')
        return redirect(url_for('.login'))
    user = User.query.filter_by(email=email).first()

    if user.confirmed:
        flash('Account already confirmed')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        #db.session.add(user)
        db.session.commit()
        flash('Account confirmed', 'success')
        
    return redirect(url_for('main.root'))

@auth.route('/resend-confirmation', methods=['GET', 'POST'])
def send_confirm_email():
    form = EmailForm()
    if form.validate_on_submit():
        send_confirmation(form.email.data)
        flash('A confirmation link has been sent to your email', 'success')
        return redirect(url_for('.login'))

    return render_template('auth/password_reset.html', form=form) 



@auth.route('/reset/password', methods=['GET', 'POST'])
def reset_password():
    form = EmailForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        if user.confirmed:
            send_password_reset(form.email.data)
            flash('Please check your email for password reset link', 'success')
        else:
            flash('Your account must be confirmed', 'danger')
            return redirect(url_for('.login'))

    
    return render_template('auth/password_reset.html', form=form)

@auth.route('/reset/password/<token>', methods=['GET', 'POST'])
def reset_password_token(token):
    try:
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = serializer.loads(token, salt='reset-password', max_age=3600)
    except:
        flash('The password reset link is invalid', 'danger')
        return redirect(url_for('.login'))

    form = PasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()

        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Password reset successful', 'success')
        return redirect(url_for('main.index'))

    return render_template('auth/password_reset_token.html', form=form)

@auth.route('/unconfirmed')
def unconfirmed():
    return render_template('auth/unconfirmed')
# email confirmation here
