import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime

class EmailService:
    """Servicio de envío de correos usando Mailtrap"""
    
    def __init__(self):
        # Configuración Mailtrap
        self.smtp_server = "sandbox.smtp.mailtrap.io"
        self.smtp_port = 2525
        self.username = "29820646eeb8eb"
        self.password = "298f6a0f84e21e"
        self.sender_email = "sistema@datux.com"
        self.sender_name = "Sistema Inmobiliario DATUX"
    
    def send_email(self, to_email, subject, message, html_message=None, attachments=None):
        """
        Enviar correo electrónico
        
        Args:
            to_email (str): Email del destinatario
            subject (str): Asunto del correo
            message (str): Mensaje en texto plano
            html_message (str, optional): Mensaje en HTML
            attachments (list, optional): Lista de rutas de archivos adjuntos
        
        Returns:
            bool: True si se envió exitosamente, False en caso contrario
        """
        try:
            # Crear mensaje
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            msg['Date'] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
            
            # Agregar mensaje de texto
            part_text = MIMEText(message, 'plain', 'utf-8')
            msg.attach(part_text)
            
            # Agregar mensaje HTML si se proporciona
            if html_message:
                part_html = MIMEText(html_message, 'html', 'utf-8')
                msg.attach(part_html)
            
            # Agregar archivos adjuntos si se proporcionan
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        self._attach_file(msg, file_path)
                    else:
                        print(f"⚠️ Archivo no encontrado: {file_path}")
            
            # Enviar correo
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                text = msg.as_string()
                server.sendmail(self.sender_email, to_email, text)
            
            print(f"✅ Correo enviado exitosamente a {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error al enviar correo a {to_email}: {e}")
            return False
    
    def _attach_file(self, msg, file_path):
        """Adjuntar archivo al mensaje"""
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                
            encoders.encode_base64(part)
            filename = os.path.basename(file_path)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}'
            )
            msg.attach(part)
            
        except Exception as e:
            print(f"❌ Error al adjuntar archivo {file_path}: {e}")
    
    def send_welcome_email(self, to_email, nombre_cliente):
        """Enviar correo de bienvenida a nuevo cliente"""
        subject = "¡Bienvenido a Sistema Inmobiliario DATUX!"
        
        message = f"""
            Estimado/a {nombre_cliente},

            ¡Bienvenido/a al Sistema Inmobiliario DATUX!

            Nos complace informarle que su registro ha sido exitoso y ahora forma parte de nuestra familia de clientes.

            En DATUX encontrará las mejores opciones inmobiliarias con un servicio personalizado y de alta calidad.

            Nuestro equipo de ventas se pondrá en contacto con usted para brindarle la mejor asesoría.

            Saludos cordiales,
            Equipo DATUX
        """
        
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .header {{ background-color: #2c5282; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .footer {{ background-color: #f7fafc; padding: 10px; text-align: center; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>¡Bienvenido a DATUX!</h1>
            </div>
            <div class="content">
                <h2>Estimado/a {nombre_cliente},</h2>
                <p>¡Bienvenido/a al Sistema Inmobiliario DATUX!</p>
                <p>Nos complace informarle que su registro ha sido exitoso y ahora forma parte de nuestra familia de clientes.</p>
                <p>En DATUX encontrará las mejores opciones inmobiliarias con un servicio personalizado y de alta calidad.</p>
                <p>Nuestro equipo de ventas se pondrá en contacto con usted para brindarle la mejor asesoría.</p>
            </div>
            <div class="footer">
                <p>Equipo DATUX - Sistema Inmobiliario</p>
                <p>Este es un correo automático, por favor no responder.</p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(to_email, subject, message, html_message)
    
    def send_transaction_notification(self, to_email, nombre_cliente, codigo_transaccion, tipo_transaccion, producto_descripcion, monto):
        """Enviar notificación de transacción"""
        subject = f"Confirmación de {tipo_transaccion.title()} - {codigo_transaccion}"
        
        message = f"""
            Estimado/a {nombre_cliente},

            Le confirmamos que su {tipo_transaccion} ha sido registrada exitosamente.

            Detalles de la transacción:
            - Código: {codigo_transaccion}
            - Tipo: {tipo_transaccion.title()}
            - Propiedad: {producto_descripcion}
            - Monto: S/. {monto:,.2f}

            En breve recibirá la documentación correspondiente.

            Saludos cordiales,
            Equipo DATUX
        """
        
        return self.send_email(to_email, subject, message)
    
    def send_payment_reminder(self, to_email, nombre_cliente, monto_pendiente, fecha_vencimiento):
        """Enviar recordatorio de pago"""
        subject = "Recordatorio de Pago - Sistema DATUX"
        
        message = f"""
        Estimado/a {nombre_cliente},

        Le recordamos que tiene un pago pendiente:

        - Monto pendiente: S/. {monto_pendiente:,.2f}
        - Fecha de vencimiento: {fecha_vencimiento}

        Para realizar su pago, puede contactarnos o acercarse a nuestras oficinas.

        Saludos cordiales,
        Equipo DATUX
    """
        
        return self.send_email(to_email, subject, message)

# Funciones de conveniencia para uso rápido
def send_simple_email(to_email, subject, message):
    """Función simple para enviar un correo básico"""
    email_service = EmailService()
    return email_service.send_email(to_email, subject, message)

def send_welcome_email(to_email, nombre_cliente):
    """Función simple para enviar correo de bienvenida"""
    email_service = EmailService()
    return email_service.send_welcome_email(to_email, nombre_cliente)

def send_notification_email(to_email, nombre_cliente, codigo_transaccion, tipo_transaccion, producto_descripcion, monto):
    """Función simple para enviar notificación de transacción"""
    email_service = EmailService()
    return email_service.send_transaction_notification(to_email, nombre_cliente, codigo_transaccion, tipo_transaccion, producto_descripcion, monto)

# Ejemplo de uso
if __name__ == "__main__":
    # Crear instancia del servicio
    email_service = EmailService()
    
    # Enviar correo simple
    resultado = email_service.send_email(
        to_email="cliente@example.com",
        subject="Prueba de Sistema DATUX",
        message="Este es un mensaje de prueba del sistema inmobiliario DATUX."
    )
    
    if resultado:
        print("Correo enviado exitosamente")
    else:
        print("Error al enviar correo")
