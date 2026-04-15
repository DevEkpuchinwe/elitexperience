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


class PageView(Base):  # NEW: Tracking opens + metadata
    __tablename__ = "page_views"
    id = Column(String, primary_key=True)
    path = Column(String)
    celeb_name = Column(String, nullable=True)  # e.g. "sydney-sweeney" or None
    ip_address = Column(String)
    user_agent = Column(Text)
    referrer = Column(Text, nullable=True)
    viewed_at = Column(DateTime, default=datetime.utcnow)


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

def get_db_session():
    return SessionLocal()

def save_page_view(path, celeb_name=None):
    session = get_db_session()
    view = PageView(
        id=str(uuid.uuid4()),
        path=path,
        celeb_name=celeb_name,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent'),
        referrer=request.referrer
    )
    session.add(view)
    session.commit()
    session.close()

def get_page_views_count():
    session = get_db_session()
    count = session.query(PageView).count()
    session.close()
    return count

# -------------------- YOUR ORIGINAL DATA --------------------


celeb_data = {
     "sydney-sweeney": {
    "name": "Sydney Sweeney",
    "management": "Brillstein Entertainment Partners",
    "tagline": "Your Dream Moment with Sydney Sweeney",
    "heroText": "Don't Miss Your Chance! Limited spots available for exclusive meet & greets, private time, and VIP experiences.",
    "stats": {
        "meetGreets": 780,
        "privateTime": 92,
        "ticketsSold": 16800,
        "fanCards": 12450
    },
    "bio": "Sydney Sweeney is a talented American actress and producer known for her breakout roles in Euphoria as Cassie Howard and The White Lotus. She has earned multiple Emmy nominations and stars in major films like Anyone But You, Immaculate, and Echo Valley. She is also the founder of her production company Fifty-Fifty Films.",
    "interests": ["Acting", "Producing", "Fashion", "Fitness", "Mixed Martial Arts"],
    "heroImage": "https://i.pinimg.com/1200x/f9/b3/5c/f9b35c27a89fddbb84f14abff68b2a7f.jpg",
    "photos": [
        "https://i.pinimg.com/736x/bc/ce/8c/bcce8cf74c9897c4d29fd2c31f6b1d54.jpg",
        "https://i.pinimg.com/736x/29/14/f8/2914f8003031dc1366dc0d560699756d.jpg",
        "https://i.pinimg.com/1200x/8c/bd/fc/8cbdfc13661202532d5471f88a3c43f4.jpg",
        "https://i.pinimg.com/736x/54/fe/80/54fe802d3154cd9811eb87102d203e8a.jpg",
        "https://i.pinimg.com/736x/54/fe/80/54fe802d3154cd9811eb87102d203e8a.jpg",
        "https://i.pinimg.com/1200x/f9/b3/5c/f9b35c27a89fddbb84f14abff68b2a7f.jpg",
        "https://i.pinimg.com/736x/f3/e0/24/f3e02402d45504967164880fae883501.jpg",
    ]
},
   "thane-rivers": {
        "name": "Thane Rivers",
        "management": "Independent (Self-Managed)",
        "tagline": "Your Dream Moment with the Bearded Viking",
        "heroText": "Don't Miss Your Chance! Limited spots available for exclusive meet & greets, private time, and VIP experiences.",
        "stats": {
            "meetGreets": 856,
            "privateTime": 124,
            "ticketsSold": 9870,
            "fanCards": 2456
        },
        "bio": "Thane Rivers, known as the Bearded Viking, is a popular social media personality and Instagram star famous for positive affirmations, lifestyle content, and making people smile. He connects with fans through heartfelt messages and uplifting vibes.",
        "interests": ["Positive Affirmations", "Coffee Mugs", "Lifestyle Content", "Making Fans Happy"],
        #"heroImage": "https://i.pinimg.com/736x/3e/44/41/3e4441961ecf89753573c39725676915.jpg",
        "heroImage": "https://ksplutifhhfhncjlwjxo.supabase.co/storage/v1/object/public/celebs/f5273171d949336f59a16f2c82566354.jpg",
        "photos": [
            "https://i.pinimg.com/736x/3e/44/41/3e4441961ecf89753573c39725676915.jpg",
            "https://ctimages.servefilesonly.com/resize/?url=https://public.onlyfans.com/files/g/gx/gxu/gxuecc0ge5b1avnkd41w1neznmrgdyry1658083671/250003521/avatar.jpg&w=480&q=100",
            "https://ksplutifhhfhncjlwjxo.supabase.co/storage/v1/object/public/celebs/f5273171d949336f59a16f2c82566354.jpg",
            "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxleGNsdXNpdmUlMjB2aXAlMjBiYWNrc3RhZ2V8ZW58MXx8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://ksplutifhhfhncjlwjxo.supabase.co/storage/v1/object/public/celebs/thanemeet.webp",
            "https://ksplutifhhfhncjlwjxo.supabase.co/storage/v1/object/public/celebs/thaneoncap.webp",
            "https://ksplutifhhfhncjlwjxo.supabase.co/storage/v1/object/public/celebs/thanewithflowerplane.jpg",
            "https://i.pinimg.com/736x/02/8a/ec/028aec4f2b1d40e2c0c76c4539609cc0.jpg"
        ]
    },
    "taylor-swift": {
        "name": "Taylor Swift",
        "management": "TN Management",
        "tagline": "Your Dream Moment with Taylor chin",
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
    
    "tony-carreira": {
        "name": "Tony Carreira",
        "management": "RegiConcerto / Self-Managed Elements",
        "tagline": "Your Dream Moment with Tony Carreira",
        "heroText": "Don't Miss Your Chance! Limited spots available for exclusive meet & greets, private time, and VIP experiences.",
        "stats": {
            "meetGreets": 1450,
            "privateTime": 210,
            "ticketsSold": 28900,
            "fanCards": 6720
        },
        "bio": "Tony Carreira is a beloved Portuguese singer known for his romantic ballads and heartfelt performances. A superstar in Portugal and among Portuguese communities worldwide, he connects deeply with fans through emotional music and personal stories.",
        "interests": ["Romantic Ballads", "Family", "Performing Live", "Philanthropy"],
        "heroImage": "https://images.unsplash.com/photo-1507679799987-c73779560269?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb25jZXJ0JTIwc3RhZ2UlMjBwZXJmb3JtZXJ8ZW58MXx8fHwxNzc1Mzk2OTQxfDA&ixlib=rb-4.1.0&q=80&w=1080",
        "photos": [
            "https://images.unsplash.com/photo-1507679799987-c73779560269?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb25jZXJ0JTIwc3RhZ2UlMjBwZXJmb3JtZXJ8ZW58MXx8fHwxNzc1Mzk2OTQxfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1517841905240-4722065025b7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxyZWQlMjBjYXJwZXQlMjBjZWxlYnJpdHl8ZW58MXx8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxiaWNrYXN0YWdlJTIwdmlwfGVufDF8fHx8MTc3NTM5Njk0Mnww&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfG1lZXQlMjBhbmQlMjBncmVldHxlbnwxfHx8fDE3NzUzOTY5NDJ8MA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfGx1eHVyeSUyMGNvbmNlcnR8ZW58MXx8fHwxNzc1Mzk2OTQzfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzZWN1cml0eSUyMHRlYW18ZW58MXx8fHwxNzc1Mzk2OTQzfDA&ixlib=rb-4.1.0&q=80&w=1080"
        ]
    },
    "elon-musk": {
        "name": "Elon Musk",
        "management": "No Traditional Management (xAI / Tesla / SpaceX Teams)",
        "tagline": "Your Dream Moment with Elon Musk",
        "heroText": "Don't Miss Your Chance! Limited spots available for exclusive meet & greets, private time, and VIP experiences.",
        "stats": {
            "meetGreets": 320,
            "privateTime": 45,
            "ticketsSold": 12450,
            "fanCards": 15670
        },
        "bio": "Elon Musk is a visionary entrepreneur and engineer leading Tesla, SpaceX, xAI, and more. Known for pushing the boundaries of technology, space exploration, and sustainable energy, he inspires fans with bold ideas and direct communication.",
        "interests": ["Space Exploration", "Electric Vehicles", "AI Innovation", "Memes and Humor"],
        "heroImage": "https://img.freepik.com/premium-photo/elon-musk-portrait_895118-25088.jpg",
        "photos": [
            "https://i.ytimg.com/vi/cBAq21jErqo/maxresdefault.jpg",
            "https://images4.alphacoders.com/139/thumbbig-1391939.webp",
  "https://img.freepik.com/premium-photo/elon-musk-portrait_895118-25088.jpg",
  "https://images8.alphacoders.com/112/thumbbig-1128981.webp",
  "https://images6.alphacoders.com/138/thumbbig-1380868.webp",
  "https://images-prod.dazeddigital.com/1400/azure/dazed-prod/1340/3/1343778.jpg",
  "https://images8.alphacoders.com/112/thumbbig-1128980.webp",
  "https://images4.alphacoders.com/138/thumbbig-1380929.webp",
  
]
    },
    "carrie-underwood": {
        "name": "Carrie Underwood",
        "management": "Ann Edelblute",
        "tagline": "Your Dream Moment with Carrie Underwood",
        "heroText": "Don't Miss Your Chance! Limited spots available for exclusive meet & greets, private time, and VIP experiences.",
        "stats": {
            "meetGreets": 1890,
            "privateTime": 156,
            "ticketsSold": 34200,
            "fanCards": 8740
        },
        "bio": "Carrie Underwood is a multi-Grammy-winning country music superstar and American Idol winner, celebrated for her powerful vocals, dynamic performances, and heartfelt songs. She also runs successful wellness and fitness brands.",
        "interests": ["Country Music", "Fitness", "Animal Welfare", "Family Time"],
        "heroImage": "https://images.unsplash.com/photo-1507679799987-c73779560269?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb3VudHJ5JTIwc3RhZ2UlMjBwZXJmb3JtZXJ8ZW58MXx8fHwxNzc1Mzk2OTQxfDA&ixlib=rb-4.1.0&q=80&w=1080",
        "photos": [
            "https://images.unsplash.com/photo-1507679799987-c73779560269?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb3VudHJ5JTIwc3RhZ2UlMjBwZXJmb3JtZXJ8ZW58MXx8fHwxNzc1Mzk2OTQxfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1517841905240-4722065025b7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHJlZCUyMGNhcnBldCUyMGNvdW50cnl8ZW58MXx8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHZpcCUyMGJhY2tzdGFnZSUyMGNvdW50cnl8ZW58MXx8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfG1lZXQlMjBncmVldCUyMGNvdW50cnl8ZW58MXx8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfGx1eHVyeSUyMGNvdW50cnl8ZXZlbnR8ZW58MXx8fHwxNzc1Mzk2OTQzfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzZWN1cml0eSUyMGNvdW50cnl8ZW58MXx8fHwxNzc1Mzk2OTQzfDA&ixlib=rb-4.1.0&q=80&w=1080"
        ]
    },
    "george-strait": {
        "name": "George Strait",
        "management": "Erv Woolsey (Legacy) / Team",
        "tagline": "Your Dream Moment with the King of Country",
        "heroText": "Don't Miss Your Chance! Limited spots available for exclusive meet & greets, private time, and VIP experiences.",
        "stats": {
            "meetGreets": 980,
            "privateTime": 67,
            "ticketsSold": 45100,
            "fanCards": 12340
        },
        "bio": "George Strait, the King of Country, is a legendary singer, songwriter, and rancher with decades of chart-topping hits and traditional country sound. He remains deeply connected to his Texas roots, family, and fans.",
        "interests": ["Team Roping", "Ranching", "Golf", "Traditional Country Music"],
        "heroImage": "https://images.unsplash.com/photo-1507679799987-c73779560269?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb3VudHJ5JTIwc3RhZ2UlMjBsZWdlbmR8ZW58MXx8fHwxNzc1Mzk2OTQxfDA&ixlib=rb-4.1.0&q=80&w=1080",
        "photos": [
            "https://images.unsplash.com/photo-1507679799987-c73779560269?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb3VudHJ5JTIwc3RhZ2UlMjBsZWdlbmR8ZW58MXx8fHwxNzc1Mzk2OTQxfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1517841905240-4722065025b7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHJlZCUyMGNhcnBldCUyMGNvdW50cnl8ZW58MXx8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHZpcCUyMGNvdW50cnl8YmFja3N0YWdlfGVufDF8fHx8MTc3NTM5Njk0Mnww&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfG1lZXQlMjBncmVldCUyMGNvdW50cnl8ZW58MXx8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfGx1eHVyeSUyMGNvdW50cnl8cmFuY2h8ZW58MXx8fHwxNzc1Mzk2OTQzfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzZWN1cml0eSUyMGNvdW50cnl8ZW58MXx8fHwxNzc1Mzk2OTQzfDA&ixlib=rb-4.1.0&q=80&w=1080"
        ]
    },
    "semino-rossi": {
        "name": "Semino Rossi",
        "management": "Booking Office (booking@seminorossi.com)",
        "tagline": "Your Dream Moment with Semino Rossi",
        "heroText": "Don't Miss Your Chance! Limited spots available for exclusive meet & greets, private time, and VIP experiences.",
        "stats": {
            "meetGreets": 1120,
            "privateTime": 98,
            "ticketsSold": 18700,
            "fanCards": 5340
        },
        "bio": "Semino Rossi is an Argentine-Tyrolean schlager singer known for his romantic, passionate performances and Latin-influenced style. He has sold millions of records across Europe and delights fans with energetic yet emotional shows.",
        "interests": ["Schlager Music", "Latin Dance", "Travel", "Romantic Ballads"],
        "heroImage": "https://images.unsplash.com/photo-1507679799987-c73779560269?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHNjaGxhZ2VyJTIwc3RhZ2UlMjBwZXJmb3JtZXJ8ZW58MXx8fHwxNzc1Mzk2OTQxfDA&ixlib=rb-4.1.0&q=80&w=1080",
        "photos": [
            "https://images.unsplash.com/photo-1507679799987-c73779560269?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHNjaGxhZ2VyJTIwc3RhZ2UlMjBwZXJmb3JtZXJ8ZW58MXx8fHwxNzc1Mzk2OTQxfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1517841905240-4722065025b7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHJlZCUyMGNhcnBldCUyMHNjaGxhZ2VyfGVufDF8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHZpcCUyMGJhY2tzdGFnZSUyMHNjaGxhZ2VyfGVufDF8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfG1lZXQlMjBncmVldCUyMHNjaGxhZ2VyfGVufDF8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfGx1eHVyeSUyMHNjaGxhZ2VyJTIwZXZlbnR8ZW58MXx8fHwxNzc1Mzk2OTQzfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzZWN1cml0eSUyMHNjaGxhZ2VyfGVufDF8fHwxNzc1Mzk2OTQzfDA&ixlib=rb-4.1.0&q=80&w=1080"
        ]
    },
    "pedro-pascal": {
        "name": "Pedro Pascal",
        "management": "Anonymous Content (Former) / Team",
        "tagline": "Your Dream Moment with Pedro Pascal",
        "heroText": "Don't Miss Your Chance! Limited spots available for exclusive meet & greets, private time, and VIP experiences.",
        "stats": {
            "meetGreets": 670,
            "privateTime": 52,
            "ticketsSold": 15600,
            "fanCards": 9870
        },
        "bio": "Pedro Pascal is a Chilean-American actor known for starring roles in The Mandalorian, The Last of Us, Game of Thrones, and Narcos. He brings depth and charisma to every character and connects warmly with fans.",
        "interests": ["Acting", "Theater", "Family", "Chilean Heritage"],
        "heroImage": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHNhY3RvciUyMHJlZCUyMGNhcnBldHxlbnwxfHx8fDE3NzUzOTY5NDF8MA&ixlib=rb-4.1.0&q=80&w=1080",
        "photos": [
            "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHNhY3RvciUyMHJlZCUyMGNhcnBldHxlbnwxfHx8fDE3NzUzOTY5NDF8MA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1517841905240-4722065025b7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHJlZCUyMGNhcnBldCUyMGFjdG9yfGVufDF8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHZpcCUyMGJhY2tzdGFnZSUyMGFjdG9yfGVufDF8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfG1lZXQlMjBncmVldCUyMGFjdG9yfGVufDF8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfGx1eHVyeSUyMGV2ZW50JTIwYWN0b3J8ZW58MXx8fHwxNzc1Mzk2OTQzfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzZWN1cml0eSUyMHRlYW0lMjBhY3RvcnxlbnwxfHx8fDE3NzUzOTY5NDN8MA&ixlib=rb-4.1.0&q=80&w=1080"
        ]
    },
    "lukas-graham": {
        "name": "Lukas Graham",
        "management": "Then We Take The World / Lasse Siegismund & Kasper Færk",
        "tagline": "Your Dream Moment with Lukas Graham",
        "heroText": "Don't Miss Your Chance! Limited spots available for exclusive meet & greets, private time, and VIP experiences.",
        "stats": {
            "meetGreets": 1340,
            "privateTime": 87,
            "ticketsSold": 21300,
            "fanCards": 4560
        },
        "bio": "Lukas Graham is a Danish pop band led by singer Lukas Forchhammer, known for heartfelt hits like '7 Years'. They blend soulful vocals with personal storytelling drawn from life in Copenhagen.",
        "interests": ["Songwriting", "Family", "Live Performances", "Personal Growth"],
        "heroImage": "https://images.unsplash.com/photo-1507679799987-c73779560269?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHBvcCUyMHN0YWdlJTIwcGVyZm9ybWVyfGVufDF8fHx8MTc3NTM5Njk0MXww&ixlib=rb-4.1.0&q=80&w=1080",
        "photos": [
            "https://images.unsplash.com/photo-1507679799987-c73779560269?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHBvcCUyMHN0YWdlJTIwcGVyZm9ybWVyfGVufDF8fHwxNzc1Mzk2OTQxfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1517841905240-4722065025b7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHJlZCUyMGNhcnBldCUyMHBvcHxlbnwxfHx8fDE3NzUzOTY5NDJ8MA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHZpcCUyMGJhY2tzdGFnZSUyMHBvcHxlbnwxfHx8fDE3NzUzOTY5NDJ8MA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfG1lZXQlMjBncmVldCUyMHBvcHxlbnwxfHx8fDE3NzUzOTY5NDJ8MA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfGx1eHVyeSUyMHBvcCUyMGV2ZW50fGVufDF8fHwxNzc1Mzk2OTQzfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzZWN1cml0eSUyMHRlYW0lMjBwb3B8ZW58MXx8fHwxNzc1Mzk2OTQzfDA&ixlib=rb-4.1.0&q=80&w=1080"
        ]
    },
    "jonny-blu": {
        "name": "Jonny Blu",
        "management": "Jonny Blu Music / Dao Feng Music",
        "tagline": "Your Dream Moment with Jonny Blu",
        "heroText": "Don't Miss Your Chance! Limited spots available for exclusive meet & greets, private time, and VIP experiences.",
        "stats": {
            "meetGreets": 540,
            "privateTime": 76,
            "ticketsSold": 8900,
            "fanCards": 3120
        },
        "bio": "Jonny Blu is an American singer-songwriter and producer who became a pioneering pop star in China, blending Western styles with Mandarin pop. He performs in English and Mandarin with a unique fusion sound.",
        "interests": ["Mandarin Pop", "Songwriting", "Martial Arts", "World Music"],
        "heroImage": "https://images.unsplash.com/photo-1507679799987-c73779560269?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHBvcCUyMHN0YWdlJTIwcGVyZm9ybWVyfGVufDF8fHwxNzc1Mzk2OTQxfDA&ixlib=rb-4.1.0&q=80&w=1080",
        "photos": [
            "https://images.unsplash.com/photo-1507679799987-c73779560269?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHBvcCUyMHN0YWdlJTIwcGVyZm9ybWVyfGVufDF8fHwxNzc1Mzk2OTQxfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1517841905240-4722065025b7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHJlZCUyMGNhcnBldCUyMHBvcHxlbnwxfHx8fDE3NzUzOTY5NDJ8MA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHZpcCUyMGJhY2tzdGFnZSUyMHBvcHxlbnwxfHx8fDE3NzUzOTY5NDJ8MA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfG1lZXQlMjBncmVldCUyMHBvcHxlbnwxfHx8fDE3NzUzOTY5NDJ8MA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfGx1eHVyeSUyMHBvcCUyMGV2ZW50fGVufDF8fHwxNzc1Mzk2OTQzfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzZWN1cml0eSUyMHRlYW0lMjBwb3B8ZW58MXx8fHwxNzc1Mzk2OTQzfDA&ixlib=rb-4.1.0&q=80&w=1080"
        ]
    },
    "luke-bryan": {
        "name": "Luke Bryan",
        "management": "KP Entertainment (Kerri Edwards)",
        "tagline": "Your Dream Moment with Luke Bryan",
        "heroText": "Don't Miss Your Chance! Limited spots available for exclusive meet & greets, private time, and VIP experiences.",
        "stats": {
            "meetGreets": 2100,
            "privateTime": 134,
            "ticketsSold": 37800,
            "fanCards": 10250
        },
        "bio": "Luke Bryan is a multi-platinum country superstar known for high-energy performances, hits like 'Country Girl (Shake It For Me)', and his role as an American Idol judge. He loves connecting with fans on and off stage.",
        "interests": ["Country Music", "Farm Life", "Family", "American Idol"],
        "heroImage": "https://images.unsplash.com/photo-1507679799987-c73779560269?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfGNvdW50cnklMjBzdGFnZSUyMHBlcmZvcm1lcnxlbnwxfHx8fDE3NzUzOTY5NDF8MA&ixlib=rb-4.1.0&q=80&w=1080",
        "photos": [
            "https://images.unsplash.com/photo-1507679799987-c73779560269?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfGNvdW50cnklMjBzdGFnZSUyMHBlcmZvcm1lcnxlbnwxfHx8fDE3NzUzOTY5NDF8MA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1517841905240-4722065025b7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHJlZCUyMGNhcnBldCUyMGNvdW50cnl8ZW58MXx8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHZpcCUyMGJhY2tzdGFnZSUyMGNvdW50cnl8ZW58MXx8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfG1lZXQlMjBncmVldCUyMGNvdW50cnl8ZW58MXx8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfGx1eHVyeSUyMGNvdW50cnl8ZXZlbnR8ZW58MXx8fHwxNzc1Mzk2OTQzfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzZWN1cml0eSUyMGNvdW50cnl8ZW58MXx8fHwxNzc1Mzk2OTQzfDA&ixlib=rb-4.1.0&q=80&w=1080"
        ]
    },
    "cello-magician-thoren-bradley": {
        "name": "Cello Magician (Thoren Bradley)",
        "management": "Independent",
        "tagline": "Your Dream Moment with the Cello Magician",
        "heroText": "Don't Miss Your Chance! Limited spots available for exclusive meet & greets, private time, and VIP experiences.",
        "stats": {
            "meetGreets": 430,
            "privateTime": 65,
            "ticketsSold": 6700,
            "fanCards": 1890
        },
        "bio": "Thoren Bradley, known as the Cello Magician, is a unique musician blending classical cello with magical, theatrical performances that captivate audiences of all ages.",
        "interests": ["Cello Performance", "Magic & Theater", "Music Innovation", "Audience Interaction"],
        "heroImage": "https://images.unsplash.com/photo-1507679799987-c73779560269?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfGNlbGxvJTIwc3RhZ2UlMjBwZXJmb3JtZXJ8ZW58MXx8fHwxNzc1Mzk2OTQxfDA&ixlib=rb-4.1.0&q=80&w=1080",
        "photos": [
            "https://images.unsplash.com/photo-1507679799987-c73779560269?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfGNlbGxvJTIwc3RhZ2UlMjBwZXJmb3JtZXJ8ZW58MXx8fHwxNzc1Mzk2OTQxfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1517841905240-4722065025b7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHJlZCUyMGNhcnBldCUyMG11c2ljfGVufDF8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHZpcCUyMGJhY2tzdGFnZSUyMG11c2ljfGVufDF8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfG1lZXQlMjBncmVldCUyMG11c2ljfGVufDF8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfGx1eHVyeSUyMG11c2ljJTIwZXZlbnR8ZW58MXx8fHwxNzc1Mzk2OTQzfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzZWN1cml0eSUyMG11c2ljfGVufDF8fHwxNzc1Mzk2OTQzfDA&ixlib=rb-4.1.0&q=80&w=1080"
        ]
    },
    "savanah-rae-demers": {
        "name": "Savannah Rae Demers",
        "management": "Golden Hour Management",
        "tagline": "Your Dream Moment with Savannah Rae Demers",
        "heroText": "Don't Miss Your Chance! Limited spots available for exclusive meet & greets, private time, and VIP experiences.",
        "stats": {
            "meetGreets": 980,
            "privateTime": 143,
            "ticketsSold": 12400,
            "fanCards": 6780
        },
        "bio": "Savannah Rae Demers is a popular TikTok star and content creator known for comedy, lifestyle, and dance videos. With millions of followers, she brings fun, relatable energy and loves engaging directly with her audience.",
        "interests": ["Comedy Skits", "Dance", "Lifestyle Content", "Social Media Creation"],
        "heroImage": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHRpa3RvayUyMGNyZWF0b3IlMjByZWQlMjBjYXJwZXR8ZW58MXx8fHwxNzc1Mzk2OTQxfDA&ixlib=rb-4.1.0&q=80&w=1080",
        "photos": [
            "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHRpa3RvayUyMGNyZWF0b3IlMjByZWQlMjBjYXJwZXR8ZW58MXx8fHwxNzc1Mzk2OTQxfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1517841905240-4722065025b7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHJlZCUyMGNhcnBldCUyMGlubmx1ZW5jZXJ8ZW58MXx8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHZpcCUyMGJhY2tzdGFnZSUyMGlubmx1ZW5jZXJ8ZW58MXx8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfG1lZXQlMjBncmVldCUyMGlubmx1ZW5jZXJ8ZW58MXx8fHwxNzc1Mzk2OTQyfDA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfGx1eHVyeSUyMGlubmx1ZW5jZXIlMjBldmVudHxlbnwxfHx8fDE3NzUzOTY5NDN8MA&ixlib=rb-4.1.0&q=80&w=1080",
            "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzZWN1cml0eSUyMGlubmx1ZW5jZXJ8ZW58MXx8fHwxNzc1Mzk2OTQzfDA&ixlib=rb-4.1.0&q=80&w=1080"
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


# -------------------- BEFORE REQUEST: Tracking --------------------
@app.before_request
def track_page_view():
    if request.method == 'GET':
        path = request.path
        celeb_name = None
        if path.startswith('/celeb/'):
            parts = path.split('/')
            if len(parts) > 2:
                celeb_name = parts[2]
        elif path == '/':
            celeb_name = 'home'
        elif path.startswith('/admin'):
            celeb_name = 'admin'
        
        if celeb_name or path in ['/', '/legal', '/privacy', '/terms', '/cookies']:
            save_page_view(path, celeb_name)

# -------------------- ROUTES --------------------

@app.route('/')
def index():
    return render_template('index.html' , celeb_data=celeb_data)

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
    total_views = get_page_views_count()  # NEW
    db_session.close()

 
    return render_template('admin_dashboard.html', bookings=bookings, leads=leads, total_views=total_views)

@app.route('/admin/pageviews')
def admin_pageviews():
    if not session.get('admin_authenticated'):
        flash('Please login first', 'error')
        return redirect(url_for('admin'))
    
    db_session = SessionLocal()
    # Get all page views, newest first, limit to 500 for performance
    page_views = db_session.query(PageView)\
        .order_by(PageView.viewed_at.desc())\
        .limit(500).all()
    
    # Optional: count per celebrity/page
    from sqlalchemy import func
    celeb_stats = db_session.query(
        PageView.celeb_name,
        func.count(PageView.id).label('views')
    ).group_by(PageView.celeb_name)\
     .order_by(func.count(PageView.id).desc()).all()
    
    db_session.close()
    
    return render_template('admin_pageviews.html', 
                           page_views=page_views,
                           celeb_stats=celeb_stats)

@app.route('/admin/pageviews/data')
def admin_pageviews_data():
    if not session.get('admin_authenticated'):
        return jsonify({"error": "Unauthorized"}), 401
    
    db_session = SessionLocal()
    
    # Latest page views
    page_views = db_session.query(PageView)\
        .order_by(PageView.viewed_at.desc())\
        .limit(500).all()
    
    # Stats by celebrity/page
    from sqlalchemy import func
    celeb_stats = db_session.query(
        PageView.celeb_name.label('celeb_name'),
        func.count(PageView.id).label('count')
    ).group_by(PageView.celeb_name)\
     .order_by(func.count(PageView.id).desc()).all()
    
    total_views = db_session.query(PageView).count()
    
    db_session.close()

    # Convert to JSON-friendly format
    views_list = [{
        "viewed_at": v.viewed_at.strftime('%Y-%m-%d %H:%M:%S'),
        "path": v.path,
        "celeb_name": v.celeb_name,
        "ip_address": v.ip_address,
        "referrer": v.referrer,
        "user_agent": v.user_agent or ""
    } for v in page_views]

    stats_list = [{"celeb_name": s.celeb_name, "count": s.count} for s in celeb_stats]

    return jsonify({
        "total_views": total_views,
        "page_views": views_list,
        "celeb_stats": stats_list
    })

# NEW: Reset (delete all) page views
@app.route('/admin/pageviews/reset', methods=['POST'])
def reset_pageviews():
    if not session.get('admin_authenticated'):
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    
    try:
        db_session = SessionLocal()
        db_session.query(PageView).delete()
        db_session.commit()
        db_session.close()
        return jsonify({"success": True})
    except Exception as e:
        print("Reset error:", e)
        return jsonify({"success": False}), 500

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