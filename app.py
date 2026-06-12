import os
from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'cbtis204_secret_key'

# Conexión con las variables de entorno del Bot de Telegram
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

# Base de datos temporal en memoria (Soporta títulos, textos y enlaces de imágenes)
avisos_db = [
    {
        "id": 1, 
        "titulo": "Inscripciones Abiertas 2026", 
        "fecha": "10 de Junio, 2026", 
        "contenido": "Proceso de entrega de fichas para alumnos de nuevo ingreso disponible en las ventanillas del plantel.",
        "imagen": "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?q=80&w=600"
    },
    {
        "id": 2, 
        "titulo": "Convocatoria Becas Benito Juárez", 
        "fecha": "08 de Junio, 2026", 
        "contenido": "Revisar la documentación requerida para la actualización del padrón de beneficiarios del gobierno federal.",
        "imagen": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?q=80&w=600"
    }
]

carreras_db = [
    {"nombre": "Técnico en Programación", "descripcion": "Aprende a desarrollar software, aplicaciones móviles y páginas web con tecnologías de vanguardia.", "campo": "Empresas de desarrollo tecnológico, soporte técnico o de ofimática."},
    {"nombre": "Técnico en Contabilidad", "descripcion": "Gestiona operaciones financieras, auditorías y declaraciones fiscales de empresas públicas y privadas.", "campo": "Despachos contables, bancos y departamentos administrativos."},
    {"nombre": "Técnico en Administración", "descripcion": "Optimiza los recursos humanos, materiales y financieros de cualquier organización moderna.", "campo": "Áreas de recursos humanos, mercadotecnia y logística corporativa."}
]

@app.route('/')
def inicio():
    enviar_notificacion_telegram("👁️ ¡Alguien acaba de visitar la plataforma interactiva del CBTis 204!")
    return render_template('index.html', avisos=avisos_db, carreras=carreras_db)

# RUTA PARA PUBLICAR NUEVOS AVISOS DESDE LA WEB
@app.route('/subir-aviso', methods=['POST'])
def subir_aviso():
    titulo = request.form.get('titulo')
    fecha = request.form.get('fecha')
    contenido = request.form.get('contenido')
    imagen = request.form.get('imagen')

    # Si no pones foto, el sistema asigna una por defecto
    if not imagen:
        imagen = "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?q=80&w=600"

    nuevo_aviso = {
        "id": len(avisos_db) + 1,
        "titulo": titulo,
        "fecha": fecha,
        "contenido": contenido,
        "imagen": imagen
    }
    
    # Se inserta en la posición 0 para que aparezca inmediatamente arriba
    avisos_db.insert(0, nuevo_aviso)
    
    enviar_notificacion_telegram(f"📢 ¡Nuevo aviso publicado en la cartelera!\nTítulo: {titulo}\nFecha: {fecha}")
    flash("¡Excelente! El aviso ha sido publicado e integrado con éxito en la cartelera.", "success")
    return redirect(url_for('inicio'))

# RUTA PARA LA VENTANILLA DE CONTACTO
@app.route('/contacto', methods=['POST'])
def contacto():
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    mensaje = request.form.get('mensaje')
    
    alerta = f"📩 ¡Nuevo Mensaje en la Web del CBTis 204!\n\n👤 Nombre: {nombre}\n📧 Correo: {correo}\n💬 Mensaje: {mensaje}"
    enviar_notificacion_telegram(alerta)
    
    flash("¡Tu mensaje ha sido enviado con éxito! El bot ha notificado a la dirección del plantel.", "success")
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
