# 🚀 Servidor Stake Arena - Em Execução

## ✅ Status do Servidor

O servidor Flask do Stake Arena está **ONLINE** e funcionando com o banco de dados PostgreSQL (Neon) configurado!

## 🌐 Acesso à Aplicação

**URL Pública**: https://5000-iazho4x0io7flmciagfwq-b60b26f0.us1.manus.computer

## 📊 Informações do Servidor

| Configuração | Valor |
|--------------|-------|
| **Framework** | Flask + Socket.IO |
| **Porta Local** | 5000 |
| **Host** | 0.0.0.0 (todas as interfaces) |
| **Banco de Dados** | PostgreSQL (Neon Cloud) |
| **Status** | ✅ Online |

## 🔧 Configuração Atual

### Banco de Dados
- **Host**: ep-wandering-truth-acvxs49u-pooler.sa-east-1.aws.neon.tech
- **Database**: neondb
- **Versão**: PostgreSQL 17.7
- **SSL**: Habilitado

### Aplicação
- **Frontend**: React (servido estaticamente)
- **Backend**: Flask com Socket.IO
- **CORS**: Habilitado para todas as origens
- **Debug Mode**: Desabilitado (produção)

## 📡 Endpoints da API

A aplicação expõe os seguintes endpoints:

### Autenticação
- `POST /api/login` - Login de usuário
- `POST /api/register` - Registro de novo usuário

### Usuários
- `GET /api/usuarios` - Listar todos os usuários
- `GET /api/usuarios/online` - Usuários online
- `GET /api/usuarios/<id>` - Detalhes de um usuário
- `PUT /api/usuarios/<id>` - Atualizar usuário
- `DELETE /api/usuarios/<id>` - Deletar usuário

### Salas
- `GET /api/salas` - Listar salas
- `POST /api/salas` - Criar nova sala
- `GET /api/salas/<id>` - Detalhes de uma sala
- `DELETE /api/salas/<id>` - Deletar sala

### Apostas
- `POST /api/apostas` - Criar aposta
- `GET /api/apostas/<id>` - Detalhes de uma aposta

### Transações
- `GET /api/transacoes` - Listar transações
- `POST /api/transacoes` - Criar transação

### Admin
- `GET /api/admin/*` - Funcionalidades administrativas

## 🔌 WebSocket (Socket.IO)

O servidor também suporta comunicação em tempo real via Socket.IO para:
- Notificações de apostas
- Atualizações de salas
- Status de usuários online
- Eventos de torneios

## 🛠️ Como Parar o Servidor

Para parar o servidor, execute:

```bash
pkill -f "python3.11 main.py"
```

Ou encontre o PID e mate o processo:

```bash
ps aux | grep "python.*main.py"
kill <PID>
```

## 🔄 Como Reiniciar o Servidor

```bash
cd /home/ubuntu/backend
python3.11 main.py
```

## 📝 Logs e Monitoramento

Para visualizar os logs do servidor em tempo real:

```bash
# Ver processo rodando
ps aux | grep python3.11

# Ver conexões na porta 5000
netstat -tlnp | grep :5000
```

## ⚠️ Observações Importantes

1. **URL Temporária**: A URL pública é temporária e válida apenas enquanto o sandbox estiver ativo
2. **Persistência**: O servidor continuará rodando em background
3. **Banco de Dados**: Todas as operações são persistidas no PostgreSQL (Neon)
4. **CORS**: Configurado para aceitar requisições de qualquer origem

## 🎯 Próximos Passos

Para deploy em produção, considere:

1. **Usar Gunicorn** ao invés do servidor de desenvolvimento do Flask
2. **Configurar Nginx** como proxy reverso
3. **Adicionar HTTPS** com certificado SSL
4. **Implementar rate limiting** para proteger a API
5. **Configurar logs** em arquivo para análise posterior
6. **Monitoramento** com ferramentas como PM2 ou Supervisor

---

**Servidor iniciado em**: 03 de Janeiro de 2026  
**Status**: ✅ Online e Operacional
