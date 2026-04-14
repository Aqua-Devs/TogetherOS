# 💕 TOGETHEROS - COMPLETE RELATIONSHIP OS

**Welkom bij TogetherOS - De ultieme web app om je romantische relatie te versterken!**

---

## 🚀 START HIER

**Nieuw hier? Begin met deze volgorde:**

1. 📖 **[QUICK_START.md](QUICK_START.md)** ← Begin hier! (5 min tot werkende app)
2. 📚 **[README.md](README.md)** ← Complete feature overzicht
3. 🗂️ **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** ← Wat zit waar?
4. ✅ **[FEATURE_CHECKLIST.md](FEATURE_CHECKLIST.md)** ← Alle 50+ features
5. 🌐 **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** ← Stap-voor-stap Render deploy

---

## ⚡ QUICK COMMANDS

### Lokaal Starten (Windows):
```batch
start.bat
```
Dan: `http://localhost:5000`

### Lokaal Starten (Mac/Linux):
```bash
python3 app.py
```
Dan: `http://localhost:5000`

### Deploy naar Render:
1. Push naar GitHub
2. Connect op Render.com
3. Add `SECRET_KEY` environment var
4. Deploy!

---

## 🎯 WAT ZIT ERIN?

**TogetherOS heeft 5 hoofdcategorieën met 50+ features:**

### 💬 **1. Communicatie & Verbinding**
- Daily check-in met mood/energy tracking
- Deep conversation prompts (36 Questions + meer)
- Appreciations (complimenten, dankbaarheid, love notes)
- Conflict log met resolution tracking

### ❤️ **2. Kwaliteitstijd & Activiteiten**
- Date night generator met ideeën
- Bucket list manager
- Activity logger voor dates
- Tradition tracker (rituelen)
- Memory vault met foto's en tags

### 🌱 **3. Love Languages & Groei**
- Love language quiz
- Shared growth goals
- Mood/energy analytics
- Relationship insights

### 📅 **4. Praktisch & Planning**
- Gedeelde kalender met events
- Gift wishlist voor elkaar
- Chores tracker met points
- Financial savings goals

### 🏆 **5. Gamification & Fun**
- Streak tracking (check-in)
- 30-day challenges (templates)
- Couple quiz ("hoe goed ken je elkaar?")
- Milestone systeem
- Points leaderboard

---

## 📁 PROJECT STRUCTUUR

```
togetheros/
├── 📄 app.py                    # Main Flask app (2200+ lines)
├── 📄 requirements.txt          # Dependencies
├── 📄 build.sh                  # Render build script
├── 📄 start.bat                 # Windows starter
├── 📄 .gitignore                # Git ignore
│
├── 📚 DOCUMENTATION
│   ├── INDEX.md                 # Dit bestand (start hier!)
│   ├── QUICK_START.md           # 5 min quick start
│   ├── README.md                # Complete docs
│   ├── DEPLOYMENT_GUIDE.md      # Render deploy guide
│   ├── PROJECT_STRUCTURE.md     # File overzicht
│   └── FEATURE_CHECKLIST.md     # Alle features
│
├── 📱 static/
│   └── manifest.json            # PWA config
│
└── 🎨 templates/ (23 files)
    ├── base.html                # Master template
    ├── login.html               # Auth pages
    ├── register.html
    ├── settings.html
    ├── dashboard.html           # Main screens
    ├── stats.html
    ├── checkin.html             # Daily features
    ├── appreciations.html
    ├── conversations.html       # Deep talks
    ├── conflicts.html
    ├── dates.html               # Activities
    ├── bucket_list.html
    ├── memories.html
    ├── traditions.html
    ├── growth_goals.html        # Planning
    ├── calendar.html
    ├── gifts.html
    ├── chores.html
    ├── financial_goals.html
    ├── challenges.html          # Gamification
    └── quiz.html
```

---

## 🎨 TECH STACK

**Backend:**
- Flask 3.0 (Python)
- SQLite (23 tables)
- Werkzeug (password hashing)
- Gunicorn (production)

**Frontend:**
- Vanilla HTML/CSS/JavaScript
- Jinja2 templating
- Mobile-first responsive
- Dark mode (pink/purple theme)
- PWA ready

**Deployment:**
- Render.com compatible
- Free tier supported
- Auto-deploy via GitHub

---

## 📊 STATISTIEKEN

- **Lines of Code:** ~3000
- **Features:** 50+
- **Routes:** 50+
- **Templates:** 23
- **Database Tables:** 23
- **Documentation:** 5 files
- **Total Files:** 35+

---

## 🚀 DEPLOYMENT OPTIES

### **Optie 1: Render (Aangeraden)**
- Gratis tier beschikbaar
- Auto-deploy via GitHub
- HTTPS included
- Stap-voor-stap guide in DEPLOYMENT_GUIDE.md

### **Optie 2: Lokaal (Testing)**
- Windows: `start.bat`
- Mac/Linux: `python3 app.py`
- Localhost op port 5000

### **Optie 3: Andere Platforms**
- Railway.app
- Fly.io
- PythonAnywhere
- DigitalOcean App Platform
- (alle werken met dezelfde config)

---

## 📱 MOBILE APP (PWA)

**Installeer als native app:**

### iPhone:
1. Safari → Open de app
2. Share → "Add to Home Screen"
3. Done! 🎉

### Android:
1. Chrome → Open de app
2. Menu → "Add to Home screen"
3. Done! 🎉

**Features:**
- Fullscreen mode (geen browser UI)
- App icon op home screen
- Offline capability (ready to implement)
- Native feel

---

## 🔐 BEVEILIGING

✅ Password hashing (bcrypt)
✅ Session-based auth
✅ SQL injection protection
✅ HTTPS (via Render)
✅ SECRET_KEY in environment vars
✅ No sensitive data in code

---

## 🎯 USE CASES

**Perfect voor:**
- 💑 Couples die meer verbinding willen
- 🌍 Long-distance relationships
- 💍 Engaged couples (wedding planning)
- 👫 Dating couples (elkaar beter leren kennen)
- 💕 Married couples (romance alive houden)

**Niet geschikt voor:**
- Business partnerships
- Friendships (kan wel, maar te romantic-focused)
- Familie relaties

---

## 🛠️ CUSTOMIZATION

**Makkelijk aan te passen:**
- ✅ Kleuren (CSS variables in base.html)
- ✅ Conversation questions (seed_initial_data in app.py)
- ✅ Challenge templates (challenges route)
- ✅ Date night ideeën (dates route)
- ✅ Quiz questions (seed_initial_data)

**Moeilijker:**
- Database schema wijzigen
- Authentication systeem
- PWA configuratie

---

## 📈 ROADMAP (Optioneel)

**Mogelijke uitbreidingen:**
- [ ] Echte foto upload UI
- [ ] Chart visualizations
- [ ] Email notifications
- [ ] Push notifications
- [ ] Dark/light mode toggle
- [ ] Export to PDF reports
- [ ] Multi-language support
- [ ] Social sharing
- [ ] Couple therapist portal

**Maar: Core app is 100% compleet!**

---

## 🐛 TROUBLESHOOTING

### App start niet:
```bash
# Check Python versie
python3 --version  # Moet 3.8+

# Installeer dependencies
pip install -r requirements.txt

# Start opnieuw
python3 app.py
```

### Deploy faalt:
1. Check Render logs
2. Verify SECRET_KEY is set
3. Check build.sh permissions
4. Lees DEPLOYMENT_GUIDE.md

### Database issues:
```bash
# Reset database
rm togetheros.db
python3 app.py  # Wordt opnieuw aangemaakt
```

---

## 💡 TIPS

**Voor beste ervaring:**
1. ✅ Gebruik dagelijks (check-in + appreciation)
2. ✅ Wekelijks deep conversation
3. ✅ Plan date nights regelmatig
4. ✅ Log je memories
5. ✅ Start challenges samen
6. ✅ Check stats om te zien hoe het gaat

**Consistentie is key!** 🔥

---

## 📞 SUPPORT

**Vragen?**
1. Check de 5 documentatie files
2. Lees comments in app.py
3. Google specifieke Flask/SQLite errors
4. GitHub Issues (als je repo hebt)

**Render specifiek:**
- [Render Docs](https://render.com/docs)
- [Community Forum](https://community.render.com)

---

## 🎉 KLAAR OM TE STARTEN?

**3 stappen:**
1. Open **QUICK_START.md**
2. Volg de instructies (5 min)
3. Begin jullie TogetherOS journey! 💕

---

## 📄 LICENSE

MIT License - Gebruik vrij!

Gebouwd door: **Niek (Quarius Digital)**
Voor: **Couples who want to strengthen their relationship**

---

## 🙏 CREDITS

**Geïnspireerd door:**
- 36 Questions to Fall in Love (Arthur Aron)
- The 5 Love Languages (Gary Chapman)
- Modern relationship psychology
- Duizenden couples die betere connectie willen

---

## 💕 FINAL MESSAGE

**TogetherOS is niet zomaar een app - het is een tool om:**
- Dagelijks te connecten
- Dieper te communiceren
- Mooie memories te maken
- Samen te groeien
- Fun te hebben
- Je relatie te versterken

**Begin vandaag. Jullie toekomst samen is worth it.** 🚀

---

**➡️ Volgende stap: Open [QUICK_START.md](QUICK_START.md)**
