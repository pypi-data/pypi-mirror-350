from openpyxl_utils.utils import iniciar_planilha, descobrir_linha_vazia_planilha


def adicionar_dados_fim_coluna(conteudo, valores_adicionar: list, coluna_inicial: str, coluna_final: str) -> None:
    """
    Adiciona todos os itens da lista informada nas linhas disponíveis na coluna informada.
    :param conteudo: Arquivo da planilha excel, podendo ser um path ou o arquivo em bytes.
    :param valores_adicionar: Lista de listas contendo os valores a serem adicionados.
    :param coluna_inicial: Primeira coluna onde os valores serão adicionados.
    :param coluna_final: Última coluna onde os valores serão adicionados.
    :return: None
    """
    try:
        ultima_linha: str = descobrir_linha_vazia_planilha(conteudo, coluna_inicial)
        comeco = int(ultima_linha) + 1
        fim = int(ultima_linha) + len(valores_adicionar)
        intervalo: str = f'{coluna_inicial}{comeco}:{coluna_final}{fim}'

        adicionar_dados_intervalo_planilha(conteudo, valores_adicionar, intervalo)
    except:
        print('Error - adicionar_dados_fim_coluna()')


def adicionar_dados_intervalo_planilha(conteudo, valores_adicionar: list, intervalo: str, ultima_linha: bool = False) -> None:
    """
    Adiciona os dados informados no intervalo especificado da planilha.
    Caso já existam dados nesse intervalo, gera um erro de Index. <- FUNCIONALIDADE DESATIVADA
    :param conteudo: Arquivo da planilha excel, podendo ser um path ou o arquivo em bytes.
    :param valores_adicionar: Lista de listas contendo os dados a serem adicionados.
    :param intervalo: Intervalo da planilha.
    :param ultima_linha: Define se deverá ser pego até a ultima linha do intervalo informado. 'A2:E'
    :return: None
    """
    if ultima_linha:
        intervalo: str = intervalo + descobrir_linha_vazia_planilha(conteudo, intervalo[0])

    planilha = iniciar_planilha(conteudo)
    aba_ativa = planilha.active

    try:
        for i, linha in enumerate(aba_ativa[intervalo]):  # -> A2, B2, C2, ...
            if i >= len(valores_adicionar):
                break
            for j, elemento in enumerate(linha):
                # if elemento.value is not None:  # -> Gerando o erro de função específica.
                    # raise IndexError("Já existe um valor na célula.")
                elemento.value = valores_adicionar[i][j]
    # except IndexError:
        # print(f'Error - adicionar_dados_intervalo_planilha() | Uma ou mais células já possuem um valor.')
    except:
        print('Error - adicionar_dados_intervalo_planilha()')
    else:
        planilha.save('PlanilhaExcel\\Arquivo.xlsx')
    finally:
        planilha.close()
