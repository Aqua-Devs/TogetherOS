import os
import sqlite3
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import base64

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

DATABASE = 'togetheros.db'

# ==================== DATABASE SETUP ====================

def get_db():
    """Get database connection with row factory"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize all database tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # USERS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            partner_id INTEGER,
            relationship_start_date DATE,
            love_language_primary TEXT,
            love_language_secondary TEXT,
            profile_photo BLOB,
            FOREIGN KEY (partner_id) REFERENCES users(id)
        )
    ''')
    
    # PARTNER INVITES TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS partner_invites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_user_id INTEGER NOT NULL,
            invite_code TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            used BOOLEAN DEFAULT 0,
            FOREIGN KEY (from_user_id) REFERENCES users(id)
        )
    ''')
    
    # DAILY CHECK-INS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date DATE NOT NULL,
            mood INTEGER CHECK(mood BETWEEN 1 AND 5),
            energy INTEGER CHECK(energy BETWEEN 1 AND 5),
            prompt_text TEXT,
            response_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, date)
        )
    ''')
    
    # DEEP CONVERSATIONS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deep_conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            couple_id TEXT NOT NULL,
            question_id INTEGER NOT NULL,
            question_text TEXT NOT NULL,
            user1_id INTEGER,
            user1_response TEXT,
            user1_answered_at TIMESTAMP,
            user2_id INTEGER,
            user2_response TEXT,
            user2_answered_at TIMESTAMP,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user1_id) REFERENCES users(id),
            FOREIGN KEY (user2_id) REFERENCES users(id)
        )
    ''')
    
    # CONVERSATION QUESTIONS BANK
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversation_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            category TEXT NOT NULL
        )
    ''')
    
    # APPRECIATIONS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appreciations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_user_id INTEGER NOT NULL,
            to_user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            read BOOLEAN DEFAULT 0,
            FOREIGN KEY (from_user_id) REFERENCES users(id),
            FOREIGN KEY (to_user_id) REFERENCES users(id)
        )
    ''')
    
    # CONFLICTS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conflicts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            couple_id TEXT NOT NULL,
            date_occurred DATE NOT NULL,
            topic TEXT NOT NULL,
            severity INTEGER CHECK(severity BETWEEN 1 AND 5),
            description TEXT,
            resolution_notes TEXT,
            resolved BOOLEAN DEFAULT 0,
            resolved_date DATE,
            lessons_learned TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # DATE NIGHTS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS date_nights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            couple_id TEXT NOT NULL,
            date DATE NOT NULL,
            activity_type TEXT,
            description TEXT NOT NULL,
            rating INTEGER CHECK(rating BETWEEN 1 AND 5),
            notes TEXT,
            photos BLOB,
            budget REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # BUCKET LIST
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bucket_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            couple_id TEXT NOT NULL,
            item TEXT NOT NULL,
            category TEXT,
            priority TEXT,
            completed BOOLEAN DEFAULT 0,
            completed_date DATE,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # TRADITIONS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS traditions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            couple_id TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            frequency TEXT,
            last_done DATE,
            times_done INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # MEMORIES
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            couple_id TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            date DATE,
            photos BLOB,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # GROWTH GOALS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS growth_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            couple_id TEXT NOT NULL,
            goal_text TEXT NOT NULL,
            category TEXT,
            target_date DATE,
            progress_notes TEXT,
            completed BOOLEAN DEFAULT 0,
            completed_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # CALENDAR EVENTS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calendar_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            couple_id TEXT NOT NULL,
            title TEXT NOT NULL,
            date DATE NOT NULL,
            type TEXT,
            recurring BOOLEAN DEFAULT 0,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # GIFT IDEAS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gift_ideas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            for_user_id INTEGER NOT NULL,
            added_by_user_id INTEGER NOT NULL,
            item TEXT NOT NULL,
            price_estimate REAL,
            url TEXT,
            priority TEXT,
            purchased BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (for_user_id) REFERENCES users(id),
            FOREIGN KEY (added_by_user_id) REFERENCES users(id)
        )
    ''')
    
    # CHORES
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            couple_id TEXT NOT NULL,
            task_name TEXT NOT NULL,
            assigned_to INTEGER,
            frequency TEXT,
            last_completed DATE,
            points INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (assigned_to) REFERENCES users(id)
        )
    ''')
    
    # CHORE COMPLETIONS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chore_completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chore_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            completed_date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chore_id) REFERENCES chores(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # FINANCIAL GOALS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS financial_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            couple_id TEXT NOT NULL,
            goal_name TEXT NOT NULL,
            target_amount REAL NOT NULL,
            current_amount REAL DEFAULT 0,
            target_date DATE,
            notes TEXT,
            completed BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # CHALLENGES
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            couple_id TEXT NOT NULL,
            challenge_name TEXT NOT NULL,
            description TEXT,
            start_date DATE NOT NULL,
            duration_days INTEGER NOT NULL,
            active BOOLEAN DEFAULT 1,
            completed BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # CHALLENGE LOGS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS challenge_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            challenge_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            date DATE NOT NULL,
            completed BOOLEAN DEFAULT 0,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (challenge_id) REFERENCES challenges(id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(challenge_id, user_id, date)
        )
    ''')
    
    # MILESTONES
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS milestones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            couple_id TEXT NOT NULL,
            milestone_type TEXT NOT NULL,
            threshold INTEGER NOT NULL,
            achieved_date DATE,
            celebrated BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # COUPLE QUIZ QUESTIONS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS couple_quiz_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            category TEXT
        )
    ''')
    
    # COUPLE QUIZ ANSWERS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS couple_quiz_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            about_self TEXT,
            about_partner TEXT,
            match BOOLEAN,
            date_answered DATE,
            FOREIGN KEY (question_id) REFERENCES couple_quiz_questions(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
    # Seed initial data
    seed_initial_data()

def seed_initial_data():
    """Seed conversation questions and quiz questions"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if already seeded
    cursor.execute('SELECT COUNT(*) FROM conversation_questions')
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    
    # Conversation Questions (36 Questions to Fall in Love + extras)
    questions = [
        # Getting to Know
        ("Als je iemand ter wereld zou kunnen kiezen, wie zou je dan als gasten aan tafel willen?", "getting_to_know"),
        ("Zou je beroemd willen zijn? Op welke manier?", "getting_to_know"),
        ("Oefen je ooit wat je gaat zeggen voordat je een telefoontje pleegt? Waarom?", "getting_to_know"),
        ("Wat zou een 'perfecte' dag voor je zijn?", "getting_to_know"),
        ("Wanneer heb je voor het laatst voor jezelf gezongen? Voor iemand anders?", "getting_to_know"),
        
        # Values & Beliefs
        ("Als je 90 zou worden en de keuze had tussen het mentale vermogen van een 30-jarige of het lichaam van een 30-jarige voor de laatste 60 jaar van je leven, wat zou je dan kiezen?", "values"),
        ("Heb je een geheim voorgevoel over hoe je zult sterven?", "values"),
        ("Noem drie dingen die jij en je partner gemeen lijken te hebben.", "values"),
        ("Voor wat in je leven voel je het meest dankbaar?", "values"),
        ("Als je iets aan de manier waarop je bent opgevoed zou kunnen veranderen, wat zou dat dan zijn?", "values"),
        
        # Future & Dreams
        ("Als je morgen wakker zou worden met een nieuwe kwaliteit of vaardigheid, wat zou je dan willen dat het was?", "future"),
        ("Als een kristallen bol je de waarheid over jezelf, je leven, de toekomst of iets anders zou kunnen vertellen, wat zou je dan willen weten?", "future"),
        ("Is er iets dat je al heel lang wilt doen? Waarom heb je het nog niet gedaan?", "future"),
        ("Wat is de grootste prestatie van je leven?", "future"),
        ("Wat waardeer je het meest in een vriendschap?", "future"),
        
        # Intimacy & Connection
        ("Wat is je meest dierbare herinnering?", "intimacy"),
        ("Wat is je meest verschrikkelijke herinnering?", "intimacy"),
        ("Als je wist dat je over een jaar plotseling zou sterven, zou je dan iets veranderen aan de manier waarop je nu leeft? Waarom?", "intimacy"),
        ("Wat betekent vriendschap voor jou?", "intimacy"),
        ("Welke rol spelen liefde en genegenheid in je leven?", "intimacy"),
        ("Deel iets dat je als een positieve eigenschap van je partner beschouwt. Deel vijf items.", "intimacy"),
        ("Hoe hecht en warm is jouw familie? Denk je dat je jeugd gelukkiger was dan die van de meeste mensen?", "intimacy"),
        ("Hoe voel je over je relatie met je moeder?", "intimacy"),
        ("Maak drie ware 'wij'-uitspraken. Bijvoorbeeld: 'We zijn beiden in deze kamer en voelen...'", "intimacy"),
        ("Maak deze zin af: 'Ik wou dat ik iemand had met wie ik kon delen...'", "intimacy"),
        ("Als je goede vrienden zou worden met je partner, deel dan wat belangrijk voor hem of haar zou zijn om te weten.", "intimacy"),
        ("Vertel je partner wat je leuk aan ze vindt; wees heel eerlijk en zeg dingen die je niet zou zeggen tegen iemand die je net hebt ontmoet.", "intimacy"),
        ("Deel met je partner een gênant moment in je leven.", "intimacy"),
        ("Wanneer heb je voor het laatst gehuild in het bijzijn van een ander? En alleen?", "intimacy"),
        ("Vertel je partner iets dat je nu al leuk aan ze vindt.", "intimacy"),
        ("Wat is te serieus om grappen over te maken, als dat überhaupt bestaat?", "intimacy"),
        ("Als je vanavond zou sterven zonder de kans om met iemand te communiceren, wat zou je dan het meest betreuren dat je niet hebt gezegd? Waarom heb je het ze nog niet verteld?", "intimacy"),
        ("Je huis staat in brand met al je bezittingen erin. Nadat je geliefden en huisdieren zijn gered, heb je tijd om veilig een laatste voorwerp te redden. Wat zou het zijn? Waarom?", "intimacy"),
        ("Van alle mensen in je familie, wiens dood zou je het meest pijnlijk vinden? Waarom?", "intimacy"),
        ("Deel een persoonlijk probleem en vraag je partner om advies over hoe hij of zij ermee om zou gaan. Vraag je partner ook om te spiegelen hoe je lijkt te voelen over het probleem dat je hebt gekozen.", "intimacy"),
    ]
    
    cursor.executemany('INSERT INTO conversation_questions (question_text, category) VALUES (?, ?)', questions)
    
    # Couple Quiz Questions
    quiz_questions = [
        ("Wat is mijn favoriete eten?", "basics"),
        ("Wat is mijn grootste angst?", "deep"),
        ("Wat is mijn droombaan?", "dreams"),
        ("Waar zou ik het liefst op vakantie gaan?", "preferences"),
        ("Wat is mijn lievelingsfilm?", "basics"),
        ("Wat doet me het meest ontspannen?", "preferences"),
        ("Wat is mijn grootste irritatiepunt?", "deep"),
        ("Hoe ga ik het liefst om met stress?", "deep"),
        ("Wat is mijn favoriete manier om tijd met jou door te brengen?", "relationship"),
        ("Wat is iets waar ik trots op ben maar niet vaak over praat?", "deep"),
        ("Wat is mijn love language?", "relationship"),
        ("Wat is mijn favoriete herinnnering van ons samen?", "relationship"),
        ("Wat maakt me het meest blij?", "deep"),
        ("Wat is iets dat ik wil leren of proberen?", "dreams"),
        ("Hoe ziet mijn perfecte vrije dag eruit?", "preferences"),
    ]
    
    cursor.executemany('INSERT INTO couple_quiz_questions (question_text, category) VALUES (?, ?)', quiz_questions)
    
    conn.commit()
    conn.close()

# ==================== HELPER FUNCTIONS ====================

def get_couple_id(user_id):
    """Get unique couple ID (sorted user IDs)"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT partner_id FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    if not result or not result['partner_id']:
        return None
    
    partner_id = result['partner_id']
    return '-'.join(map(str, sorted([user_id, partner_id])))

def get_partner_id(user_id):
    """Get partner ID for a user"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT partner_id FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result['partner_id'] if result else None

def has_partner(user_id):
    """Check if user has a partner"""
    return get_partner_id(user_id) is not None

def login_required(f):
    """Decorator for routes that require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Je moet ingelogd zijn om deze pagina te bekijken.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def partner_required(f):
    """Decorator for routes that require a partner"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Je moet ingelogd zijn om deze pagina te bekijken.', 'warning')
            return redirect(url_for('login'))
        if not has_partner(session['user_id']):
            flash('Je moet een partner koppelen om deze feature te gebruiken.', 'info')
            return redirect(url_for('settings'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email'].lower().strip()
        password = request.form['password']
        name = request.form['name']
        invite_code = request.form.get('invite_code', '').strip()
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if email exists
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            flash('Dit e-mailadres is al geregistreerd.', 'danger')
            conn.close()
            return redirect(url_for('register'))
        
        # Hash password and create user
        password_hash = generate_password_hash(password)
        cursor.execute('''
            INSERT INTO users (email, password_hash, name)
            VALUES (?, ?, ?)
        ''', (email, password_hash, name))
        user_id = cursor.lastrowid
        
        # Handle invite code if provided
        if invite_code:
            cursor.execute('''
                SELECT from_user_id FROM partner_invites 
                WHERE invite_code = ? AND used = 0
            ''', (invite_code,))
            invite = cursor.fetchone()
            
            if invite:
                partner_id = invite['from_user_id']
                
                # Link both users
                cursor.execute('UPDATE users SET partner_id = ? WHERE id = ?', (partner_id, user_id))
                cursor.execute('UPDATE users SET partner_id = ? WHERE id = ?', (user_id, partner_id))
                cursor.execute('UPDATE partner_invites SET used = 1 WHERE invite_code = ?', (invite_code,))
                
                flash(f'Account aangemaakt en gekoppeld aan je partner! 💕', 'success')
            else:
                flash('Account aangemaakt! Ongeldige invite code - je kunt later een partner koppelen.', 'warning')
        else:
            flash('Account aangemaakt! Koppel je partner in de instellingen.', 'success')
        
        conn.commit()
        conn.close()
        
        session['user_id'] = user_id
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].lower().strip()
        password = request.form['password']
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id, password_hash FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            flash('Welkom terug! ❤️', 'success')
            return redirect(url_for('dashboard'))
        
        flash('Ongeldige inloggegevens.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Je bent uitgelogd.', 'info')
    return redirect(url_for('login'))

# ==================== MAIN DASHBOARD ====================

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    conn = get_db()
    cursor = conn.cursor()
    
    # Get user info
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    
    stats = {}
    
    # Basic stats
    stats['has_partner'] = user['partner_id'] is not None
    
    if stats['has_partner']:
        couple_id = get_couple_id(user_id)
        
        # Days together
        if user['relationship_start_date']:
            start = datetime.strptime(user['relationship_start_date'], '%Y-%m-%d')
            stats['days_together'] = (datetime.now() - start).days
        else:
            stats['days_together'] = 0
        
        # Check-in streak
        cursor.execute('''
            SELECT date FROM daily_checkins 
            WHERE user_id = ? 
            ORDER BY date DESC
        ''', (user_id,))
        checkins = cursor.fetchall()
        streak = 0
        if checkins:
            current_date = datetime.now().date()
            for checkin in checkins:
                checkin_date = datetime.strptime(checkin['date'], '%Y-%m-%d').date()
                if checkin_date == current_date or checkin_date == current_date - timedelta(days=streak):
                    streak += 1
                    current_date = checkin_date
                else:
                    break
        stats['checkin_streak'] = streak
        
        # Unread appreciations
        cursor.execute('''
            SELECT COUNT(*) as count FROM appreciations 
            WHERE to_user_id = ? AND read = 0
        ''', (user_id,))
        stats['unread_appreciations'] = cursor.fetchone()['count']
        
        # Total appreciations sent
        cursor.execute('''
            SELECT COUNT(*) as count FROM appreciations 
            WHERE from_user_id = ?
        ''', (user_id,))
        stats['appreciations_sent'] = cursor.fetchone()['count']
        
        # Date nights count
        cursor.execute('''
            SELECT COUNT(*) as count FROM date_nights 
            WHERE couple_id = ?
        ''', (couple_id,))
        stats['date_nights'] = cursor.fetchone()['count']
        
        # Bucket list progress
        cursor.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as completed
            FROM bucket_list WHERE couple_id = ?
        ''', (couple_id,))
        bucket = cursor.fetchone()
        stats['bucket_total'] = bucket['total']
        stats['bucket_completed'] = bucket['completed'] or 0
        
        # Active challenges
        cursor.execute('''
            SELECT COUNT(*) as count FROM challenges 
            WHERE couple_id = ? AND active = 1
        ''', (couple_id,))
        stats['active_challenges'] = cursor.fetchone()['count']
        
        # Recent memories
        cursor.execute('''
            SELECT * FROM memories 
            WHERE couple_id = ? 
            ORDER BY created_at DESC LIMIT 3
        ''', (couple_id,))
        stats['recent_memories'] = cursor.fetchall()
        
        # Upcoming calendar events
        cursor.execute('''
            SELECT * FROM calendar_events 
            WHERE couple_id = ? AND date >= date('now')
            ORDER BY date ASC LIMIT 3
        ''', (couple_id,))
        stats['upcoming_events'] = cursor.fetchall()
        
    else:
        # No partner yet
        stats['days_together'] = 0
        stats['checkin_streak'] = 0
        stats['unread_appreciations'] = 0
        stats['appreciations_sent'] = 0
        stats['date_nights'] = 0
        stats['bucket_total'] = 0
        stats['bucket_completed'] = 0
        stats['active_challenges'] = 0
        stats['recent_memories'] = []
        stats['upcoming_events'] = []
    
    conn.close()
    
    return render_template('dashboard.html', user=user, stats=stats)

# ==================== SETTINGS & PARTNER LINKING ====================

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    user_id = session['user_id']
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'generate_invite':
            # Generate invite code
            invite_code = secrets.token_urlsafe(8)
            cursor.execute('''
                INSERT INTO partner_invites (from_user_id, invite_code)
                VALUES (?, ?)
            ''', (user_id, invite_code))
            conn.commit()
            flash(f'Invite code aangemaakt: {invite_code}', 'success')
        
        elif action == 'update_profile':
            name = request.form['name']
            relationship_start = request.form.get('relationship_start')
            love_primary = request.form.get('love_primary')
            love_secondary = request.form.get('love_secondary')
            
            cursor.execute('''
                UPDATE users SET 
                    name = ?,
                    relationship_start_date = ?,
                    love_language_primary = ?,
                    love_language_secondary = ?
                WHERE id = ?
            ''', (name, relationship_start, love_primary, love_secondary, user_id))
            conn.commit()
            flash('Profiel bijgewerkt!', 'success')
        
        elif action == 'unlink_partner':
            partner_id = get_partner_id(user_id)
            if partner_id:
                cursor.execute('UPDATE users SET partner_id = NULL WHERE id = ?', (user_id,))
                cursor.execute('UPDATE users SET partner_id = NULL WHERE id = ?', (partner_id,))
                conn.commit()
                flash('Partner ontkoppeld.', 'info')
    
    # Get user data
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    
    # Get partner data if linked
    partner = None
    if user['partner_id']:
        cursor.execute('SELECT * FROM users WHERE id = ?', (user['partner_id'],))
        partner = cursor.fetchone()
    
    # Get active invite codes
    cursor.execute('''
        SELECT invite_code, created_at FROM partner_invites 
        WHERE from_user_id = ? AND used = 0
        ORDER BY created_at DESC
    ''', (user_id,))
    invites = cursor.fetchall()
    
    conn.close()
    
    return render_template('settings.html', user=user, partner=partner, invites=invites)

# ==================== DAILY CHECK-IN ====================

@app.route('/checkin', methods=['GET', 'POST'])
@login_required
def checkin():
    user_id = session['user_id']
    conn = get_db()
    cursor = conn.cursor()
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    if request.method == 'POST':
        mood = request.form['mood']
        energy = request.form['energy']
        prompt = request.form['prompt']
        response = request.form['response']
        
        cursor.execute('''
            INSERT OR REPLACE INTO daily_checkins 
            (user_id, date, mood, energy, prompt_text, response_text)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, today, mood, energy, prompt, response))
        conn.commit()
        flash('Check-in opgeslagen! 🌟', 'success')
        return redirect(url_for('checkin'))
    
    # Check if already checked in today
    cursor.execute('''
        SELECT * FROM daily_checkins WHERE user_id = ? AND date = ?
    ''', (user_id, today))
    today_checkin = cursor.fetchone()
    
    # Get random prompt
    prompts = [
        "Wat was het hoogtepunt van je dag?",
        "Waar ben je vandaag dankbaar voor?",
        "Wat heeft je vandaag aan het lachen gemaakt?",
        "Wat heb je vandaag geleerd?",
        "Waarmee heb je vandaag geworsteld?",
        "Wat ga je morgen anders doen?",
        "Wat wil je delen met je partner?",
    ]
    import random
    prompt = random.choice(prompts)
    
    # Get recent check-ins
    cursor.execute('''
        SELECT * FROM daily_checkins 
        WHERE user_id = ? 
        ORDER BY date DESC LIMIT 7
    ''', (user_id,))
    recent_checkins = cursor.fetchall()
    
    conn.close()
    
    return render_template('checkin.html', 
                         today_checkin=today_checkin, 
                         prompt=prompt,
                         recent_checkins=recent_checkins)

# ==================== APPRECIATIONS ====================

@app.route('/appreciations', methods=['GET', 'POST'])
@partner_required
def appreciations():
    user_id = session['user_id']
    partner_id = get_partner_id(user_id)
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        message = request.form['message']
        category = request.form.get('category', 'gratitude')
        
        cursor.execute('''
            INSERT INTO appreciations (from_user_id, to_user_id, message, category)
            VALUES (?, ?, ?, ?)
        ''', (user_id, partner_id, message, category))
        conn.commit()
        flash('Appreciation verzonden! 💕', 'success')
        return redirect(url_for('appreciations'))
    
    # Mark all as read
    cursor.execute('UPDATE appreciations SET read = 1 WHERE to_user_id = ?', (user_id,))
    conn.commit()
    
    # Get received appreciations
    cursor.execute('''
        SELECT a.*, u.name as from_name 
        FROM appreciations a
        JOIN users u ON a.from_user_id = u.id
        WHERE a.to_user_id = ?
        ORDER BY a.created_at DESC
    ''', (user_id,))
    received = cursor.fetchall()
    
    # Get sent appreciations
    cursor.execute('''
        SELECT a.*, u.name as to_name 
        FROM appreciations a
        JOIN users u ON a.to_user_id = u.id
        WHERE a.from_user_id = ?
        ORDER BY a.created_at DESC
    ''', (user_id,))
    sent = cursor.fetchall()
    
    conn.close()
    
    return render_template('appreciations.html', received=received, sent=sent)

# ==================== DEEP CONVERSATIONS ====================

@app.route('/conversations')
@partner_required
def conversations():
    user_id = session['user_id']
    couple_id = get_couple_id(user_id)
    partner_id = get_partner_id(user_id)
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get answered conversations
    cursor.execute('''
        SELECT * FROM deep_conversations 
        WHERE couple_id = ?
        ORDER BY created_at DESC
    ''', (couple_id,))
    answered = cursor.fetchall()
    
    # Get available questions
    cursor.execute('''
        SELECT * FROM conversation_questions
        WHERE id NOT IN (
            SELECT question_id FROM deep_conversations WHERE couple_id = ?
        )
        ORDER BY RANDOM() LIMIT 10
    ''', (couple_id,))
    available = cursor.fetchall()
    
    conn.close()
    
    return render_template('conversations.html', 
                         answered=answered, 
                         available=available,
                         user_id=user_id,
                         partner_id=partner_id)

@app.route('/conversations/start/<int:question_id>')
@partner_required
def start_conversation(question_id):
    user_id = session['user_id']
    partner_id = get_partner_id(user_id)
    couple_id = get_couple_id(user_id)
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get question
    cursor.execute('SELECT * FROM conversation_questions WHERE id = ?', (question_id,))
    question = cursor.fetchone()
    
    # Create conversation
    cursor.execute('''
        INSERT INTO deep_conversations 
        (couple_id, question_id, question_text, user1_id, user2_id, category)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (couple_id, question_id, question['question_text'], user_id, partner_id, question['category']))
    
    conn.commit()
    conv_id = cursor.lastrowid
    conn.close()
    
    return redirect(url_for('answer_conversation', conv_id=conv_id))

@app.route('/conversations/answer/<int:conv_id>', methods=['GET', 'POST'])
@partner_required
def answer_conversation(conv_id):
    user_id = session['user_id']
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM deep_conversations WHERE id = ?', (conv_id,))
    conv = cursor.fetchone()
    
    if request.method == 'POST':
        response = request.form['response']
        
        # Determine which user is answering
        if conv['user1_id'] == user_id:
            cursor.execute('''
                UPDATE deep_conversations 
                SET user1_response = ?, user1_answered_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (response, conv_id))
        else:
            cursor.execute('''
                UPDATE deep_conversations 
                SET user2_response = ?, user2_answered_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (response, conv_id))
        
        conn.commit()
        flash('Antwoord opgeslagen! 💬', 'success')
        return redirect(url_for('conversations'))
    
    conn.close()
    
    return render_template('answer_conversation.html', conv=conv, user_id=user_id)

# ==================== CONFLICTS ====================

@app.route('/conflicts', methods=['GET', 'POST'])
@partner_required
def conflicts():
    couple_id = get_couple_id(session['user_id'])
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            topic = request.form['topic']
            severity = request.form['severity']
            description = request.form.get('description')
            date_occurred = request.form.get('date_occurred', datetime.now().strftime('%Y-%m-%d'))
            
            cursor.execute('''
                INSERT INTO conflicts (couple_id, date_occurred, topic, severity, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (couple_id, date_occurred, topic, severity, description))
            conn.commit()
            flash('Conflict gelogd. 📝', 'info')
        
        elif action == 'resolve':
            conflict_id = request.form['conflict_id']
            resolution = request.form['resolution']
            lessons = request.form.get('lessons')
            
            cursor.execute('''
                UPDATE conflicts 
                SET resolved = 1, resolved_date = ?, resolution_notes = ?, lessons_learned = ?
                WHERE id = ?
            ''', (datetime.now().strftime('%Y-%m-%d'), resolution, lessons, conflict_id))
            conn.commit()
            flash('Conflict opgelost! ✅', 'success')
        
        return redirect(url_for('conflicts'))
    
    # Get conflicts
    cursor.execute('''
        SELECT * FROM conflicts 
        WHERE couple_id = ?
        ORDER BY date_occurred DESC
    ''', (couple_id,))
    all_conflicts = cursor.fetchall()
    
    conn.close()
    
    return render_template('conflicts.html', conflicts=all_conflicts)

# ==================== DATE NIGHTS ====================

@app.route('/dates', methods=['GET', 'POST'])
@partner_required
def dates():
    couple_id = get_couple_id(session['user_id'])
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'log':
            description = request.form['description']
            date = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
            activity_type = request.form.get('activity_type')
            rating = request.form.get('rating')
            notes = request.form.get('notes')
            budget = request.form.get('budget')
            
            cursor.execute('''
                INSERT INTO date_nights 
                (couple_id, date, description, activity_type, rating, notes, budget)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (couple_id, date, description, activity_type, rating, notes, budget))
            conn.commit()
            flash('Date night gelogd! 🎉', 'success')
        
        return redirect(url_for('dates'))
    
    # Get date nights
    cursor.execute('''
        SELECT * FROM date_nights 
        WHERE couple_id = ?
        ORDER BY date DESC
    ''', (couple_id,))
    all_dates = cursor.fetchall()
    
    # Date ideas
    date_ideas = [
        {"activity": "Picknick in het park", "type": "outdoor", "budget": "low"},
        {"activity": "Kook samen een nieuw recept", "type": "indoor", "budget": "low"},
        {"activity": "Sterren kijken", "type": "outdoor", "budget": "free"},
        {"activity": "Game night thuis", "type": "indoor", "budget": "free"},
        {"activity": "Museum bezoek", "type": "cultural", "budget": "medium"},
        {"activity": "Spa dag", "type": "relaxation", "budget": "high"},
        {"activity": "Road trip", "type": "adventure", "budget": "medium"},
        {"activity": "Dans les samen", "type": "active", "budget": "medium"},
        {"activity": "Wine tasting", "type": "culinary", "budget": "high"},
        {"activity": "Wandeling bij zonsondergang", "type": "outdoor", "budget": "free"},
    ]
    
    conn.close()
    
    return render_template('dates.html', dates=all_dates, date_ideas=date_ideas)

# ==================== BUCKET LIST ====================

@app.route('/bucket-list', methods=['GET', 'POST'])
@partner_required
def bucket_list():
    couple_id = get_couple_id(session['user_id'])
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            item = request.form['item']
            category = request.form.get('category')
            priority = request.form.get('priority', 'medium')
            
            cursor.execute('''
                INSERT INTO bucket_list (couple_id, item, category, priority)
                VALUES (?, ?, ?, ?)
            ''', (couple_id, item, category, priority))
            conn.commit()
            flash('Item toegevoegd aan bucket list! 🎯', 'success')
        
        elif action == 'complete':
            item_id = request.form['item_id']
            notes = request.form.get('notes')
            
            cursor.execute('''
                UPDATE bucket_list 
                SET completed = 1, completed_date = ?, notes = ?
                WHERE id = ?
            ''', (datetime.now().strftime('%Y-%m-%d'), notes, item_id))
            conn.commit()
            flash('Gefeliciteerd! Item afgevinkt! 🎉', 'success')
        
        elif action == 'delete':
            item_id = request.form['item_id']
            cursor.execute('DELETE FROM bucket_list WHERE id = ?', (item_id,))
            conn.commit()
            flash('Item verwijderd.', 'info')
        
        return redirect(url_for('bucket_list'))
    
    # Get bucket list items
    cursor.execute('''
        SELECT * FROM bucket_list 
        WHERE couple_id = ?
        ORDER BY completed ASC, priority DESC, created_at DESC
    ''', (couple_id,))
    items = cursor.fetchall()
    
    conn.close()
    
    return render_template('bucket_list.html', items=items)

# ==================== MEMORIES ====================

@app.route('/memories', methods=['GET', 'POST'])
@partner_required
def memories():
    couple_id = get_couple_id(session['user_id'])
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description')
        date = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
        tags = request.form.get('tags')
        
        cursor.execute('''
            INSERT INTO memories (couple_id, title, description, date, tags)
            VALUES (?, ?, ?, ?, ?)
        ''', (couple_id, title, description, date, tags))
        conn.commit()
        flash('Memory opgeslagen! 💭', 'success')
        return redirect(url_for('memories'))
    
    # Get memories
    cursor.execute('''
        SELECT * FROM memories 
        WHERE couple_id = ?
        ORDER BY date DESC
    ''', (couple_id,))
    all_memories = cursor.fetchall()
    
    conn.close()
    
    return render_template('memories.html', memories=all_memories)

# ==================== TRADITIONS ====================

@app.route('/traditions', methods=['GET', 'POST'])
@partner_required
def traditions():
    couple_id = get_couple_id(session['user_id'])
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            name = request.form['name']
            description = request.form.get('description')
            frequency = request.form.get('frequency')
            
            cursor.execute('''
                INSERT INTO traditions (couple_id, name, description, frequency)
                VALUES (?, ?, ?, ?)
            ''', (couple_id, name, description, frequency))
            conn.commit()
            flash('Traditie toegevoegd! 🎊', 'success')
        
        elif action == 'log':
            tradition_id = request.form['tradition_id']
            cursor.execute('''
                UPDATE traditions 
                SET last_done = ?, times_done = times_done + 1
                WHERE id = ?
            ''', (datetime.now().strftime('%Y-%m-%d'), tradition_id))
            conn.commit()
            flash('Traditie gevierd! 🎉', 'success')
        
        return redirect(url_for('traditions'))
    
    cursor.execute('''
        SELECT * FROM traditions 
        WHERE couple_id = ?
        ORDER BY last_done DESC NULLS LAST
    ''', (couple_id,))
    all_traditions = cursor.fetchall()
    
    conn.close()
    
    return render_template('traditions.html', traditions=all_traditions)

# ==================== GROWTH GOALS ====================

@app.route('/growth-goals', methods=['GET', 'POST'])
@partner_required
def growth_goals():
    couple_id = get_couple_id(session['user_id'])
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            goal_text = request.form['goal_text']
            category = request.form.get('category')
            target_date = request.form.get('target_date')
            
            cursor.execute('''
                INSERT INTO growth_goals (couple_id, goal_text, category, target_date)
                VALUES (?, ?, ?, ?)
            ''', (couple_id, goal_text, category, target_date))
            conn.commit()
            flash('Groeidoel toegevoegd! 🌱', 'success')
        
        elif action == 'update':
            goal_id = request.form['goal_id']
            progress = request.form.get('progress')
            
            cursor.execute('''
                UPDATE growth_goals 
                SET progress_notes = ?
                WHERE id = ?
            ''', (progress, goal_id))
            conn.commit()
            flash('Voortgang bijgewerkt!', 'success')
        
        elif action == 'complete':
            goal_id = request.form['goal_id']
            cursor.execute('''
                UPDATE growth_goals 
                SET completed = 1, completed_date = ?
                WHERE id = ?
            ''', (datetime.now().strftime('%Y-%m-%d'), goal_id))
            conn.commit()
            flash('Doel behaald! 🎯', 'success')
        
        return redirect(url_for('growth_goals'))
    
    cursor.execute('''
        SELECT * FROM growth_goals 
        WHERE couple_id = ?
        ORDER BY completed ASC, target_date ASC NULLS LAST
    ''', (couple_id,))
    goals = cursor.fetchall()
    
    conn.close()
    
    return render_template('growth_goals.html', goals=goals)

# ==================== CALENDAR ====================

@app.route('/calendar', methods=['GET', 'POST'])
@partner_required
def calendar():
    couple_id = get_couple_id(session['user_id'])
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            title = request.form['title']
            date = request.form['date']
            event_type = request.form.get('type')
            recurring = request.form.get('recurring') == 'on'
            notes = request.form.get('notes')
            
            cursor.execute('''
                INSERT INTO calendar_events 
                (couple_id, title, date, type, recurring, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (couple_id, title, date, event_type, recurring, notes))
            conn.commit()
            flash('Event toegevoegd aan kalender! 📅', 'success')
        
        elif action == 'delete':
            event_id = request.form['event_id']
            cursor.execute('DELETE FROM calendar_events WHERE id = ?', (event_id,))
            conn.commit()
            flash('Event verwijderd.', 'info')
        
        return redirect(url_for('calendar'))
    
    cursor.execute('''
        SELECT * FROM calendar_events 
        WHERE couple_id = ?
        ORDER BY date ASC
    ''', (couple_id,))
    events = cursor.fetchall()
    
    conn.close()
    
    return render_template('calendar.html', events=events)

# ==================== GIFT IDEAS ====================

@app.route('/gifts', methods=['GET', 'POST'])
@partner_required
def gifts():
    user_id = session['user_id']
    partner_id = get_partner_id(user_id)
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            for_partner = request.form.get('for_partner') == 'on'
            for_user = partner_id if for_partner else user_id
            item = request.form['item']
            price = request.form.get('price')
            url = request.form.get('url')
            priority = request.form.get('priority', 'medium')
            
            cursor.execute('''
                INSERT INTO gift_ideas 
                (for_user_id, added_by_user_id, item, price_estimate, url, priority)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (for_user, user_id, item, price, url, priority))
            conn.commit()
            flash('Gift idee toegevoegd! 🎁', 'success')
        
        elif action == 'purchased':
            gift_id = request.form['gift_id']
            cursor.execute('UPDATE gift_ideas SET purchased = 1 WHERE id = ?', (gift_id,))
            conn.commit()
            flash('Gemarkeerd als gekocht!', 'success')
        
        return redirect(url_for('gifts'))
    
    # Get gifts for user
    cursor.execute('''
        SELECT g.*, u.name as added_by_name 
        FROM gift_ideas g
        JOIN users u ON g.added_by_user_id = u.id
        WHERE g.for_user_id = ?
        ORDER BY g.purchased ASC, g.priority DESC
    ''', (user_id,))
    for_me = cursor.fetchall()
    
    # Get gifts for partner
    cursor.execute('''
        SELECT g.*, u.name as added_by_name 
        FROM gift_ideas g
        JOIN users u ON g.added_by_user_id = u.id
        WHERE g.for_user_id = ?
        ORDER BY g.purchased ASC, g.priority DESC
    ''', (partner_id,))
    for_partner = cursor.fetchall()
    
    conn.close()
    
    return render_template('gifts.html', for_me=for_me, for_partner=for_partner)

# ==================== CHORES ====================

@app.route('/chores', methods=['GET', 'POST'])
@partner_required
def chores():
    user_id = session['user_id']
    partner_id = get_partner_id(user_id)
    couple_id = get_couple_id(user_id)
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            task_name = request.form['task_name']
            assigned_to = request.form.get('assigned_to')
            frequency = request.form.get('frequency')
            points = request.form.get('points', 1)
            
            cursor.execute('''
                INSERT INTO chores (couple_id, task_name, assigned_to, frequency, points)
                VALUES (?, ?, ?, ?, ?)
            ''', (couple_id, task_name, assigned_to, frequency, points))
            conn.commit()
            flash('Taak toegevoegd! 🧹', 'success')
        
        elif action == 'complete':
            chore_id = request.form['chore_id']
            today = datetime.now().strftime('%Y-%m-%d')
            
            cursor.execute('''
                INSERT INTO chore_completions (chore_id, user_id, completed_date)
                VALUES (?, ?, ?)
            ''', (chore_id, user_id, today))
            
            cursor.execute('''
                UPDATE chores SET last_completed = ? WHERE id = ?
            ''', (today, chore_id))
            
            conn.commit()
            flash('Taak voltooid! ✅', 'success')
        
        return redirect(url_for('chores'))
    
    # Get chores
    cursor.execute('''
        SELECT c.*, u.name as assigned_name 
        FROM chores c
        LEFT JOIN users u ON c.assigned_to = u.id
        WHERE c.couple_id = ?
        ORDER BY c.last_completed ASC NULLS FIRST
    ''', (couple_id,))
    all_chores = cursor.fetchall()
    
    # Get points scoreboard
    cursor.execute('''
        SELECT user_id, SUM(c.points) as total_points
        FROM chore_completions cc
        JOIN chores c ON cc.chore_id = c.id
        WHERE c.couple_id = ?
        GROUP BY user_id
    ''', (couple_id,))
    scoreboard = cursor.fetchall()
    
    # Get user info
    cursor.execute('SELECT id, name FROM users WHERE id IN (?, ?)', (user_id, partner_id))
    users = cursor.fetchall()
    
    conn.close()
    
    return render_template('chores.html', 
                         chores=all_chores, 
                         scoreboard=scoreboard,
                         users=users,
                         user_id=user_id,
                         partner_id=partner_id)

# ==================== FINANCIAL GOALS ====================

@app.route('/financial-goals', methods=['GET', 'POST'])
@partner_required
def financial_goals():
    couple_id = get_couple_id(session['user_id'])
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            goal_name = request.form['goal_name']
            target_amount = request.form['target_amount']
            current_amount = request.form.get('current_amount', 0)
            target_date = request.form.get('target_date')
            notes = request.form.get('notes')
            
            cursor.execute('''
                INSERT INTO financial_goals 
                (couple_id, goal_name, target_amount, current_amount, target_date, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (couple_id, goal_name, target_amount, current_amount, target_date, notes))
            conn.commit()
            flash('Financieel doel toegevoegd! 💰', 'success')
        
        elif action == 'update':
            goal_id = request.form['goal_id']
            amount = request.form['amount']
            
            cursor.execute('''
                UPDATE financial_goals 
                SET current_amount = current_amount + ?
                WHERE id = ?
            ''', (amount, goal_id))
            
            # Check if completed
            cursor.execute('''
                UPDATE financial_goals 
                SET completed = 1
                WHERE id = ? AND current_amount >= target_amount
            ''', (goal_id,))
            
            conn.commit()
            flash('Bedrag toegevoegd!', 'success')
        
        return redirect(url_for('financial_goals'))
    
    cursor.execute('''
        SELECT * FROM financial_goals 
        WHERE couple_id = ?
        ORDER BY completed ASC, target_date ASC NULLS LAST
    ''', (couple_id,))
    goals = cursor.fetchall()
    
    conn.close()
    
    return render_template('financial_goals.html', goals=goals)

# ==================== CHALLENGES ====================

@app.route('/challenges', methods=['GET', 'POST'])
@partner_required
def challenges():
    user_id = session['user_id']
    partner_id = get_partner_id(user_id)
    couple_id = get_couple_id(user_id)
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'start':
            challenge_name = request.form['challenge_name']
            description = request.form.get('description')
            duration = request.form.get('duration', 30)
            
            cursor.execute('''
                INSERT INTO challenges 
                (couple_id, challenge_name, description, start_date, duration_days)
                VALUES (?, ?, ?, ?, ?)
            ''', (couple_id, challenge_name, description, datetime.now().strftime('%Y-%m-%d'), duration))
            conn.commit()
            flash('Challenge gestart! 🚀', 'success')
        
        elif action == 'log':
            challenge_id = request.form['challenge_id']
            today = datetime.now().strftime('%Y-%m-%d')
            completed = request.form.get('completed') == 'on'
            notes = request.form.get('notes')
            
            cursor.execute('''
                INSERT OR REPLACE INTO challenge_logs 
                (challenge_id, user_id, date, completed, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (challenge_id, user_id, today, completed, notes))
            conn.commit()
            flash('Dag gelogd!', 'success')
        
        return redirect(url_for('challenges'))
    
    # Get active challenges
    cursor.execute('''
        SELECT * FROM challenges 
        WHERE couple_id = ? AND active = 1
        ORDER BY start_date DESC
    ''', (couple_id,))
    active = cursor.fetchall()
    
    # Get completed challenges
    cursor.execute('''
        SELECT * FROM challenges 
        WHERE couple_id = ? AND completed = 1
        ORDER BY start_date DESC
    ''', (couple_id,))
    completed_challenges = cursor.fetchall()
    
    # Challenge templates
    templates = [
        {"name": "30 Dagen Complimenteren", "description": "Geef elke dag een oprecht compliment", "duration": 30},
        {"name": "7 Dagen Date Nights", "description": "Elke avond quality time samen", "duration": 7},
        {"name": "30 Dagen Dankbaarheid", "description": "Deel dagelijks iets waar je dankbaar voor bent", "duration": 30},
        {"name": "14 Dagen Geen Telefoon", "description": "Geen schermen tijdens etenstijd", "duration": 14},
        {"name": "21 Dagen Actief Samen", "description": "Dagelijks samen bewegen", "duration": 21},
    ]
    
    conn.close()
    
    return render_template('challenges.html', 
                         active=active, 
                         completed=completed_challenges,
                         templates=templates)

# ==================== COUPLE QUIZ ====================

@app.route('/quiz', methods=['GET', 'POST'])
@partner_required
def quiz():
    user_id = session['user_id']
    partner_id = get_partner_id(user_id)
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        question_id = request.form['question_id']
        about_self = request.form.get('about_self')
        about_partner = request.form.get('about_partner')
        today = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute('''
            INSERT OR REPLACE INTO couple_quiz_answers 
            (question_id, user_id, about_self, about_partner, date_answered)
            VALUES (?, ?, ?, ?, ?)
        ''', (question_id, user_id, about_self, about_partner, today))
        conn.commit()
        
        # Check if partner answered too
        cursor.execute('''
            SELECT about_self FROM couple_quiz_answers 
            WHERE question_id = ? AND user_id = ?
        ''', (question_id, partner_id))
        partner_answer = cursor.fetchone()
        
        if partner_answer:
            # Check match
            match = about_partner.lower().strip() == partner_answer['about_self'].lower().strip()
            cursor.execute('''
                UPDATE couple_quiz_answers 
                SET match = ?
                WHERE question_id = ? AND user_id = ?
            ''', (match, question_id, user_id))
            conn.commit()
            
            if match:
                flash('Match! Je kent je partner goed! 💚', 'success')
            else:
                flash('Geen match - leer elkaar beter kennen! 💭', 'info')
        else:
            flash('Antwoord opgeslagen! Wacht op je partner.', 'info')
        
        return redirect(url_for('quiz'))
    
    # Get unanswered questions
    cursor.execute('''
        SELECT q.* FROM couple_quiz_questions q
        WHERE q.id NOT IN (
            SELECT question_id FROM couple_quiz_answers WHERE user_id = ?
        )
        ORDER BY RANDOM() LIMIT 5
    ''', (user_id,))
    unanswered = cursor.fetchall()
    
    # Get answered questions with results
    cursor.execute('''
        SELECT q.question_text, 
               a1.about_self as my_answer,
               a1.about_partner as my_guess,
               a2.about_self as partner_answer,
               a1.match
        FROM couple_quiz_answers a1
        JOIN couple_quiz_questions q ON a1.question_id = q.id
        LEFT JOIN couple_quiz_answers a2 ON a1.question_id = a2.question_id AND a2.user_id = ?
        WHERE a1.user_id = ?
        ORDER BY a1.date_answered DESC
    ''', (partner_id, user_id))
    answered = cursor.fetchall()
    
    conn.close()
    
    return render_template('quiz.html', unanswered=unanswered, answered=answered)

# ==================== ANALYTICS/STATS ====================

@app.route('/stats')
@partner_required
def stats():
    user_id = session['user_id']
    couple_id = get_couple_id(user_id)
    conn = get_db()
    cursor = conn.cursor()
    
    analytics = {}
    
    # Mood trend (last 30 days)
    cursor.execute('''
        SELECT date, AVG(mood) as avg_mood, AVG(energy) as avg_energy
        FROM daily_checkins
        WHERE user_id = ? AND date >= date('now', '-30 days')
        GROUP BY date
        ORDER BY date
    ''', (user_id,))
    analytics['mood_trend'] = cursor.fetchall()
    
    # Appreciation stats
    cursor.execute('''
        SELECT COUNT(*) as total,
               SUM(CASE WHEN category = 'compliment' THEN 1 ELSE 0 END) as compliments,
               SUM(CASE WHEN category = 'gratitude' THEN 1 ELSE 0 END) as gratitude,
               SUM(CASE WHEN category = 'love_note' THEN 1 ELSE 0 END) as love_notes
        FROM appreciations
        WHERE from_user_id = ?
    ''', (user_id,))
    analytics['appreciations'] = cursor.fetchone()
    
    # Date night frequency
    cursor.execute('''
        SELECT COUNT(*) as total, AVG(rating) as avg_rating
        FROM date_nights
        WHERE couple_id = ? AND date >= date('now', '-90 days')
    ''', (couple_id,))
    analytics['dates'] = cursor.fetchone()
    
    # Conflict resolution rate
    cursor.execute('''
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN resolved = 1 THEN 1 ELSE 0 END) as resolved
        FROM conflicts
        WHERE couple_id = ?
    ''', (couple_id,))
    analytics['conflicts'] = cursor.fetchone()
    
    conn.close()
    
    return render_template('stats.html', analytics=analytics)

# ==================== INIT APP ====================

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
