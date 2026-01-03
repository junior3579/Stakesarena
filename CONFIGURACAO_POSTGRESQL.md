# Configuração do PostgreSQL (Neon) - Stake Arena

## ✅ Status da Configuração

A configuração do banco de dados PostgreSQL foi concluída com sucesso! O projeto Stake Arena agora está conectado ao banco de dados Neon.

## 📋 Resumo das Alterações

### 1. Arquivo `backend/database_config.py`

O arquivo foi completamente reescrito para suportar PostgreSQL ao invés de SQLite. As principais mudanças incluem:

- **Biblioteca**: Migrado de `sqlite3` para `psycopg2`
- **Configuração de conexão**: Adicionadas credenciais do Neon
- **Sintaxe SQL**: Ajustada para PostgreSQL (SERIAL ao invés de AUTOINCREMENT, %s ao invés de ?)
- **Timestamps**: Melhor tratamento de timezone com PostgreSQL

#### Configuração do Banco de Dados

```python
DB_CONFIG = {
    "user": "neondb_owner",
    "password": "npg_5zKcDn8GmAUi",
    "host": "ep-wandering-truth-acvxs49u-pooler.sa-east-1.aws.neon.tech",
    "database": "neondb",
    "sslmode": "require"
}
```

### 2. Arquivo `requirements.txt`

Adicionada a dependência do PostgreSQL:

```
psycopg2-binary==2.9.9
```

**Nota**: Removida a dependência `pg8000` que estava no arquivo original, pois `psycopg2` é mais robusto e amplamente utilizado.

### 3. Instalação da Dependência

A biblioteca `psycopg2-binary` foi instalada com sucesso no ambiente Python.

## 🧪 Testes Realizados

Foi criado o arquivo `backend/test_connection.py` para validar a configuração. Os testes executados incluíram:

1. ✅ **Conexão com o banco de dados**: Estabelecida com sucesso
2. ✅ **Versão do PostgreSQL**: PostgreSQL 17.7 (Neon)
3. ✅ **Listagem de tabelas**: 25 tabelas encontradas no banco
4. ✅ **Criação de tabelas**: Tabelas do Stake Arena criadas/verificadas
5. ✅ **Contagem de registros**: Verificado que há 1 usuário cadastrado

### Tabelas do Stake Arena

As seguintes tabelas foram criadas/verificadas no banco de dados:

- `usuarios` - Usuários do sistema (1 registro existente)
- `salas` - Salas de apostas
- `apostas` - Apostas realizadas
- `transacoes` - Transações financeiras
- `categorias` - Categorias de salas
- `torneios` - Torneios criados
- `torneio_participantes` - Participantes dos torneios

## 🔧 Principais Diferenças: SQLite → PostgreSQL

| Aspecto | SQLite | PostgreSQL |
|---------|--------|------------|
| **Auto-incremento** | `AUTOINCREMENT` | `SERIAL` |
| **Placeholders** | `?` | `%s` |
| **Timestamps** | String ISO | Tipo `TIMESTAMP` nativo |
| **Conexão** | Arquivo local | Conexão remota via rede |
| **SSL** | Não aplicável | `sslmode='require'` |
| **Rollback** | Implícito | Explícito com `conn.rollback()` |

## 🚀 Como Executar o Projeto

### 1. Instalar Dependências

```bash
cd /home/ubuntu
pip3 install -r requirements.txt
```

### 2. Testar Conexão (Opcional)

```bash
cd /home/ubuntu/backend
python3.11 test_connection.py
```

### 3. Executar o Servidor

```bash
cd /home/ubuntu/backend
python3.11 main.py
```

## 📝 Observações Importantes

### Compatibilidade

Todas as funções mantiveram suas assinaturas originais para garantir compatibilidade com o código existente:

- `conectar_banco_local()` - Agora conecta ao PostgreSQL
- `executar_query_fetchall(query, params)` - Usa sintaxe PostgreSQL
- `executar_query_commit(query, params)` - Inclui rollback em caso de erro
- `criar_tabelas_remoto()` - Cria tabelas com sintaxe PostgreSQL

### Segurança

⚠️ **IMPORTANTE**: As credenciais do banco de dados estão hardcoded no arquivo `database_config.py`. Para produção, considere:

1. Usar variáveis de ambiente
2. Criar um arquivo `.env` (não versionado)
3. Usar serviços de gerenciamento de secrets

### Banco de Dados Existente

O banco de dados Neon já continha várias tabelas de outros projetos. As tabelas do Stake Arena foram criadas sem conflitos. Se necessário, você pode:

- Usar prefixos nas tabelas (ex: `sa_usuarios`)
- Criar um schema separado
- Usar um banco de dados dedicado

## 🔍 Próximos Passos Recomendados

1. **Migração de Dados**: Se havia dados no SQLite local, criar script de migração
2. **Variáveis de Ambiente**: Mover credenciais para arquivo `.env`
3. **Backup**: Configurar rotina de backup do banco PostgreSQL
4. **Monitoramento**: Implementar logs de conexão e queries
5. **Pool de Conexões**: Para melhor performance, considerar usar `psycopg2.pool`

## 📊 Status do Banco de Dados

```
Versão: PostgreSQL 17.7
Host: ep-wandering-truth-acvxs49u-pooler.sa-east-1.aws.neon.tech
Database: neondb
Total de Tabelas: 25
Usuários Cadastrados: 1
```

---

**Configuração realizada em**: 03 de Janeiro de 2026  
**Status**: ✅ Operacional
