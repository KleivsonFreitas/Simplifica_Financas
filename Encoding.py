import os
import glob

# Dicionário de correções
correcoes = {
    'Ã§': 'ç',
    'Ã£': 'ã',
    'Ã¡': 'á',
    'Ã©': 'é',
    'Ã­': 'í',
    'Ã³': 'ó',
    'Ãº': 'ú',
    'Ã¢': 'â',
    'Ãª': 'ê',
    'Ã´': 'ô',
    'Ã ': 'à',
    'Ã‰': 'É',
    'Ãš': 'Ú',
    'ðŸ': '🔒',  # Emojis quebrados
    'â€œ': '"',
    'â€': '"',
    '�': '',  # Remove caracteres inválidos
}

def corrigir_arquivo(caminho):
    """Corrige encoding de um arquivo"""
    try:
        # Tenta ler com diferentes encodings
        conteudo = None
        for encoding in ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']:
            try:
                with open(caminho, 'r', encoding=encoding) as f:
                    conteudo = f.read()
                    print(f"✓ Lido {caminho} como {encoding}")
                    break
            except UnicodeDecodeError:
                continue
        
        if conteudo is None:
            print(f"✗ Não foi possível ler {caminho}")
            return False
        
        # Aplica correções
        conteudo_corrigido = conteudo
        for errado, correto in correcoes.items():
            conteudo_corrigido = conteudo_corrigido.replace(errado, correto)
        
        # Salva como UTF-8
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(conteudo_corrigido)
        
        print(f"✓ Corrigido e salvo: {caminho}")
        return True
        
    except Exception as e:
        print(f"✗ Erro em {caminho}: {e}")
        return False

def main():
    """Corrige todos os arquivos HTML e Python"""
    print("=" * 60)
    print("CORREÇÃO DE ENCODING - SISTEMA GESTÃO FINANCEIRA")
    print("=" * 60)
    print()
    
    # Lista de arquivos para corrigir
    arquivos = [
        'templates/base.html',
        'templates/index.html',
        'templates/login.html',
        'templates/registro.html',
        'templates/dashboard_simples.html',
        'templates/dashboard_avancado.html',
        'templates/adicionar_transacao_simples.html',
        'templates/adicionar_transacao_avancado.html',
        'templates/configuracoes.html',
        'templates/relatorios.html',
        'app.py',
    ]
    
    total = len(arquivos)
    corrigidos = 0
    
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            if corrigir_arquivo(arquivo):
                corrigidos += 1
        else:
            print(f"⚠ Arquivo não encontrado: {arquivo}")
    
    print()
    print("=" * 60)
    print(f"RESULTADO: {corrigidos}/{total} arquivos corrigidos")
    print("=" * 60)
    print()
    
    if corrigidos == total:
        print("✓ SUCESSO! Todos os arquivos foram corrigidos.")
        print("  Agora teste sua aplicação: python app.py")
    else:
        print("⚠ Alguns arquivos não foram encontrados ou tiveram erro.")
        print("  Verifique se está executando o script na pasta raiz do projeto.")

if __name__ == '__main__':
    main()