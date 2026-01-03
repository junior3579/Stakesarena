
import psycopg2
import psycopg2.extras
import os
from datetime import datetime, timezone

# Configuração do PostgreSQL (Neon)
# Prioriza variáveis de ambiente, com fallback para valores hardcoded
DB_CONFIG = {
    "user": os.getenv("DB_USER", "neondb_owner"),
    "password": os.getenv("DB_PASSWORD", "npg_5zKcDn8GmAUi"),
    "host": os.getenv("DB_HOST", "ep-wandering-truth-acvxs49u-pooler.sa-east-1.aws.neon.tech"),
    "database": os.getenv("DB_NAME", "neondb"),
    "sslmode": os.getenv("DB_SSLMODE", "require")
}

def conectar_banco_local():
    """
    Conecta ao banco de dados PostgreSQL (Neon).
    Mantém o nome da função para compatibilidade com o código existente.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco PostgreSQL: {e}")
        return None

def executar_query_fetchall(query, params=()):
    """
    Executa uma query SELECT e retorna todos os resultados.
    """
    conn = conectar_banco_local()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Erro na query: {e}")
        return None
    finally:
        conn.close()

def executar_query_commit(query, params=()):
    """
    Executa uma query de modificação (INSERT, UPDATE, DELETE) e faz commit.
    """
    conn = conectar_banco_local()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro na query: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def criar_tabelas_remoto():
    """
    Cria todas as tabelas necessárias no banco de dados PostgreSQL.
    """
    queries = [
        '''
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            pontos INTEGER NOT NULL,
            whatsapp TEXT,
            pix_tipo TEXT,
            pix_chave TEXT,
            last_seen TIMESTAMP,
            posicao INTEGER
        )
        ''',
        '''
        CREATE TABLE IF NOT EXISTS categorias (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL UNIQUE
        )
        ''',
        '''
        CREATE TABLE IF NOT EXISTS salas (
            id_sala SERIAL PRIMARY KEY,
            nome_sala TEXT NOT NULL,
            valor_inicial INTEGER NOT NULL,
            criador TEXT NOT NULL,
            jogadores TEXT,
            whatsapp TEXT,
            categoria_id INTEGER,
            FOREIGN KEY(categoria_id) REFERENCES categorias(id)
        )
        ''',
        '''
        CREATE TABLE IF NOT EXISTS apostas (
            id SERIAL PRIMARY KEY,
            id_sala INTEGER NOT NULL,
            id_usuario INTEGER NOT NULL,
            valor_aposta INTEGER NOT NULL,
            status TEXT DEFAULT 'pendente',
            resultado TEXT DEFAULT 'pendente',
            FOREIGN KEY(id_sala) REFERENCES salas(id_sala),
            FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
        )
        ''',
        '''
        CREATE TABLE IF NOT EXISTS transacoes (
            id SERIAL PRIMARY KEY,
            id_usuario INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            valor INTEGER NOT NULL,
            status TEXT DEFAULT 'pendente',
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
        )
        ''',
        '''
        CREATE TABLE IF NOT EXISTS torneios (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            status TEXT DEFAULT 'inscricao',
            vencedor_id INTEGER,
            FOREIGN KEY(vencedor_id) REFERENCES usuarios(id)
        )
        ''',
        '''
        CREATE TABLE IF NOT EXISTS torneio_participantes (
            id SERIAL PRIMARY KEY,
            torneio_id INTEGER NOT NULL,
            usuario_id INTEGER NOT NULL,
            status TEXT DEFAULT 'ativo',
            FOREIGN KEY(torneio_id) REFERENCES torneios(id),
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
        '''
    ]
    for q in queries:
        executar_query_commit(q)

def reordenar_posicoes():
    """
    Reordena as posições dos usuários de forma sequencial.
    """
    query_usuarios = "SELECT id FROM usuarios ORDER BY posicao ASC, id ASC"
    usuarios = executar_query_fetchall(query_usuarios)
    
    if not usuarios:
        return
    
    for index, (user_id,) in enumerate(usuarios, start=1):
        executar_query_commit(
            "UPDATE usuarios SET posicao = %s WHERE id = %s",
            (index, user_id)
        )

def obter_proxima_posicao_vaga():
    """
    Obtém a próxima posição vaga disponível.
    """
    result = executar_query_fetchall("SELECT posicao FROM usuarios ORDER BY posicao")
    posicoes_ocupadas = {r[0] for r in result if r[0] is not None}
    
    pos = 1
    while pos in posicoes_ocupadas:
        pos += 1
    return pos

def obter_menor_id_vago():
    """
    Encontra o menor ID disponível na tabela usuarios para reutilização.
    """
    result = executar_query_fetchall("SELECT id FROM usuarios ORDER BY id")
    ids_ocupados = {r[0] for r in result}
    
    id_vago = 1
    while id_vago in ids_ocupados:
        id_vago += 1
    return id_vago

def atualizar_atividade_usuario(id_usuario):
    """
    Atualiza o timestamp de última atividade do usuário.
    """
    executar_query_commit(
        "UPDATE usuarios SET last_seen = %s WHERE id = %s",
        (datetime.now(timezone.utc), id_usuario)
    )

def listar_usuarios_online(minutos=5):
    """
    Lista os usuários que estiveram online nos últimos X minutos.
    """
    from datetime import timedelta
    limite = datetime.now(timezone.utc) - timedelta(minutes=minutos)
    result = executar_query_fetchall(
        "SELECT nome, last_seen FROM usuarios WHERE last_seen >= %s ORDER BY last_seen DESC",
        (limite,)
    )
    if not result:
        return []
    
    usuarios_online = []
    for nome, last_seen in result:
        if last_seen:
            try:
                # Ajusta para o timezone local (GMT-3)
                last_seen_local = last_seen - timedelta(hours=3)
                usuarios_online.append({
                    'nome': nome,
                    'last_seen': last_seen_local.strftime('%H:%M:%S')
                })
            except:
                continue
    
    return usuarios_online
