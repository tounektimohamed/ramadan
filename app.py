from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify
import os
import secrets
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
from datetime import datetime
import functools

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(16))
vercel_app = app

# Configuration Firebase Admin SDK
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "zoom-3c767",
    "private_key_id": "2a691b2aaa60e6cc9b5c51f3d168908c699ef980",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCkTzYY8v5EcL0S\n8O2vjnIp7jw6m5xa0UC/eyia0BsOfdYpf7krmzrFjuCei4OyzxNcQ4wFfK/HARLx\nED4p81JhmTZPRiBpyQLaZYvl7rv0JiCRmbMtje90Drk4FhZOcBthA8FyzWrldIF7\nbjCoscVdbG1Wnioun0kFSYmfATEGA4qAVvvMYdmLvl3oVpesxEMDjZYO0S+UCiV0\nr9O0iXromPwsjX+5zVGDMjQCzD1ziZ+FoddbpOo0tLlK3Y+S7QjTmKFvmX0wGMoo\nE+lpdJ/WlFyZuvXeXeqTjct8jLMnh8yltS09g/tyzIbzFSeAuukwevyrDX9NkYBp\nSBvY8W3xAgMBAAECggEALTiTxfgSnNl+YBkpAXkt2HZ14xdyx9fxfwGxYjJGUA24\nBIHff63gVgEFtvzkyTCOvoTko5n2csnL4ca7pSYPlUbqmJTPVO36uArcnvK+jep0\naj4n/zCiJ4np1hLWHs5h6qhy9Fquwen3vPXNtJAApr6xtPYg2+YA3dCobLeSO3oK\n6mOxv1cImfbCduFEMM8LcWIo9MXACn/MgDUmB7/zKZXNwOVXTBsAIt5mmIfp60CS\npUZlQdUMDK7EcezW8IxlXpFFf2SdBRk8zfIAtwkAEYWwqKtsHk8dJW/IYqRjE8sw\noS6tQEUm46KXv8v3/axbzuXD3/CzLV5T/OikkBzfhQKBgQDZ07DJxcNjMMMNb+OQ\niw77W8flfkI5lcEbXOfttU0OpYwY+y8jafSbhPtj7y3YbkVOPm8EKQZ3iRHOyVmW\noEA0h8FQQgEScOZ0tRMseimWcaeReAru5VojtHUPEiMCXs28P3oWda8u6m6gY/jY\nmvx1OHF7AFzAlSDTE9crCFjbWwKBgQDBGpRzwNz/au33f9kEofQCdUsOlJRJNB8v\nIvvw4nBJGR/jHKjbbsTZ9cacM7dW8E+aN+XZOf64ltie52dDB7f41GXB8lZ8Antx\njIKxw6dN4emRr+3ejgKUAo1HE2Jil47s5bG49x3kEVnrzg+NOWSPxPoCzJ4qJYyT\nV8nL8du5owKBgEZi8jhw8A8IPa8E3briRGgSo0hUASBMdMbbwZH9SLYX5mpYGEZQ\nQZtTYExNiDnsf/allAf7HbzYjOmOBKX4iGaxC1Vczq3fz4gczuJLY07a0PPfn2DM\nudDZyg2hpbBpY/+VX2UMiBwX4sFvLIUJp9RU9c5yMoaEacPrIFcmblgLAoGBAKii\n3rwL1LPWHQVEiDBsgtzWs/qCtNENDKKsiZr/FRIxN9CtyaUAIjc6VP06iMUKzmme\noULIS/PGAF0dNuepyPcr/cWXLgHUZRtvmv9FH0l7ne+V1UTDfermI5zLh+MT+kRV\n/5PJczgmEwJEDP7G/VQ0sCVbrlCeRBq00s0hZULDAoGBAKhsN67DNVgqgDFmBeYw\n0zNeRiE3I2elnnVCLJOXMTS/1NdYQz/MZ0mwcGhsyyekhGwJKvtX4Kkk75mWrXiy\nmiyXzqJmh4RRcrAjnnwcP+STnJmkjhyIr6QxqhROKVosmMz/oWIF6zOJDXDoMibf\nB0ldoOtv3T2R9hnW9cfe0aS9\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-ga2t9@zoom-3c767.iam.gserviceaccount.com",
    "client_id": "111377422433159462393",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token"
})

firebase_admin.initialize_app(cred)
db = firestore.client()

# Configuration Pyrebase pour l'authentification (pas pour Firestore)
firebase_config = {
    "apiKey": "AIzaSyCWDbl_4bUZG2IHDxnxPcan-eBzZtsuY0M",
    "authDomain": "zoom-3c767.firebaseapp.com",
    "databaseURL": "https://zoom-3c767-default-rtdb.firebaseio.com",
    "projectId": "zoom-3c767",
    "storageBucket": "zoom-3c767.appspot.com",
    "messagingSenderId": "481214437178",
    "appId": "1:481214437178:web:eb621d71c88af5d4412203",
    "measurementId": "G-W25S1BEK4D"
}

# Initialiser Pyrebase pour l'authentification
pyrebase_app = pyrebase.initialize_app(firebase_config)
auth_pyrebase = pyrebase_app.auth()

# Décorateur pour vérifier l'authentification
def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_token' not in session:
            return redirect(url_for('admin_login'))
        try:
            # Vérifier si le token est toujours valide
            user = auth_pyrebase.get_account_info(session['user_token'])
            return f(*args, **kwargs)
        except:
            session.pop('user_token', None)
            session.pop('user_email', None)
            return redirect(url_for('admin_login'))
    return decorated_function

# Fonctions pour interagir avec Firestore
def load_data():
    try:
        doc_ref = db.collection('campaign').document('data')
        doc = doc_ref.get()
        
        if doc.exists:
            data = doc.to_dict()
            return {
                'total': data.get('total', 5000),
                'goal': data.get('goal', 100),
                'basket_price': data.get('basket_price', 100)
            }
        else:
            # Créer le document s'il n'existe pas
            init_data = {'total': 5000, 'goal': 100, 'basket_price': 100}
            doc_ref.set(init_data)
            return init_data
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {e}")
        return {'total': 5000, 'goal': 100, 'basket_price': 100}

def save_data(data):
    try:
        doc_ref = db.collection('campaign').document('data')
        data['last_updated'] = datetime.now().isoformat()
        data['updated_by'] = session.get('user_email', 'unknown')
        doc_ref.set(data, merge=True)
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")
        return False

def init_firebase_data():
    """Initialise les données dans Firestore si elles n'existent pas"""
    try:
        doc_ref = db.collection('campaign').document('data')
        doc = doc_ref.get()
        
        if not doc.exists:
            # Créer le document avec les données initiales
            doc_ref.set({
                'total': 5000,
                'goal': 100,
                'basket_price': 100,
                'last_updated': datetime.now().isoformat(),
                'updated_by': 'system'
            })
            print("✅ Données initiales créées dans Firestore")
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")

# Routes API
@app.route('/api/data')
def get_data():
    data = load_data()
    return jsonify({'total': data.get('total', 5000)})

@app.route('/api/update', methods=['POST'])
@login_required
def update_data():
    try:
        new_data = request.json
        current_data = load_data()
        current_data['total'] = new_data.get('total', current_data['total'])
        
        if save_data(current_data):
            return jsonify({'success': True, 'total': current_data['total']})
        else:
            return jsonify({'success': False, 'error': 'Erreur lors de la sauvegarde'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Routes pour l'authentification
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            # Authentification avec Pyrebase
            user = auth_pyrebase.sign_in_with_email_and_password(email, password)
            session['user_token'] = user['idToken']
            session['user_email'] = email
            session['user_local_id'] = user['localId']
            
            # Initialiser les données si nécessaire
            init_firebase_data()
            
            return redirect(url_for('dashboard'))
        except Exception as e:
            print(f"Erreur de connexion: {e}")
            error_message = "❌ Email ou mot de passe incorrect"
            return render_template_string(LOGIN_PAGE, error=error_message)
    
    return render_template_string(LOGIN_PAGE, error=None)

@app.route('/admin/logout')
def admin_logout():
    session.pop('user_token', None)
    session.pop('user_email', None)
    session.pop('user_local_id', None)
    return redirect(url_for('admin_login'))

# Routes principales
@app.route('/')
def home():
    return render_template_string(CAMPAIGN_PAGE)

@app.route('/admin')
def admin_redirect():
    return redirect(url_for('admin_login'))

@app.route('/dashboard')
@login_required
def dashboard():
    data = load_data()
    return render_template_string(ADMIN_PAGE, current_total=data.get('total', 5000))

# Template de la page principale
CAMPAIGN_PAGE = '''<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>حملة الخير 2 - رمضان 2026</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
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
}
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
<div class="stars" id="stars"></div>
<div class="orb"></div>
<div class="logo-container">
    <img src="{{ url_for('static', filename='logo.png') }}" class="logo-img" alt="شعار الحملة" onerror="this.style.display='none'">
</div>
<div class="lantern-container">
    <img src="{{ url_for('static', filename='lantern.png') }}" class="lantern-img" alt="فانوس رمضاني" onerror="this.style.display='none'">
</div>
<div class="container">
    <h1>🌙 حملة الخير 2 🌙</h1>
    <div class="countdown-box" id="countdown">--:--:--</div>
    <div class="money">💰 <span id="money">0</span> دينار</div>
    <div class="baskets" id="baskets">0 / 100 قفة</div>
    <div class="progress-bar"><div class="progress-fill" id="progress"></div></div>
    <div class="footer">❤️ هدفنا إدخال الفرحة إلى 100 عائلة محتاجة</div>
</div>
<script>
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
function updateCountdown() {
    const now = new Date();
    const today9am = new Date(now);
    today9am.setHours(9, 0, 0, 0);
    if (now > today9am) {
        document.getElementById('countdown').innerHTML = '🚀 الحملة منطلقة الآن!';
        return;
    }
    const diff = today9am - now;
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);
    document.getElementById('countdown').innerHTML = 
        hours.toString().padStart(2, '0') + ':' + 
        minutes.toString().padStart(2, '0') + ':' + 
        seconds.toString().padStart(2, '0');
}
window.addEventListener('load', () => {
    createStars();
    loadData();
    updateCountdown();
    setInterval(loadData, 5000);
    setInterval(updateCountdown, 1000);
});
</script>
</body>
</html>
'''

# Page Admin
ADMIN_PAGE = '''<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>لوحة التحكم - حملة الخير 2</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
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
.user-info {
    margin-top: 15px;
    color: #FFD700;
    font-size: 14px;
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
        <span id="currentValue">{{ current_total }}</span> دينار
    </div>
    <div class="info">أدخل المبلغ الجديد:</div>
    <input type="number" id="newTotal" placeholder="المبلغ بالدينار" value="{{ current_total }}">
    <button onclick="updateTotal()">💾 تحديث المبلغ</button>
    <div id="message" class="message"></div>
    <button class="logout-btn" onclick="window.location.href='/admin/logout'">🚪 تسجيل الخروج</button>
    <div class="user-info">👤 {{ session.get('user_email', '') }}</div>
</div>
<script>
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
function showMessage(text, isSuccess) {
    const messageDiv = document.getElementById('message');
    messageDiv.innerHTML = text;
    messageDiv.className = 'message ' + (isSuccess ? 'success' : 'error');
    setTimeout(() => {
        messageDiv.className = 'message';
    }, 3000);
}
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
loadCurrentValue();
setInterval(loadCurrentValue, 5000);
</script>
</body>
</html>
'''

# Page de login
LOGIN_PAGE = '''<!DOCTYPE html>
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
.info-text {
    margin-top: 20px;
    color: #888;
    font-size: 14px;
}
</style>
</head>
<body>
<div class="login-box">
    <h2>🔐 تسجيل الدخول</h2>
    <form method="POST">
        <input type="email" name="email" placeholder="البريد الإلكتروني" required>
        <input type="password" name="password" placeholder="كلمة المرور" required>
        <button type="submit">دخول</button>
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
    </form>
    <div class="info-text">استخدم حساب Firebase الخاص بك</div>
</div>
</body>
</html>
'''
if __name__ == '__main__':
    # Remplacer la fin de votre fichier par ceci :
    port = int(os.environ.get('PORT', 5000))  # Utilise le port Render ou 5000 en local
    app.run(host='0.0.0.0', port=port)
    print("\n" + "="*60)
    print("🚀 APPLICATION DÉMARRÉE AVEC SUCCÈS")
    print("="*60)
    print("📱 Page publique: http://localhost:5000")
    print("🔐 Page admin: http://localhost:5000/admin/login")
    print("💾 Base de données: Firebase Firestore")
    print("🔑 Authentification: Firebase Auth")
    print("="*60 + "\n")
    
    # Pour développement local seulement
    if os.environ.get('VERCEL_ENV') is None:
        app.run(debug=True, host='0.0.0.0', port=5000)

# Pour Vercel - point d'entrée
vercel_app = app