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

# Base de datos en memoria con fotos académicas predeterminadas
avisos_db = [
    {
        "id": 1, 
        "titulo": "Proceso de Inscripciones Ciclo Escolar", 
        "fecha": "14 de Junio, 2026", 
        "contenido": "Se convoca a todos los alumnos aspirantes a completar la entrega de expedientes y recepción de fichas oficiales de admisión en las ventanillas de Servicios Escolares.",
        "imagen": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=600"
    },
    {
        "id": 2, 
        "titulo": "Actualización Padrón Becas Benito Juárez", 
        "fecha": "08 de Junio, 2026", 
        "contenido": "Atención becarios del plantel: Favor de acudir con la documentación oficial solicitada a las oficinas de Vinculación para validar sus datos de apoyo económico.",
        "imagen": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?q=80&w=600"
    }
]

carreras_db = [
    {"nombre": "Técnico en Programación", "descripcion": "Formación integral centrada en el diseño, desarrollo, pruebas y mantenimiento de sistemas de software, aplicaciones web y móviles multiplataforma.", "campo": "Empresas globales de TI, consultorías de desarrollo, startups y departamentos de soporte técnico informático o de ofimática."},
    {"nombre": "Técnico en Contabilidad", "descripcion": "Capacitación especializada en el registro de operaciones financieras, control de presupuestos, auditorías contables y declaraciones fiscales empresariales.", "campo": "Despachos contables, instituciones bancarias, dependencias fiscales de gobierno y áreas financieras de corporativos."},
    {"nombre": "Técnico en Administración", "descripcion": "Desarrollo de competencias estratégicas para coordinar capital humano, optimizar recursos materiales y estructurar planes comerciales institucionales.", "campo": "Áreas de recursos humanos, logística, planeación comercial y control de operaciones en micro, medianas y grandes empresas."}
]

@app.route('/')
def inicio():
    enviar_notificacion_telegram("👁️ ¡Exploración detectada en la plataforma estructurada del CBTis 204!")
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
    enviar_notificacion_telegram(f"📢 ¡Nuevo Aviso publicado en Cartelera!\nTítulo: {titulo}")
    flash("El aviso institucional ha sido publicado de forma exitosa en la sección de Cartelera.", "success")
    return redirect(url_for('inicio'))

@app.route('/contacto', methods=['POST'])
def contacto():
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    mensaje = request.form.get('mensaje')
    
    alerta = f"📩 ¡Nueva consulta formal en ventanilla!\n\n👤 Remitente: {nombre}\n📧 Correo: {correo}\n💬 Mensaje: {mensaje}"
    enviar_notificacion_telegram(alerta)
    
    flash("Su mensaje formal ha sido turnado de forma exitosa mediante la interconexión digital.", "success")
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
