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

# Base de datos de avisos con imágenes académicas de alta definición incorporadas
avisos_db = [
    {
        "id": 1, 
        "titulo": "Apertura del Registro de Nuevos Ingresos 2026", 
        "fecha": "14 de Junio, 2026", 
        "contenido": "Se informa a todos los egresados de secundaria del estado de Michoacán que las ventanillas de Servicios Escolares han abierto la recepción física de carpetas para el examen de admisión del periodo actual.",
        "imagen": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=600"
    },
    {
        "id": 2, 
        "titulo": "Convocatoria Oficial: Becas Benito Juárez", 
        "fecha": "10 de Junio, 2026", 
        "contenido": "El Departamento de Vinculación convoca a los alumnos de todos los semestres a revisar las listas del padrón y entregar la documentación requerida para evitar suspensiones del apoyo.",
        "imagen": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?q=80&w=600"
    }
]

# LAS 5 CARRERAS OFICIALES DEL CBTIS 204
carreras_db = [
    {
        "nombre": "Técnico en Ofimática", 
        "icono": "fa-desktop",
        "descripcion": "Especialidad enfocada en la gestión de sistemas de información, automatización de procesos administrativos, diseño de documentos digitales y optimización de bases de datos de entornos corporativos.", 
        "campo": "Departamentos administrativos, empresas de servicios, gestión de datos y secretarías digitales."
    },
    {
        "nombre": "Técnico en Construcción", 
        "icono": "fa-helmet-safety",
        "descripcion": "Capacitación en interpretación de planos arquitectónicos, supervisión de obras civiles, estimación de costos y presupuestos, y control de calidad de materiales bajo normas de seguridad industrial.", 
        "campo": "Constructoras privadas, despachos de arquitectura, obras públicas y supervisión de proyectos edilicios."
    },
    {
        "nombre": "Técnico en Administración", 
        "icono": "fa-briefcase",
        "descripcion": "Formación estratégica orientada al desarrollo de planes de marketing corporativo, gestión eficiente del capital humano, logística de inventarios y control operativo empresarial.", 
        "campo": "Áreas de recursos humanos, departamentos de ventas, logística comercial y control interno de empresas."
    },
    {
        "nombre": "Técnico en Contabilidad", 
        "icono": "fa-calculator",
        "descripcion": "Especialidad en el registro sistemático de operaciones financieras, auditorías internas, cálculo de obligaciones fiscales y control presupuestario de organizaciones públicas y privadas.", 
        "campo": "Despachos contables, instituciones bancarias, finanzas corporativas y tesorerías."
    },
    {
        "nombre": "Técnico en Vida Saludable", 
        "icono": "fa-heart-pulse",
        "descripcion": "Área de vanguardia enfocada en la promoción del bienestar integral, desarrollo de planes de nutrición comunitaria, acondicionamiento físico adaptado y fomento de hábitos sustentables.", 
        "campo": "Centros de salud comunitaria, instituciones deportivas, consultorías de bienestar y desarrollo social."
    }
]

@app.route('/')
def inicio():
    enviar_notificacion_telegram("👁️ ¡Portal Premium DGETI del CBTis 204 cargado en la web!")
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
    enviar_notificacion_telegram(f"📢 ¡Aviso publicado!\nTítulo: {titulo}")
    flash("El comunicado institucional ha sido integrado con éxito a la cartelera pública de la DGETI.", "success")
    return redirect(url_for('inicio'))

@app.route('/contacto', methods=['POST'])
def contacto():
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    mensaje = request.form.get('mensaje')
    
    alerta = f"📩 ¡Nueva correspondencia en el portal del CBTis 204!\n\n👤 Remitente: {nombre}\n📧 Correo: {correo}\n💬 Mensaje: {mensaje}"
    enviar_notificacion_telegram(alerta)
    
    flash("Su correspondencia virtual ha sido procesada e interconectada con el sistema de dirección.", "success")
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
