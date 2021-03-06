function formatarMoeda(element) {
    const valor = element.value.match(/[0-9]/g).join('').padStart(3, '0');
    if (valor === '000'){
        element.value = '';
    } else {
        const [inteiro, decimal] = (parseInt(valor) / 100).toFixed(2).split('.');
        const inteiro_formatado = inteiro.split('').reverse().reduce((grupo, numero, ordem) => {
            if (ordem <= 1) {
                grupo.push(numero);
            } else {
                if (((ordem + 1) % 3) === 1) {
                    grupo.push(`${numero}.`);
                } else {
                    grupo.push(numero);
                }
            }
            return grupo;
        }, []).reverse().join('');
        element.value = `${inteiro_formatado},${decimal}`;
    }
}