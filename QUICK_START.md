# 🚀 TOGETHEROS - QUICK START

**5 minuten van download naar werkende app!**

---

## ⚡ SNELSTE WEG: Lokaal Testen (Windows)

1. **Download** de hele `togetheros` folder
2. **Dubbelklik** `start.bat`
3. **Open** browser: `http://localhost:5000`
4. **Registreer** een account
5. **Klaar!** ✅

---

## 🌐 SNELSTE WEG: Online Deploy (Render)

### Voorbereiding (5 min):
1. **GitHub account** aanmaken (als je die nog niet hebt)
2. **Render account** aanmaken op render.com (gratis)

### Upload naar GitHub (2 min):
```bash
cd togetheros
git init
git add .
git commit -m "TogetherOS initial commit"
git remote add origin https://github.com/JOUW_USERNAME/togetheros.git
git push -u origin main
```

### Deploy op Render (3 min):
1. **New +** → **Web Service**
2. **Connect** je GitHub repo
3. **Settings:**
   - Build Command: `./build.sh`
   - Start Command: `gunicorn app:app`
   - Python 3
4. **Environment Variables:**
   - Key: `SECRET_KEY`
   - Value: `python3 -c "import secrets; print(secrets.token_hex(32))"` (run dit en plak output)
5. **Create Web Service**
6. **Wacht 5 min** → LIVE! 🎉

---

## 📱 Installeer als App (iPhone/Android)

### iPhone:
- Safari → Open de URL
- Share icon → "Add to Home Screen"
- Done! Je hebt nu een app icon 💕

### Android:
- Chrome → Open de URL
- Menu (3 dots) → "Add to Home screen"
- Done! App geïnstalleerd 💕

---

## 👥 Partner Koppelen

1. **Jij:** Registreer account → Settings → "Genereer Invite Code"
2. **Kopieer** de code (bijv: `a8Kf2mPq`)
3. **Partner:** Registreer nieuw account → Voer code in
4. **Automatisch gekoppeld!** 🎉

Of andersom - partner genereert code, jij gebruikt die.

---

## 🎯 Eerste Stappen na Koppeling

**Direct beginnen:**
1. ✅ **Daily Check-in** → Mood & Energy loggen
2. 💕 **Stuur Appreciation** → Zeg iets liefs
3. 💬 **Deep Conversation** → Beantwoord een vraag samen
4. 🎯 **Bucket List** → Voeg iets toe dat jullie willen doen
5. ❤️ **Log een Date** → Laatste date loggen

**Build de gewoonte:**
- Dagelijks: Check-in + Appreciation
- Wekelijks: Deep Conversation + Date Night
- Maandelijks: Bekijk Stats & Bucket List progress

---

## 🐛 Problemen?

### App start niet lokaal:
```bash
# Check of Python geïnstalleerd is:
py --version

# Installeer dependencies:
py -m pip install -r requirements.txt

# Start opnieuw:
py app.py
```

### Deploy faalt op Render:
1. Check Logs tab in Render
2. Verify SECRET_KEY is ingesteld
3. Check dat build.sh executable is:
   ```bash
   chmod +x build.sh
   git add build.sh
   git commit -m "Fix permissions"
   git push
   ```

### Database weg na Render deploy:
- Render free tier = geen persistent storage
- Database reset bij elke deploy
- Upgrade naar Starter plan ($7/maand) voor persistent disk
- Of: gebruik PostgreSQL (instructies in README.md)

---

## 📚 Meer Info

- **README.md** → Complete feature lijst
- **DEPLOYMENT_GUIDE.md** → Gedetailleerde Render instructies
- **app.py** → Alle code met comments

---

## 🎉 Success Checklist

- [ ] App draait lokaal OF online
- [ ] Account geregistreerd
- [ ] Partner gekoppeld
- [ ] Eerste check-in gedaan
- [ ] Eerste appreciation verzonden
- [ ] PWA geïnstalleerd op telefoon
- [ ] Eerste date gelogd

**Als alle vakjes gecheckt → jullie zijn klaar!** 💕

---

**Vragen? Check de README.md!**

**Veel plezier met TogetherOS!** 🚀
