from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import mysql.connector
from functools import wraps
import os
from dotenv import load_dotenv
import io
import pandas as pd
from fpdf import FPDF
from flask import send_file

# Carrega variáveis de ambiente
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback-key-only-for-dev')

# Configuração do Banco de Dados (agora com variáveis de ambiente)
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'gestao_financeira')
}

def get_db_connection():
    """Cria conexão com o banco de dados"""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as e:
        print(f"Erro ao conectar ao banco: {e}")
        raise

# ============== FUNÇÃO HELPER PARA CORES ==============

def get_cor_clara(cor_hex, brilho=32):
    """
    Retorna uma versão mais clara da cor HEX (string) para fundo.
    Aceita formatos: '#RRGGBB' ou 'RRGGBB'. Retorna '#RRGGBB' em maiúsculas.
    Em caso de entrada inválida, retorna um fallback agradável.
    """
    if not cor_hex:
        return '#E0E7FF'  # Fallback padrão
    
    # Normaliza: remove espaços e #, converte para string
    cor = str(cor_hex).strip()
    if cor.startswith('#'):
        cor = cor[1:]
    # Agora cor deve ter exatamente 6 caracteres hex
    if len(cor) != 6:
        return '#E0E7FF'
    try:
        r = int(cor[0:2], 16)
        g = int(cor[2:4], 16)
        b = int(cor[4:6], 16)
    except ValueError:
        return '#E0E7FF'
    # Aumenta brilho de forma segura
    try:
        brilho_int = int(brilho)
    except (TypeError, ValueError):
        brilho_int = 32
    r = min(255, max(0, r + brilho_int))
    g = min(255, max(0, g + brilho_int))
    b = min(255, max(0, b + brilho_int))
    return "#{:02X}{:02X}{:02X}".format(r, g, b)

# ============== REGISTRA A FUNÇÃO NO JINJA ==============
# Agora a função JÁ está definida acima, então pode ser registrada

app.jinja_env.globals['get_cor_clara'] = get_cor_clara

# Registra também como filtro Jinja (p.ex. {{ meta.cor|cor_clara(40) }})
@app.template_filter('cor_clara')
def cor_clara_filter(cor_hex, brilho=32):
    return get_cor_clara(cor_hex, brilho)

# ============== CONTEXT PROCESSOR ==============
@app.context_processor
def utility_processor():
    """Disponibiliza funções para todos os templates"""
    return dict(get_cor_clara=get_cor_clara)

# ============== DECORATORS ==============
def login_required(f):
    """Decorator para proteger rotas que precisam de autenticação"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, faça login para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ============== ROTAS DE AUTENTICAÇÃO ==============
@app.route('/')
def index():
    """Página inicial"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Página de registro de novos usuários"""
    if request.method == 'POST':
        conn = None
        try:
            nome = request.form.get('nome', '').strip()
            email = request.form.get('email', '').strip().lower()
            senha = request.form.get('senha', '')
            modo = request.form.get('modo', 'simples')
            
            # Validações
            if not nome or len(nome) < 3:
                flash('Nome deve ter pelo menos 3 caracteres!', 'danger')
                return redirect(url_for('registro'))
            
            if not email or '@' not in email:
                flash('Email inválido!', 'danger')
                return redirect(url_for('registro'))
            
            if not senha or len(senha) < 6:
                flash('Senha deve ter pelo menos 6 caracteres!', 'danger')
                return redirect(url_for('registro'))
            
            if modo not in ['simples', 'avancado']:
                modo = 'simples'
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Verifica se email já existe
            cursor.execute('SELECT id FROM usuarios WHERE email = %s', (email,))
            if cursor.fetchone():
                flash('Email já cadastrado!', 'danger')
                return redirect(url_for('registro'))
            
            # Cria novo usuário
            senha_hash = generate_password_hash(senha)
            cursor.execute(
                'INSERT INTO usuarios (nome, email, senha, modo_interface) VALUES (%s, %s, %s, %s)',
                (nome, email, senha_hash, modo)
            )
            conn.commit()
            
            flash('Cadastro realizado com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            flash(f'Erro ao criar conta: {str(e)}', 'danger')
            return redirect(url_for('registro'))
            
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
    
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        conn = None
        try:
            email = request.form.get('email', '').strip().lower()
            senha = request.form.get('senha', '')
            
            if not email or not senha:
                flash('Preencha email e senha!', 'danger')
                return redirect(url_for('login'))
            
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
            usuario = cursor.fetchone()
            
            if usuario and check_password_hash(usuario['senha'], senha):
                session['user_id'] = usuario['id']
                session['user_nome'] = usuario['nome']
                session['user_modo'] = usuario['modo_interface']
                flash(f'Bem-vindo(a), {usuario["nome"]}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Email ou senha incorretos!', 'danger')
                
        except Exception as e:
            flash(f'Erro ao fazer login: {str(e)}', 'danger')
            
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout do usuário"""
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('index'))

# ============== DASHBOARD ==============
@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal - mostra resumo financeiro"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Busca saldo total
        cursor.execute('''
            SELECT 
                COALESCE(SUM(CASE WHEN tipo = 'receita' THEN valor ELSE -valor END), 0) as saldo
            FROM transacoes 
            WHERE usuario_id = %s
        ''', (session['user_id'],))
        saldo_data = cursor.fetchone()
        saldo = saldo_data['saldo']
        
        # Busca receitas e despesas do mês atual
        cursor.execute('''
            SELECT 
                tipo,
                SUM(valor) as total
            FROM transacoes 
            WHERE usuario_id = %s 
            AND MONTH(data) = MONTH(CURRENT_DATE())
            AND YEAR(data) = YEAR(CURRENT_DATE())
            GROUP BY tipo
        ''', (session['user_id'],))
        
        mes_atual = {'receitas': 0, 'despesas': 0}
        for row in cursor.fetchall():
            if row['tipo'] == 'receita':
                mes_atual['receitas'] = row['total']
            else:
                mes_atual['despesas'] = row['total']
        
        # Busca últimas transações
        cursor.execute('''
            SELECT * FROM transacoes 
            WHERE usuario_id = %s 
            ORDER BY data DESC, id DESC 
            LIMIT 10
        ''', (session['user_id'],))
        ultimas_transacoes = cursor.fetchall()
        
        modo = session.get('user_modo', 'simples')
        template = 'dashboard_simples.html' if modo == 'simples' else 'dashboard_avancado.html'
        
        return render_template(template, 
                             saldo=saldo, 
                             mes_atual=mes_atual,
                             transacoes=ultimas_transacoes)
        
    except Exception as e:
        flash(f'Erro ao carregar dashboard: {str(e)}', 'danger')
        return redirect(url_for('index'))
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# ============== TRANSAÇÕES ==============
@app.route('/adicionar-transacao', methods=['GET', 'POST'])
@login_required
def adicionar_transacao():
    """Adiciona nova transação"""
    if request.method == 'POST':
        conn = None
        try:
            # Validações
            tipo = request.form.get('tipo')
            if tipo not in ['receita', 'despesa']:
                flash('Tipo de transação inválido!', 'danger')
                return redirect(url_for('adicionar_transacao'))
            
            try:
                valor = float(request.form.get('valor', 0))
            except ValueError:
                flash('Valor inválido!', 'danger')
                return redirect(url_for('adicionar_transacao'))
            
            if valor <= 0:
                flash('Valor deve ser maior que zero!', 'danger')
                return redirect(url_for('adicionar_transacao'))
            
            descricao = request.form.get('descricao', '').strip()
            if not descricao or len(descricao) < 3:
                flash('Descrição deve ter pelo menos 3 caracteres!', 'danger')
                return redirect(url_for('adicionar_transacao'))
            
            if len(descricao) > 200:
                flash('Descrição muito longa (máximo 200 caracteres)!', 'danger')
                return redirect(url_for('adicionar_transacao'))
            
            categoria = request.form.get('categoria', 'Outros').strip()
            if not categoria:
                categoria = 'Outros'
            
            data_str = request.form.get('data')
            if not data_str:
                data = datetime.now().date()
            else:
                try:
                    data = datetime.strptime(data_str, '%Y-%m-%d').date()
                    # Não permite datas futuras
                    if data > datetime.now().date():
                        flash('Data não pode ser futura!', 'warning')
                        data = datetime.now().date()
                except ValueError:
                    flash('Data inválida!', 'danger')
                    return redirect(url_for('adicionar_transacao'))
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO transacoes (usuario_id, tipo, valor, descricao, categoria, data)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (session['user_id'], tipo, valor, descricao, categoria, data))
            conn.commit()
            
            mensagem = 'Receita' if tipo == 'receita' else 'Despesa'
            flash(f'{mensagem} adicionada com sucesso!', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            flash(f'Erro ao adicionar transação: {str(e)}', 'danger')
            return redirect(url_for('adicionar_transacao'))
            
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
    
    # GET request
    modo = session.get('user_modo', 'simples')
    template = 'adicionar_transacao_simples.html' if modo == 'simples' else 'adicionar_transacao_avancado.html'
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template(template, today=today)

@app.route('/excluir-transacao/<int:id>')
@login_required
def excluir_transacao(id):
    """Exclui uma transação"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verifica se a transação pertence ao usuário
        cursor.execute('SELECT id FROM transacoes WHERE id = %s AND usuario_id = %s', 
                      (id, session['user_id']))
        
        if not cursor.fetchone():
            flash('Transação não encontrada!', 'danger')
            return redirect(url_for('dashboard'))
        
        cursor.execute('DELETE FROM transacoes WHERE id = %s AND usuario_id = %s', 
                      (id, session['user_id']))
        conn.commit()
        
        flash('Transação excluída com sucesso!', 'success')
        
    except Exception as e:
        flash(f'Erro ao excluir transação: {str(e)}', 'danger')
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    
    return redirect(url_for('dashboard'))

# ============== CONFIGURAÇÕES ==============
@app.route('/configuracoes', methods=['GET', 'POST'])
@login_required
def configuracoes():
    """Página de configurações do usuário"""
    if request.method == 'POST':
        conn = None
        try:
            novo_modo = request.form.get('modo')
            
            if novo_modo not in ['simples', 'avancado']:
                flash('Modo inválido!', 'danger')
                return redirect(url_for('configuracoes'))
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE usuarios SET modo_interface = %s WHERE id = %s',
                          (novo_modo, session['user_id']))
            conn.commit()
            
            session['user_modo'] = novo_modo
            flash('Modo de interface atualizado!', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            flash(f'Erro ao atualizar configurações: {str(e)}', 'danger')
            
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
    
    return render_template('configuracoes.html')

# ============== RELATÓRIOS (MODO AVANÇADO) ==============
@app.route('/relatorios')
@login_required
def relatorios():
    """Página de relatórios - apenas modo avançado"""
    if session.get('user_modo') != 'avancado':
        flash('Esta funcionalidade está disponível apenas no modo avançado.', 'info')
        return redirect(url_for('dashboard'))
    
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Despesas por categoria
        cursor.execute('''
            SELECT categoria, SUM(valor) as total
            FROM transacoes
            WHERE usuario_id = %s AND tipo = 'despesa'
            GROUP BY categoria
            ORDER BY total DESC
        ''', (session['user_id'],))
        despesas_categoria = cursor.fetchall()
        
        # Evolução mensal
        cursor.execute('''
            SELECT 
                DATE_FORMAT(data, '%Y-%m') as mes,
                tipo,
                SUM(valor) as total
            FROM transacoes
            WHERE usuario_id = %s
            GROUP BY mes, tipo
            ORDER BY mes DESC
            LIMIT 12
        ''', (session['user_id'],))
        evolucao_mensal = cursor.fetchall()
        
        return render_template('relatorios.html', 
                             despesas_categoria=despesas_categoria,
                             evolucao_mensal=evolucao_mensal)
        
    except Exception as e:
        flash(f'Erro ao carregar relatórios: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# ============== METAS FINANCEIRAS (PRINCIPAL) ==============
@app.route('/metas')
@login_required
def metas():
    """Página de metas financeiras"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Busca todas as metas do usuário com cálculos
        cursor.execute('''
            SELECT 
                id,
                titulo,
                descricao,
                categoria,
                valor_alvo,
                valor_atual,
                (valor_alvo - valor_atual) AS valor_faltante,
                CASE 
                    WHEN valor_alvo > 0 THEN 
                        GREATEST(LEAST((valor_atual / valor_alvo * 100), 100), 0)
                    ELSE 0 
                END AS progresso,
                status,
                data_inicio,
                data_limite,
                data_conclusao,
                cor,
                CASE
                    WHEN status = 'ativa'
                         AND data_limite IS NOT NULL
                         AND data_limite < CURRENT_DATE
                    THEN 1
                    ELSE 0
                END AS atrasada,
                CASE 
                    WHEN data_limite IS NOT NULL THEN
                        DATEDIFF(data_limite, CURRENT_DATE)
                    ELSE NULL
                END AS dias_restantes
            FROM metas
            WHERE usuario_id = %s
            ORDER BY
                FIELD(status, 'ativa', 'concluida', 'cancelada'),
                data_limite IS NULL,
                data_limite ASC
        ''', (session['user_id'],))
        metas_lista = cursor.fetchall()
        
        # Busca estatísticas gerais
        cursor.execute('''
            SELECT
                COUNT(*) AS total_metas,
                SUM(CASE WHEN status = 'ativa' THEN 1 ELSE 0 END) AS metas_ativas,
                SUM(CASE WHEN status = 'concluida' THEN 1 ELSE 0 END) AS metas_concluidas,
                COALESCE(SUM(valor_atual), 0) AS total_economizado,
                COALESCE(SUM(CASE WHEN status = 'ativa' THEN valor_alvo ELSE 0 END), 0) AS total_objetivo
            FROM metas
            WHERE usuario_id = %s
        ''', (session['user_id'],))
        stat = cursor.fetchone()
        
        estatisticas = {
            'total_metas': int(stat['total_metas'] or 0),
            'metas_ativas': int(stat['metas_ativas'] or 0),
            'metas_concluidas': int(stat['metas_concluidas'] or 0),
            'total_economizado': float(stat['total_economizado'] or 0),
            'total_objetivo': float(stat['total_objetivo'] or 0),
        }
        
        if estatisticas['total_objetivo'] > 0:
            estatisticas['progresso_geral'] = (
                estatisticas['total_economizado'] / estatisticas['total_objetivo'] * 100
            )
        else:
            estatisticas['progresso_geral'] = 0.0
        
        # Metas com prazo próximo (7 dias)
        cursor.execute('''
            SELECT id, titulo, data_limite,
                   DATEDIFF(data_limite, CURRENT_DATE) as dias_restantes
            FROM metas
            WHERE usuario_id = %s
              AND status = 'ativa'
              AND data_limite IS NOT NULL
              AND data_limite BETWEEN CURRENT_DATE AND DATE_ADD(CURRENT_DATE, INTERVAL 7 DAY)
            ORDER BY data_limite ASC
        ''', (session['user_id'],))
        metas_proximas = cursor.fetchall()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # === CORREÇÃO: SELECIONA O TEMPLATE DINAMICAMENTE ===
        modo = session.get('user_modo', 'simples')
        template_name = 'metas_simples.html' if modo == 'simples' else 'metas_avancado.html'
        
        return render_template(
            template_name,
            metas=metas_lista,
            estatisticas=estatisticas,
            metas_proximas=metas_proximas,
            today=today
        )
        
    except Exception as e:
        flash(f'Erro ao carregar metas: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/adicionar-meta', methods=['POST'])
@login_required
def adicionar_meta():
    """Adiciona nova meta"""
    conn = None
    try:
        titulo = request.form.get('titulo', '').strip()
        descricao = request.form.get('descricao', '').strip()
        
        try:
            valor_alvo = float(request.form.get('valor_alvo', 0))
        except ValueError:
            flash('Valor alvo inválido!', 'danger')
            return redirect(url_for('metas'))
        
        categoria = request.form.get('categoria', 'Outros')
        data_inicio_str = request.form.get('data_inicio')
        data_limite_str = request.form.get('data_limite')
        cor = request.form.get('cor', '#6366F1')
        
        # Validações
        if not titulo or len(titulo) < 3:
            flash('Título deve ter pelo menos 3 caracteres!', 'danger')
            return redirect(url_for('metas'))
        
        if valor_alvo <= 0:
            flash('Valor alvo deve ser maior que zero!', 'danger')
            return redirect(url_for('metas'))
        
        # Processar datas
        try:
            data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
            if data_inicio > datetime.now().date():
                flash('Data de início não pode ser futura!', 'warning')
                data_inicio = datetime.now().date()
        except (ValueError, TypeError):
            flash('Data de início inválida!', 'danger')
            return redirect(url_for('metas'))
        
        data_limite = None
        if data_limite_str:
            try:
                data_limite = datetime.strptime(data_limite_str, '%Y-%m-%d').date()
                if data_limite < data_inicio:
                    flash('Data limite não pode ser anterior à data de início!', 'danger')
                    return redirect(url_for('metas'))
            except (ValueError, TypeError):
                flash('Data limite inválida!', 'danger')
                return redirect(url_for('metas'))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO metas (usuario_id, titulo, descricao, valor_alvo, categoria, data_inicio, data_limite, cor)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (session['user_id'], titulo, descricao, valor_alvo, categoria, data_inicio, data_limite, cor))
        conn.commit()
        
        flash('Meta criada com sucesso!', 'success')
        
    except Exception as e:
        flash(f'Erro ao criar meta: {str(e)}', 'danger')
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    
    return redirect(url_for('metas'))

@app.route('/adicionar-valor-meta', methods=['POST'])
@login_required
def adicionar_valor_meta():
    """Adiciona valor a uma meta"""
    conn = None
    try:
        meta_id = request.form.get('meta_id')
        valor_str = request.form.get('valor')
        
        if not meta_id or not valor_str:
            flash('Dados inválidos!', 'danger')
            return redirect(url_for('metas'))
        
        try:
            valor = float(valor_str)
        except ValueError:
            flash('Valor inválido!', 'danger')
            return redirect(url_for('metas'))
        
        if valor <= 0:
            flash('Valor deve ser maior que zero!', 'danger')
            return redirect(url_for('metas'))
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verifica se a meta pertence ao usuário e está ativa
        cursor.execute('''
            SELECT valor_atual, valor_alvo FROM metas 
            WHERE id = %s AND usuario_id = %s AND status = 'ativa'
        ''', (meta_id, session['user_id']))
        
        meta = cursor.fetchone()
        if not meta:
            flash('Meta não encontrada ou não está ativa!', 'danger')
            return redirect(url_for('metas'))
        
        novo_valor = float(meta['valor_atual']) + valor
        
        # Atualiza o valor atual
        cursor.execute('''
            UPDATE metas 
            SET valor_atual = %s 
            WHERE id = %s AND usuario_id = %s
        ''', (novo_valor, meta_id, session['user_id']))
        conn.commit()
        
        # Verifica se a meta foi concluída
        if novo_valor >= float(meta['valor_alvo']):
            cursor.execute('''
                UPDATE metas 
                SET status = 'concluida', data_conclusao = CURRENT_TIMESTAMP 
                WHERE id = %s AND usuario_id = %s
            ''', (meta_id, session['user_id']))
            conn.commit()
            flash('Parabéns! Meta concluída! 🎉', 'success')
        else:
            flash('Valor adicionado à meta com sucesso!', 'success')
        
    except Exception as e:
        flash(f'Erro ao adicionar valor: {str(e)}', 'danger')
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    
    return redirect(url_for('metas'))

@app.route('/concluir-meta/<int:id>')
@login_required
def concluir_meta(id):
    """Marca uma meta como concluída"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verifica se a meta pertence ao usuário
        cursor.execute('SELECT id FROM metas WHERE id = %s AND usuario_id = %s', 
                      (id, session['user_id']))
        
        if not cursor.fetchone():
            flash('Meta não encontrada!', 'danger')
            return redirect(url_for('metas'))
        
        cursor.execute('''
            UPDATE metas 
            SET status = 'concluida', data_conclusao = CURRENT_TIMESTAMP 
            WHERE id = %s AND usuario_id = %s
        ''', (id, session['user_id']))
        conn.commit()
        
        flash('Meta marcada como concluída!', 'success')
        
    except Exception as e:
        flash(f'Erro ao concluir meta: {str(e)}', 'danger')
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    
    return redirect(url_for('metas'))

@app.route('/editar-meta', methods=['POST'])
@login_required
def editar_meta():
    """Edita uma meta existente"""
    conn = None
    try:
        meta_id = request.form.get('meta_id')
        titulo = request.form.get('titulo', '').strip()
        descricao = request.form.get('descricao', '').strip()
        
        try:
            valor_alvo = float(request.form.get('valor_alvo', 0))
        except ValueError:
            flash('Valor alvo inválido!', 'danger')
            return redirect(url_for('metas'))
        
        categoria = request.form.get('categoria', 'Outros')
        data_limite_str = request.form.get('data_limite')
        cor = request.form.get('cor', '#6366F1')
        
        # Validações
        if not titulo or len(titulo) < 3:
            flash('Título deve ter pelo menos 3 caracteres!', 'danger')
            return redirect(url_for('metas'))
        
        if valor_alvo <= 0:
            flash('Valor alvo deve ser maior que zero!', 'danger')
            return redirect(url_for('metas'))
        
        data_limite = None
        if data_limite_str:
            try:
                data_limite = datetime.strptime(data_limite_str, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                flash('Data limite inválida!', 'danger')
                return redirect(url_for('metas'))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verifica se a meta pertence ao usuário
        cursor.execute('SELECT id FROM metas WHERE id = %s AND usuario_id = %s', 
                      (meta_id, session['user_id']))
        
        if not cursor.fetchone():
            flash('Meta não encontrada!', 'danger')
            return redirect(url_for('metas'))
        
        cursor.execute('''
            UPDATE metas 
            SET titulo = %s, descricao = %s, valor_alvo = %s, categoria = %s, data_limite = %s, cor = %s
            WHERE id = %s AND usuario_id = %s
        ''', (titulo, descricao, valor_alvo, categoria, data_limite, cor, meta_id, session['user_id']))
        conn.commit()
        
        flash('Meta atualizada com sucesso!', 'success')
        
    except Exception as e:
        flash(f'Erro ao editar meta: {str(e)}', 'danger')
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    
    return redirect(url_for('metas'))

@app.route('/excluir-meta/<int:id>')
@login_required
def excluir_meta(id):
    """Exclui uma meta"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verifica se a meta pertence ao usuário
        cursor.execute('SELECT id FROM metas WHERE id = %s AND usuario_id = %s', 
                      (id, session['user_id']))
        
        if not cursor.fetchone():
            flash('Meta não encontrada!', 'danger')
            return redirect(url_for('metas'))
        
        cursor.execute('DELETE FROM metas WHERE id = %s AND usuario_id = %s', 
                      (id, session['user_id']))
        conn.commit()
        
        flash('Meta excluída com sucesso!', 'success')
        
    except Exception as e:
        flash(f'Erro ao excluir meta: {str(e)}', 'danger')
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    
    return redirect(url_for('metas'))

# ============== ROTA DE TESTE (DEV) ==============
@app.route('/dev/test-metas')
def dev_test_metas():
    """
    Rota de desenvolvimento para testar o template 'metas.html' com dados mock.
    Disponível SOMENTE quando app.debug == True.
    """
    if not app.debug:
        abort(404)
    
    # Mock de metas para testar renderização e get_cor_clara
    hoje = datetime.now().date()
    metas_mock = [
        {
            'id': 1,
            'titulo': 'Viagem para o Nordeste',
            'descricao': 'Economizar para as férias de verão.',
            'valor_alvo': 3000.00,
            'valor_atual': 1200.00,
            'valor_faltante': 1800.00,
            'categoria': 'Viagem',
            'data_inicio': hoje - timedelta(days=30),
            'data_limite': hoje + timedelta(days=60),
            'dias_restantes': 60,
            'progresso': 40.0,
            'cor': '#6366F1',
            'status': 'ativa',
            'atrasada': 0
        },
        {
            'id': 2,
            'titulo': 'Fundo de Emergência',
            'descricao': 'Reserva de 6 meses.',
            'valor_alvo': 6000.00,
            'valor_atual': 6000.00,
            'valor_faltante': 0.00,
            'categoria': 'Economia',
            'data_inicio': hoje - timedelta(days=400),
            'data_limite': None,
            'dias_restantes': None,
            'progresso': 100.0,
            'cor': '#10B981',
            'status': 'concluida',
            'atrasada': 0
        }
    ]
    
    estatisticas_mock = {
        'total_metas': 2,
        'metas_ativas': 1,
        'metas_concluidas': 1,
        'total_economizado': 7200.00,
        'total_objetivo': 3000.00,
        'progresso_geral': 40.0
    }
    
    metas_proximas_mock = [
        {
            'id': 1,
            'titulo': 'Viagem para o Nordeste',
            'data_limite': hoje + timedelta(days=5),
            'dias_restantes': 5
        }
    ]
    
    today = hoje.strftime('%Y-%m-%d')
    
    # Seleciona o template com base no modo do usuário
    modo = session.get('user_modo', 'simples')
    template_name = 'metas_simples.html' if modo == 'simples' else 'metas_avancado.html'

    return render_template(
        template_name,  # Usa a variável dinâmica
        metas=metas_mock,          # CORRIGIDO: Usa os dados mock
        estatisticas=estatisticas_mock, # CORRIGIDO
        metas_proximas=metas_proximas_mock, # CORRIGIDO
        today=today
    )

# ============== TRATAMENTO DE ERROS ==============
@app.errorhandler(404)
def page_not_found(e):
    """Página não encontrada"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """Erro interno do servidor"""
    flash('Ocorreu um erro interno. Tente novamente.', 'danger')
    return redirect(url_for('index'))

# ============== EXPORTAÇÃO ==============

@app.route('/exportar/excel')
@login_required
def exportar_excel():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        # Busca todas as transações do usuário
        query = """
            SELECT tipo, categoria, descricao, valor, data 
            FROM transacoes 
            WHERE usuario_id = %s 
            ORDER BY data DESC
        """
        # Usamos pandas para ler direto do SQL, muito mais fácil
        df = pd.read_sql(query, conn, params=(session['user_id'],))
        
        # Formata a coluna de data
        df['data'] = pd.to_datetime(df['data']).dt.strftime('%d/%m/%Y')
        
        # Cria um buffer de memória (arquivo virtual)
        output = io.BytesIO()
        
        # Escreve o Excel nesse buffer
        # Requer 'openpyxl' instalado
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Transacoes')
            
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'extrato_{datetime.now().strftime("%Y%m%d")}.xlsx'
        )

    except Exception as e:
        print(f"Erro export Excel: {e}")
        flash(f'Erro ao exportar Excel: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))
        
    finally:
        if conn and conn.is_connected():
            conn.close()

@app.route('/exportar/pdf')
@login_required
def exportar_pdf():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT tipo, categoria, descricao, valor, data 
            FROM transacoes 
            WHERE usuario_id = %s 
            ORDER BY data DESC
        """, (session['user_id'],))
        transacoes = cursor.fetchall()
        
        # Criação do PDF usando FPDF
        class PDF(FPDF):
            def header(self):
                self.set_font('Arial', 'B', 15)
                self.cell(0, 10, 'Relatório Financeiro', 0, 1, 'C')
                self.ln(5)
                
            def footer(self):
                self.set_y(-15)
                self.set_font('Arial', 'I', 8)
                self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)
        
        # Cabeçalho da Tabela
        pdf.set_fill_color(200, 220, 255)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(30, 10, "Data", 1, 0, 'C', True)
        pdf.cell(30, 10, "Tipo", 1, 0, 'C', True)
        pdf.cell(40, 10, "Categoria", 1, 0, 'C', True)
        pdf.cell(60, 10, "Descrição", 1, 0, 'C', True)
        pdf.cell(30, 10, "Valor", 1, 1, 'C', True)
        
        # Linhas da Tabela
        pdf.set_font("Arial", size=9)
        for t in transacoes:
            data_fmt = t['data'].strftime('%d/%m/%Y')
            valor_fmt = f"R$ {t['valor']:.2f}"
            
            # Ajuste simples de cor para Receita/Despesa
            pdf.set_text_color(0, 0, 0)
            if t['tipo'] == 'despesa':
                pdf.set_text_color(180, 0, 0) # Vermelho escuro
            elif t['tipo'] == 'receita':
                pdf.set_text_color(0, 100, 0) # Verde escuro
                
            pdf.cell(30, 10, data_fmt, 1, 0, 'C')
            pdf.cell(30, 10, t['tipo'].capitalize(), 1, 0, 'C')
            pdf.cell(40, 10, t['categoria'][:20], 1, 0, 'L') # Limita caracteres
            pdf.cell(60, 10, t['descricao'][:30], 1, 0, 'L') # Limita caracteres
            pdf.cell(30, 10, valor_fmt, 1, 1, 'R')
            
        # Saída
        return send_file(
            io.BytesIO(pdf.output(dest='S').encode('latin-1', 'replace')),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'relatorio_{datetime.now().strftime("%Y%m%d")}.pdf'
        )

    except Exception as e:
        print(f"Erro export PDF: {e}")
        flash(f'Erro ao exportar PDF: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))
        
    finally:
        if conn and conn.is_connected():
            conn.close()
            
if __name__ == '__main__':
    # Para habilitar a rota de testes use FLASK_DEBUG=True no .env ou no ambiente
    app.run(debug=os.getenv('FLASK_DEBUG', 'False') == 'True')