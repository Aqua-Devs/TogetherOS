# 📁 TOGETHEROS - PROJECT STRUCTURE

**Complete overzicht van alle bestanden en hun functie.**

---

## 🗂️ ROOT FILES

```
togetheros/
│
├── 📄 app.py                    # MAIN Flask applicatie (alle backend logic)
├── 📄 requirements.txt          # Python dependencies
├── 📄 build.sh                  # Render build script
├── 📄 start.bat                 # Windows local development starter
├── 📄 .gitignore                # Git ignore rules
│
├── 📄 README.md                 # Complete documentatie (lees dit eerst!)
├── 📄 DEPLOYMENT_GUIDE.md       # Stap-voor-stap Render deploy instructies
├── 📄 QUICK_START.md            # Snelste weg om te beginnen
├── 📄 PROJECT_STRUCTURE.md      # Dit bestand
│
└── 📄 create_remaining_templates.py  # Script gebruikt om templates te genereren (niet nodig voor productie)
```

---

## 🎨 TEMPLATES FOLDER

**Alle HTML templates (Jinja2):**

```
templates/
│
├── 📄 base.html                 # Master template (gebruikt door alle andere pages)
│
├── 🔐 AUTH
│   ├── login.html               # Login pagina
│   ├── register.html            # Registratie + partner invite code
│   └── settings.html            # Profiel, partner linking, logout
│
├── 📊 DASHBOARD
│   ├── dashboard.html           # Home screen met stats & quick actions
│   └── stats.html               # Analytics dashboard (mood trends, etc.)
│
├── 💬 CONNECT (Communicatie)
│   ├── checkin.html             # Daily check-in (mood + energy + prompt)
│   ├── appreciations.html       # Send & view love notes
│   ├── conversations.html       # Deep conversation prompts lijst
│   └── answer_conversation.html # Beantwoord specifieke vraag
│
├── ❤️ RELATIONSHIP
│   ├── conflicts.html           # Conflict log & resolution tracker
│   ├── dates.html               # Date night generator & logger
│   ├── bucket_list.html         # Shared bucket list manager
│   ├── memories.html            # Memory vault met tags
│   └── traditions.html          # Jullie rituelen & inside jokes
│
├── 🌱 GROWTH
│   └── growth_goals.html        # Shared relationship goals
│
├── 📅 PLANNING
│   ├── calendar.html            # Events & important dates
│   ├── gifts.html               # Gift wishlist voor elkaar
│   ├── chores.html              # Taak verdeling + points scoreboard
│   └── financial_goals.html     # Savings goals met progress bars
│
└── 🏆 FUN
    ├── challenges.html          # 30-day challenges + templates
    └── quiz.html                # Couple quiz ("hoe goed ken je elkaar?")
```

**Total: 23 templates**

---

## 📱 STATIC FOLDER

```
static/
│
└── 📄 manifest.json             # PWA manifest (voor app installatie)
```

**Nog toe te voegen (optioneel):**
- `icon-192.png` → App icon (192x192px)
- `icon-512.png` → App icon (512x512px)
- `style.css` → Extra custom CSS (alles zit nu in base.html)

---

## 🗄️ DATABASE (runtime)

**Wordt automatisch aangemaakt:**

```
togetheros.db                    # SQLite database (gitignored)
```

**23 Tables:**
1. `users` → Accounts + partner linking
2. `partner_invites` → Invite codes
3. `daily_checkins` → Mood + energy tracking
4. `deep_conversations` → Conversation instances
5. `conversation_questions` → Pre-seeded prompts (36 Questions + more)
6. `appreciations` → Love notes/compliments
7. `conflicts` → Conflict log
8. `date_nights` → Date logger
9. `bucket_list` → Shared dreams
10. `traditions` → Rituelen
11. `memories` → Photo/text vault
12. `growth_goals` → Relationship goals
13. `calendar_events` → Important dates
14. `gift_ideas` → Wishlist
15. `chores` → Taken
16. `chore_completions` → Completion log
17. `financial_goals` → Savings tracker
18. `challenges` → Active challenges
19. `challenge_logs` → Daily check-offs
20. `milestones` → Achievements
21. `couple_quiz_questions` → Quiz vragenbank
22. `couple_quiz_answers` → User responses
23. `milestones` → Auto-detected milestones

---

## 🔧 APP.PY STRUCTURE

**Main Flask file breakdown:**

```python
# IMPORTS
# DATABASE SETUP
    - get_db()
    - init_db()
    - seed_initial_data()

# HELPER FUNCTIONS
    - get_couple_id()
    - get_partner_id()
    - has_partner()
    - @login_required decorator
    - @partner_required decorator

# AUTH ROUTES
    - / (redirect)
    - /register
    - /login
    - /logout

# MAIN DASHBOARD
    - /dashboard (home screen)

# SETTINGS
    - /settings (profile + partner linking)

# DAILY CHECK-IN
    - /checkin

# APPRECIATIONS
    - /appreciations

# DEEP CONVERSATIONS
    - /conversations
    - /conversations/start/<id>
    - /conversations/answer/<id>

# CONFLICTS
    - /conflicts

# DATE NIGHTS
    - /dates

# BUCKET LIST
    - /bucket-list

# MEMORIES
    - /memories

# TRADITIONS
    - /traditions

# GROWTH GOALS
    - /growth-goals

# CALENDAR
    - /calendar

# GIFT IDEAS
    - /gifts

# CHORES
    - /chores

# FINANCIAL GOALS
    - /financial-goals

# CHALLENGES
    - /challenges

# COUPLE QUIZ
    - /quiz

# ANALYTICS
    - /stats

# APP RUNNER
    - if __name__ == '__main__'
```

**Total: 50+ routes, ~2200 lines of code**

---

## 🎯 KEY FEATURES PER FILE

### **app.py:**
- ✅ Complete auth systeem
- ✅ Partner invite systeem
- ✅ Multi-tenant (couples alleen hun eigen data)
- ✅ Database schema met foreign keys
- ✅ Pre-seeded content (36 Questions, quiz questions)
- ✅ Helper functions voor couple operations

### **base.html:**
- ✅ Mobile-first responsive design
- ✅ Dark mode gradient theme (roze/paars)
- ✅ Bottom navigation bar
- ✅ Flash messages systeem
- ✅ PWA meta tags
- ✅ Reusable card/button components

### **Dashboard:**
- ✅ Key metrics (days together, streaks, counts)
- ✅ Unread notifications
- ✅ Recent activity feed
- ✅ Quick actions

### **Settings:**
- ✅ Partner invite code generator
- ✅ Profile editor (love languages, start date)
- ✅ Unlink partner option

---

## 🚀 DEPLOYMENT FILES

### **requirements.txt:**
```
Flask==3.0.0
Werkzeug==3.0.1
gunicorn==21.2.0
```

### **build.sh:**
```bash
#!/bin/bash
pip install -r requirements.txt
```

### **start.bat (Windows):**
```batch
@echo off
py app.py
pause
```

---

## 📊 FILE SIZES (approximate)

```
app.py                  →  85 KB  (complete backend)
base.html               →  10 KB  (master template + styling)
Other templates         →  2-5 KB each
README.md               →  12 KB
DEPLOYMENT_GUIDE.md     →  8 KB
QUICK_START.md          →  4 KB
```

**Total project: ~200 KB** (zonder database)

---

## 🔄 DATA FLOW EXAMPLES

### **Partner Linking:**
```
User A → Settings → Generate Invite → Code: "a8Kf2mPq"
User B → Register → Enter code: "a8Kf2mPq"
System → Links users.partner_id both ways
Couple ID → "1-2" (sorted user IDs)
All couple data → Uses couple_id as foreign key
```

### **Daily Check-in:**
```
User → /checkin
Form → mood (1-5), energy (1-5), response to prompt
Submit → INSERT into daily_checkins
Streak calculation → Check consecutive dates
Dashboard → Update streak stat
```

### **Deep Conversation:**
```
User A → /conversations → Pick question
System → Creates conversation instance with couple_id
User A → Answers
User B → Sees same question → Answers
Both answered → Both can see each other's responses
```

---

## 🎨 STYLING SYSTEM

**CSS Variables (in base.html):**
```css
--primary: #ff6b9d      (roze)
--secondary: #c06c84    (mauve)
--accent: #f67280       (koraal)
--dark: #1a0a2e         (donker paars)
--success: #00d9a3      (groen)
--danger: #ff5252       (rood)
```

**Component Classes:**
- `.card` → Rounded container met blur effect
- `.btn-primary` → Gradient button
- `.stat-card` → Metric display box
- `.grid` → Responsive grid layout
- `.progress` → Progress bar component

---

## 🔐 SECURITY

**Password Hashing:**
- `Werkzeug.security` → bcrypt hashing
- Never stores plain passwords

**Session Management:**
- Flask sessions met SECRET_KEY
- Server-side session storage

**SQL Injection Protection:**
- Parameterized queries (`?` placeholders)
- No string concatenation in SQL

---

## 📱 PWA CONFIGURATION

**manifest.json:**
```json
{
  "name": "TogetherOS",
  "start_url": "/dashboard",
  "display": "standalone",
  "theme_color": "#ff6b9d"
}
```

**Meta tags (in base.html):**
```html
<meta name="apple-mobile-web-app-capable">
<meta name="theme-color">
<meta name="viewport" (mobile optimized)>
```

---

## 🛠️ CUSTOMIZATION GUIDE

### **Wijzig Kleuren:**
Edit `base.html` → `:root` CSS variables

### **Voeg Features Toe:**
1. Database: Add table in `init_db()`
2. Route: Add `@app.route()` in `app.py`
3. Template: Create HTML in `templates/`
4. Link: Update `base.html` bottom nav

### **Voeg Conversation Questions Toe:**
Edit `seed_initial_data()` in `app.py`:
```python
questions = [
    ("Nieuwe vraag?", "category"),
    # ... more
]
```

---

## 📈 PERFORMANCE

**Optimizations:**
- ✅ Single file app (fast startup)
- ✅ SQLite (no external DB needed)
- ✅ Vanilla JS (no framework overhead)
- ✅ Minimal dependencies (3 packages)
- ✅ CSS in base template (no extra requests)

**Bottlenecks (on Free Tier):**
- ❌ Cold starts (15 min inactivity)
- ❌ SQLite resets on redeploy
- ❌ Limited RAM (512 MB)

**Solutions:**
- Upgrade to paid plan ($7/mo)
- Or migrate to PostgreSQL

---

## 🎯 WHAT'S NOT INCLUDED (yet)

**Features je kunt toevoegen:**
- [ ] Photo upload (base64 in DB werkt, maar geen UI)
- [ ] Push notifications
- [ ] Email notifications
- [ ] Dark/light mode toggle
- [ ] Export to PDF
- [ ] Multi-language support
- [ ] Social sharing
- [ ] Relationship score algorithm

**Infrastructure:**
- [ ] PostgreSQL migration
- [ ] Redis caching
- [ ] CDN for assets
- [ ] Monitoring/alerting
- [ ] Automated backups

---

## 💡 TIPS

### **Development:**
- Edit templates → Auto-reload in Flask debug mode
- Database changes → Delete `togetheros.db` and restart
- CSS changes → Edit `base.html` → Refresh browser

### **Deployment:**
- Every git push → Auto-deploys on Render (if enabled)
- Check logs → Render dashboard → "Logs" tab
- Rollback → Render dashboard → "Manual Deploy" → Select old commit

### **Database:**
- Local: `sqlite3 togetheros.db` to inspect
- Remote: Download from Render (not available on free tier)

---

## 🎉 YOU'RE READY!

**Je hebt nu:**
- ✅ Complete codebase
- ✅ Alle features geïmplementeerd
- ✅ Deploy-ready configuratie
- ✅ Complete documentatie

**Next step:** Open QUICK_START.md en begin! 🚀

---

**Vragen? Alles staat in de docs!** 📚
