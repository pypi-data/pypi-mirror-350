from openpyxl_utils.utils import iniciar_planilha, descobrir_linha_vazia_planilha, is_merged, List


def pegar_dados_intervalo_planilha(conteudo, intervalo: str, ultima_linha: bool = False) -> List[list]:
    """
    Retorna os valores presentes no intervalo informado.
    Os valores são retornados dentro de uma lista.
    A lista retornada contém listas para cada linha do intervalo informado.
    Ex: [['Pessoa1', 46, 2500, 'Jogador', '987654321'], ['Pessoa2', 22, 8000, 'Streamer', '768948302']]
    :param conteudo: Arquivo da planilha excel, podendo ser um path ou o arquivo em bytes.
    :param intervalo: Intervalo da planilha.
    :param ultima_linha: Define se deverá ser pego até a ultima linha do intervalo informado.
    :return: Retorna uma lista contendo os valores.
    """
    if ultima_linha:
        intervalo: str = intervalo + descobrir_linha_vazia_planilha(conteudo)

    planilha = iniciar_planilha(conteudo)
    aba_ativa = planilha.active

    try:
        valores: list = []

        merged_ranges = aba_ativa.merged_cells.ranges  # -> Coleta todas as faixas de células mescladas na aba ativa da planilha.
        """
            merged_ranges = aba_ativa.merged_cells.ranges
            Explicação: 
                aba_ativa.merged_cells - Retorna um objeto que contém todas as faixas de células mescladas na planilha.
                ranges - Fornece uma lista de todas as faixas mescladas. Cada faixa é representada como um objeto CellRange.
        """

        # Adicionei os if's para impedir que dados vazios sejam obtidos.
        for linha in aba_ativa[intervalo]:
            valores_linha: list = []
            is_full_empty: bool = True

            for celula in linha:
                if celula.value is not None:
                    valores_linha.append(celula.value)
                    is_full_empty = False
                elif is_merged(celula, merged_ranges):
                    pass  # -> Célula mesclada sem valor direto
                else:  # -> Se não tiver valor, coloco string vazia.
                    valores_linha.append('')  # -> # Mantém a posição.

            if len(valores_linha) > 0:
                if not is_full_empty:
                    valores.append(valores_linha)
    except Exception as e:
        print(f"[ERRO] pegar_dados_intervalo_planilha: {e}")
        return []
    else:
        return valores
    finally:
        planilha.close()
