# 💕 TogetherOS - Complete Relationship Management Platform

**Een all-in-one web applicatie om je romantische relatie te versterken.**

---

## 🌟 Features

### 1. **Communicatie & Verbinding**
- ✅ Daily check-in met mood/energy tracking
- ✅ Deep conversation prompts (36 Questions to Fall in Love + meer)
- ✅ Appreciations systeem (complimenten, dankbaarheid, love notes)
- ✅ Conflict log met resolution tracking

### 2. **Kwaliteitstijd & Activiteiten**
- ✅ Date night generator met ideeën
- ✅ Date logger met ratings en foto's
- ✅ Bucket list manager
- ✅ Memory vault met tags
- ✅ Traditions tracker

### 3. **Love Languages & Groei**
- ✅ Love language quiz en tracking
- ✅ Mood/energy check-ins
- ✅ Shared growth goals
- ✅ Conflict resolution metrics

### 4. **Praktisch & Planning**
- ✅ Gedeelde kalender met recurring events
- ✅ Gift ideas wishlist
- ✅ Chores tracker met points systeem
- ✅ Financial goals met progress tracking

### 5. **Gamification & Fun**
- ✅ Relationship streak tracking
- ✅ Challenge systeem (30-day templates)
- ✅ Milestone detection
- ✅ Couple quiz (hoe goed ken je elkaar?)
- ✅ Analytics dashboard

---

## 🚀 Tech Stack

**Backend:**
- Flask 3.0 (Python)
- SQLite database
- Werkzeug password hashing
- Session-based authentication

**Frontend:**
- Vanilla HTML/CSS/JavaScript (NO frameworks)
- Jinja2 templating
- Mobile-first responsive design
- Dark mode pink/purple theme
- PWA ready (installeerbaar op iOS/Android)

**Deployment:**
- Render (free tier compatible)
- Gunicorn production server

---

## 📦 Local Development

### Vereisten:
- Python 3.8+

### Setup:

1. **Clone/download de code**

2. **Windows:**
   ```batch
   start.bat
   ```

3. **Mac/Linux:**
   ```bash
   python3 app.py
   ```

4. **Open browser:**
   ```
   http://localhost:5000
   ```

---

## 🌐 Deploy naar Render

### Stap 1: Maak een Render account
- Ga naar [render.com](https://render.com)
- Sign up (gratis)

### Stap 2: Nieuwe Web Service
1. Click "New +" → "Web Service"
2. Connect je GitHub repo (of upload code)
3. Configureer:
   - **Name:** `togetheros` (of jouw keuze)
   - **Environment:** Python 3
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free

### Stap 3: Environment Variables
Voeg toe in Render dashboard:
- **Key:** `SECRET_KEY`
- **Value:** [genereer random string, bijv: `openssl rand -hex 32`]

### Stap 4: Deploy!
- Click "Create Web Service"
- Wacht 5-10 minuten
- Je app is live! 🎉

---

## 📱 PWA Installatie (Mobile)

### iPhone:
1. Open de app in Safari
2. Klik op het "Share" icoontje
3. Scroll naar "Add to Home Screen"
4. Confirm

### Android:
1. Open de app in Chrome
2. Klik op de drie puntjes (menu)
3. "Add to Home screen"
4. Confirm

**Nu heb je een native app ervaring!** 💕

---

## 🔐 Gebruik

### Eerste Keer:
1. **Registreer** een account
2. **Genereer invite code** in Settings
3. **Deel code** met je partner
4. Partner **registreert met code**
5. Jullie zijn **automatisch gekoppeld**! 🎉

### Partner Koppeling Later:
- Ga naar Settings
- Genereer invite code
- Partner voert code in bij registratie
- OF: Partner genereert code en jij gebruikt die

---

## 🗄️ Database

SQLite database (`togetheros.db`) wordt automatisch aangemaakt bij eerste run.

**Tables:**
- users (accounts + partner linking)
- daily_checkins
- deep_conversations
- conversation_questions (pre-seeded)
- appreciations
- conflicts
- date_nights
- bucket_list
- traditions
- memories
- growth_goals
- calendar_events
- gift_ideas
- chores + chore_completions
- financial_goals
- challenges + challenge_logs
- milestones
- couple_quiz_questions + answers

---

## 🎨 Kleuren & Stijl

**Dark Mode Theme:**
- Primary: `#ff6b9d` (roze)
- Secondary: `#c06c84`
- Accent: `#f67280`
- Background: Gradient van `#1a0a2e` → `#16213e` → `#0f3460`
- Success: `#00d9a3`
- Danger: `#ff5252`

**Font:**
- System fonts (Apple/Android native)

---

## 📊 Analytics

De `/stats` route toont:
- Mood trend (laatste 30 dagen)
- Appreciation breakdown
- Date night frequency + avg rating
- Conflict resolution rate

---

## 🔧 Customization

### Eigen Conversation Questions Toevoegen:

Voeg toe in `seed_initial_data()` functie in `app.py`:

```python
questions = [
    ("Jouw vraag hier?", "category"),
    # ... meer vragen
]
```

### Eigen Challenge Templates:

Bewerk in de `/challenges` route:

```python
templates = [
    {"name": "Challenge naam", "description": "...", "duration": 30},
    # ... meer templates
]
```

---

## 🐛 Troubleshooting

### Database errors:
```bash
rm togetheros.db
python3 app.py  # Re-creates database
```

### Port already in use:
Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### Deploy issues op Render:
- Check logs in Render dashboard
- Verify `SECRET_KEY` environment variable is set
- Ensure `build.sh` has execute permissions

---

## 🚦 Roadmap / Future Ideas

**Mogelijk in volgende versie:**
- [ ] Photo upload voor memories en dates
- [ ] Push notifications (reminders)
- [ ] Export to PDF (relationship report)
- [ ] Mood/energy chart visualization
- [ ] Dark/light mode toggle
- [ ] Multi-language support
- [ ] Email notifications
- [ ] Shared notes/journal

---

## 📝 Credits

**Built by:** Niek (Quarius Digital)
**For:** Couples who want to strengthen their relationship
**Stack:** Flask + SQLite + Vanilla JS
**License:** MIT (use freely!)

---

## 💕 Support

Vragen? Bugs? Suggesties?
- Open een GitHub issue
- Of mail: [je email hier]

**Enjoy strengthening your relationship!** 🎉

---

**Pro Tip:** Gebruik de app dagelijks voor de beste resultaten. Consistentie is key! 🔥
