from openpyxl_utils.utils import iniciar_planilha, descobrir_linha_vazia_planilha


def remover_dados_intervalo_planilha(conteudo, intervalo: str, ultima_linha: bool = False) -> None:
    """
    Apaga os dados presentes no intervalo informado.
    Caso o intervalo esteja vazio, um erro de Index é gerado. <- FUNCIONALIDADE DESATIVADA
    :param conteudo: Arquivo da planilha excel.
    :param intervalo: Intervalo que será apagado.
    :param ultima_linha: Define se deverá ser pego até a ultima linha do intervalo informado. 'A2:E'
    :return: None
    """
    if ultima_linha:
        intervalo: str = intervalo + descobrir_linha_vazia_planilha(conteudo, intervalo[0])

    planilha = iniciar_planilha(conteudo)
    aba_ativa = planilha.active

    try:
        for celula in aba_ativa[intervalo]:
            for elemento in celula:
                # if elemento.value is None:  # -> Gerando o erro de função específica.
                    # raise IndexError
                elemento.value = None
    # except IndexError:
        # print('Error - remover_dados_intervalo_planilha() | Uma ou mais células já estão vazias.')
    except:
        print('Error - remover_dados_intervalo_planilha()')
    else:
        planilha.save('PlanilhaExcel\\Arquivo.xlsx')
    finally:
        planilha.close()
