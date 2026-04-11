# 🎤 Elite Xperience — Celebrity Booking Platform

Elite Xperience is a full-stack web platform that allows users to book exclusive experiences with celebrities — including meet & greets, VIP access, private sessions, and more.

Built with **Flask + SQLAlchemy**, designed for scalability with **SQLite (dev)** and **PostgreSQL/Supabase (production)**.

---

## 🚀 Features

### 👥 User Side

* Browse celebrity landing pages
* Book experiences (meet & greet, VIP, private time, etc.)
* Submit partnership/contact messages
* Receive email confirmations

### 🛠 Admin Dashboard

* View all bookings
* Filter (All / Sent / Pending)
* Bulk email users
* Mark bookings as sent
* Delete entries
* View contact messages (Leads tab)
* Tab-based UI (Bookings / Messages)

### 📧 Email System

* Integrated with **Brevo (Sendinblue)**
* Sends:

  * Booking confirmation to users
  * Notification to admin
  * Bulk email from dashboard

### 🧠 Smart Architecture

* SQLite for local development
* PostgreSQL (Supabase/Railway) in production
* Easily switch via `DATABASE_URL`

---

## 🏗 Tech Stack

* **Backend:** Flask
* **Database:** SQLAlchemy ORM
* **Frontend:** HTML, CSS, JS
* **Email:** Brevo API
* **Deployment:** Railway
* **Optional Frontend Tooling:** Vite

---

## ⚙️ Installation (Local Setup)

### 1. Clone the repo

```bash
git clone https://github.com/DevEkpuchinwe/elitexperience.git
cd elitexperience
```

### 2. Create virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

```env
DATABASE_URL=sqlite:///local.db
SECRET_KEY=your-secret-key
BREVO_API_KEY=your-api-key
ADMIN_EMAIL=elitexperience.teams@gmail.com
SENDER_EMAIL=elitexperience.teams@gmail.com
REPLY_TO_EMAIL=elitexperience.teams@gmail.com
```

### 5. Run app

```bash
python app.py
```

---

## 🔐 Environment Variables

| Variable         | Description                       |
| ---------------- | --------------------------------- |
| `DATABASE_URL`   | SQLite (dev) or PostgreSQL (prod) |
| `SECRET_KEY`     | Flask session security            |
| `BREVO_API_KEY`  | Email API key                     |
| `ADMIN_EMAIL`    | Admin notification email          |
| `SENDER_EMAIL`   | Email sender                      |
| `REPLY_TO_EMAIL` | Reply email                       |

---

## 🧪 Database

### Development

Uses SQLite:

```env
DATABASE_URL=sqlite:///local.db
```

### Production (Railway / Supabase)

```env
DATABASE_URL=postgresql://user:password@host:5432/db
```

No code changes required ✅

---

## 🧑‍💼 Admin Access

Visit:

```
/admin
```

Default password:

```
admin123
```

⚠️ Change this in production.

---

## 🌍 Deployment (Railway)

### 1. Push to GitHub

```bash
git add .
git commit -m "deploy"
git push
```

### 2. Deploy on Railway

* Create new project
* Connect GitHub repo
* Add environment variables in Railway dashboard

### 3. Start command (if needed)

```bash
gunicorn app:app
```

---

## 📁 Project Structure

```
elitexperience/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
│
├── templates/
│   ├── index.html
│   ├── celeb.html
│   ├── booking.html
│   ├── success.html
│   ├── admin_dashboard.html
│   ├── admin_login.html
│
├── static/
│   ├── css/
│   ├── js/
│
└── local.db (ignored)
```

---

## 📩 Contact Integration

After booking success:

* WhatsApp support: **+1 912 548 3232**
* Telegram: **@elitexperience**

---

## 💬 Live Chat (Tawk.to)

To enable live chat, paste this before `</body>` in your base template:

```html
<script type="text/javascript">
var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
(function(){
var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
s1.async=true;
s1.src='https://embed.tawk.to/69d9ee6c83428a1c31aa69d5/1jltkmmi5';
s1.charset='UTF-8';
s1.setAttribute('crossorigin','*');
s0.parentNode.insertBefore(s1,s0);
})();
</script>
```

---

## ⚠️ Security Notes

* Never commit `.env`
* Use `.env.example` for sharing config
* Change admin password before production
* Use HTTPS in production

---

## 🔮 Future Improvements

* Payment integration (Stripe/Flutterwave)
* Real-time notifications
* Role-based admin system
* AI chatbot assistant
* Mobile app (Flutter integration)

---

## 👨‍💻 Author

**Ekpu Chinwe**
Software Developer

---

## ⭐ License

This project is for educational and commercial use.

---

## 💡 Final Note

This system is built to be **scalable, monetizable, and production-ready** — you can plug it into real celebrity management workflows or expand into a full marketplace.

---
