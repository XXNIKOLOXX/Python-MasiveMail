import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

# Lista de correos y nombres
Lista_Correos = [
    ["empresa1@gmail.com", "Empresa 1"],
    ["empresa2@gmail.com", "Empresa2"],
    ["Empresa3@gmail.com", "Empresa3"]
]

# Configuración del servidor SMTP
smtp_server = 'smtp.gmail.com'
smtp_port = 465  # Puerto para conexiones SSL
your_email = os.getenv("MAIL_SENDER")  # Tu correo electrónico
your_password = os.getenv("PASSWORD")  # Tu contraseña o token de acceso

# Crear conexión con el servidor SMTP utilizando SSL
server = smtplib.SMTP_SSL(smtp_server, smtp_port)

# Iniciar sesión en el servidor
try:
    server.login(your_email, your_password)
except Exception as e:
    print(f'Error en el inicio de sesión: {e}')
    server.quit()
    raise

# Asunto y cuerpo del mensaje
subject = 'Solicitud de práctica de inducción - Estudiante de Ingeniería Civil Industrial'
body_template = '''Estimado equipo de {NombreEmpresa}:

Mi nombre es Nicolás Reyes, soy estudiante de Ingeniería Civil Industrial en la Universidad Austral de Chile. Estoy buscando realizar una práctica de inducción de 360 horas durante los meses de enero y febrero.

Me gustaría conocer sobre las oportunidades disponibles en su empresa y cómo podría contribuir y aprender durante ese tiempo. Adjunto mi currículum y quedo a disposición para cualquier consulta.

Agradezco su atención y quedo atento a su respuesta.

Saludos cordiales,

Nicolás Reyes
+56 9 6361 5571
{tu_email}
'''

# Ruta al currículum
cv_path = r'C:\Users\Lenovo\Desktop\EnvioCorreos\CV Nicolás Reyes.pdf'  # Ruta al currículum

# Índice para el ciclo while
index = 0

# Ciclo while para enviar correos
while index < len(Lista_Correos):
    email, name = Lista_Correos[index]
    
    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = your_email
    msg['To'] = email
    msg['Subject'] = subject

    # Personalizar el cuerpo del mensaje
    body = body_template.format(NombreEmpresa=name, tu_email=your_email)
    msg.attach(MIMEText(body, 'plain'))

    # Adjuntar el currículum
    with open(cv_path, 'rb') as file:
        part = MIMEApplication(file.read(), Name=os.path.basename(cv_path))
    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(cv_path)}"'
    msg.attach(part)

    # Enviar el correo
    try:
        server.send_message(msg)
        print(f'Correo enviado a {name} <{email}>')
    except Exception as e:
        print(f'Error al enviar correo a {name} <{email}>: {e}')

    # Incrementar el índice
    index += 1

# Cerrar la conexión
server.quit()
