# Python Data Integration System

Sistema robusto de integração de vendas desenvolvido em Python e MySQL, utilizando padrões de **Repository Pattern**, **Soft Delete** e **Auditoria de Dados**.

## 🛠️ Estrutura do Projeto

- **config/**: Configurações de ambiente e variáveis globais.
- **database/**: Gerenciamento da conexão com o MySQL.
- **models/**: Classes que representam as entidades (Customer, Product, Order).
- **repositories/**: Camada de persistência (Queries SQL isoladas).
- **services/**: Lógica de negócio e orquestração de dados.
- **data/**: Armazenamento de arquivos para importação/exportação.
- **logs/**: Registros de execução e erros do sistema.

## 🚀 Como Configurar

### 1. Pré-requisitos
- Python 3.8+
- MySQL Server 8.0+

### 2. Instalação de Dependências
No terminal, instale os pacotes necessários:
```bash
pip install -r requirements.txt