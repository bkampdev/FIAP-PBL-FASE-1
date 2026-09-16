CONSTANTE MODULOS_CRITICOS <- ["suporte_vida", "energia", "comunicacao", "propulsao", "navegacao"]

INICIO verificar_pre_decolagem(dados, energia, limites)

    motivos <- lista vazia

    PARA CADA campo EM limites FACA
        SE campo NAO EXISTE EM dados ENTAO
            adicionar "Campo ausente na telemetria: {campo}" em motivos
            PROXIMO campo
        FIM SE

        valor  <- dados[campo]
        minimo <- limites[campo][0]
        maximo <- limites[campo][1]

        SE valor < minimo ENTAO
            adicionar "{campo} {valor} abaixo do minimo de {minimo}" em motivos
        FIM SE

        SE valor > maximo ENTAO
            adicionar "{campo} {valor} acima do maximo de {maximo}" em motivos
        FIM SE
    FIM PARA

    SE "integridade_estrutural" NAO EXISTE EM dados ENTAO
        adicionar "Campo ausente na telemetria: integridade_estrutural" em motivos
    SENAO SE dados["integridade_estrutural"] DIFERENTE DE "NOMINAL" E DIFERENTE DE 1 ENTAO
        adicionar "Integridade estrutural {dados["integridade_estrutural"]}, esperado NOMINAL ou 1" em motivos
    FIM SE

    SE "modulos" NAO EXISTE EM dados ENTAO
        adicionar "Campo ausente na telemetria: modulos" em motivos
    SENAO
        PARA CADA modulo EM MODULOS_CRITICOS FACA
            SE modulo NAO EXISTE EM dados["modulos"] ENTAO
                adicionar "Modulo ausente na telemetria: {modulo}" em motivos
            SENAO SE dados["modulos"][modulo] IGUAL A "FALHA" ENTAO
                adicionar "Modulo critico em falha: {modulo}" em motivos
            FIM SE
        FIM PARA
    FIM SE

    SE energia NAO E UM DICIONARIO ENTAO
        adicionar "Resultado energetico ausente ou invalido" em motivos
    SENAO SE energia["viavel"] DIFERENTE DE VERDADEIRO ENTAO
        saldo <- energia["saldo_kwh"]
        SE saldo E NUMERO (inteiro ou real, exceto booleano) ENTAO
            adicionar "Energia insuficiente: saldo de {saldo} kWh" em motivos
        SENAO
            adicionar "Resultado energetico invalido" em motivos
        FIM SE
    FIM SE

    SE tamanho(motivos) IGUAL A 0 ENTAO
        RETORNAR {decisao: "PRONTO PARA DECOLAR", motivos: lista vazia}
    SENAO
        RETORNAR {decisao: "DECOLAGEM ABORTADA", motivos: motivos}
    FIM SE

FIM