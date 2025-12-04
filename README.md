# 💰 Sistema de Gestão Financeira - Simplifica Finanças

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.0-green)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/mysql-8.0-orange)](https://www.mysql.com/)
[![Tests](https://img.shields.io/badge/tests-15%20passing-success)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen)](tests/)

> Sistema web de controle financeiro pessoal com interface adaptativa (simples/avançada), desenvolvido como projeto A3 de Gestão e Qualidade de Software.

---

## 🔗 Links Importantes

- 🌐 **Landing Page:** [https://github.com/KleivsonFreitas/Simplifica_Financas.git](https://github.com/KleivsonFreitas/Simplifica_Financas.git)
- 📁 **Repositório:** [https://github.com/KleivsonFreitas/Simplifica_Financas.git](https://github.com/KleivsonFreitas/Simplifica_Financas.git)
- 📸 **Screenshots:** [Google Drive - Imagens](https://drive.google.com/drive/folders/1BEIK509JvN_ix2QaX9444uPEb_iNrUY3?hl=pt-br)
- 🎥 **Vídeos Demonstrativos:** [Google Drive - Vídeos](https://drive.google.com/drive/folders/1BEIK509JvN_ix2QaX9444uPEb_iNrUY3?hl=pt-br)
- 📁 **Arquivo.Rar:** [Google Drive - Arquivo.rar](https://drive.google.com/drive/folders/1BEIK509JvN_ix2QaX9444uPEb_iNrUY3?hl=pt-br)

---

## 📑 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#️-tecnologias)
- [Arquitetura](#️-arquitetura)
- [Instalação](#-instalação)
- [Uso](#-uso)
- [Testes](#-testes)
- [Capturas de Tela](#-capturas-de-tela)
- [Vídeos Demonstrativos](#-vídeos-demonstrativos)
- [Qualidade de Código](#-qualidade-de-código)
- [Roadmap](#️-roadmap)
- [Equipe](#-equipe)
- [Licença](#-licença)

---

## 🎯 Sobre o Projeto

O **Simplifica Finanças** é um sistema web desenvolvido para facilitar o controle financeiro pessoal, atendendo tanto usuários iniciantes quanto avançados através de interfaces adaptativas.

### Problema Identificado

- Aplicativos financeiros são **complexos demais** para usuários iniciantes
- Exigem cadastro de banco, sincronização e configurações complicadas
- Interface única não atende diferentes perfis de usuários
- Falta de simplicidade no registro de transações

### Solução Proposta

Sistema com **dois modos de interface**:

#### 🟢 Modo Simples
- Para idosos, aposentados e iniciantes em tecnologia
- Botões grandes e coloridos
- Interface limpa com apenas o essencial
- Ideal para uso diário rápido

#### 🔵 Modo Avançado
- Para empreendedores e usuários experientes
- Gráficos e relatórios detalhados
- Análise de tendências
- Exportação de dados

### Diferenciais

✅ **Sem complicação:** Não precisa cadastrar banco ou conta  
✅ **Interface adaptativa** sem perda de funcionalidades  
✅ **Design responsivo** para desktop e mobile  
✅ **Exportação** em Excel e PDF  
✅ **Sistema de metas** com feedback visual  
✅ **100% gratuito** e open-source  

---

## ⚡ Funcionalidades

### 💸 Gerenciamento de Transações
- ✏️ Cadastro de receitas e despesas
- 📊 Categorização automática
- 🗑️ Exclusão com confirmação
- 📅 Filtro por período
- 💰 Cálculo automático de saldo

### 🎯 Sistema de Metas
- 🎯 Criação de metas financeiras
- 📈 Acompanhamento de progresso visual
- 🎨 Personalização de cores
- 🏆 Notificações de conquista
- ⏰ Alertas de prazo próximo

### 📊 Relatórios (Modo Avançado)
- 📉 Gráficos de pizza (despesas por categoria)
- 📊 Gráfico de evolução mensal
- 💡 Insights automáticos
- 📝 Análise de tendências

### 📥 Exportação de Dados
- 📗 Exportação em Excel (.xlsx)
- 📕 Exportação em PDF
- 📋 Relatórios personalizados
- 💾 Backup completo dos dados

### 🔒 Segurança
- 🔐 Autenticação com hash de senha (Werkzeug)
- 🛡️ Proteção CSRF
- 🚪 Sessões seguras
- ✅ Validação de dados server-side
- 🔑 Criptografia de senhas

---

## 🛠️ Tecnologias

### Backend
- **Python 3.10+** - Linguagem principal
- **Flask 3.0** - Framework web minimalista
- **MySQL 8.0** - Banco de dados relacional
- **Werkzeug 3.0.1** - Hashing de senhas
- **python-dotenv 1.0.0** - Gestão de variáveis de ambiente

### Frontend
- **HTML5/CSS3** - Estrutura e estilo
- **Bootstrap 5** - Framework CSS responsivo
- **JavaScript (Vanilla)** - Interatividade
- **Font Awesome** - Ícones

### Bibliotecas Python
```txt
Flask==3.0.0
mysql-connector-python==8.2.0
Werkzeug==3.0.1
python-dotenv==1.0.0
pandas==2.1.4
openpyxl==3.1.2
fpdf==1.7.2
gunicorn==21.2.0
```

### Ferramentas de Desenvolvimento
- **Git** - Controle de versão
- **unittest** - Framework de testes
- **Coverage.py** - Cobertura de testes
- **GitHub Pages** - Hospedagem da landing page

---

## 🗂️ Arquitetura

### Estrutura do Projeto
```
Simplifica-Finan-as/
│
├── app.py                      # Aplicação Flask principal
├── database_schema.sql         # Script de criação do banco
├── requirements.txt            # Dependências Python
├── .env.example               # Exemplo de variáveis de ambiente
├── .gitignore                 # Arquivos ignorados
│
├── templates/                  # Templates HTML
│   ├── base.html              # Template base
│   ├── index.html             # Página inicial
│   ├── login.html             # Login
│   ├── registro.html          # Cadastro
│   ├── dashboard_simples.html # Dashboard modo simples
│   ├── dashboard_avancado.html# Dashboard modo avançado
│   ├── metas_simples.html     # Metas modo simples
│   ├── metas_avancado.html    # Metas modo avançado
│   ├── configuracoes.html     # Configurações
│   └── relatorios.html        # Relatórios
│
├── tests/                      # Testes automatizados
│   ├── __init__.py
│   └── test_app.py            # 15 testes (unitários + integração)
│
└── docs/                       # Documentação
    └── index.html             # Landing page (GitHub Pages)
```

### Diagrama de Arquitetura

```
┌────────────────────────────────────────────────┐
│                   FRONTEND                     │
│  ┌──────────────┐  ┌──────────────┐           │
│  │ Modo Simples │  │ Modo Avançado│           │
│  └──────┬───────┘  └──────┬───────┘           │
│         │                  │                   │
│         └──────────┬───────┘                   │
└────────────────────┼───────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────┐
│                  FLASK APP                     │
│  ┌──────────────────────────────────────────┐ │
│  │          Rotas & Controllers             │ │
│  │  /login  /dashboard  /metas  /relatorios │ │
│  └────────────────┬─────────────────────────┘ │
│                   │                            │
│  ┌────────────────▼─────────────────────────┐ │
│  │        Lógica de Negócio                 │ │
│  │  • Autenticação  • Transações  • Metas   │ │
│  └────────────────┬─────────────────────────┘ │
└───────────────────┼────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────┐
│                MySQL Database                  │
│  ┌─────────┐  ┌──────────┐  ┌────────┐       │
│  │usuarios │  │transacoes│  │ metas  │       │
│  └─────────┘  └──────────┘  └────────┘       │
└────────────────────────────────────────────────┘
```

---

## 🚀 Instalação

### Pré-requisitos
- Python 3.10 ou superior
- MySQL 8.0 ou superior
- Git

### Passo 1: Clone o Repositório
```bash
git clone https://github.com/KleivsonFreitas/Simplifica_Financas.git
cd Simplifica_Financas
```

### Passo 2: Crie Ambiente Virtual
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### Passo 3: Instale Dependências
```bash
pip install -r requirements.txt
```

### Passo 4: Configure o Banco de Dados
```bash
# Entre no MySQL
mysql -u root -p

# Execute o script
source database_schema.sql
```

### Passo 5: Configure Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Chave secreta da aplicação
SECRET_KEY=sua_chave_secreta_aqui

# Configurações do Banco de Dados MySQL
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha_mysql
DB_NAME=gestao_financeira

# Ambiente
FLASK_ENV=development
FLASK_DEBUG=True
```

### Passo 6: Execute a Aplicação
```bash
python app.py
```

Acesse: **http://localhost:5000**

### 👤 Usuários de Teste

| Email | Senha | Modo |
|-------|-------|------|
| maria@email.com | 123456 | Simples |
| carlos@email.com | 123456 | Avançado |

---

## 📖 Uso

### 1️⃣ Primeiro Acesso
1. Acesse a página inicial
2. Clique em **"Cadastrar"**
3. Escolha seu **modo de interface** (simples/avançado)
4. Preencha nome, email e senha

### 2️⃣ Adicionando Transações

**Modo Simples:**
- Clique no botão grande "Adicionar Movimentação"
- Escolha se é RECEITA ou DESPESA
- Informe valor, descrição e categoria
- Clique em SALVAR

**Modo Avançado:**
- Clique em "Nova Transação"
- Preencha o formulário detalhado
- Opcionalmente ajuste data e categoria
- Salve a transação

### 3️⃣ Criando Metas
1. Acesse o menu **"Metas"**
2. Clique em **"Nova Meta"**
3. Defina:
   - Título (ex: "Viagem para Europa")
   - Valor alvo (ex: R$ 5.000,00)
   - Categoria e cor personalizadas
   - Data limite (opcional)
4. Adicione valores conforme economizar

### 4️⃣ Exportando Dados
- **Excel:** Menu Dashboard → Botão "Exportar Excel"
- **PDF:** Menu Dashboard → Botão "Exportar PDF"

### 5️⃣ Alternando Modos
1. Menu **"Configurações"**
2. Escolha novo modo
3. Clique em **"Salvar Alterações"**

---

## 🧪 Testes

### Executar Todos os Testes
```bash
python tests/test_app.py
```

### Com Relatório de Cobertura
```bash
coverage run -m unittest tests/test_app.py
coverage report
coverage html
```

### Cobertura de Testes

| Categoria | Testes | Descrição |
|-----------|--------|-----------|
| **Autenticação** | 5 | Login, registro, hash de senha, proteção de rotas |
| **Banco de Dados** | 2 | Conexão, estrutura de tabelas |
| **Transações** | 2 | Validações, regras de negócio |
| **Metas** | 2 | Cálculos, lógica de conclusão |
| **Utilitários** | 2 | Funções auxiliares |
| **Integração** | 2 | Fluxos completos end-to-end |
| **TOTAL** | **15** | Taxa de sucesso: **100%** ✅ |

### Exemplo de Saída
```
======================================================================
🧪 EXECUTANDO SUITE DE TESTES - GESTÃO FINANCEIRA
======================================================================

🧪 Executando TA-01: Hash de Senha...
✅ TA-01: PASSOU

🧪 Executando TA-02: Página de Login...
✅ TA-02: PASSOU

[... 13 testes adicionais ...]

======================================================================
📊 RELATÓRIO FINAL
======================================================================
✅ Testes executados: 15
✅ Sucessos: 15
❌ Falhas: 0
⚠️  Erros: 0
📈 Taxa de Sucesso: 100.0%

🎉 TODOS OS TESTES PASSARAM!
======================================================================
```

---

## 📸 Capturas de Tela

Todas as imagens do sistema estão disponíveis no Google Drive:

**🔗 [Ver Todas as Screenshots](https://drive.google.com/drive/folders/1BEIK509JvN_ix2QaX9444uPEb_iNrUY3?hl=pt-br)**

### Principais Telas

- 🔐 **Tela de Login** - Interface de autenticação segura
- 📊 **Dashboard Simples** - Interface clara e intuitiva para iniciantes
- 📈 **Dashboard Avançado** - Gráficos e análises detalhadas
- 🎯 **Metas Financeiras** - Acompanhamento visual de objetivos
- 💸 **Adicionar Transação** - Formulário rápido de registro
- 📊 **Relatórios** - Análises por categoria e evolução temporal
- ⚙️ **Configurações** - Alternância entre modos de interface

---

## 🎥 Vídeos Demonstrativos

Todos os vídeos estão disponíveis no Google Drive:

**🔗 [Assistir Vídeos Completos](https://drive.google.com/drive/folders/1BEIK509JvN_ix2QaX9444uPEb_iNrUY3?hl=pt-br)**

### Conteúdo dos Vídeos

- 🎬 **Pitch do Projeto (5 minutos)** - Apresentação completa do sistema
- 🎬 **Demonstração Completa** - Passo a passo de todas as funcionalidades
- 🧪 **Execução dos Testes** - 15 testes automatizados rodando com sucesso
- 🎯 **Tutorial de Uso** - Como usar o sistema passo a passo

---

## 📊 Qualidade de Código

### Métricas de Qualidade

| Métrica | Valor | Status |
|---------|-------|--------|
| **Linhas de Código** | ~1.900 | ✅ |
| **Cobertura de Testes** | ~85% | ✅ |
| **Complexidade Ciclomática** | 3.2 (Baixa) | ✅ |
| **Testes Aprovados** | 15/15 (100%) | ✅ |
| **Bugs Críticos** | 0 | ✅ |

### Estimativas de Esforço

#### Pontos de Função (PF)

| Funcionalidade | Tipo | Complexidade | PF |
|----------------|------|--------------|-----|
| Autenticação | EI | Baixa | 3 |
| CRUD Transações | EI | Média | 4 |
| Dashboard | EO | Alta | 6 |
| Metas Financeiras | EI | Média | 4 |
| Relatórios | EO | Alta | 6 |
| Exportação | EO | Média | 4 |
| **TOTAL** | | | **27** |

**Estimativa de Esforço:**
- Produtividade: 5 horas/PF
- Esforço Estimado: 135 horas
- Esforço Real: 140 horas
- Variação: +3.7% ✅

### Boas Práticas Aplicadas

✅ **Clean Code:** Nomes descritivos, funções pequenas  
✅ **DRY:** Código reutilizável, sem duplicação  
✅ **SOLID:** Separação de responsabilidades  
✅ **Segurança:** Hashing de senhas, validação de inputs  
✅ **Testes:** Cobertura alta com cenários positivos e negativos  
✅ **Documentação:** README completo, comentários no código  

---

## 🗺️ Roadmap

### Versão 2.0 (Planejado)
- [ ] Modo escuro automático
- [ ] Aplicativo mobile (React Native)
- [ ] Notificações push
- [ ] Importação de extratos bancários

### Versão 3.0 (Futuro)
- [ ] Inteligência Artificial para sugestões
- [ ] Multi-moeda
- [ ] Compartilhamento de metas (social)
- [ ] API REST pública

---

## 👥 Equipe

### Desenvolvedores

| Nome | RA | Função |
|------|-----|--------|
| **Janary Victor do Nascimento Júnior** | 1362416604 | Desenvolvedor Full-Stack |
| **José Kleivson da Silva Freitas** | 1362411072 | Banco de Dados / Backend |
| **Daniel Obede da Silva** | 1362112473 | Frontend / Testes |
| **Gabriel Jonathas Santos de Oliveira** | 1362317022 | Desenvolvedor Full-Stack |
| **Carlos Henrique Cavalcante Moreira** | 1362416272  | Banco de Dados / Backend |
|

### Informações Acadêmicas

**Orientador:** Prof. Antunes e Artur 
**Instituição:** Faculdade Internacional da Paraíba (FPB) - Campus Tambiá  
**Curso:** Ciência da Computação 
**Disciplina:** Gestão e Qualidade de Software (A3)  
**Semestre:** 2025.2  

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos na disciplina de Gestão e Qualidade de Software.

---

## 🙏 Agradecimentos

- [Flask](https://flask.palletsprojects.com/) - Framework web
- [Bootstrap](https://getbootstrap.com/) - Framework CSS
- [MySQL](https://www.mysql.com/) - Sistema de banco de dados
- [Font Awesome](https://fontawesome.com/) - Ícones
- Prof. Antunes e Artur - Orientação e suporte
- FPB - Infraestrutura e recursos

---

## 📞 Contato

- 📧 **Email:** [kleivsonfreitas@gmail.com]
- 🐙 **GitHub:** [@kleivsonfreitas](https://github.com/KleivsonFreitas/Simplifica_Financas.git)

---

<div align="center">

**⭐ Se este projeto te ajudou, deixe uma estrela no GitHub!**

![GitHub stars](https://github.com/KleivsonFreitas/Simplifica_Financas.git)
![GitHub forks](https://github.com/KleivsonFreitas/Simplifica_Financas.git)

---

**Desenvolvido com ❤️ para a A3 de Gestão e Qualidade de Software**

[⬆ Voltar ao topo](#-sistema-de-gestão-financeira---simplifica-finanças)

</div>
