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

# Base de datos provisional estructurada
avisos_db = [
    {
        "id": 1, 
        "titulo": "Inicio de Evaluaciones del Periodo Escolar", 
        "fecha": "14 de Junio, 2026", 
        "contenido": "Se convoca a los alumnos a revisar los calendarios oficiales de exámenes colgados en la coordinación del plantel.",
        "imagen": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=600"
    },
    {
        "id": 2, 
        "titulo": "Reunión General de Padres de Familia", 
        "fecha": "10 de Junio, 2026", 
        "contenido": "Aviso oficial dirigido a los tutores legales para la entrega presencial de las boletas correspondientes al avance actual.",
        "imagen": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?q=80&w=600"
    }
]

@app.route('/')
def inicio():
    enviar_notificacion_telegram("👁️ ¡Portal Estructurado del CBTis 204 visitado!")
    return render_template('index.html', avisos=avisos_db)

@app.route('/subir-aviso', methods=['POST'])
def subir_aviso():
    titulo = request.form.get('titulo')
    fecha = request.form.get('fecha')
    contenido = request.form.get('contenido')
    imagen = request.form.get('imagen')

    if not imagen:
        imagen = "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=600"

    nuevo_aviso = {
        "id": len(avisos_db) + 1,
        "titulo": titulo,
        "fecha": fecha,
        "contenido": contenido,
        "imagen": imagen
    }
    
    avisos_db.insert(0, nuevo_aviso)
    enviar_notificacion_telegram(f"📢 ¡Aviso Monumental Publicado!\nTítulo: {titulo}")
    flash("El aviso se ha integrado al panel dinámico de la cartelera de forma exitosa.", "success")
    return redirect(url_for('inicio'))

@app.route('/contacto', methods=['POST'])
def contacto():
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    mensaje = request.form.get('mensaje')
    
    alerta = f"📩 ¡Nuevo Comentario Escolar Recibido!\n\n👤 Remitente: {nombre}\n📧 Correo: {correo}\n💬 Comentario: {mensaje}"
    enviar_notificacion_telegram(alerta)
    
    flash("Su comentario formal ha sido procesado e interconectado correctamente con la dirección.", "success")
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
