function formatarMoeda(elemento) {
    const elementoValor = elemento.value.replace(/[\D]+/g, '');
    if (elementoValor){
        const [inteiro, decimal] = (parseInt(elementoValor) / 100).toFixed(2).split('.');
        const inteiro_formatado = []
        inteiro.split('').reverse().forEach((numero, ordem) => {
            if (ordem <= 1) {
                inteiro_formatado.push(numero);
            } else {
                if (((ordem + 1) % 3) === 1){
                    inteiro_formatado.push(`${numero}.`);
                } else {
                    inteiro_formatado.push(numero);
                }
            }
        });
        const valorFormatado = `${inteiro_formatado.reverse().join('')},${decimal}`;
        elemento.value = valorFormatado;
    }
}