from flask import Flask, render_template, redirect, url_for, flash , request
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# app = Flask(__name__) 
app = Flask(__name__, template_folder='templates', static_folder='static')

app.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

# Configure app from environment variables
app.secret_key = os.environ['SECRET_KEY']  # Using [] instead of getenv for required vars

# Email configuration with defaults
app.config.update(
    MAIL_SERVER=os.getenv('MAIL_SERVER', 'smtp.gmail.com'),
    MAIL_PORT=int(os.getenv('MAIL_PORT', 587)),
    MAIL_USE_TLS=os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', '1', 't'],
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER', os.getenv('MAIL_USERNAME'))
)

# Validate minimum config
if not app.secret_key:
    raise ValueError("No SECRET_KEY set for Flask application")
if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
    raise ValueError("MAIL_USERNAME and MAIL_PASSWORD must be set for Flask-Mail")

mail = Mail(app)

# Routes remain the same as before
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')
import os
print(os.path.abspath(app.template_folder))


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        try:
            msg = Message(
                subject=f"New Contact Form Message from {name}",
                sender=os.getenv('MAIL_DEFAULT_SENDER'),  # Your website's identity
                recipients=[os.getenv('MAIL_RECIPIENT')],  # Your personal email
            )

            msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
            mail.send(msg)
            flash('Your message has been sent!', 'success')
            print(f"{name}!, Your Message sent to {os.getenv('MAIL_RECIPIENT')}")
        except Exception as e:
            flash('An error occurred while sending your message. Please try again.', 'danger')
            print(f"Error: {e}")

        return redirect(url_for('contact'))
    
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)