import os
from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'cbtis204_secret_key'

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')

def enviar_notificacion_telegram(mensaje):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
        try:
            requests.post(url, json=payload, timeout=5)
        except Exception as e:
            print(f"Error al enviar a Telegram: {e}")

avisos_db = [
    {"id": 1, "titulo": "Inscripciones Abiertas 2026", "fecha": "10 de Junio, 2026", "contenido": "Proceso de entrega de fichas para alumnos de nuevo ingreso disponible en las ventanillas del plantel."},
    {"id": 2, "titulo": "Convocatoria Becas Benito Juárez", "fecha": "08 de Junio, 2026", "contenido": "Revisar la documentación requerida para la actualización del padrón de beneficiarios."}
]

carreras_db = [
    {"nombre": "Técnico en Programación", "descripcion": "Aprende a desarrollar software, aplicaciones móviles y páginas web con tecnologías de vanguardia.", "campo": "Empresas de desarrollo tecnológico, soporte técnico o emprendimiento propio."},
    {"nombre": "Técnico en Contabilidad", "descripcion": "Gestiona operaciones financieras, auditorías y declaraciones fiscales de empresas públicas y privadas.", "campo": "Despachos contables, bancos y departamentos administrativos."},
    {"nombre": "Técnico en Administración", "descripcion": "Optimiza los recursos humanos, materiales y financieros de cualquier organización moderna.", "campo": "Áreas de recursos humanos, mercadotecnia y logística corporativa."}
]

@app.route('/')
def inicio():
    enviar_notificacion_telegram("👁️ Alguien acaba de visitar la página de Inicio del CBTis 204.")
    return render_template('index.html', avisos=avisos_db, carreras=carreras_db)

@app.route('/contacto', methods=['POST'])
def contacto():
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    mensaje = request.form.get('mensaje')

    alerta = f"📩 ¡Nuevo Mensaje en la Web del CBTis 204!\n\n👤 Nombre: {nombre}\n📧 Correo: {correo}\n💬 Mensaje: {mensaje}"
    enviar_notificacion_telegram(alerta)

    flash("¡Tu mensaje ha sido enviado con éxito! El bot ha notificado al administrador.", "success")
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
