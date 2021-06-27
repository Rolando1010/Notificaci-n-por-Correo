import sqlite3
import smtplib

def realizarConsulta(consulta, cant_datos):
    conexion = sqlite3.connect('recursos/correos.sqlite3')
    tabla = conexion.execute(consulta)
    datos = []
    for fila in tabla:
        dato = []
        for i in range(0,cant_datos):
            dato += [fila[i]]
        datos += [dato]
    conexion.close()
    return datos

def ejecutarConsulta(consulta):
    conexion = sqlite3.connect('recursos/correos.sqlite3')
    conexion.execute(consulta)
    conexion.commit()

def ingresarCorreo(correo,contrasenna):
    consulta = realizarConsulta("select contrasenna from Correos where correo='"+correo+"'",1)
    if len(consulta)==0:
        prueba = enviarCorreo(correo,"notificacioncorreosportafolio@gmail.com",contrasenna,"Prueba","Prueba de Mensaje")
        if(prueba):
            ejecutarConsulta("insert into Correos (correo,contrasenna) values('"+correo+"','"+contrasenna+"')")
        else:
            return {"mensaje":"Sucedió un error, quizás no estés ingresando correctamente tu correo o contraseña.","advertencia":{"advertencia":"Es posible que la seguridad de tu correo esté impidiendo el ingreso, visita el enlace para solucionarlo.","enlace":"https://myaccount.google.com/u/0/lesssecureapps"}}
    else:
        if contrasenna!=consulta[0][0]:
            return {"mensaje":"La contraseña ingresada no corresponde con la específicada previamente."}


def enviarCorreo(emisor,receptor,contrasenna,asunto,mensaje):
    try:
        extension = 'outlook'
        if '@gmail.com' in emisor:
            extension = 'gmail'
        server = smtplib.SMTP('smtp.'+extension+'.com:587')
        server.ehlo()
        server.starttls()
        server.login(emisor, contrasenna)
        message = 'subject: {}\n\n{}'.format(asunto,mensaje)
        server.sendmail(emisor,receptor, message)
        server.quit()
        return True
    except:
        return False

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def enviarCorreoEnriquecido(emisor,receptor,contrasenna,asunto,mensaje):
    try:
        extension = 'outlook'
        if '@gmail.com' in emisor:
            extension = 'gmail'
        server = smtplib.SMTP('smtp.'+extension+'.com:587')
        server.ehlo()
        server.starttls()
        server.login(emisor, contrasenna)
        contenido = MIMEMultipart()
        mensajeHTML = MIMEText(mensaje, 'html')
        contenido["Subject"] = asunto
        contenido.attach(mensajeHTML)
        server.sendmail(emisor,receptor, contenido.as_string())
        server.quit()
        return True
    except:
        return False

def obtenerIdCorreo(correo):
    return realizarConsulta("select id from Correos where correo='"+correo+"'",1)[0][0]

def obtenerCorreoId(id_correo):
    return realizarConsulta("select correo from Correos where id="+str(id_correo),1)[0][0]

def obtenerContrasennaCorreo(correo):
    return realizarConsulta("select contrasenna from Correos where correo='"+correo+"'",1)[0][0]

def envioCorreoUsuario(emisor,receptor,asunto,mensaje):
    exito = enviarCorreoEnriquecido(emisor,receptor,obtenerContrasennaCorreo(emisor),asunto,mensaje)
    if exito:
        consulta = realizarConsulta("select id from Contactos where idCorreo="+str(obtenerIdCorreo(emisor))+" and correo='"+receptor+"'",1)
        if len(consulta)==0:
            ejecutarConsulta("insert into Contactos(idCorreo,correo) values("+str(obtenerIdCorreo(emisor))+",'"+receptor+"')")
    return exito

def obtenerContactosUsuario(id_correo):
    consulta = realizarConsulta("select correo from Contactos where idCorreo="+id_correo,1)
    contactos = []
    for i in range(0,len(consulta)):
        contactos+=[consulta[i][0]]
    return contactos