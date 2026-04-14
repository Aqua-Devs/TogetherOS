# 🚀 TogetherOS - Render Deployment Guide

**Complete stap-voor-stap instructies om TogetherOS live te krijgen.**

---

## 📋 Checklist voor je Start

- [ ] GitHub account (of Git repo)
- [ ] Render account (gratis op render.com)
- [ ] Code geüpload naar GitHub repository

---

## 🔧 Stap 1: Repository Voorbereiden

### Upload naar GitHub:

1. **Maak een nieuwe repository** op GitHub
   - Naam: bijv. `togetheros`
   - Public of Private (beide werken)

2. **Push je code:**
   ```bash
   cd togetheros
   git init
   git add .
   git commit -m "Initial commit - TogetherOS complete"
   git branch -M main
   git remote add origin https://github.com/JOUW_USERNAME/togetheros.git
   git push -u origin main
   ```

---

## 🌐 Stap 2: Render Setup

### Account Aanmaken:

1. Ga naar **[render.com](https://render.com)**
2. Sign up (gratis)
   - Kies "Sign up with GitHub" voor makkelijke integratie
   - Authorize Render om je repos te zien

---

## 🚀 Stap 3: Web Service Aanmaken

### In Render Dashboard:

1. **Click** "New +" in de top-right
2. **Selecteer** "Web Service"

### Repository Koppelen:

3. **Connect repository:**
   - Als je GitHub hebt gebruikt: klik op "Connect" bij je repo
   - Anders: klik "Public Git Repository" en plak de URL

### Service Configureren:

4. **Vul in:**
   
   **Basic Settings:**
   - **Name:** `togetheros` (of jouw gekozen naam)
   - **Region:** Europe (West) ← dichtst bij NL
   - **Branch:** `main`
   - **Root Directory:** (laat leeg)
   
   **Build & Deploy:**
   - **Runtime:** Python 3
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn app:app`
   
   **Plan:**
   - **Instance Type:** Free
   - **Auto-Deploy:** Yes (aangeraden)

5. **Click** "Advanced" om uit te klappen

---

## 🔐 Stap 4: Environment Variables

### Secret Key Genereren:

**Optie A - Op je computer (Mac/Linux):**
```bash
openssl rand -hex 32
```

**Optie B - Python:**
```python
python3 -c "import secrets; print(secrets.token_hex(32))"
```

**Optie C - Online:**
Ga naar [randomkeygen.com](https://randomkeygen.com/) en kopieer een "Fort Knox" key.

### Toevoegen in Render:

1. **Scroll** naar "Environment Variables" sectie
2. **Click** "Add Environment Variable"
3. **Vul in:**
   - **Key:** `SECRET_KEY`
   - **Value:** [je gegenereerde key]
4. **Click** "Save"

---

## 🎉 Stap 5: Deploy!

1. **Click** "Create Web Service" onderaan
2. **Wacht** 5-10 minuten terwijl Render:
   - Code download
   - Dependencies installeert (`build.sh`)
   - Server start (`gunicorn`)
3. **Check** de logs voor progress:
   - Klik op "Logs" tab
   - Moet eindigen met: `Booting worker with pid: ...`

---

## ✅ Stap 6: Eerste Test

### Je App is Live!

1. **URL vinden:**
   - In Render dashboard zie je: `https://togetheros.onrender.com`
   - Of: custom domain als je die hebt ingesteld

2. **Open de URL** in je browser

3. **Test registratie:**
   - Maak een account aan
   - Check of login werkt

4. **Test partner koppeling:**
   - Genereer invite code in Settings
   - Open in incognito/private venster
   - Registreer tweede account met code
   - Check of koppeling werkt

---

## 📱 Stap 7: PWA Installatie (Mobile App)

### Op iPhone:

1. Open `https://togetheros.onrender.com` in **Safari**
2. Klik op **Share icon** (vierkantje met pijl omhoog)
3. Scroll en klik **"Add to Home Screen"**
4. Pas naam aan (optioneel)
5. Klik **"Add"**
6. Je hebt nu een app icon! 🎉

### Op Android:

1. Open de URL in **Chrome**
2. Klik op **3 puntjes** menu (top-right)
3. Klik **"Add to Home screen"**
4. Confirm
5. App icon verschijnt! 🎉

---

## 🔧 Troubleshooting

### "Application Error" op Render:

**Check deze dingen:**

1. **Logs bekijken:**
   - Render Dashboard → je service → "Logs" tab
   - Lees de error messages

2. **Build.sh permissions:**
   ```bash
   chmod +x build.sh
   git add build.sh
   git commit -m "Fix build.sh permissions"
   git push
   ```

3. **Requirements.txt:**
   - Verify dat het bestand bestaat
   - Check spelling van packages

4. **SECRET_KEY:**
   - Ga naar "Environment" tab
   - Verify dat `SECRET_KEY` is ingesteld
   - Als niet: add it

### Database Issues:

**Render free tier heeft geen persistent storage!**
- Database wordt reset bij elke nieuwe deploy
- Voor production: gebruik Render PostgreSQL (betaald)
- Of: gebruik externe database (Supabase, PlanetScale)

**Workaround voor nu:**
- Elke deploy = fresh database
- Acceptabel voor testing
- Upgrade naar paid plan voor persistent SQLite
- Of migreer naar PostgreSQL

### Slow Cold Starts:

Free tier services "slapen" na 15 min inactiviteit.

**Gevolg:**
- Eerste request na inactiviteit = 30-60 sec load time
- Daarna = snel

**Oplossing:**
- Upgrade naar paid plan ($7/maand = altijd actief)
- Of: accepteer de cold starts

---

## 🎨 Custom Domain (Optioneel)

### Je eigen domeinnaam gebruiken:

1. **Koop een domain** (bijv. via Namecheap, Google Domains)
2. **In Render:**
   - Ga naar je service
   - Click "Settings" tab
   - Scroll naar "Custom Domain"
   - Click "Add Custom Domain"
   - Voer in: `www.togetheros.nl` (bijvoorbeeld)
3. **In je domain registrar:**
   - Voeg CNAME record toe:
     - Name: `www`
     - Value: `togetheros.onrender.com`
4. **Wacht** 5-60 minuten voor DNS propagation
5. **Done!** Je app is bereikbaar via jouw domein

---

## 📊 Monitoring & Logs

### Live Logs Bekijken:

1. **Render Dashboard** → je service
2. **Click** "Logs" tab
3. **Live stream** van server logs
4. **Filter** op errors: zoek naar `ERROR` in logs

### Metrics (Paid Plans):

- CPU usage
- Memory usage
- Request count
- Response times

---

## 💰 Kosten

### Free Tier:
- **Prijs:** €0/maand
- **Limits:**
  - 750 uur/maand (= 31.25 dagen)
  - Cold starts na 15 min inactiviteit
  - 512 MB RAM
  - 0.1 CPU
- **Perfect voor:** Testing, personal use, prototypes

### Starter ($7/maand):
- **Voordelen:**
  - Altijd actief (geen cold starts)
  - 512 MB RAM
  - Persistent disk storage (voor SQLite)
- **Aangeraden voor:** 2-10 couples

### Standard ($25/maand):
- 2 GB RAM
- Meer CPU
- Voor: 10+ couples

---

## 🔒 Beveiliging Tips

### Environment Variables:

**NOOIT in code:**
```python
# ❌ FOUT:
app.secret_key = 'mijn_geheime_sleutel_hier'

# ✅ GOED:
app.secret_key = os.environ.get('SECRET_KEY')
```

### HTTPS:

- Render geeft **automatisch HTTPS**
- Je app is altijd encrypted
- Geen extra configuratie nodig

### Database:

- Huidige SQLite = niet persistent op free tier
- Upgrade of gebruik externe DB voor production

---

## 🚀 Next Steps

**Na succesvolle deployment:**

1. **Test alle features**
   - Maak test accounts
   - Probeer elk feature uit
   - Check mobile responsiveness

2. **Invite je partner**
   - Genereer invite code
   - Laat partner registreren
   - Begin jullie reis! 💕

3. **Monitor logs**
   - Check logs eerste dagen
   - Fix eventuele bugs

4. **Feedback verzamelen**
   - Gebruik het zelf
   - Noteer verbeteringen
   - Itereer!

---

## 📞 Support

### Render Support:

- [Render Docs](https://render.com/docs)
- [Community Forum](https://community.render.com)
- [Status Page](https://status.render.com)

### TogetherOS Issues:

- GitHub Issues op je repo
- Of: mail naar [je email]

---

## 🎉 Success!

**Je app is nu live!** 🚀

Share de URL met je partner en begin jullie TogetherOS journey! 💕

---

**Questions? Check README.md voor meer info.**
