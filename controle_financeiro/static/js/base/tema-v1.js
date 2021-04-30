function menuLateralAbrir(acao = true){
    for (const elem of document.querySelectorAll('div[class^="menu-lateral"]')){
        if (acao) {
            elem.className = elem.className.replace("fechado", "aberto");
        } else {
            elem.className = elem.className.replace("aberto", "fechado");
        }
    }
}