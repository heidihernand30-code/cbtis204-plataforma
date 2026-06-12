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

# Base de datos temporal con imágenes de calidad académica incorporadas
avisos_db = [
    {
        "id": 1, 
        "titulo": "Proceso de Inscripciones Ciclo Escolar", 
        "fecha": "12 de Junio, 2026", 
        "contenido": "Se convoca a la comunidad de alumnos aspirantes a completar el registro de expedientes y recepción de fichas en el departamento de Servicios Escolares del plantel.",
        "imagen": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=600"
    },
    {
        "id": 2, 
        "titulo": "Actualización Padrón Becas Benito Juárez", 
        "fecha": "08 de Junio, 2026", 
        "contenido": "Atención becarios: Favor de acudir con la documentación oficial solicitada a las ventanillas de Oficina de Vinculación para evitar suspensiones del apoyo.",
        "imagen": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?q=80&w=600"
    }
]

carreras_db = [
    {"nombre": "Técnico en Programación", "descripcion": "Formación integral centrada en el diseño, desarrollo, pruebas y mantenimiento de sistemas de software, aplicaciones web y móviles optimizadas.", "campo": "Empresas globales de TI, consultorías de software, startups tecnológicas y departamentos de soporte técnico informático."},
    {"nombre": "Técnico en Contabilidad", "descripcion": "Capacitación especializada en el registro de operaciones financieras, control de presupuestos, auditorías internas y declaraciones fiscales oficiales.", "campo": "Despachos contables, instituciones bancarias, dependencias de gobierno y áreas administrativas corporativas."},
    {"nombre": "Técnico en Administración", "descripcion": "Desarrollo de competencias para coordinar el capital humano, optimizar recursos materiales y estructurar planes de marketing estratégicos.", "campo": "Áreas de recursos humanos, logística, planeación comercial y control operativo de todo tipo de empresas."}
]

@app.route('/')
def inicio():
    enviar_notificacion_telegram("👁️ ¡Visita detectada en el nuevo portal institucional DGETI del CBTis 204!")
    return render_template('index.html', avisos=avisos_db, carreras=carreras_db)

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
    enviar_notificacion_telegram(f"📢 ¡Nuevo Comunicado Institucional publicado!\nTítulo: {titulo}")
    flash("El comunicado ha sido integrado con éxito a la cartelera oficial DGETI.", "success")
    return redirect(url_for('inicio'))

@app.route('/contacto', methods=['POST'])
def contacto():
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    mensaje = request.form.get('mensaje')
    
    alerta = f"📩 ¡Correspondencia Virtual Recibida!\n\n👤 Remitente: {nombre}\n📧 Correo: {correo}\n💬 Asunto: {mensaje}"
    enviar_notificacion_telegram(alerta)
    
    flash("Su mensaje formal ha sido turnado con éxito a las autoridades escolares mediante la interconexión digital.", "success")
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
