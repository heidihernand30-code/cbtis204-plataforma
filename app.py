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

# Base de datos en memoria ahora categorizada para el filtro interactivo
avisos_db = [
    {
        "id": 1, 
        "titulo": "Entrega de Fichas Oficiales 2026", 
        "fecha": "15 de Junio, 2026", 
        "categoria": "Inscripciones",
        "contenido": "Se abre el registro oficial de expedientes en las ventanillas de Servicios Escolares para alumnos de nuevo ingreso.",
        "imagen": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=600"
    },
    {
        "id": 2, 
        "titulo": "Validación de Becas Benito Juárez", 
        "fecha": "08 de Junio, 2026", 
        "categoria": "Becas",
        "contenido": "Atención becarios: Acudir con su credencial y expediente al departamento de Vinculación para asegurar la continuidad del apoyo.",
        "imagen": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?q=80&w=600"
    }
]

carreras_db = [
    {"nombre": "Técnico en Programación", "descripcion": "Estudio avanzado del desarrollo de sistemas lógicos, algoritmos complejos, páginas web dinámicas e ingeniería de software institucional.", "campo": "Empresas tecnológicas globales, administración de servidores web, soporte técnico corporativo y de ofimática."},
    {"nombre": "Técnico en Contabilidad", "descripcion": "Especialidad en auditorías, cálculo de presupuestos institucionales, balances generales financieros y declaraciones fiscales gubernamentales.", "campo": "Despachos contables, sector bancario, departamentos de finanzas públicos y privados."},
    {"nombre": "Técnico en Administración", "descripcion": "Formación enfocada en la optimización de recursos humanos, planeación estratégica de mercadotecnia y control logístico corporativo.", "campo": "Áreas de recursos humanos, gestión comercial, logística y control administrativo de empresas públicas o privadas."}
]

@app.route('/')
def inicio():
    enviar_notificacion_telegram("👁️ ¡Exploración avanzada en el portal interactivo del CBTis 204!")
    return render_template('index.html', avisos=avisos_db, carreras=carreras_db)

@app.route('/subir-aviso', methods=['POST'])
def subir_aviso():
    titulo = request.form.get('titulo')
    fecha = request.form.get('fecha')
    categoria = request.form.get('categoria')
    contenido = request.form.get('contenido')
    imagen = request.form.get('imagen')

    if not imagen:
        imagen = "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=600"

    nuevo_aviso = {
        "id": len(avisos_db) + 1,
        "titulo": titulo,
        "fecha": fecha,
        "categoria": categoria,
        "contenido": contenido,
        "imagen": imagen
    }
    
    avisos_db.insert(0, nuevo_aviso)
    enviar_notificacion_telegram(f"📢 ¡Se publicó un anuncio en {categoria}!\nTítulo: {titulo}")
    return redirect(url_for('inicio'))

@app.route('/contacto', methods=['POST'])
def contacto():
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    mensaje = request.form.get('mensaje')
    
    alerta = f"📩 ¡Nueva consulta escolar!\n\n👤 Remitente: {nombre}\n📧 Correo: {correo}\n💬 Mensaje: {mensaje}"
    enviar_notificacion_telegram(alerta)
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
