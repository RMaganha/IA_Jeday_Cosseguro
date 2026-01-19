# Extrator de Apólices V20 (Visão Nativa)

Sistema de extração automática de dados de apólices de seguros e especificações de cosseguro usando Gemini Vision AI e Streamlit.

## 🚀 Melhorias Implementadas

### Segurança
- ✅ Credenciais movidas para variáveis de ambiente (.env)
- ✅ Validação de configurações na inicialização
- ✅ Tratamento específico de exceções

### Arquitetura
- ✅ Código modularizado em serviços separados
- ✅ Separação de responsabilidades (MVC-like)
- ✅ Remoção de código duplicado
- ✅ Sistema de logging aprimorado

### Performance
- ✅ Processamento paralelo de múltiplos agentes Gemini
- ✅ Retry automático para operações de banco de dados
- ✅ Validação de arquivos antes do processamento

### Qualidade
- ✅ Validação de dados extraídos
- ✅ Tratamento robusto de erros
- ✅ Documentação completa (docstrings)
- ✅ Formatação consistente

## 📁 Estrutura do Projeto

```
project/
├── config/
│   ├── settings.py          # Configurações centralizadas
│   └── prompts.py            # Prompts do Gemini
├── services/
│   ├── gemini_service.py     # Wrapper da API Gemini
│   ├── database_service.py   # Operações SQL
│   └── pdf_processor.py      # Lógica de processamento
├── ui/
│   └── components.py         # Componentes Streamlit
├── utils/
│   ├── formatters.py         # Formatação de dados
│   ├── validators.py         # Validações
│   └── logger.py             # Sistema de logs
├── app.py                    # Aplicação principal
├── .env.example              # Exemplo de variáveis de ambiente
├── requirements.txt          # Dependências
└── README.md                 # Este arquivo
```

## 🔧 Instalação

1. **Clone o repositório**
```bash
git clone <seu-repositorio>
cd extrator-apolices
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

## ⚙️ Configuração

### Arquivo .env

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
# API Gemini
GEMINI_API_KEY=sua_chave_api_gemini_aqui

# Banco de Dados SQL Server
SQL_CONNECTION_STRING=Driver={ODBC Driver 17 for SQL Server};Server=SEU_SERVIDOR,PORTA;Database=NOME_DB;UID=usuario;PWD=senha;TrustServerCertificate=yes;
```

### Obtendo as Credenciais

**Gemini API Key:**
1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crie uma nova chave API
3. Copie a chave para o arquivo `.env`

**SQL Server:**
1. Use as credenciais fornecidas pelo administrador do banco
2. Ajuste a connection string no `.env`

## 🚀 Uso

### Executar a Aplicação

```bash
streamlit run app.py
```

A aplicação abrirá automaticamente no navegador em `http://localhost:8501`

### Processar uma Apólice

1. Digite o número da solicitação
2. Clique em "🚀 Processar Apólice"
3. Aguarde o processamento
4. Visualize os dados nas abas organizadas
5. O JSON será salvo automaticamente na pasta `json/`

## 📊 Funcionalidades

- ✅ Extração automática de dados da apólice
- ✅ Extração de locais de risco
- ✅ Extração de coberturas
- ✅ Extração de dados financeiros
- ✅ Formatação automática de valores monetários
- ✅ Interface organizada em abas
- ✅ Logs em tempo real
- ✅ Salvamento automático em JSON

## 🔍 Validações Implementadas

- Validação de formato de arquivo (PDF)
- Validação de tamanho de arquivo (max 50MB)
- Validação de campos obrigatórios
- Validação de CNPJ
- Validação de datas
- Retry automático para falhas de rede

## 🛠️ Desenvolvimento

### Adicionar Novos Prompts

Edite o arquivo `config/prompts.py` e adicione seu novo prompt:

```python
PROMPT_NOVO = """
Seu prompt aqui...
"""
```

### Adicionar Novas Validações

Edite o arquivo `utils/validators.py`:

```python
def validar_novo_campo(valor: str) -> bool:
    # Sua lógica de validação
    return True
```

### Adicionar Novos Componentes de UI

Edite o arquivo `ui/components.py`:

```python
def nova_aba_custom(dados: Dict):
    st.subheader("Nova Aba")
    # Seu código aqui
```

## 📝 Logs

Os logs são exibidos em tempo real na interface e incluem:
- Informações de processamento
- Avisos sobre dados incompletos
- Erros detalhados com stack trace

## 🔒 Segurança

- ✅ Credenciais em variáveis de ambiente
- ✅ Conexões SQL com timeout
- ✅ Validação de entrada de dados
- ✅ Tratamento de exceções
- ⚠️ Nunca commite o arquivo `.env` no Git

## 🐛 Troubleshooting

### Erro: "GEMINI_API_KEY não configurada"
- Verifique se o arquivo `.env` existe
- Verifique se a variável está corretamente configurada

### Erro: "Conexão com banco de dados falhou"
- Verifique a string de conexão
- Verifique se o servidor está acessível
- Verifique credenciais de usuário/senha

### Erro: "Arquivo não é um PDF válido"
- Verifique se o arquivo está corrompido
- Verifique se é realmente um PDF

## 📈 Próximas Melhorias

- [ ] Testes unitários completos
- [ ] Cache de resultados processados
- [ ] Suporte a múltiplos idiomas
- [ ] API REST para integração
- [ ] Dashboard de métricas
- [ ] Exportação para Excel

## 📄 Licença

[Sua licença aqui]

## 👥 Contribuição

Contribuições são bem-vindas! Por favor:
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório.