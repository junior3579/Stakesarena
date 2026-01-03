#!/usr/bin/env python3
"""
Script de teste de conexão com o banco de dados PostgreSQL (Neon)
"""

from database_config import conectar_banco_local, criar_tabelas_remoto, executar_query_fetchall

def testar_conexao():
    """Testa a conexão com o banco de dados"""
    print("=" * 60)
    print("TESTE DE CONEXÃO - POSTGRESQL (NEON)")
    print("=" * 60)
    
    # Teste 1: Conectar ao banco
    print("\n[1] Testando conexão com o banco de dados...")
    conn = conectar_banco_local()
    
    if conn:
        print("✓ Conexão estabelecida com sucesso!")
        
        # Teste 2: Verificar versão do PostgreSQL
        print("\n[2] Verificando versão do PostgreSQL...")
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✓ Versão: {version}")
        except Exception as e:
            print(f"✗ Erro ao verificar versão: {e}")
        
        # Teste 3: Listar tabelas existentes
        print("\n[3] Listando tabelas existentes...")
        try:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tabelas = cursor.fetchall()
            if tabelas:
                print(f"✓ Tabelas encontradas ({len(tabelas)}):")
                for (tabela,) in tabelas:
                    print(f"  - {tabela}")
            else:
                print("⚠ Nenhuma tabela encontrada (banco vazio)")
        except Exception as e:
            print(f"✗ Erro ao listar tabelas: {e}")
        
        conn.close()
        
        # Teste 4: Criar tabelas
        print("\n[4] Criando tabelas no banco de dados...")
        try:
            criar_tabelas_remoto()
            print("✓ Tabelas criadas/verificadas com sucesso!")
        except Exception as e:
            print(f"✗ Erro ao criar tabelas: {e}")
        
        # Teste 5: Verificar tabelas criadas
        print("\n[5] Verificando tabelas após criação...")
        result = executar_query_fetchall("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        if result:
            print(f"✓ Total de tabelas: {len(result)}")
            for (tabela,) in result:
                print(f"  - {tabela}")
        
        # Teste 6: Contar registros em cada tabela
        print("\n[6] Contando registros em cada tabela...")
        tabelas_principais = ['usuarios', 'salas', 'apostas', 'transacoes', 'categorias', 'torneios', 'torneio_participantes']
        
        for tabela in tabelas_principais:
            try:
                result = executar_query_fetchall(f"SELECT COUNT(*) FROM {tabela}")
                if result:
                    count = result[0][0]
                    print(f"  - {tabela}: {count} registro(s)")
            except Exception as e:
                print(f"  - {tabela}: Erro ao contar ({e})")
        
        print("\n" + "=" * 60)
        print("✓ TESTE CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        
    else:
        print("✗ Falha ao conectar ao banco de dados!")
        print("\nVerifique:")
        print("  - Credenciais no arquivo database_config.py")
        print("  - Conectividade com a internet")
        print("  - Status do serviço Neon")

if __name__ == "__main__":
    testar_conexao()
