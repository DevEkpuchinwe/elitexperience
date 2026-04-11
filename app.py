from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify 
from datetime import datetime
import os
import json
import uuid

# NEW: DB + EMAIL
from sqlalchemy import create_engine, Column, String, Text, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')

# -------------------- DATABASE SETUP --------------------

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///local.db")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(String, primary_key=True)
    celeb_name = Column(String)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    country = Column(String)
    address = Column(Text)
    selectedServices = Column(Text)
    message = Column(Text)
    occupation = Column(String)
    age = Column(String)
    submittedAt = Column(DateTime, default=datetime.utcnow)
    emailSent = Column(Boolean, default=False)

class Lead(Base):
    __tablename__ = "leads"

    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)
    company = Column(String)
    message = Column(Text)
    createdAt = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(engine)

# KEEP VARIABLE (not used anymore but not removed)
bookings_db = []

# -------------------- EMAIL SETUP (BREVO) --------------------

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "elitexperience.teams@gmail.com")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "elitexperience.teams@gmail.com")
REPLY_TO_EMAIL = os.getenv("REPLY_TO_EMAIL", "elitexperience.teams@gmail.com")

def send_booking_email(booking):
    if not BREVO_API_KEY:
        print("No Brevo API key set")
        return

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = BREVO_API_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    html_content = f"""
    <h2>New Booking</h2>
    <p><b>Name:</b> {booking['name']}</p>
    <p><b>Email:</b> {booking['email']}</p>
    <p><b>Celebrity:</b> {booking['celeb_name']}</p>
    <p><b>Services:</b> {', '.join(booking['selectedServices'])}</p>
    <p><b>Message:</b> {booking['message']}</p>
    """

    try:
        # Send to user
        api_instance.send_transac_email(
            sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": booking['email']}],
                sender={"email": SENDER_EMAIL},
                reply_to={"email": REPLY_TO_EMAIL},
                subject="Booking Confirmation",
                html_content=html_content
            )
        )

        # Send to admin
        api_instance.send_transac_email(
            sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": ADMIN_EMAIL}],
                sender={"email": SENDER_EMAIL},
                reply_to={"email": REPLY_TO_EMAIL},
                subject="New Booking Alert",
                html_content=html_content
            )
        )

    except ApiException as e:
        print("Email error:", e)

# -------------------- HELPERS --------------------

def save_booking(data):
    session = SessionLocal()
    booking = Booking(**data)
    session.add(booking)
    session.commit()
    session.close()

def get_bookings():
    session = SessionLocal()
    data = session.query(Booking).order_by(Booking.submittedAt.desc()).all()
    session.close()
    return data

def delete_booking_db(booking_id):
    session = SessionLocal()
    session.query(Booking).filter(Booking.id == booking_id).delete()
    session.commit()
    session.close()

def mark_sent_db(booking_id):
    session = SessionLocal()
    booking = session.query(Booking).filter(Booking.id == booking_id).first()
    if booking:
        booking.emailSent = True
        session.commit()
    session.close()

def save_lead(data):
    session = SessionLocal()
    lead = Lead(**data)
    session.add(lead)
    session.commit()
    session.close()

# -------------------- YOUR ORIGINAL DATA --------------------


celeb_data = {
    "taylor-swift": {
        "name": "Taylor Swift",
        "management": "TN Management",
        "tagline": "Your Dream Moment with Taylor",
        "heroText": "Don't Miss Your Chance! Limited spots available for exclusive meet & greets, private time, and VIP experiences.",
        "stats": {
            "meetGreets": 1247,
            "privateTime": 89,
            "ticketsSold": 15420,
            "fanCards": 3892
        },
        "bio": "Taylor Swift is a global superstar known for her heartfelt songwriting and incredible performances. She loves connecting with fans, exploring new cities, and creating unforgettable moments.",
        "interests": ["Songwriting", "Cats", "Baking", "Surprise Songs"],
        "heroImage": "https://images.unsplash.com/photo-1772587023108-61e60c18537a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb25jZXJ0JTIwc3RhZ2UlMjBwZXJmb3JtZXIlMjBzcG90bGlnaHR8ZW58MXx8fHwxNzc1Mzk2OTQxfDA&ixlib=rb-4.1.0&q=80&w=1080",
        "photos": [
            "https://images.unsplash.com/photo-1772587023108-61e60c18537a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb25jZXJ0JTIwc3RhZ2UlMjBwZXJmb3JtZXIlMjBzcG90bGlnaHR8ZW58MXx8fHwxNzc1Mzk2OTQxfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1765560008448-612e4b17877f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjZWxlYnJpdHklMjByZWQlMjBjYXJwZXQlMjBldmVudHxlbnwxfHx8fDE3NzUzOTY5NDJ8MA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1716187249622-4bd9ae36a24c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxleGNsdXNpdmUlMjB2aXAlMjBiYWNrc3RhZ2V8ZW58MXx8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1741829186423-43f6fa5ac781?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtZWV0JTIwYW5kJTIwZ3JlZXQlMjBmYW5zfGVufDF8fHx8MTc3NTM5Njk0Mnww&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1761110787206-2cc164e4913c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxsdXh1cnklMjBldmVudCUyMHZlbnVlfGVufDF8fHx8MTc3NTM5Njk0M3ww&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1771402899438-55fd9b239c6f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwcm9mZXNzaW9uYWwlMjBzZWN1cml0eSUyMGd1YXJkc3xlbnwxfHx8fDE3NzUzOTY5NDN8MA&ixlib=rb-4.1.0&q=80&w=1080"
        ]
    },
    "default": {
        "name": "Your Favorite Artist",
        "management": "Elite Artist Management",
        "tagline": "Exclusive Access to Your Favorite Stars",
        "heroText": "Experience once-in-a-lifetime moments with top celebrities. Limited availability - Book now before spots fill up!",
        "stats": {
            "meetGreets": 500,
            "privateTime": 50,
            "ticketsSold": 10000,
            "fanCards": 2000
        },
        "bio": "Connect with your favorite celebrities through our exclusive booking platform. We specialize in creating unforgettable experiences.",
        "interests": ["Music", "Fashion", "Travel", "Fans"],
        "heroImage": "https://images.unsplash.com/photo-1772587023108-61e60c18537a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb25jZXJ0JTIwc3RhZ2UlMjBwZXJmb3JtZXIlMjBzcG90bGlnaHR8ZW58MXx8fHwxNzc1Mzk2OTQxfDA&ixlib=rb-4.1.0&q=80&w=1080",
        "photos": [
            "https://images.unsplash.com/photo-1772587023108-61e60c18537a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb25jZXJ0JTIwc3RhZ2UlMjBwZXJmb3JtZXIlMjBzcG90bGlnaHR8ZW58MXx8fHwxNzc1Mzk2OTQxfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1765560008448-612e4b17877f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjZWxlYnJpdHklMjByZWQlMjBjYXJwZXQlMjBldmVudHxlbnwxfHx8fDE3NzUzOTY5NDJ8MA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1716187249622-4bd9ae36a24c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxleGNsdXNpdmUlMjB2aXAlMjBiYWNrc3RhZ2V8ZW58MXx8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1741829186423-43f6fa5ac781?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtZWV0JTIwYW5kJTIwZ3JlZXQlMjBmYW5zfGVufDF8fHx8MTc3NTM5Njk0Mnww&ixlib=rb-4.1.0&q=80&w=1080"
        ]
    }
}

services = [
    {"id": "fan-card", "name": "Official Fan Card", "description": "Get your exclusive verified fan card with special perks"},
    {"id": "meet-greet", "name": "Meet & Greet", "description": "Personal meet and greet session with your favorite celebrity"},
    {"id": "tickets", "name": "Concert Tickets", "description": "Premium tickets to upcoming shows and events"},
    {"id": "premium-seats", "name": "Premium VIP Seats", "description": "Front row and VIP seating arrangements"},
    {"id": "after-event", "name": "After Event Meet-up", "description": "Exclusive backstage access after the show"},
    {"id": "photo-time", "name": "Photo Session", "description": "Professional photo opportunity with the celebrity"},
    {"id": "private-time", "name": "Private Time Together", "description": "One-on-one exclusive time with the celebrity"}
]


# -------------------- ROUTES --------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    lead = {
        "id": str(uuid.uuid4()),
        "name": request.form.get('name'),
        "email": request.form.get('email'),
        "company": request.form.get('company'),
        "message": request.form.get('message'),
        "createdAt": datetime.utcnow()
    }

    # SAVE TO DATABASE
    save_lead(lead)

    # OPTIONAL: send email notification (reuse your system)
    send_booking_email({
        "name": lead["name"],
        "email": lead["email"],
        "celeb_name": "New Partnership Inquiry",
        "selectedServices": ["N/A"],
        "message": lead["message"]
    })

    # REDIRECT TO ADMIN DASHBOARD
    return redirect(url_for('admin'))

@app.route('/celeb/<celeb_name>')
def celeb_page(celeb_name):
    celeb = celeb_data.get(celeb_name, celeb_data['default'])
    return render_template('celeb.html', celeb=celeb, celeb_name=celeb_name)

@app.route('/celeb/<celeb_name>/book', methods=['GET', 'POST'])
def booking_page(celeb_name):
    celeb = celeb_data.get(celeb_name, celeb_data['default'])
    
    if request.method == 'POST':
        booking = {
            'id': str(uuid.uuid4()),
            'celeb_name': celeb_name,
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'country': request.form.get('country'),
            'address': request.form.get('address'),
            'selectedServices': request.form.getlist('services'),
            'message': request.form.get('message'),
            'occupation': request.form.get('occupation'),
            'age': request.form.get('age'),
            'submittedAt': datetime.utcnow(),
            'emailSent': False
        }

        # SAVE TO REAL DB
        save_booking({
            **booking,
            "selectedServices": ",".join(booking['selectedServices'])
        })

        # SEND EMAIL
        send_booking_email(booking)

        flash('Your booking request has been submitted! We\'ll contact you within 24 hours.', 'success')
        #return redirect(url_for('booking_page', celeb_name=celeb_name))
        return render_template('success.html',celeb_name=celeb_name)
    
    return render_template('booking.html', celeb=celeb, celeb_name=celeb_name, services=services)

@app.route('/legal')
def legal():
    return render_template('legal.html')

@app.route('/privacy')
def privacy():
    return redirect('/legal#privacy')

@app.route('/terms')
def terms():
    return redirect('/legal#terms')

@app.route('/cookies')
def cookies():
    return redirect('/legal#cookies')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'admin123':
            session['admin_authenticated'] = True
            return redirect(url_for('admin'))
        else:
            flash('Incorrect password', 'error')
            return redirect(url_for('admin'))
    
    if not session.get('admin_authenticated'):
        return render_template('admin_login.html')
    
    bookings = get_bookings()
    db_session = SessionLocal()
    leads = db_session.query(Lead).order_by(Lead.createdAt.desc()).all()
    db_session.close()

 
    return render_template('admin_dashboard.html', bookings=bookings, leads=leads)

@app.route('/admin/send-email', methods=['POST'])
def send_bulk_email():
    if not session.get('admin_authenticated'):
        return jsonify({"success": False})

    data = request.get_json()
    emails = data.get("emails", [])
    subject = data.get("subject")
    body = data.get("body")

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.getenv("BREVO_API_KEY")

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    try:
        api_instance.send_transac_email(
            sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": e} for e in emails],
                sender={"email": "SENDER_EMAIL"},
                reply_to={"email": "REPLY_TO_EMAIL"},
                subject=subject,
                html_content=body
            )
        )

        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return jsonify({"success": False})

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_authenticated', None)
    return redirect(url_for('admin'))

@app.route('/admin/delete/<booking_id>', methods=['POST'])
def delete_booking(booking_id):
    if not session.get('admin_authenticated'):
        return redirect(url_for('admin'))
    
    delete_booking_db(booking_id)

    flash('Booking deleted successfully', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/mark-sent/<booking_id>', methods=['POST'])
def mark_sent(booking_id):
    if not session.get('admin_authenticated'):
        return redirect(url_for('admin'))
    
    mark_sent_db(booking_id)

    flash('Marked as sent', 'success')
    return redirect(url_for('admin'))



if __name__ == '__main__':
    app.run(debug=True)

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=5000)