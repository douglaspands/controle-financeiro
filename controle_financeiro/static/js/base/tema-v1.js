function menuLateralAbrir(acao = true){
    for (const elem of document.querySelectorAll('div[class^="menu-lateral"]')){
        if (acao) {
            elem.className = elem.className.replace("fechado", "aberto");
        } else {
            elem.className = elem.className.replace("aberto", "fechado");
        }
    }
}

class Modal {
    constructor(modalId) {
        this.modal = document.getElementById(modalId);
        window.onclick = function(event) {
            if (event.target == this.modal) {
              modal.style.display = "none";
            }
        }
    }
    open() {
        this.modal.style.display = "block";
    }
    close() {
        this.modal.style.display = "none";
    }
}
