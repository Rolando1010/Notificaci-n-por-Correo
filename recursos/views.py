from recursos import app
from flask import render_template, request, redirect, url_for
from recursos.models import ingresarCorreo, obtenerCorreoId, obtenerIdCorreo, envioCorreoUsuario, obtenerContactosUsuario

@app.route("/", methods = ["POST","GET"])
def index():
    mensaje = ""
    if request.method=="POST":
        correo = request.form["correo"]
        contrasenna = request.form["contrasenna"]
        mensaje = ingresarCorreo(correo,contrasenna)
        if not mensaje:
            return redirect(url_for(".correos",id_correo=obtenerIdCorreo(correo)))
    return render_template("index.html",mensaje=mensaje)

@app.route("/<id_correo>", methods = ["POST","GET"])
def correos(id_correo):
    if id_correo!="favicon.ico":
        if request.method=="POST":
            print("! POST !")
            emisor = obtenerCorreoId(id_correo)
            receptor = request.form["receptor"]
            asunto = request.form["asunto"]
            texto = request.form["texto"]
            error = not envioCorreoUsuario(emisor,receptor,asunto,texto)
            return render_template("correos.html",correo=obtenerCorreoId(id_correo),envio=True,error=error,contactos=obtenerContactosUsuario(id_correo))
        return render_template("correos.html",correo=obtenerCorreoId(id_correo), contactos=obtenerContactosUsuario(id_correo))
    return render_template("correos.html",correo="a@a.a")