const contactos = document.querySelectorAll(".btn-contacto");

var activo;

for (var i=0;i<contactos.length;i++){
    contactos[i].addEventListener("click",(evento)=>{
        contacto = evento.path[0];
        if(activo){
            activo.classList.remove("active");
        }
        document.querySelector(".receptor").value = contacto.innerText;
        contacto.classList.add("active");
        activo = contacto
    });
}