from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify
import os
import secrets
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(16))
vercel_app = app

# Identifiants admin
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "campaign2024"

# Fichier pour stocker les données
DATA_FILE = 'campaign_data.json'

# Initialiser les données
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'total': 5000}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Page principale
CAMPAIGN_PAGE = '''
<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>حملة الخير 2 - رمضان 2026</title>
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: 'Tahoma', Arial, sans-serif;
    direction: rtl;
    text-align: center;
    color: white;
    background: linear-gradient(135deg, #0b1d2a 0%, #030712 100%);
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
}

/* خلفية النجوم */
.stars {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
}

.star {
    position: absolute;
    background: white;
    border-radius: 50%;
    animation: twinkle var(--duration) infinite ease-in-out;
    opacity: 0;
}

@keyframes twinkle {
    0%, 100% { opacity: 0; transform: scale(0.5); }
    50% { opacity: 1; transform: scale(1.2); }
}

/* الشمس/القمر */
.orb {
    position: absolute;
    top: 20px;
    left: 20px;
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, #fffac2, #FFD700);
    box-shadow: 0 0 50px #ffaa00;
    z-index: 1;
    transition: all 1s ease;
}

/* حاويات اللوجو والفانوس */
.logo-container {
    position: absolute;
    left: 5%;
    top: 15px;
    z-index: 100;
    filter: drop-shadow(0 0 15px gold);
    animation: floatLogo 4s ease-in-out infinite;
}

.lantern-container {
    position: absolute;
    right: 5%;
    top: 10px;
    z-index: 100;
    filter: drop-shadow(0 0 20px #ffaa00);
    animation: swingLantern 3.5s ease-in-out infinite;
    transform-origin: top center;
}

.logo-img, .lantern-img {
    width: 130px;
    height: auto;
    display: block;
}

@keyframes floatLogo {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

@keyframes swingLantern {
    0%, 100% { transform: rotate(5deg); }
    50% { transform: rotate(-5deg); }
}

/* تأثير الضوء خلف الفانوس */
.lantern-container::after {
    content: '';
    position: absolute;
    bottom: -15px;
    left: 50%;
    transform: translateX(-50%);
    width: 80%;
    height: 20px;
    background: radial-gradient(ellipse at center, rgba(255,215,0,0.6) 0%, transparent 80%);
    border-radius: 50%;
    filter: blur(8px);
    z-index: -1;
    animation: glowPulse 3s infinite alternate;
}

@keyframes glowPulse {
    from { opacity: 0.4; width: 70%; }
    to { opacity: 0.8; width: 90%; }
}

/* Conteneur principal */
.container {
    position: relative;
    z-index: 10;
    margin-top: 150px;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(10px);
    padding: 40px 30px;
    border-radius: 50px;
    width: 85%;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
    border: 2px solid rgba(255, 215, 0, 0.3);
    box-shadow: 0 0 50px rgba(0, 0, 0, 0.5);
}

h1 {
    font-size: 48px;
    color: #FFD700;
    text-shadow: 0 0 20px gold, 0 0 40px #ffaa00;
    margin-bottom: 20px;
}

.countdown-label {
    font-size: 20px;
    color: #ffffffdd;
    margin-bottom: 10px;
}

.countdown-box {
    background: rgba(0, 0, 0, 0.6);
    padding: 15px 30px;
    border-radius: 60px;
    display: inline-block;
    margin: 15px auto;
    border: 2px solid #FFD700;
    font-size: 32px;
    font-weight: bold;
    color: #FFE55C;
    direction: ltr;
    box-shadow: 0 0 30px rgba(255,215,0,0.3);
}

.money {
    font-size: 64px;
    margin: 20px 0;
    color: #00ff99;
    text-shadow: 0 0 20px #00ff99, 0 0 40px #00cc77;
}

.baskets {
    font-size: 28px;
    margin-bottom: 20px;
    font-weight: bold;
    color: white;
}

.progress-bar {
    width: 80%;
    margin: 25px auto;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 40px;
    height: 30px;
    overflow: hidden;
    border: 2px solid rgba(255, 215, 0, 0.5);
}

.progress-fill {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, gold, #00ff99, gold);
    transition: width 1s ease;
    box-shadow: 0 0 30px #00ff99;
}

.footer {
    margin-top: 30px;
    font-size: 22px;
    color: #ffe4b5;
}

/* Responsive */
@media (max-width: 768px) {
    .logo-img, .lantern-img { width: 90px; }
    h1 { font-size: 36px; }
    .money { font-size: 48px; }
    .countdown-box { font-size: 24px; }
    .container { width: 90%; padding: 30px 15px; }
}
</style>
</head>
<body>

<!-- Création des étoiles -->
<div class="stars" id="stars"></div>

<!-- Éléments décoratifs -->
<div class="orb"></div>

<!-- Logo et Lanterne -->
<div class="logo-container">
    <img src="{{ url_for('static', filename='logo.png') }}" class="logo-img" alt="شعار الحملة" onerror="this.style.display='none'">
</div>

<div class="lantern-container">
    <img src="{{ url_for('static', filename='lantern.png') }}" class="lantern-img" alt="فانوس رمضاني" onerror="this.style.display='none'">
</div>

<!-- Contenu principal -->
<div class="container">
    <h1>🌙 حملة الخير 2 🌙</h1>
    
    <div class="countdown-label">⏳ موعد انطلاق الحملة (غداً 9 صباحاً)</div>
    <div class="countdown-box" id="countdown">--:--:--</div>
    
    <div class="money">
        💰 <span id="money">0</span> دينار
    </div>
    
    <div class="baskets" id="baskets">
        0 / 100 قفة
    </div>
    
    <div class="progress-bar">
        <div class="progress-fill" id="progress"></div>
    </div>
    
    <div class="footer">
        ❤️ هدفنا إدخال الفرحة إلى 100 عائلة محتاجة
    </div>
</div>

<script>
// ========== إنشاء النجوم ==========
function createStars() {
    const starsContainer = document.getElementById('stars');
    const numberOfStars = 150;
    
    for (let i = 0; i < numberOfStars; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        
        const size = Math.random() * 3 + 1;
        const x = Math.random() * 100;
        const y = Math.random() * 100;
        const duration = Math.random() * 3 + 2;
        
        star.style.width = size + 'px';
        star.style.height = size + 'px';
        star.style.left = x + '%';
        star.style.top = y + '%';
        star.style.setProperty('--duration', duration + 's');
        
        starsContainer.appendChild(star);
    }
}

// ========== Charger les données ==========
async function loadData() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        updateDisplay(data.total);
    } catch (error) {
        console.error('Erreur de chargement:', error);
    }
}

const basketPrice = 100;
const goal = 100;

function updateDisplay(total) {
    document.getElementById('money').innerText = total.toLocaleString();
    
    const baskets = Math.floor(total / basketPrice);
    document.getElementById('baskets').innerText = baskets + ' / 100 قفة';
    
    const percent = Math.min((baskets / goal) * 100, 100);
    document.getElementById('progress').style.width = percent + '%';
}

// ========== Compte à rebours ==========
// ========== Compte à rebours corrigé ==========
function updateCountdown() {
    const now = new Date();
    
    // Date d'aujourd'hui à 9h du matin
    const today9am = new Date(now);
    today9am.setHours(9, 0, 0, 0); // 9:00:00 aujourd'hui
    
    // Si maintenant est après 9h, la campagne a déjà commencé
    if (now > today9am) {
        document.getElementById('countdown').innerHTML = '🚀 الحملة منطلقة الآن!';
        return;
    }
    
    // Calculer le temps restant jusqu'à 9h aujourd'hui
    const diff = today9am - now;
    
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);
    
    // Afficher uniquement heures:minutes:secondes
    document.getElementById('countdown').innerHTML = 
        hours.toString().padStart(2, '0') + ':' + 
        minutes.toString().padStart(2, '0') + ':' + 
        seconds.toString().padStart(2, '0');
}

// Mise à jour chaque seconde
updateCountdown();
setInterval(updateCountdown, 1000);


// ========== Initialisation ==========
window.addEventListener('load', () => {
    createStars();
    loadData();
    updateCountdown();
    
    // Mettre à jour toutes les 5 secondes
    setInterval(loadData, 5000);
    setInterval(updateCountdown, 1000);
});
</script>
</body>
</html>
'''

# Page Admin
ADMIN_PAGE = '''
<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>لوحة التحكم - حملة الخير 2</title>
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Tahoma', Arial, sans-serif;
    direction: rtl;
    text-align: center;
    background: linear-gradient(135deg, #1a2634, #0f1722);
    color: white;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.admin-box {
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(10px);
    padding: 50px;
    border-radius: 40px;
    width: 100%;
    max-width: 500px;
    border: 3px solid #FFD700;
    box-shadow: 0 0 50px rgba(255, 215, 0, 0.3);
}

h2 {
    color: #FFD700;
    font-size: 36px;
    margin-bottom: 30px;
    text-shadow: 0 0 15px gold;
}

.info {
    color: #FFD700;
    font-size: 20px;
    margin: 20px 0 10px;
}

.current-value {
    background: linear-gradient(145deg, #1a1f2e, #0f1422);
    padding: 25px;
    border-radius: 20px;
    margin: 20px 0;
    border: 2px solid #00ff99;
}

.current-value span {
    color: #00ff99;
    font-size: 64px;
    font-weight: bold;
    text-shadow: 0 0 20px #00ff99;
}

input {
    padding: 18px;
    width: 100%;
    margin: 15px 0;
    border-radius: 15px;
    border: 2px solid #FFD700;
    font-size: 20px;
    text-align: center;
    background: rgba(255, 255, 255, 0.1);
    color: white;
}

input:focus {
    outline: none;
    box-shadow: 0 0 20px gold;
}

button {
    padding: 18px 40px;
    background: #FFD700;
    border: none;
    border-radius: 15px;
    cursor: pointer;
    font-size: 22px;
    font-weight: bold;
    margin: 10px 0;
    transition: all 0.3s;
    width: 100%;
}

button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 30px gold;
    background: #ffed4a;
}

.logout-btn {
    background: #e74c3c;
    color: white;
    margin-top: 20px;
}

.logout-btn:hover {
    background: #c0392b;
    box-shadow: 0 0 30px #e74c3c;
}

.message {
    margin: 15px 0;
    padding: 15px;
    border-radius: 10px;
    font-size: 18px;
    display: none;
}

.success {
    display: block;
    background: rgba(0, 255, 0, 0.2);
    color: #00ff99;
    border: 2px solid #00ff99;
}

.error {
    display: block;
    background: rgba(255, 0, 0, 0.2);
    color: #ff6b6b;
    border: 2px solid #ff6b6b;
}

@media (max-width: 600px) {
    .admin-box { padding: 30px; }
    h2 { font-size: 28px; }
    .current-value span { font-size: 48px; }
}
</style>
</head>
<body>

<div class="admin-box">
    <h2>🔧 لوحة التحكم</h2>
    
    <div class="info">💰 القيمة الحالية:</div>
    <div class="current-value">
        <span id="currentValue">0</span> دينار
    </div>
    
    <div class="info">أدخل المبلغ الجديد:</div>
    <input type="number" id="newTotal" placeholder="المبلغ بالدينار" value="5000">
    
    <button onclick="updateTotal()">💾 تحديث المبلغ</button>
    
    <div id="message" class="message"></div>
    
    <button class="logout-btn" onclick="window.location.href='/logout'">🚪 تسجيل الخروج</button>
</div>

<script>
// Charger la valeur actuelle
async function loadCurrentValue() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        document.getElementById('currentValue').innerText = data.total;
        document.getElementById('newTotal').value = data.total;
    } catch (error) {
        console.error('Erreur de chargement:', error);
        showMessage('❌ خطأ في تحميل البيانات', false);
    }
}

// Afficher un message
function showMessage(text, isSuccess) {
    const messageDiv = document.getElementById('message');
    messageDiv.innerHTML = text;
    messageDiv.className = 'message ' + (isSuccess ? 'success' : 'error');
    
    setTimeout(() => {
        messageDiv.className = 'message';
    }, 3000);
}

// Mettre à jour la valeur
async function updateTotal() {
    const value = parseFloat(document.getElementById('newTotal').value);
    
    if (isNaN(value) || value < 0) {
        showMessage('❌ الرجاء إدخال رقم صحيح', false);
        return;
    }
    
    try {
        const response = await fetch('/api/update', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({total: value})
        });
        
        const result = await response.json();
        
        if (result.success) {
            showMessage('✅ تم التحديث بنجاح', true);
            document.getElementById('currentValue').innerText = value;
        } else {
            showMessage('❌ خطأ في التحديث', false);
        }
    } catch (error) {
        console.error('Erreur:', error);
        showMessage('❌ خطأ في الاتصال', false);
    }
}

// Charger au démarrage et toutes les 5 secondes
loadCurrentValue();
setInterval(loadCurrentValue, 5000);
</script>
</body>
</html>
'''

# Page de login
LOGIN_PAGE = '''
<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>تسجيل الدخول - لوحة التحكم</title>
<style>
body {
    font-family: 'Tahoma', Arial, sans-serif;
    direction: rtl;
    text-align: center;
    background: linear-gradient(135deg, #1a2634, #0f1722);
    color: white;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.login-box {
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(10px);
    padding: 50px;
    border-radius: 40px;
    width: 100%;
    max-width: 400px;
    border: 3px solid #FFD700;
    box-shadow: 0 0 50px rgba(255, 215, 0, 0.3);
}

h2 {
    color: #FFD700;
    font-size: 36px;
    margin-bottom: 30px;
    text-shadow: 0 0 15px gold;
}

input {
    padding: 18px;
    width: 100%;
    margin: 15px 0;
    border-radius: 15px;
    border: 2px solid #FFD700;
    font-size: 18px;
    text-align: center;
    background: rgba(255, 255, 255, 0.1);
    color: white;
}

input:focus {
    outline: none;
    box-shadow: 0 0 20px gold;
}

button {
    padding: 18px 40px;
    background: #FFD700;
    border: none;
    border-radius: 15px;
    cursor: pointer;
    font-size: 22px;
    font-weight: bold;
    margin-top: 20px;
    transition: all 0.3s;
    width: 100%;
}

button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 30px gold;
}

.error {
    color: #ff6b6b;
    margin-top: 15px;
    padding: 10px;
    background: rgba(255, 0, 0, 0.1);
    border-radius: 10px;
    font-size: 16px;
}
</style>
</head>
<body>

<div class="login-box">
    <h2>🔐 تسجيل الدخول</h2>
    
    <form method="POST">
        <input type="text" name="username" placeholder="اسم المستخدم" required>
        <input type="password" name="password" placeholder="كلمة المرور" required>
        <button type="submit">دخول</button>
        
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
    </form>
</div>

</body>
</html>
'''

# Routes API
@app.route('/api/data')
def get_data():
    data = load_data()
    return jsonify(data)

@app.route('/api/update', methods=['POST'])
def update_data():
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'error': 'Non autorisé'}), 401
    
    try:
        new_data = request.json
        current_data = load_data()
        current_data['total'] = new_data.get('total', current_data['total'])
        save_data(current_data)
        return jsonify({'success': True, 'total': current_data['total']})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Routes principales
@app.route('/')
def home():
    return render_template_string(CAMPAIGN_PAGE)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template_string(LOGIN_PAGE, error="❌ اسم المستخدم أو كلمة المرور غير صحيحة")
    
    return render_template_string(LOGIN_PAGE, error=None)

@app.route('/dashboard')
def dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin'))
    return render_template_string(ADMIN_PAGE)

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin'))
# ... (tout votre code existant) ...

if __name__ == '__main__':
    # Créer le dossier static s'il n'existe pas
    if not os.path.exists('static'):
        os.makedirs('static')
        print("📁 Dossier 'static' créé - Placez vos images ici")
    
    # Initialiser le fichier de données
    if not os.path.exists(DATA_FILE):
        save_data({'total': 5000})
        print("📁 Fichier de données créé")
    
    print("\n" + "="*60)
    print("🚀 APPLICATION DÉMARRÉE AVEC SUCCÈS")
    print("="*60)
    print("📱 Page publique: http://localhost:5000")
    print("🔐 Page admin: http://localhost:5000/admin")
    print("👤 Identifiants: admin / campaign2024")
    print("💾 Données: " + DATA_FILE)
    print("="*60 + "\n")
    
    # Pour développement local seulement
    if os.environ.get('VERCEL_ENV') is None:
        app.run(debug=True, host='0.0.0.0', port=5000)

# Pour Vercel - point d'entrée
vercel_app = app