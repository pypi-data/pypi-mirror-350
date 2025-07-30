# 📊 openpyxl-utils

[![PyPI version](https://badge.fury.io/py/openpyxl-utils.svg)](https://pypi.org/project/openpyxl-utils/)
[![Python version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Uma biblioteca **não oficial** com funções utilitárias para facilitar o uso da [openpyxl](https://openpyxl.readthedocs.io/en/stable/).  
Ideal para manipulações frequentes e repetitivas em arquivos `.xlsx` de forma mais simples e eficiente.

> ⚠️ Este projeto **não é afiliado ao projeto oficial `openpyxl`**. Trata-se de um *wrapper* auxiliar criado por terceiros.

---

## 🚀 Instalação

```bash 
  pip install openpyxl-utils
```

---

## ⚠️ Aviso 

⚠️ Esta biblioteca está em desenvolvimento. Algumas funções ainda estão sendo validadas.

---

## 💡 Exemplos de uso

### Leitura rápida de planilhas

```python
from openpyxl_utils import pegar_dados_intervalo_planilha

data = pegar_dados_intervalo_planilha("planilha.xlsx")
print(data)
```

---

## 🧱 Estrutura da biblioteca

```
openpyxl_utils/
├── adder/      # Funções para adicionar colunas, células, dados, etc.
├── reader/     # Funções para leitura facilitada
├── remover/    # Funções para limpeza e remoção de elementos
├── updater/    # Funções para atualizações de conteúdo
├── utils/      # Funções auxiliares internas
```

---

## 🤝 Contribuindo

Contribuições são muito bem-vindas!  
Sinta-se livre para abrir uma issue ou um pull request.

---

## 📄 Licença

Este projeto está licenciado sob a MIT License.

---

## 📬 Contato

Criado por **Witor Oliveira**  
🔗 [LinkedIn](https://www.linkedin.com/in/witoroliveira/)  
📫 [Contato por e-mail](mailto:witoredson@gmail.com)