const ojo = document.querySelector(".mostrar-ocultar-contrasenna");
const entrada_contrasenna = document.querySelector(".entrada-contrasenna");

const mostrar = `<i class="fas fa-eye"></i>`;
const ocultar = `<i class="fas fa-eye-slash"></i>`;

var oculto = true;

ojo.addEventListener("click",()=>{
    if(oculto){
        entrada_contrasenna.type = "text";
        ojo.innerHTML = ocultar;
    }else{
        entrada_contrasenna.type = "password";
        ojo.innerHTML = mostrar;
    }
    oculto = !oculto;
});