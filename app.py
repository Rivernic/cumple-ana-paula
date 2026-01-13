import streamlit as st
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import os
import streamlit.components.v1 as components

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Mis 15 - Ana Paula", page_icon="👑", layout="centered")

# --- VARIABLES ---
NOMBRE_CUMPLEAÑERA = "Ana Paula Scotta"
FECHA_TEXTO = "11 de Abril de 2026, 21:00 hs"
TARGET_DATE_JS = "Apr 11, 2026 21:00:00" 
LUGAR_NOMBRE = "Salón 'El Fortín'"
MAPA_LINK = "https://maps.app.goo.gl/F5ZfASp4LdbSMhBh9?g_st=iw"
FECHA_LIMITE = "10 de Marzo"
EMAIL_SENDER = st.secrets["EMAIL_SENDER"]
EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]
ARCHIVO_EXCEL = "invitados_cumple.xlsx"

# --- CSS DEFINITIVO (FONDO ANIMADO VISIBLE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&family=Great+Vibes&display=swap');

    /* 1. ELIMINAMOS EL FONDO POR DEFECTO DE STREAMLIT PARA VER LA ANIMACIÓN */
    .stApp {
        background: transparent !important;
    }

    /* 2. CAPA DE ANIMACIÓN (ÁREA COMPLETA) */
    .area {
        background: #FFF0F5; /* Fondo base rosa pálido */
        background: -webkit-linear-gradient(to left, #8f94fb, #4e54c8);  
        width: 100%;
        height: 100vh;
        position: fixed;
        top: 0;
        left: 0;
        z-index: -1; /* Detrás de todo */
    }

    .circles {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        margin: 0;
        padding: 0;
    }

    .circles li {
        position: absolute;
        display: block;
        list-style: none;
        width: 20px;
        height: 20px;
        background: rgba(233, 30, 99, 0.4); /* Color de los globos (Rosa fuerte transparente) */
        animation: animate 25s linear infinite;
        bottom: -150px;
        border-radius: 50%; /* Hacemos que sean círculos */
    }

    /* CONFIGURACIÓN DE CADA GLOBO (TAMAÑO, POSICIÓN Y VELOCIDAD) */
    .circles li:nth-child(1) { left: 25%; width: 80px; height: 80px; animation-delay: 0s; }
    .circles li:nth-child(2) { left: 10%; width: 20px; height: 20px; animation-delay: 2s; animation-duration: 12s; }
    .circles li:nth-child(3) { left: 70%; width: 20px; height: 20px; animation-delay: 4s; }
    .circles li:nth-child(4) { left: 40%; width: 60px; height: 60px; animation-delay: 0s; animation-duration: 18s; }
    .circles li:nth-child(5) { left: 65%; width: 20px; height: 20px; animation-delay: 0s; }
    .circles li:nth-child(6) { left: 75%; width: 110px; height: 110px; animation-delay: 3s; }
    .circles li:nth-child(7) { left: 35%; width: 150px; height: 150px; animation-delay: 7s; }
    .circles li:nth-child(8) { left: 50%; width: 25px; height: 25px; animation-delay: 15s; animation-duration: 45s; }
    .circles li:nth-child(9) { left: 20%; width: 15px; height: 15px; animation-delay: 2s; animation-duration: 35s; }
    .circles li:nth-child(10){ left: 85%; width: 150px; height: 150px; animation-delay: 0s; animation-duration: 11s; }

    @keyframes animate {
        0% {
            transform: translateY(0) rotate(0deg);
            opacity: 1;
            border-radius: 50%;
        }
        100% {
            transform: translateY(-1000px) rotate(720deg);
            opacity: 0;
            border-radius: 50%;
        }
    }

    /* 3. ESTILOS DE LA TARJETA PRINCIPAL (SOLIDA PARA LEER BIEN) */
    .main .block-container {
        background-color: rgba(255, 255, 255, 0.90) !important; /* Blanca casi solida */
        padding: 3rem 2rem;
        border-radius: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        max-width: 700px;
        margin-top: 2rem;
    }

    /* 4. RESTO DEL DISEÑO (INPUTS, FUENTES, ETC) */
    .stTextInput input, .stNumberInput input, .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #333333 !important;
        border: 2px solid #FCE4EC !important;
        border-radius: 15px !important;
        padding: 10px !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
        border-color: #EC407A !important;
        box-shadow: 0 0 8px rgba(236, 64, 122, 0.3) !important;
    }

    .info-card {
        background-color: #FCE4EC;
        border: 1px solid #F8BBD0;
        color: #880E4F;
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        height: 100%;
        transition: transform 0.3s ease;
    }
    .info-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(233, 30, 99, 0.15);
    }
    .info-titulo {
        font-weight: bold;
        color: #D81B60;
        font-size: 1.1rem;
        margin-bottom: 5px;
        display: block;
    }
    .mapa-btn {
        display: inline-block;
        margin-top: 10px;
        background-color: #FFFFFF;
        color: #D81B60;
        padding: 8px 15px;
        border-radius: 20px;
        text-decoration: none;
        font-weight: bold;
        font-size: 0.9rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    h1 {
        font-family: 'Great Vibes', cursive;
        color: #D81B60 !important;
        text-align: center;
        font-size: 4rem !important;
        margin-bottom: 5px;
        font-weight: 400;
        text-shadow: 2px 2px 4px rgba(255,255,255,0.8);
    }
    
    .subtitulo {
        text-align: center;
        font-family: 'Quicksand', sans-serif;
        color: #EC407A;
        font-size: 1.2rem;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 30px;
        font-weight: bold;
    }
    
    label {
        color: #880E4F !important;
        font-weight: 700 !important;
        font-family: 'Quicksand', sans-serif !important;
        font-size: 15px !important;
    }
    
    .seccion-titulo {
        color: #AD1457;
        font-weight: bold;
        margin-top: 25px;
        margin-bottom: 15px;
        border-bottom: 2px dashed #F8BBD0;
        padding-bottom: 5px;
        font-family: 'Quicksand', sans-serif;
    }

    div.stButton > button:first-child {
        background: linear-gradient(45deg, #EC407A, #D81B60) !important;
        color: white !important;
        border: none;
        border-radius: 50px;
        padding: 15px 30px;
        font-size: 18px;
        font-weight: bold;
        width: 100%;
        transition: 0.3s;
        box-shadow: 0 5px 15px rgba(233, 30, 99, 0.3);
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.03);
        box-shadow: 0 8px 20px rgba(233, 30, 99, 0.4);
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    
    <div class="area" >
        <ul class="circles">
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
        </ul>
    </div >
    """, unsafe_allow_html=True)

# --- JAVASCRIPT: CUENTA REGRESIVA ---
def mostrar_contador_js():
    contador_html = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@700&display=swap');
        .countdown-container {{
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 30px;
            font-family: 'Quicksand', sans-serif;
        }}
        .time-box {{
            background-color: #FFFFFF;
            color: #D81B60;
            padding: 10px;
            border-radius: 18px;
            text-align: center;
            min-width: 75px;
            border: 2px solid #FCE4EC;
            box-shadow: 0 4px 10px rgba(233, 30, 99, 0.1);
        }}
        .time-number {{
            font-size: 26px;
            font-weight: bold;
            display: block;
        }}
        .time-label {{
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #880E4F;
        }}
    </style>
    <div class="countdown-container" id="countdown">
        <div class="time-box"><span class="time-number" id="days">00</span><span class="time-label">Días</span></div>
        <div class="time-box"><span class="time-number" id="hours">00</span><span class="time-label">Hs</span></div>
        <div class="time-box"><span class="time-number" id="minutes">00</span><span class="time-label">Min</span></div>
        <div class="time-box"><span class="time-number" id="seconds">00</span><span class="time-label">Seg</span></div>
    </div>
    <script>
    var countDownDate = new Date("{TARGET_DATE_JS}").getTime();
    var x = setInterval(function() {{
        var now = new Date().getTime();
        var distance = countDownDate - now;
        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);
        document.getElementById("days").innerHTML = days;
        document.getElementById("hours").innerHTML = hours;
        document.getElementById("minutes").innerHTML = minutes;
        document.getElementById("seconds").innerHTML = seconds;
        if (distance < 0) {{
            clearInterval(x);
            document.getElementById("countdown").innerHTML = "¡HOY ES!";
        }}
    }}, 1000);
    </script>
    """
    components.html(contador_html, height=110)

# --- BACKEND ---
def guardar_en_excel(datos):
    try:
        if os.path.exists(ARCHIVO_EXCEL):
            df_existente = pd.read_excel(ARCHIVO_EXCEL)
            df_nuevo = pd.DataFrame([datos])
            df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
        else:
            df_final = pd.DataFrame([datos])
        df_final.to_excel(ARCHIVO_EXCEL, index=False)
        return True
    except:
        return False

def enviar_confirmacion(invitado, asistencia, adultos, menores, celiacos, vegetarianos, veganos, observaciones):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_SENDER
        msg['Subject'] = f"XV ANA PAULA - {invitado}"
        
        body = f"""
        NUEVA RESPUESTA DE: {invitado}
        ------------------------------------------
        ASISTENCIA: {asistencia}
        
        👥 INVITADOS:
        - Mayores (>10 años): {adultos}
        - Menores (hasta 10): {menores}
        - TOTAL: {adultos + menores}
        
        🍽️ MENÚS ESPECIALES:
        - Celíacos: {celiacos}
        - Vegetarianos: {vegetarianos}
        - Veganos: {veganos}
        
        📝 MENSAJE: {observaciones}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_SENDER, msg.as_string())
        server.quit()
        return True
    except:
        return False

# --- UI VISUAL ---
st.markdown(f"<h1>{NOMBRE_CUMPLEAÑERA}</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitulo'>MIS 15 AÑOS</p>", unsafe_allow_html=True)

mostrar_contador_js()
st.write("---")

# INFO DE FECHA Y LUGAR
c1, c2 = st.columns(2)
with c1:
    st.markdown(f"""
    <div class="info-card">
        <span class="info-titulo">📅 CUÁNDO</span>
        <br>
        {FECHA_TEXTO}
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="info-card">
        <span class="info-titulo">📍 DÓNDE</span>
        <br>
        {LUGAR_NOMBRE}
        <br>
        <a href="{MAPA_LINK}" target="_blank" class="mapa-btn">VER MAPA 🗺️</a>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"<p style='text-align:center; margin-top:20px; color:#AD1457; font-weight:bold;'>⚠️ Confirmar antes del {FECHA_LIMITE}</p>", unsafe_allow_html=True)

# FORMULARIO
st.markdown("<h3 style='text-align: center; color: #880E4F; margin-top: 30px;'>💌 Confirmación</h3>", unsafe_allow_html=True)

with st.form("form_fiesta"):
    nombre = st.text_input("Apellido de Familia / Nombre:")
    asistencia = st.radio("¿Vas a venir?", ["¡Sí, confirmo!", "No puedo ir"], horizontal=True)
    
    st.markdown("<div class='seccion-titulo'>👥 Cantidad de Invitados</div>", unsafe_allow_html=True)
    c_adultos, c_menores = st.columns(2)
    adultos = c_adultos.number_input("Mayores (+10 años)", min_value=0, value=1)
    menores = c_menores.number_input("Menores (hasta 10 años)", min_value=0, value=0)
    
    st.markdown("<div class='seccion-titulo'>🍽️ Menús Especiales</div>", unsafe_allow_html=True)
    st.caption("Indicá cantidad si corresponde (dejá en 0 si no):")
    
    col_menu1, col_menu2, col_menu3 = st.columns(3)
    celiacos = col_menu1.number_input("Celíacos", min_value=0, value=0)
    vegetarianos = col_menu2.number_input("Vegetarianos", min_value=0, value=0)
    veganos = col_menu3.number_input("Veganos", min_value=0, value=0)

    # Validación visual de cantidad
    if (celiacos + vegetarianos + veganos) > (adultos + menores):
        st.warning("⚠️ ¡Ojo! Hay más pedidos de menús especiales que invitados totales.")

    st.markdown("<div class='seccion-titulo'>📝 Mensaje</div>", unsafe_allow_html=True)
    observaciones = st.text_area("Dejanos un saludo o aclaración:", height=80)
    
    submitted = st.form_submit_button("ENVIAR RESPUESTA")
    
    if submitted:
        if not nombre:
            st.error("Por favor escribí tu nombre.")
        else:
            enviar_confirmacion(nombre, asistencia, adultos, menores, celiacos, vegetarianos, veganos, observaciones)
            guardar_en_excel({
                "Fecha": datetime.now().strftime("%Y-%m-%d"), 
                "Nombre": nombre, 
                "Asistencia": asistencia,
                "Mayores (+10)": adultos,
                "Menores (hasta 10)": menores,
                "Celíacos": celiacos,
                "Vegetarianos": vegetarianos,
                "Veganos": veganos,
                "Mensaje": observaciones
            })
            st.success(f"¡Gracias {nombre}! Confirmado.")