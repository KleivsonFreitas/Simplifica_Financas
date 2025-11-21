#!/usr/bin/env python3
"""
Script de Inicialização do Sistema de Gestão Financeira
Verifica se tudo está configurado corretamente antes de iniciar
"""

import sys
import os
import mysql.connector
from mysql.connector import Error

def verificar_python():
    """Verifica versão do Python"""
    print("🐍 Verificando Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 ou superior é necessário!")
        print(f"   Versão atual: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def verificar_dependencias():
    """Verifica se as dependências estão instaladas"""
    print("\n📦 Verificando dependências...")
    dependencias = {
        'flask': 'Flask',
        'mysql.connector': 'mysql-connector-python',
        'werkzeug': 'Werkzeug'
    }
    
    todas_instaladas = True
    for modulo, nome in dependencias.items():
        try:
            __import__(modulo)
            print(f"✅ {nome} - Instalado")
        except ImportError:
            print(f"❌ {nome} - NÃO instalado")
            todas_instaladas = False
    
    if not todas_instaladas:
        print("\n💡 Para instalar as dependências, execute:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def verificar_mysql():
    """Verifica conexão com MySQL"""
    print("\n🗄️  Verificando MySQL...")
    
    # Configurações padrão
    configs = {
        'host': 'localhost',
        'user': 'root',
        'password': input("Digite a senha do MySQL (root): ")
    }
    
    try:
        # Tenta conectar
        conn = mysql.connector.connect(**configs)
        
        if conn.is_connected():
            print("✅ MySQL - Conectado")
            
            # Verifica se o banco existe
            cursor = conn.cursor()
            cursor.execute("SHOW DATABASES LIKE 'gestao_financeira'")
            result = cursor.fetchone()
            
            if result:
                print("✅ Banco 'gestao_financeira' - Encontrado")
                
                # Verifica tabelas
                cursor.execute("USE gestao_financeira")
                cursor.execute("SHOW TABLES")
                tabelas = cursor.fetchall()
                
                if len(tabelas) >= 4:
                    print(f"✅ {len(tabelas)} tabelas encontradas")
                else:
                    print(f"⚠️  Apenas {len(tabelas)} tabelas encontradas")
                    print("   Execute o arquivo database.sql no MySQL")
            else:
                print("❌ Banco 'gestao_financeira' - NÃO encontrado")
                print("\n💡 Para criar o banco, execute no MySQL:")
                print("   mysql -u root -p < database.sql")
                
            cursor.close()
            conn.close()
            return True
            
    except Error as e:
        print(f"❌ Erro ao conectar ao MySQL: {e}")
        print("\n💡 Verifique se:")
        print("   1. O MySQL está rodando")
        print("   2. A senha está correta")
        print("   3. O usuário 'root' tem permissões adequadas")
        return False

def verificar_estrutura_arquivos():
    """Verifica se os arquivos necessários existem"""
    print("\n📁 Verificando estrutura de arquivos...")
    
    arquivos_necessarios = {
        'app.py': 'Aplicação Flask principal',
        'database.sql': 'Script de criação do banco',
        'requirements.txt': 'Dependências Python',
        'templates/': 'Pasta de templates HTML',
        'templates/base.html': 'Template base'
    }
    
    todos_existem = True
    for arquivo, descricao in arquivos_necessarios.items():
        if os.path.exists(arquivo):
            print(f"✅ {arquivo} - OK")
        else:
            print(f"❌ {arquivo} - NÃO encontrado ({descricao})")
            todos_existem = False
    
    return todos_existem

def main():
    """Função principal"""
    print("=" * 60)
    print("🚀 VERIFICAÇÃO DO SISTEMA DE GESTÃO FINANCEIRA")
    print("=" * 60)
    
    # Verificações
    resultados = []
    resultados.append(verificar_python())
    resultados.append(verificar_dependencias())
    resultados.append(verificar_estrutura_arquivos())
    resultados.append(verificar_mysql())
    
    print("\n" + "=" * 60)
    if all(resultados):
        print("✅ TUDO PRONTO! O sistema está configurado corretamente.")
        print("\n🎉 Para iniciar o sistema, execute:")
        print("   python app.py")
        print("\n📱 Depois acesse no navegador:")
        print("   http://localhost:5000")
        print("=" * 60)
        
        # Pergunta se deseja iniciar
        iniciar = input("\nDeseja iniciar o sistema agora? (s/n): ")
        if iniciar.lower() == 's':
            print("\n🚀 Iniciando sistema...")
            os.system('python app.py')
    else:
        print("❌ Existem problemas que precisam ser corrigidos.")
        print("\n📚 Consulte o arquivo INSTALACAO.md para mais detalhes.")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()