from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import box
from sqlite3 import Connection
from config.email import EmailService

import sqlite3
from sqlite3 import Connection

class InmobiliariaService:
    def __init__(self, conn: Connection):
        self.conn = conn

    def listar_propiedades(self):
        """Muestra todas las propiedades disponibles"""
        cursor = self.conn.cursor()
        try:
            # Seleccionamos codigo, titulo, precio y estado
            query = "SELECT codigo_producto, titulo, precio, moneda, estado FROM productos"
            cursor.execute(query)
            propiedades = cursor.fetchall()

            if not propiedades:
                print("\n⚠️ No hay propiedades registradas.")
                return

            print("\n--- 🏠 LISTADO DE PROPIEDADES ---")
            print(f"{'CÓDIGO':<10} | {'PRECIO':<15} | {'ESTADO':<12} | {'TÍTULO'}")
            print("-" * 80)
            
            for p in propiedades:
                # p[0]=codigo, p[1]=titulo, p[2]=precio, p[3]=moneda, p[4]=estado
                precio_fmt = f"{p[3]} {p[2]:,.2f}"
                print(f"{p[0]:<10} | {precio_fmt:<15} | {p[4]:<12} | {p[1]}")
            print("-" * 80)

        except Exception as e:
            print(f"❌Error al listar propiedades: {e}")

    def listar_clientes(self):
        """Muestra la cartera de clientes"""
        cursor = self.conn.cursor()
        try:
            query = "SELECT nombre, apellido, email, telefono FROM clientes"
            cursor.execute(query)
            clientes = cursor.fetchall()

            if not clientes:
                print("\n⚠️ No hay clientes registrados.")
                return

            print("\n--- 👥 CARTERA DE CLIENTES ---")
            for c in clientes:
                print(f"👤 {c[0]} {c[1]} | 📧 {c[2]} | 📞 {c[3]}")
        except Exception as e:
            print(f"❌ Error al listar clientes: {e}")


    #ENVIAR EMAIL
    def enviar_ficha_propiedad(self):
        """Envía los detalles de una propiedad por correo"""
        self.console.print("\n[bold blue]📧 ENVIAR FICHA DE PROPIEDAD[/bold blue]")
        
        #Pedimos el código de la propiedad
        codigo = Prompt.ask("Ingrese el [cyan]CÓDIGO[/cyan] de la propiedad")
        
        cursor = self.conn.cursor()
        query = "SELECT codigo_producto, titulo, descripcion, precio, moneda, direccion, area_total FROM productos WHERE codigo_producto = ?"
        cursor.execute(query, (codigo,))
        propiedad = cursor.fetchone()

        if not propiedad:
            self.console.print(f"[bold red]❌ La propiedad {codigo} no existe.[/bold red]")
            return

        #Pedimos el correo del destinatario
        destinatario = Prompt.ask("Ingrese el [green]EMAIL[/green] del cliente")

        #Preparamos el Asunto y Mensaje Personalizado
        #Desempaquetamos datos:
        titulo_prop = propiedad[1]
        precio_fmt = f"{propiedad[4]} {propiedad[3]:,.2f}"
        
        
        subject = f"Oportunidad Inmobiliaria: {titulo_prop} - DATUX"
        
        mensaje = f"""
        Hola,

        Gracias por tu interés en nuestras propiedades. Aquí tienes la ficha técnica solicitada:

        🏡 {titulo_prop}
        ----------------------------------------------------
        💰 Precio:      {precio_fmt}
        📍 Dirección:   {propiedad[5]}
        sz  Área Total:  {propiedad[6]} m2
        📝 Descripción: {propiedad[2]}
        ----------------------------------------------------

        Si deseas agendar una visita, responde a este correo.

        Atentamente,
        El Equipo de Ventas DATUX
        """

        self.console.print("[yellow]Enviando correo...[/yellow]")
        
        #Llamamos a la clase EmailService
        exito = self.email_service.send_email(
            to_email=destinatario,
            subject=subject,
            message=mensaje,
        )

        if exito:
            self.console.print(f"[bold green]✅ Ficha enviada correctamente a {destinatario}[/bold green]")
        else:
            self.console.print("[bold red]❌ Hubo un error al enviar el correo.[/bold red]")