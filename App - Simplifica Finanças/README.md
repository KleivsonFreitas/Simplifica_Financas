# 💰 Sistema de Gestão Financeira - Simplifica Finanças

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)](https://www.mysql.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-Academic-red.svg)](LICENSE)

> Sistema web de gestão financeira pessoal com interface adaptativa para diferentes níveis de experiência

## 📋 Sumário

- [Sobre o Projeto](#-sobre-o-projeto)
- [Tecnologias](#-tecnologias)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura](#-arquitetura)
- [Instalação](#-instalação)
- [Uso](#-uso)
- [Testes](#-testes)
- [Documentação](#-documentação)
- [Contribuindo](#-contribuindo)

---

## 🎯 Sobre o Projeto

**Simplifica Finanças** é um sistema web para gestão financeira pessoal desenvolvido como projeto acadêmico (A3) para a disciplina de Gestão e Qualidade de Software.

### Diferencial: Dois Modos de Interface

#### 🟢 Modo Simples
- Interface clara e intuitiva
- Botões grandes e acessíveis
- Ideal para iniciantes e aposentados
- Foco no essencial

#### 🔵 Modo Avançado
- Gráficos e relatórios detalhados
- Análise por categoria
- Exportação Excel/PDF
- Ideal para empreendedores

### Público-Alvo
- Pessoas com pouca familiaridade tecnológica
- Aposentados gerenciando finanças pessoais
- Empreendedores que precisam de controle detalhado
- Qualquer pessoa que queira organizar suas finanças

---

## 🚀 Tecnologias

### Backend
- **Python 3.8+** - Linguagem principal
- **Flask 3.0** - Framework web
- **MySQL 8.0** - Banco de dados
- **SQLAlchemy** - ORM (opcional)
- **Werkzeug** - Segurança e hash de senhas

### Frontend
- **HTML5/CSS3** - Estrutura e estilo
- **Bootstrap 5.3** - Framework CSS
- **JavaScript Vanilla** - Interatividade
- **Chart.js 4.4** - Gráficos
- **Font Awesome 6.4** - Ícones

### Bibliotecas Python
```python
Flask==3.0.0
mysql-connector-python==8.2.0
python-dotenv==1.0.0
werkzeug==3.0.1
pandas==2.1.3
openpyxl==3.1.2
fpdf==1.7.2
```

---

## ✨ Funcionalidades

### 🏠 Dashboard
- Visualização do saldo total
- Receitas e despesas do mês
- Últimas transações
- Cards estatísticos (modo avançado)

### 💸 Transações
- Adicionar receitas e despesas
- Categorização automática
- Descrição detalhada
- Histórico completo
- Exclusão de registros

### 🎯 Metas Financeiras
- Criar metas com valor alvo
- Acompanhar progresso visual
- Cores personalizadas
- Data limite (opcional)
- Notificação de conclusão
- Estatísticas gerais

### 📊 Relatórios (Modo Avançado)
- Gráfico de despesas por categoria
- Evolução mensal de receitas/despesas
- Tabela resumida com percentuais
- Insights financeiros

### 📥 Exportação
- **Excel (.xlsx)** - Todas as transações formatadas
- **PDF (.pdf)** - Relatório completo com tabela

### ⚙️ Configurações
- Alternar entre Modo Simples/Avançado
- Informações da conta
- Gerenciamento de perfil

## 🔐 Backup Automático
   
   Sistema completo de backup incluído.
   
   **Uso rápido:**
```bash
   python backup_automatico.py  # Menu interativo
```
---

## 🏗️ Arquitetura

### Estrutura de Diretórios

```
gestao-financeira/
├── app.py                         # Aplicação Flask principal
├── README.md                      # Este arquivo
├── requirements.txt               # Dependências Python
├── .env                           # Variáveis de ambiente
├── database_schema.sql            # Schema do banco
│
├── templates/                    # Templates Jinja2
│   ├── base.html                 # Template base
│   ├── index.html                # Landing page
│   ├── login.html                # Autenticação
│   ├── registro.html             # Cadastro
│   ├── dashboard_simples.html    # Dashboard modo simples
│   ├── dashboard_avancado.html   # Dashboard modo avançado
│   ├── adicionar_transacao_simples.html
│   ├── adicionar_transacao_avancado.html
│   ├── metas_simples.html        # Metas modo simples
│   ├── metas_avancado.html       # Metas modo avançado
│   ├── configuracoes.html        # Configurações
│   └── relatorios.html           # Relatórios avançados
│
├── static/                       # Arquivos estáticos
│   ├── css/
│   │   └── custom.css
│   └── js/
│       └── scripts.js
│
├── tests/                        # Testes automatizados
│   └── test_app.py               # Suite de 15 testes
│
└── utils/                        # Scripts utilitários
    ├── criar_usuarios_teste.py   # Popula DB com dados teste
    ├── Encoding.py               # Corrige encoding UTF-8
    └── test_script.py            # Testes básicos
```

### Modelo de Dados

```
┌─────────────────┐
│    USUARIOS     │
├─────────────────┤
│ id (PK)         │
│ nome            │
│ email (UNIQUE)  │
│ senha (hash)    │
│ modo_interface  │
│ data_cadastro   │
└─────────────────┘
        │
        │ 1:N
        │
        ├──────────────────────┐
        │                      │
        ▼                      ▼
┌─────────────────┐    ┌─────────────────┐
│   TRANSACOES    │    │      METAS      │
├─────────────────┤    ├─────────────────┤
│ id (PK)         │    │ id (PK)         │
│ usuario_id (FK) │    │ usuario_id (FK) │
│ tipo            │    │ titulo          │
│ valor           │    │ valor_alvo      │
│ descricao       │    │ valor_atual     │
│ categoria       │    │ progresso       │
│ data            │    │ status          │
└─────────────────┘    └─────────────────┘
```

---

## 🔧 Instalação

### Pré-requisitos

```bash
✅ Python 3.8 ou superior
✅ MySQL 8.0 ou superior
✅ pip (gerenciador de pacotes)
✅ Git (opcional)
```

### Passo a Passo

#### 1️⃣ Clone o Repositório

```bash
git clone https://github.com/KleivsonFreitas/Simplifica_Financas.git
cd Simplifica-Financas
```

#### 2️⃣ Crie o Ambiente Virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

#### 3️⃣ Instale as Dependências

```bash
pip install -r requirements.txt
```

#### 4️⃣ Configure o Banco de Dados

```bash
# Entre no MySQL
mysql -u root -p

# Execute o schema
mysql -u root -p < database_schema.sql

# Ou manualmente:
mysql> CREATE DATABASE gestao_financeira;
mysql> USE gestao_financeira;
mysql> source database_schema.sql;
```

#### 5️⃣ Configure as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua_chave_secreta_aqui_64_caracteres_minimo
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha_mysql
DB_NAME=gestao_financeira
FLASK_ENV=development
FLASK_DEBUG=True
```

**Dica:** Para gerar uma SECRET_KEY segura:

```python
import secrets
print(secrets.token_hex(32))
```

#### 6️⃣ Crie Usuários de Teste (Opcional)

```bash
python criar_usuarios_teste.py
```

Isto criará dois usuários:

| Email | Senha | Modo |
|-------|-------|------|
| maria@email.com | 123456 | Simples |
| carlos@email.com | 123456 | Avançado |

#### 7️⃣ Execute a Aplicação

```bash
python app.py
```

#### 8️⃣ Acesse no Navegador

```
http://localhost:5000
```

---

## 🎮 Uso

### Primeiro Acesso

1. **Cadastre-se** em `/registro`
2. Escolha o **Modo de Interface** (Simples ou Avançado)
3. Faça **login** com suas credenciais
4. Adicione sua **primeira transação**

### Fluxo Básico

```
┌─────────────┐
│   Login     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Dashboard  │────► Ver Saldo e Transações
└──────┬──────┘
       │
       ├──► Adicionar Transação
       │
       ├──► Gerenciar Metas
       │
       ├──► Ver Relatórios (Modo Avançado)
       │
       └──► Exportar Excel/PDF
```

### Dicas de Uso

💡 **Para Iniciantes (Modo Simples):**
- Use botões grandes para adicionar receitas/despesas
- Visualize seu saldo de forma clara
- Exporte PDF para imprimir

💡 **Para Avançados:**
- Analise gráficos de despesas
- Configure metas financeiras
- Use filtros nos relatórios
- Exporte Excel para análises externas

---

## 🧪 Testes

### Suite de Testes Automatizados

O projeto inclui **15 testes** distribuídos em:

- ✅ 5 Testes Unitários
- ✅ 4 Testes de Integração  
- ✅ 6 Testes Funcionais

### Executar Todos os Testes

```bash
# Windows
executar_teste.bat

### Cobertura de Testes

| Categoria | Testes |
|-----------|--------|
| Autenticação | Hash de senha, Login, Registro |
| Banco de Dados | Conexão, Estrutura de tabelas |
| Transações | Validações, CRUD |
| Metas | Cálculo de progresso, Conclusão |
| Utilitários | Função cor_clara |
| Integração | Fluxo completo de usuário |

### Exemplo de Saída

```
🧪 EXECUTANDO SUITE DE TESTES
=====================================
✅ TA-01: Hash de Senha - PASSOU
✅ TA-02: Página de Login - PASSOU
✅ TA-03: Registro de Usuário - PASSOU
...
=====================================
📊 RELATÓRIO FINAL
Total: 15 testes
Sucessos: 15 ✅
Falhas: 0 ❌
Taxa de Sucesso: 100%
=====================================
```

---

## 📚 Documentação

### Segurança

#### Hash de Senhas
```python
from werkzeug.security import generate_password_hash, check_password_hash

# Criar hash
senha_hash = generate_password_hash('minha_senha')

# Verificar
check_password_hash(senha_hash, 'minha_senha')  # True
```

#### Proteção de Rotas
```python
@app.route('/dashboard')
@login_required  # ← Decorator de proteção
def dashboard():
    return render_template('dashboard.html')
```

### API Interna

#### Adicionar Transação

```python
POST /adicionar-transacao

Body:
{
    "tipo": "receita",        # ou "despesa"
    "valor": 100.50,
    "descricao": "Salário",
    "categoria": "Trabalho",
    "data": "2025-11-29"
}
```

#### Criar Meta

```python
POST /adicionar-meta

Body:
{
    "titulo": "Viagem",
    "valor_alvo": 5000.00,
    "categoria": "Viagem",
    "data_inicio": "2025-11-01",
    "data_limite": "2025-12-31",
    "cor": "#6366F1"
}
```

### Variáveis de Sessão

```python
session['user_id']      # ID do usuário logado
session['user_nome']    # Nome do usuário
session['user_modo']    # 'simples' ou 'avancado'
```

---

## 🎨 Customização

### Cores do Sistema

Edite em `templates/base.html`:

```css
:root {
    --primary-color: #4f46e5;   /* Índigo */
    --success-color: #10b981;   /* Verde */
    --danger-color: #ef4444;    /* Vermelho */
    --warning-color: #f59e0b;   /* Âmbar */
    --info-color: #3b82f6;      /* Azul */
}
```

### Adicionar Nova Categoria

Edite `templates/adicionar_transacao_*.html`:

```html
<option value="Nova Categoria">🎯 Nova Categoria</option>
```

---

## 🐛 Troubleshooting

### Problema: Erro de Conexão com MySQL

```bash
❌ mysql.connector.errors.ProgrammingError: Access denied

✅ Solução:
1. Verifique usuário e senha no .env
2. Confirme que o MySQL está rodando
3. Teste: mysql -u root -p
```

### Problema: Encoding UTF-8

```bash
❌ Caracteres especiais aparecendo errados (Ã§, Ã£)

✅ Solução:
python Encoding.py
```

### Problema: Porta 5000 em Uso

```bash
❌ OSError: [Errno 48] Address already in use

✅ Solução:
# Altere a porta em app.py
app.run(port=5001)
```

### Problema: Módulo não encontrado

```bash
❌ ModuleNotFoundError: No module named 'flask'

✅ Solução:
pip install -r requirements.txt
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Siga os passos:

### 1. Fork o Projeto
### 2. Crie uma Branch

```bash
git checkout -b feature/nova-funcionalidade
```

### 3. Commit suas Mudanças

```bash
git commit -m "feat: adiciona funcionalidade X"
```

Padrão de commits:
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação
- `refactor:` Refatoração
- `test:` Testes
- `chore:` Manutenção

### 4. Push para a Branch

```bash
git push origin feature/nova-funcionalidade
```

### 5. Abra um Pull Request

---

## 📈 Roadmap

### Versão 2.0 (Planejado)

- [ ] API REST completa
- [ ] App mobile (React Native)
- [ ] Modo escuro (dark mode)
- [ ] Notificações push
- [ ] Importação de extratos bancários (OFX)
- [ ] Dashboard com IA para insights
- [ ] Compartilhamento de metas
- [ ] Integração Open Banking
- [ ] Previsão de gastos (Machine Learning)
- [ ] Multi-idiomas (i18n)

---

## 📄 Licença

Este projeto é um trabalho acadêmico desenvolvido para fins educacionais.

**Projeto A3 - Gestão e Qualidade de Software**  
Universidade: [Nome da Instituição]  
Ano: 2025

---

## 👥 Autores

- **José Kleivson da Silva Freitas** - [RA 1362411072 - CCO](https://github.com/KleivsonFreitas/Simplifica_Financas.git)
- **Janary Victor do Nascimento Júnior** - [RA 1362416604 - CCO](https://github.com/KleivsonFreitas/Simplifica_Financas.git)
- **Gabriel Jonathas Santos de Oliveira** - [RA 1362317022 - ADS](https://github.com/KleivsonFreitas/Simplifica_Financas.git)
- **Carlos Henrique Cavalcante Moreira** - [RA 1362416272 - CCO](https://github.com/KleivsonFreitas/Simplifica_Financas.git)
- **Daniel Obede da Silva** - [RA 1362112473 - CCO](https://github.com/KleivsonFreitas/Simplifica_Financas.git)
---

## 🙏 Agradecimentos

- Professor(a) Glauber, Antunes, Artur.

---

## 📞 Contato

- 📧 Email: kleivsonfreitas@gmail.com

---

<div align="center">