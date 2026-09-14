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
        adicionar "Integridade estrutural {valor}, esperado NOMINAL ou 1" em motivos
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

    SE energia E NULO ENTAO
        adicionar "Resultado energetico ausente" em motivos
    SENAO SE energia MENOR OU IGUAL A ZERO ENTAO
        adicionar "Energia insuficiente: autonomia de {energia} h" em motivos
    FIM SE

    SE tamanho(motivos) IGUAL A 0 ENTAO
        RETORNAR {decisao: "PRONTO PARA DECOLAR", motivos: lista vazia}
    SENAO
        RETORNAR {decisao: "DECOLAGEM ABORTADA", motivos: motivos}
    FIM SE

FIM
