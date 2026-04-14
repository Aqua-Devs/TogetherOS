# Script to create all remaining templates

templates = {
    "conversations.html": '''{% extends "base.html" %}
{% block title %}Conversations - TogetherOS{% endblock %}
{% block content %}
<div class="mt-2">
    <h2>💬 Deep Conversations</h2>
    
    <div class="card">
        <h3>Nieuwe Gesprekken</h3>
        {% if available|length > 0 %}
            {% for q in available %}
            <div style="padding: 0.75rem; background: rgba(255,255,255,0.05); border-radius: 8px; margin-bottom: 0.5rem;">
                <p>{{ q['question_text'] }}</p>
                <a href="/conversations/start/{{ q['id'] }}" class="btn btn-primary mt-1">Start Gesprek</a>
            </div>
            {% endfor %}
        {% else %}
            <p class="text-secondary">Alle vragen beantwoord! 🎉</p>
        {% endif %}
    </div>
    
    <div class="card mt-2">
        <h3>Beantwoorde Gesprekken</h3>
        {% if answered|length > 0 %}
            {% for conv in answered %}
            <div style="padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 8px; margin-bottom: 0.75rem;">
                <p><strong>{{ conv['question_text'] }}</strong></p>
                {% if conv['user1_response'] %}
                    <p class="mt-2 text-secondary">{{ conv['user1_response'] if conv['user1_id'] == user_id else conv['user2_response'] }}</p>
                {% endif %}
                {% if conv['user1_response'] and conv['user2_response'] %}
                    <a href="/conversations/answer/{{ conv['id'] }}" class="btn btn-secondary mt-2">Bekijk Beide Antwoorden</a>
                {% endif %}
            </div>
            {% endfor %}
        {% else %}
            <p class="text-secondary">Nog geen gesprekken beantwoord.</p>
        {% endif %}
    </div>
</div>
{% endblock %}''',

    "answer_conversation.html": '''{% extends "base.html" %}
{% block title %}Answer Conversation - TogetherOS{% endblock %}
{% block content %}
<div class="mt-2">
    <div class="card">
        <h3>{{ conv['question_text'] }}</h3>
        <form method="POST">
            <div class="form-group">
                <label>Jouw Antwoord</label>
                <textarea name="response" required></textarea>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Opslaan</button>
        </form>
    </div>
</div>
{% endblock %}''',

    "conflicts.html": '''{% extends "base.html" %}
{% block title %}Conflicts - TogetherOS{% endblock %}
{% block content %}
<div class="mt-2">
    <h2>🤝 Conflict Log</h2>
    
    <div class="card">
        <h3>Nieuw Conflict Loggen</h3>
        <form method="POST">
            <input type="hidden" name="action" value="add">
            <div class="form-group">
                <label>Onderwerp</label>
                <input type="text" name="topic" required>
            </div>
            <div class="form-group">
                <label>Severity (1-5)</label>
                <input type="range" name="severity" min="1" max="5" value="3" required>
            </div>
            <div class="form-group">
                <label>Beschrijving</label>
                <textarea name="description"></textarea>
            </div>
            <div class="form-group">
                <label>Datum</label>
                <input type="date" name="date_occurred">
            </div>
            <button type="submit" class="btn btn-primary btn-block">Loggen</button>
        </form>
    </div>
    
    <div class="card mt-2">
        <h3>Conflict Historie</h3>
        {% for conflict in conflicts %}
        <div style="padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 8px; margin-bottom: 0.75rem; {% if conflict['resolved'] %}border-left: 3px solid var(--success);{% else %}border-left: 3px solid var(--danger);{% endif %}">
            <p><strong>{{ conflict['topic'] }}</strong> {% if conflict['resolved'] %}✅{% else %}🔴{% endif %}</p>
            <p class="text-secondary">{{ conflict['date_occurred'] }} | Severity: {{ conflict['severity'] }}/5</p>
            {% if not conflict['resolved'] %}
            <form method="POST" class="mt-2">
                <input type="hidden" name="action" value="resolve">
                <input type="hidden" name="conflict_id" value="{{ conflict['id'] }}">
                <textarea name="resolution" placeholder="Hoe opgelost?" required></textarea>
                <textarea name="lessons" placeholder="Wat geleerd?" class="mt-1"></textarea>
                <button type="submit" class="btn btn-success mt-1">Markeer als Opgelost</button>
            </form>
            {% else %}
            <p class="mt-2">✅ Opgelost op {{ conflict['resolved_date'] }}</p>
            <p class="text-secondary">{{ conflict['resolution_notes'] }}</p>
            {% endif %}
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}''',

    "dates.html": '''{% extends "base.html" %}
{% block title %}Date Nights - TogetherOS{% endblock %}
{% block content %}
<div class="mt-2">
    <h2>❤️ Date Nights</h2>
    
    <div class="card">
        <h3>Date Night Generator</h3>
        <p class="text-secondary mb-2">Random date ideeën voor jullie:</p>
        <div class="grid grid-2">
            {% for idea in date_ideas[:4] %}
            <div style="padding: 0.75rem; background: rgba(255, 107, 157, 0.1); border-radius: 8px; text-align: center;">
                <p style="font-size: 0.9rem;">{{ idea['activity'] }}</p>
                <p class="text-secondary" style="font-size: 0.8rem;">{{ idea['type'] }} | {{ idea['budget'] }}</p>
            </div>
            {% endfor %}
        </div>
    </div>
    
    <div class="card mt-2">
        <h3>Log een Date Night</h3>
        <form method="POST">
            <input type="hidden" name="action" value="log">
            <div class="form-group">
                <label>Wat deden jullie?</label>
                <input type="text" name="description" required>
            </div>
            <div class="form-group">
                <label>Datum</label>
                <input type="date" name="date" required>
            </div>
            <div class="form-group">
                <label>Type</label>
                <select name="activity_type">
                    <option value="indoor">Indoor</option>
                    <option value="outdoor">Outdoor</option>
                    <option value="cultural">Cultural</option>
                    <option value="culinary">Culinary</option>
                    <option value="active">Active</option>
                    <option value="relaxation">Relaxation</option>
                </select>
            </div>
            <div class="form-group">
                <label>Rating (1-5)</label>
                <input type="range" name="rating" min="1" max="5" value="5">
            </div>
            <div class="form-group">
                <label>Notes</label>
                <textarea name="notes"></textarea>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Opslaan</button>
        </form>
    </div>
    
    <div class="card mt-2">
        <h3>Eerdere Dates</h3>
        {% for date in dates %}
        <div style="padding: 0.75rem; background: rgba(255,255,255,0.05); border-radius: 8px; margin-bottom: 0.5rem;">
            <p><strong>{{ date['description'] }}</strong> {% if date['rating'] %}{{ '⭐' * date['rating']|int }}{% endif %}</p>
            <p class="text-secondary" style="font-size: 0.9rem;">{{ date['date'] }}</p>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}''',

    "bucket_list.html": '''{% extends "base.html" %}
{% block title %}Bucket List - TogetherOS{% endblock %}
{% block content %}
<div class="mt-2">
    <h2>🎯 Bucket List</h2>
    
    <div class="card">
        <h3>Nieuw Item Toevoegen</h3>
        <form method="POST">
            <input type="hidden" name="action" value="add">
            <div class="form-group">
                <label>Wat willen jullie doen?</label>
                <input type="text" name="item" required>
            </div>
            <div class="form-group">
                <label>Categorie</label>
                <select name="category">
                    <option value="travel">✈️ Travel</option>
                    <option value="experience">🎭 Experience</option>
                    <option value="milestone">🏆 Milestone</option>
                    <option value="adventure">🚀 Adventure</option>
                </select>
            </div>
            <div class="form-group">
                <label>Prioriteit</label>
                <select name="priority">
                    <option value="high">🔥 High</option>
                    <option value="medium" selected>⚡ Medium</option>
                    <option value="low">💤 Low</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Toevoegen</button>
        </form>
    </div>
    
    <div class="card mt-2">
        <h3>Jullie Bucket List</h3>
        {% for item in items %}
        <div style="padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 8px; margin-bottom: 0.75rem; {% if item['completed'] %}opacity: 0.6; text-decoration: line-through;{% endif %}">
            <p><strong>{{ item['item'] }}</strong> {% if item['completed'] %}✅{% endif %}</p>
            <p class="text-secondary" style="font-size: 0.9rem;">{{ item['category'] }} | {{ item['priority'] }}</p>
            {% if not item['completed'] %}
            <form method="POST" class="mt-2">
                <input type="hidden" name="action" value="complete">
                <input type="hidden" name="item_id" value="{{ item['id'] }}">
                <textarea name="notes" placeholder="Hoe was het?" class="mt-1"></textarea>
                <button type="submit" class="btn btn-success mt-1">Afvinken!</button>
            </form>
            {% endif %}
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}''',

    "memories.html": '''{% extends "base.html" %}
{% block title %}Memories - TogetherOS{% endblock %}
{% block content %}
<div class="mt-2">
    <h2>💭 Memory Vault</h2>
    
    <div class="card">
        <h3>Nieuwe Memory</h3>
        <form method="POST">
            <div class="form-group">
                <label>Titel</label>
                <input type="text" name="title" required>
            </div>
            <div class="form-group">
                <label>Beschrijving</label>
                <textarea name="description"></textarea>
            </div>
            <div class="form-group">
                <label>Datum</label>
                <input type="date" name="date">
            </div>
            <div class="form-group">
                <label>Tags (komma gescheiden)</label>
                <input type="text" name="tags" placeholder="vakantie, verjaardag, special">
            </div>
            <button type="submit" class="btn btn-primary btn-block">Opslaan</button>
        </form>
    </div>
    
    <div class="card mt-2">
        <h3>Jullie Memories</h3>
        {% for memory in memories %}
        <div style="padding: 1rem; background: rgba(255, 107, 157, 0.1); border-radius: 12px; margin-bottom: 0.75rem;">
            <p><strong>{{ memory['title'] }}</strong></p>
            <p class="text-secondary" style="font-size: 0.9rem;">{{ memory['date'] }}</p>
            <p style="margin-top: 0.5rem;">{{ memory['description'] }}</p>
            {% if memory['tags'] %}
            <p style="font-size: 0.8rem; margin-top: 0.5rem; color: var(--accent);">🏷️ {{ memory['tags'] }}</p>
            {% endif %}
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}''',

    "traditions.html": '''{% extends "base.html" %}
{% block title %}Traditions - TogetherOS{% endblock %}
{% block content %}
<div class="mt-2">
    <h2>🎊 Traditions</h2>
    
    <div class="card">
        <h3>Nieuwe Traditie</h3>
        <form method="POST">
            <input type="hidden" name="action" value="add">
            <div class="form-group">
                <label>Naam</label>
                <input type="text" name="name" required>
            </div>
            <div class="form-group">
                <label>Beschrijving</label>
                <textarea name="description"></textarea>
            </div>
            <div class="form-group">
                <label>Frequentie</label>
                <select name="frequency">
                    <option value="daily">Dagelijks</option>
                    <option value="weekly">Wekelijks</option>
                    <option value="monthly">Maandelijks</option>
                    <option value="yearly">Jaarlijks</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Toevoegen</button>
        </form>
    </div>
    
    <div class="card mt-2">
        <h3>Jullie Tradities</h3>
        {% for trad in traditions %}
        <div style="padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 8px; margin-bottom: 0.75rem;">
            <p><strong>{{ trad['name'] }}</strong></p>
            <p class="text-secondary" style="font-size: 0.9rem;">{{ trad['frequency'] }} | {{ trad['times_done'] }}x gedaan</p>
            <p style="margin-top: 0.5rem;">{{ trad['description'] }}</p>
            <form method="POST" class="mt-2">
                <input type="hidden" name="action" value="log">
                <input type="hidden" name="tradition_id" value="{{ trad['id'] }}">
                <button type="submit" class="btn btn-secondary">Vandaag Gevierd! 🎉</button>
            </form>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}''',

    "growth_goals.html": '''{% extends "base.html" %}
{% block title %}Growth Goals - TogetherOS{% endblock %}
{% block content %}
<div class="mt-2">
    <h2>🌱 Growth Goals</h2>
    
    <div class="card">
        <h3>Nieuw Groeidoel</h3>
        <form method="POST">
            <input type="hidden" name="action" value="add">
            <div class="form-group">
                <label>Doel</label>
                <input type="text" name="goal_text" required>
            </div>
            <div class="form-group">
                <label>Categorie</label>
                <select name="category">
                    <option value="communication">💬 Communicatie</option>
                    <option value="intimacy">❤️ Intimiteit</option>
                    <option value="fun">🎉 Fun</option>
                    <option value="health">💪 Gezondheid</option>
                    <option value="finance">💰 Financieel</option>
                </select>
            </div>
            <div class="form-group">
                <label>Target Datum</label>
                <input type="date" name="target_date">
            </div>
            <button type="submit" class="btn btn-primary btn-block">Toevoegen</button>
        </form>
    </div>
    
    <div class="card mt-2">
        <h3>Doelen</h3>
        {% for goal in goals %}
        <div style="padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 8px; margin-bottom: 0.75rem; {% if goal['completed'] %}opacity: 0.6;{% endif %}">
            <p><strong>{{ goal['goal_text'] }}</strong> {% if goal['completed'] %}✅{% endif %}</p>
            <p class="text-secondary" style="font-size: 0.9rem;">{{ goal['category'] }}{% if goal['target_date'] %} | {{ goal['target_date'] }}{% endif %}</p>
            {% if goal['progress_notes'] %}
            <p style="margin-top: 0.5rem; font-size: 0.9rem;">{{ goal['progress_notes'] }}</p>
            {% endif %}
            {% if not goal['completed'] %}
            <div class="mt-2" style="display: flex; gap: 0.5rem;">
                <form method="POST" style="flex: 1;">
                    <input type="hidden" name="action" value="update">
                    <input type="hidden" name="goal_id" value="{{ goal['id'] }}">
                    <input type="text" name="progress" placeholder="Voortgang..." required>
                    <button type="submit" class="btn btn-secondary mt-1" style="width: 100%;">Update</button>
                </form>
                <form method="POST">
                    <input type="hidden" name="action" value="complete">
                    <input type="hidden" name="goal_id" value="{{ goal['id'] }}">
                    <button type="submit" class="btn btn-success mt-1">✓</button>
                </form>
            </div>
            {% endif %}
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}''',

    "calendar.html": '''{% extends "base.html" %}
{% block title %}Calendar - TogetherOS{% endblock %}
{% block content %}
<div class="mt-2">
    <h2>📅 Kalender</h2>
    
    <div class="card">
        <h3>Nieuw Event</h3>
        <form method="POST">
            <input type="hidden" name="action" value="add">
            <div class="form-group">
                <label>Titel</label>
                <input type="text" name="title" required>
            </div>
            <div class="form-group">
                <label>Datum</label>
                <input type="date" name="date" required>
            </div>
            <div class="form-group">
                <label>Type</label>
                <select name="type">
                    <option value="anniversary">💕 Anniversary</option>
                    <option value="birthday">🎂 Birthday</option>
                    <option value="date_night">🌹 Date Night</option>
                    <option value="reminder">⏰ Reminder</option>
                </select>
            </div>
            <div class="form-group">
                <label><input type="checkbox" name="recurring"> Jaarlijks herhalen</label>
            </div>
            <div class="form-group">
                <label>Notes</label>
                <textarea name="notes"></textarea>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Toevoegen</button>
        </form>
    </div>
    
    <div class="card mt-2">
        <h3>Events</h3>
        {% for event in events %}
        <div style="padding: 0.75rem; background: rgba(255,255,255,0.05); border-radius: 8px; margin-bottom: 0.5rem;">
            <p><strong>{{ event['title'] }}</strong></p>
            <p class="text-secondary" style="font-size: 0.9rem;">{{ event['date'] }} | {{ event['type'] }}</p>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}''',

    "gifts.html": '''{% extends "base.html" %}
{% block title %}Gift Ideas - TogetherOS{% endblock %}
{% block content %}
<div class="mt-2">
    <h2>🎁 Gift Ideas</h2>
    
    <div class="card">
        <h3>Nieuw Gift Idee</h3>
        <form method="POST">
            <input type="hidden" name="action" value="add">
            <div class="form-group">
                <label><input type="checkbox" name="for_partner"> Voor mijn partner</label>
            </div>
            <div class="form-group">
                <label>Item</label>
                <input type="text" name="item" required>
            </div>
            <div class="form-group">
                <label>Geschatte Prijs</label>
                <input type="number" name="price" step="0.01">
            </div>
            <div class="form-group">
                <label>URL</label>
                <input type="url" name="url">
            </div>
            <div class="form-group">
                <label>Prioriteit</label>
                <select name="priority">
                    <option value="high">High</option>
                    <option value="medium" selected>Medium</option>
                    <option value="low">Low</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Toevoegen</button>
        </form>
    </div>
    
    <div class="card mt-2">
        <h3>Voor Mij</h3>
        {% for gift in for_me %}
        <div style="padding: 0.75rem; background: rgba(255,255,255,0.05); border-radius: 8px; margin-bottom: 0.5rem; {% if gift['purchased'] %}opacity: 0.6;{% endif %}">
            <p><strong>{{ gift['item'] }}</strong> {% if gift['purchased'] %}✅{% endif %}</p>
            <p class="text-secondary" style="font-size: 0.9rem;">
                {% if gift['price_estimate'] %}€{{ gift['price_estimate'] }}{% endif %}
                | {{ gift['priority'] }}
            </p>
        </div>
        {% endfor %}
    </div>
    
    <div class="card mt-2">
        <h3>Voor Partner</h3>
        {% for gift in for_partner %}
        <div style="padding: 0.75rem; background: rgba(255,255,255,0.05); border-radius: 8px; margin-bottom: 0.5rem; {% if gift['purchased'] %}opacity: 0.6;{% endif %}">
            <p><strong>{{ gift['item'] }}</strong> {% if gift['purchased'] %}✅{% endif %}</p>
            <p class="text-secondary" style="font-size: 0.9rem;">
                {% if gift['price_estimate'] %}€{{ gift['price_estimate'] }}{% endif %}
                | {{ gift['priority'] }}
            </p>
            {% if not gift['purchased'] %}
            <form method="POST" class="mt-1">
                <input type="hidden" name="action" value="purchased">
                <input type="hidden" name="gift_id" value="{{ gift['id'] }}">
                <button type="submit" class="btn btn-success">Gekocht!</button>
            </form>
            {% endif %}
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}''',

    "chores.html": '''{% extends "base.html" %}
{% block title %}Chores - TogetherOS{% endblock %}
{% block content %}
<div class="mt-2">
    <h2>🧹 Chores</h2>
    
    <div class="card">
        <h3>📊 Scoreboard</h3>
        {% for score in scoreboard %}
        <div style="padding: 0.5rem; background: rgba(255,255,255,0.05); border-radius: 8px; margin-bottom: 0.5rem;">
            <p><strong>{% if score['user_id'] == user_id %}Jij{% else %}Partner{% endif %}:</strong> {{ score['total_points'] }} punten</p>
        </div>
        {% endfor %}
    </div>
    
    <div class="card mt-2">
        <h3>Nieuwe Taak</h3>
        <form method="POST">
            <input type="hidden" name="action" value="add">
            <div class="form-group">
                <label>Taak</label>
                <input type="text" name="task_name" required>
            </div>
            <div class="form-group">
                <label>Toegewezen aan</label>
                <select name="assigned_to">
                    <option value="">Niemand</option>
                    <option value="{{ user_id }}">Mij</option>
                    <option value="{{ partner_id }}">Partner</option>
                </select>
            </div>
            <div class="form-group">
                <label>Frequentie</label>
                <select name="frequency">
                    <option value="daily">Dagelijks</option>
                    <option value="weekly">Wekelijks</option>
                    <option value="monthly">Maandelijks</option>
                </select>
            </div>
            <div class="form-group">
                <label>Punten</label>
                <input type="number" name="points" value="1" min="1">
            </div>
            <button type="submit" class="btn btn-primary btn-block">Toevoegen</button>
        </form>
    </div>
    
    <div class="card mt-2">
        <h3>Taken</h3>
        {% for chore in chores %}
        <div style="padding: 0.75rem; background: rgba(255,255,255,0.05); border-radius: 8px; margin-bottom: 0.5rem;">
            <p><strong>{{ chore['task_name'] }}</strong> ({{ chore['points'] }} punten)</p>
            <p class="text-secondary" style="font-size: 0.9rem;">
                {{ chore['frequency'] }}
                {% if chore['assigned_name'] %} | Toegewezen aan: {{ chore['assigned_name'] }}{% endif %}
            </p>
            <form method="POST" class="mt-1">
                <input type="hidden" name="action" value="complete">
                <input type="hidden" name="chore_id" value="{{ chore['id'] }}">
                <button type="submit" class="btn btn-success">Voltooid!</button>
            </form>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}''',

    "financial_goals.html": '''{% extends "base.html" %}
{% block title %}Financial Goals - TogetherOS{% endblock %}
{% block content %}
<div class="mt-2">
    <h2>💰 Financial Goals</h2>
    
    <div class="card">
        <h3>Nieuw Spaardoel</h3>
        <form method="POST">
            <input type="hidden" name="action" value="add">
            <div class="form-group">
                <label>Doel</label>
                <input type="text" name="goal_name" required>
            </div>
            <div class="form-group">
                <label>Target Bedrag (€)</label>
                <input type="number" name="target_amount" step="0.01" required>
            </div>
            <div class="form-group">
                <label>Huidig Bedrag (€)</label>
                <input type="number" name="current_amount" step="0.01" value="0">
            </div>
            <div class="form-group">
                <label>Target Datum</label>
                <input type="date" name="target_date">
            </div>
            <button type="submit" class="btn btn-primary btn-block">Toevoegen</button>
        </form>
    </div>
    
    <div class="card mt-2">
        <h3>Spaardoelen</h3>
        {% for goal in goals %}
        <div style="padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 8px; margin-bottom: 0.75rem;">
            <p><strong>{{ goal['goal_name'] }}</strong> {% if goal['completed'] %}✅{% endif %}</p>
            <p class="text-secondary" style="font-size: 0.9rem;">€{{ goal['current_amount'] }} / €{{ goal['target_amount'] }}</p>
            <div class="progress mt-2">
                <div class="progress-bar" style="width: {{ (goal['current_amount'] / goal['target_amount'] * 100) if goal['target_amount'] > 0 else 0 }}%"></div>
            </div>
            {% if not goal['completed'] %}
            <form method="POST" class="mt-2">
                <input type="hidden" name="action" value="update">
                <input type="hidden" name="goal_id" value="{{ goal['id'] }}">
                <input type="number" name="amount" step="0.01" placeholder="Bedrag toevoegen" required>
                <button type="submit" class="btn btn-success mt-1">Toevoegen</button>
            </form>
            {% endif %}
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}''',

    "challenges.html": '''{% extends "base.html" %}
{% block title %}Challenges - TogetherOS{% endblock %}
{% block content %}
<div class="mt-2">
    <h2>🏆 Challenges</h2>
    
    <div class="card">
        <h3>Templates</h3>
        <div class="grid">
            {% for template in templates %}
            <div style="padding: 0.75rem; background: rgba(255, 107, 157, 0.1); border-radius: 8px;">
                <p><strong>{{ template['name'] }}</strong></p>
                <p class="text-secondary" style="font-size: 0.9rem;">{{ template['description'] }}</p>
                <p class="text-secondary" style="font-size: 0.8rem; margin-top: 0.5rem;">{{ template['duration'] }} dagen</p>
            </div>
            {% endfor %}
        </div>
    </div>
    
    <div class="card mt-2">
        <h3>Start Nieuwe Challenge</h3>
        <form method="POST">
            <input type="hidden" name="action" value="start">
            <div class="form-group">
                <label>Naam</label>
                <input type="text" name="challenge_name" required>
            </div>
            <div class="form-group">
                <label>Beschrijving</label>
                <textarea name="description"></textarea>
            </div>
            <div class="form-group">
                <label>Duur (dagen)</label>
                <input type="number" name="duration" value="30" min="1" required>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Start Challenge!</button>
        </form>
    </div>
    
    <div class="card mt-2">
        <h3>Actieve Challenges</h3>
        {% for ch in active %}
        <div style="padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 8px; margin-bottom: 0.75rem;">
            <p><strong>{{ ch['challenge_name'] }}</strong></p>
            <p class="text-secondary" style="font-size: 0.9rem;">{{ ch['description'] }}</p>
            <p style="font-size: 0.9rem; margin-top: 0.5rem;">Start: {{ ch['start_date'] }} | {{ ch['duration_days'] }} dagen</p>
            <form method="POST" class="mt-2">
                <input type="hidden" name="action" value="log">
                <input type="hidden" name="challenge_id" value="{{ ch['id'] }}">
                <label><input type="checkbox" name="completed"> Vandaag gedaan!</label>
                <textarea name="notes" placeholder="Notes..." class="mt-1"></textarea>
                <button type="submit" class="btn btn-success mt-1">Log Vandaag</button>
            </form>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}''',

    "quiz.html": '''{% extends "base.html" %}
{% block title %}Couple Quiz - TogetherOS{% endblock %}
{% block content %}
<div class="mt-2">
    <h2>🎯 Couple Quiz</h2>
    
    {% if unanswered|length > 0 %}
    <div class="card">
        <h3>Beantwoord de Vragen</h3>
        {% for q in unanswered %}
        <form method="POST" style="padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 8px; margin-bottom: 1rem;">
            <input type="hidden" name="question_id" value="{{ q['id'] }}">
            <p><strong>{{ q['question_text'] }}</strong></p>
            <div class="form-group mt-2">
                <label>Voor mezelf:</label>
                <input type="text" name="about_self" required>
            </div>
            <div class="form-group">
                <label>Voor mijn partner:</label>
                <input type="text" name="about_partner" required>
            </div>
            <button type="submit" class="btn btn-primary">Opslaan</button>
        </form>
        {% endfor %}
    </div>
    {% endif %}
    
    <div class="card mt-2">
        <h3>Resultaten</h3>
        {% for a in answered %}
        <div style="padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 8px; margin-bottom: 0.75rem; border-left: 3px solid {% if a['match'] %}var(--success){% else %}var(--danger){% endif %};">
            <p><strong>{{ a['question_text'] }}</strong></p>
            <p class="mt-2"><strong>Jouw antwoord:</strong> {{ a['my_answer'] }}</p>
            <p><strong>Jouw gok voor partner:</strong> {{ a['my_guess'] }}</p>
            {% if a['partner_answer'] %}
            <p><strong>Partner's antwoord:</strong> {{ a['partner_answer'] }}</p>
            <p class="mt-2 {% if a['match'] %}text-success{% else %}text-danger{% endif %}">
                {% if a['match'] %}✅ Match!{% else %}❌ Geen match{% endif %}
            </p>
            {% else %}
            <p class="text-secondary mt-2">Partner heeft nog niet geantwoord...</p>
            {% endif %}
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}''',

    "stats.html": '''{% extends "base.html" %}
{% block title %}Stats - TogetherOS{% endblock %}
{% block content %}
<div class="mt-2">
    <h2>📊 Analytics</h2>
    
    <div class="card">
        <h3>Mood Trend (30 dagen)</h3>
        <p class="text-secondary">Coming soon: mood chart</p>
    </div>
    
    <div class="card mt-2">
        <h3>Appreciation Stats</h3>
        <p>Totaal verzonden: {{ analytics['appreciations']['total'] }}</p>
        <p>Complimenten: {{ analytics['appreciations']['compliments'] }}</p>
        <p>Dankbaarheid: {{ analytics['appreciations']['gratitude'] }}</p>
    </div>
    
    <div class="card mt-2">
        <h3>Date Nights (90 dagen)</h3>
        <p>Totaal: {{ analytics['dates']['total'] }}</p>
        <p>Gemiddelde rating: {{ "%.1f"|format(analytics['dates']['avg_rating'] or 0) }}/5</p>
    </div>
    
    <div class="card mt-2">
        <h3>Conflict Resolution</h3>
        <p>Totaal: {{ analytics['conflicts']['total'] }}</p>
        <p>Opgelost: {{ analytics['conflicts']['resolved'] }}</p>
        {% if analytics['conflicts']['total'] > 0 %}
        <div class="progress mt-2">
            <div class="progress-bar" style="width: {{ (analytics['conflicts']['resolved'] / analytics['conflicts']['total'] * 100) }}%"></div>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}''',
}

import os

for filename, content in templates.items():
    filepath = f"/home/claude/togetheros/templates/{filename}"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {filename}")

print(f"\nTotal templates created: {len(templates)}")
