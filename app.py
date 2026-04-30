import streamlit as st
import pickle
import numpy as np
import time

st.set_page_config(
    page_title="Churn Predictor AI",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS + Animated Background
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

    * { font-family: 'Rajdhani', sans-serif; }

    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #0d1117 50%, #0a0a1a 100%);
        color: #e0e0e0;
    }

    /* Animated background canvas */
    #bg-canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 0;
        pointer-events: none;
    }

    .block-container {
        position: relative;
        z-index: 1;
    }

    .main-title {
        font-family: 'Orbitron', monospace;
        font-size: 3rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00d4ff, #7b2ff7, #00d4ff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        margin-bottom: 0.2rem;
        letter-spacing: 3px;
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    .subtitle {
        text-align: center;
        color: #888;
        font-size: 1.1rem;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 2rem;
    }

    .card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(0, 212, 255, 0.15);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.05);
    }

    .section-title {
        font-family: 'Orbitron', monospace;
        font-size: 0.85rem;
        color: #00d4ff;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
        border-bottom: 1px solid rgba(0, 212, 255, 0.2);
        padding-bottom: 0.5rem;
    }

    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #00d4ff, #7b2ff7);
        color: white;
        border: none;
        padding: 0.9rem 2rem;
        font-family: 'Orbitron', monospace;
        font-size: 1rem;
        font-weight: 700;
        letter-spacing: 3px;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        margin-top: 1rem;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 25px rgba(0, 212, 255, 0.5);
    }

    .result-churn {
        background: linear-gradient(135deg, rgba(255,50,50,0.1), rgba(255,100,50,0.05));
        border: 1px solid rgba(255, 50, 50, 0.4);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        animation: pulse-red 2s infinite;
    }

    .result-stay {
        background: linear-gradient(135deg, rgba(0,255,150,0.1), rgba(0,212,255,0.05));
        border: 1px solid rgba(0, 255, 150, 0.4);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        animation: pulse-green 2s infinite;
    }

    @keyframes pulse-red {
        0%, 100% { box-shadow: 0 0 20px rgba(255,50,50,0.2); }
        50% { box-shadow: 0 0 40px rgba(255,50,50,0.5); }
    }

    @keyframes pulse-green {
        0%, 100% { box-shadow: 0 0 20px rgba(0,255,150,0.2); }
        50% { box-shadow: 0 0 40px rgba(0,255,150,0.5); }
    }

    .result-title {
        font-family: 'Orbitron', monospace;
        font-size: 1.8rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
    }

    .result-subtitle {
        font-size: 1rem;
        color: #aaa;
        letter-spacing: 2px;
    }

    .metric-box {
        background: rgba(0, 212, 255, 0.05);
        border: 1px solid rgba(0, 212, 255, 0.15);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }

    .metric-value {
        font-family: 'Orbitron', monospace;
        font-size: 1.8rem;
        font-weight: 700;
        color: #00d4ff;
    }

    .metric-label {
        font-size: 0.8rem;
        color: #666;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    label { color: #aaa !important; letter-spacing: 1px; }
    </style>

    <!-- Animated Background -->
    <canvas id="bg-canvas"></canvas>
    <script>
    const canvas = document.getElementById('bg-canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });

    const shapes = [];
    const shapeTypes = ['circle', 'bar', 'dot', 'line', 'triangle', 'cross'];
    const colors = ['#00d4ff', '#7b2ff7', '#00ff96', '#ff6b6b'];

    for (let i = 0; i < 60; i++) {
        shapes.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 18 + 4,
            type: shapeTypes[Math.floor(Math.random() * shapeTypes.length)],
            color: colors[Math.floor(Math.random() * colors.length)],
            alpha: Math.random() * 0.25 + 0.05,
            speedX: (Math.random() - 0.5) * 0.4,
            speedY: (Math.random() - 0.5) * 0.4,
            rotation: Math.random() * Math.PI * 2,
            rotSpeed: (Math.random() - 0.5) * 0.01,
            pulse: Math.random() * Math.PI * 2,
        });
    }

    function drawShape(s) {
        ctx.save();
        ctx.translate(s.x, s.y);
        ctx.rotate(s.rotation);
        s.pulse += 0.02;
        const alpha = s.alpha * (0.7 + 0.3 * Math.sin(s.pulse));
        ctx.globalAlpha = alpha;
        ctx.strokeStyle = s.color;
        ctx.fillStyle = s.color;
        ctx.lineWidth = 1.2;

        if (s.type === 'circle') {
            ctx.beginPath();
            ctx.arc(0, 0, s.size, 0, Math.PI * 2);
            ctx.stroke();
        } else if (s.type === 'bar') {
            // Mini bar chart
            const bars = [0.4, 0.7, 0.5, 1.0, 0.6];
            bars.forEach((h, i) => {
                ctx.fillRect(i * (s.size * 0.4) - s.size, -h * s.size, s.size * 0.3, h * s.size);
            });
        } else if (s.type === 'dot') {
            ctx.beginPath();
            ctx.arc(0, 0, s.size * 0.3, 0, Math.PI * 2);
            ctx.fill();
        } else if (s.type === 'line') {
            // Mini line chart
            ctx.beginPath();
            const pts = [0, 0.5, 0.2, 0.8, 0.4, 0.3, 0.6, 0.9, 0.8, 0.6, 1.0, 1.0];
            ctx.moveTo(-s.size, -pts[1] * s.size);
            for (let i = 2; i < pts.length; i += 2) {
                ctx.lineTo(-s.size + pts[i] * s.size * 2, -pts[i+1] * s.size);
            }
            ctx.stroke();
        } else if (s.type === 'triangle') {
            ctx.beginPath();
            ctx.moveTo(0, -s.size);
            ctx.lineTo(s.size * 0.866, s.size * 0.5);
            ctx.lineTo(-s.size * 0.866, s.size * 0.5);
            ctx.closePath();
            ctx.stroke();
        } else if (s.type === 'cross') {
            // Neural node cross
            ctx.beginPath();
            ctx.moveTo(-s.size, 0); ctx.lineTo(s.size, 0);
            ctx.moveTo(0, -s.size); ctx.lineTo(0, s.size);
            ctx.stroke();
            ctx.beginPath();
            ctx.arc(0, 0, s.size * 0.25, 0, Math.PI * 2);
            ctx.fill();
        }

        ctx.restore();
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        shapes.forEach(s => {
            s.x += s.speedX;
            s.y += s.speedY;
            s.rotation += s.rotSpeed;
            if (s.x < -50) s.x = canvas.width + 50;
            if (s.x > canvas.width + 50) s.x = -50;
            if (s.y < -50) s.y = canvas.height + 50;
            if (s.y > canvas.height + 50) s.y = -50;
            drawShape(s);
        });
        requestAnimationFrame(animate);
    }
    animate();
    </script>
""", unsafe_allow_html=True)

# Load model
model = pickle.load(open('model.pkl', 'rb'))

# Header
st.markdown('<div class="main-title">CHURN PREDICTOR AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Powered by XGBoost · Real-time Prediction Engine</div>', unsafe_allow_html=True)

# Metrics row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="metric-box"><div class="metric-value">7K+</div><div class="metric-label">Training Records</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-box"><div class="metric-value">76%</div><div class="metric-label">Accuracy</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-box"><div class="metric-value">19</div><div class="metric-label">Features</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-box"><div class="metric-value">XGB</div><div class="metric-label">Model Type</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Input form
left, right = st.columns(2)

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">// Customer Profile</div>', unsafe_allow_html=True)
    gender = st.selectbox('Gender', ['Male', 'Female'])
    senior_citizen = st.selectbox('Senior Citizen', [0, 1], format_func=lambda x: 'Yes' if x == 1 else 'No')
    partner = st.selectbox('Has Partner', ['Yes', 'No'])
    dependents = st.selectbox('Has Dependents', ['Yes', 'No'])
    tenure = st.slider('Tenure (months)', 0, 72, 12)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">// Service & Billing</div>', unsafe_allow_html=True)
    internet_service = st.selectbox('Internet Service', ['DSL', 'Fiber optic', 'No'])
    contract = st.selectbox('Contract Type', ['Month-to-month', 'One year', 'Two year'])
    paperless_billing = st.selectbox('Paperless Billing', ['Yes', 'No'])
    payment_method = st.selectbox('Payment Method', [
        'Bank transfer (automatic)', 'Credit card (automatic)',
        'Electronic check', 'Mailed check'
    ])
    monthly_charges = st.number_input('Monthly Charges ($)', 0.0, 150.0, 50.0)
    total_charges = st.number_input('Total Charges ($)', 0.0, 10000.0, 500.0)
    st.markdown('</div>', unsafe_allow_html=True)

# Predict button
col_btn = st.columns([1, 2, 1])[1]
with col_btn:
    predict_btn = st.button('⚡ ANALYZE CUSTOMER')

# Prediction
if predict_btn:
    with st.spinner('Running neural analysis...'):
        time.sleep(1.5)

    gender_encoded = 1 if gender == 'Male' else 0
    partner_encoded = 1 if partner == 'Yes' else 0
    dependents_encoded = 1 if dependents == 'Yes' else 0
    contract_encoded = ['Month-to-month', 'One year', 'Two year'].index(contract)
    internet_encoded = ['DSL', 'Fiber optic', 'No'].index(internet_service)
    paperless_encoded = 1 if paperless_billing == 'Yes' else 0
    payment_encoded = ['Bank transfer (automatic)', 'Credit card (automatic)',
                       'Electronic check', 'Mailed check'].index(payment_method)

    input_data = np.array([[
        gender_encoded, senior_citizen, partner_encoded, dependents_encoded,
        tenure, 0, 0, internet_encoded, 0, 0, 0, 0, 0, 0,
        contract_encoded, paperless_encoded, payment_encoded,
        monthly_charges, total_charges
    ]])

    prediction = model.predict(input_data)

    st.markdown("<br>", unsafe_allow_html=True)

    if prediction[0] == 1:
        st.markdown('''
            <div class="result-churn">
                <div class="result-title" style="color:#ff5050">⚠ HIGH CHURN RISK DETECTED</div>
                <div class="result-subtitle">This customer is likely to leave — immediate action recommended</div>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
            <div class="result-stay">
                <div class="result-title" style="color:#00ff96">✓ CUSTOMER RETENTION CONFIRMED</div>
                <div class="result-subtitle">This customer is likely to stay — low churn risk</div>
            </div>
        ''', unsafe_allow_html=True)