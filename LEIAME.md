# Servidor MCP para WhatsApp

Este é um servidor Model Context Protocol (MCP) para WhatsApp.

Com ele você pode pesquisar e ler suas mensagens pessoais do WhatsApp (incluindo imagens, vídeos, documentos e mensagens de áudio), pesquisar seus contatos e enviar mensagens para indivíduos ou grupos. Você também pode enviar arquivos de mídia, incluindo imagens, vídeos, documentos e mensagens de áudio.

Ele se conecta à sua **conta pessoal do WhatsApp** diretamente via API multidevice do WhatsApp Web (usando a biblioteca [whatsmeow](https://github.com/tulir/whatsmeow)). Todas as suas mensagens são armazenadas localmente em um banco de dados SQLite e enviadas apenas para um LLM (como Claude) quando o agente as acessa por meio de ferramentas (que você controla).

Aqui está um exemplo do que você pode fazer quando estiver conectado ao Claude.

![WhatsApp MCP](./example-use.png)

> Para receber atualizações sobre este e outros projetos em que trabalho, [insira seu e-mail aqui](https://docs.google.com/forms/d/1rTF9wMBTN0vPfzWuQa2BjfGKdKIpTbyeKxhPMcEzgyI/preview)

> *Atenção:* assim como muitos servidores MCP, o WhatsApp MCP está sujeito à [tríade letal](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/). Isso significa que a injeção de projeto pode levar à exfiltração de dados privados.

## Instalação

### Pré-requisitos

- Go
- Python 3.6+
- Aplicativo Anthropic Claude Desktop (ou Cursor)
- UV (gerenciador de pacotes Python), instale com `curl -LsSf https://astral.sh/uv/install.sh | sh`
- FFmpeg (_opcional_) - Necessário apenas para mensagens de áudio. Se você quiser enviar arquivos de áudio como mensagens de voz reproduzíveis do WhatsApp, eles devem estar no formato `.ogg` Opus. Com o FFmpeg instalado, o servidor MCP converterá automaticamente arquivos de áudio que não estejam em Opus. Sem o FFmpeg, você ainda pode enviar arquivos de áudio brutos usando a ferramenta `send_file`.

### Passos para Instalação

1. **Clone este repositório**

   ```bash
   git clone https://github.com/Copyxyzai/whatsapp-mcp.git
   cd whatsapp-mcp
   ```

2. **Execute a ponte do WhatsApp**

   Navegue até o diretório whatsapp-bridge e execute o aplicativo Go:

   ```bash
   cd whatsapp-bridge
   go run main.go
   ```

   Na primeira vez que você executá-lo, será solicitado que você escaneie um código QR. Escaneie o código QR com o aplicativo WhatsApp do seu celular para autenticar.

   Após aproximadamente 20 dias, você poderá precisar autenticar novamente.

3. **Conecte-se ao servidor MCP**

   Copie o JSON abaixo com os valores apropriados de {{PATH}}:

   ```json
   {
     "mcpServers": {
       "whatsapp": {
         "command": "{{PATH_TO_UV}}", // Execute `which uv` e coloque a saída aqui
         "args": [
           "--directory",
           "{{PATH_TO_SRC}}/whatsapp-mcp/whatsapp-mcp-server", // Entre no repositório, execute `pwd` e insira a saída aqui + "/whatsapp-mcp-server"
           "run",
           "main.py"
         ]
       }
     }
   }
   ```

   Para o **Claude**, salve isso como `claude_desktop_config.json` no diretório de configuração do Claude Desktop em:

   ```
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

   Para o **Cursor**, salve isso como `mcp.json` no diretório de configuração do Cursor em:

   ```
   ~/.cursor/mcp.json
   ```

4. **Reinicie o Claude Desktop / Cursor**

   Abra o Claude Desktop e você deverá ver o WhatsApp como uma integração disponível.

   Ou reinicie o Cursor.

### Compatibilidade com Windows

Se você estiver executando este projeto no Windows, esteja ciente de que o `go-sqlite3` requer que o **CGO esteja habilitado** para compilar e funcionar corretamente. Por padrão, o **CGO está desabilitado no Windows**, então você precisa habilitá-lo explicitamente e ter um compilador C instalado.

#### Passos para fazer funcionar:

1. **Instale um compilador C**  
   Recomendamos usar [MSYS2](https://www.msys2.org/) para instalar um compilador C para Windows. Após instalar o MSYS2, certifique-se de adicionar a pasta `ucrt64\bin` ao seu `PATH`.  
   → Um guia passo a passo está disponível [aqui](https://code.visualstudio.com/docs/cpp/config-mingw).

2. **Habilite o CGO e execute o aplicativo**

   ```bash
   cd whatsapp-bridge
   go env -w CGO_ENABLED=1
   go run main.go
   ```

Sem essa configuração, você provavelmente encontrará erros como:

> `Binary was compiled with 'CGO_ENABLED=0', go-sqlite3 requires cgo to work.`

## Visão Geral da Arquitetura

Esta aplicação consiste em dois componentes principais:

1. **Ponte WhatsApp em Go** (`whatsapp-bridge/`): Um aplicativo Go que se conecta à API web do WhatsApp, gerencia a autenticação via código QR e armazena o histórico de mensagens no SQLite. Ele serve como a ponte entre o WhatsApp e o servidor MCP.

2. **Servidor MCP em Python** (`whatsapp-mcp-server/`): Um servidor Python que implementa o Model Context Protocol (MCP), que fornece ferramentas padronizadas para o Claude interagir com dados do WhatsApp e enviar/receber mensagens.

### Armazenamento de Dados

- Todo o histórico de mensagens é armazenado em um banco de dados SQLite dentro do diretório `whatsapp-bridge/store/`
- O banco de dados mantém tabelas para chats e mensagens
- As mensagens são indexadas para pesquisa e recuperação eficientes

## Uso

Uma vez conectado, você pode interagir com seus contatos do WhatsApp através do Claude, aproveitando as capacidades de IA do Claude em suas conversas do WhatsApp.

### Ferramentas MCP

O Claude pode acessar as seguintes ferramentas para interagir com o WhatsApp:

- **search_contacts**: Pesquisar contatos por nome ou número de telefone
- **list_messages**: Recuperar mensagens com filtros e contexto opcionais
- **list_chats**: Listar chats disponíveis com metadados
- **get_chat**: Obter informações sobre um chat específico
- **get_direct_chat_by_contact**: Encontrar um chat direto com um contato específico
- **get_contact_chats**: Listar todos os chats envolvendo um contato específico
- **get_last_interaction**: Obter a mensagem mais recente com um contato
- **get_message_context**: Recuperar contexto ao redor de uma mensagem específica
- **send_message**: Enviar uma mensagem WhatsApp para um número de telefone ou JID de grupo especificado
- **send_file**: Enviar um arquivo (imagem, vídeo, áudio bruto, documento) para um destinatário especificado
- **send_audio_message**: Enviar um arquivo de áudio como mensagem de voz do WhatsApp (requer que o arquivo seja um .ogg opus ou que o ffmpeg esteja instalado)
- **download_media**: Baixar mídia de uma mensagem WhatsApp e obter o caminho do arquivo local

### Recursos de Manipulação de Mídia

O servidor MCP suporta envio e recebimento de vários tipos de mídia:

#### Envio de Mídia

Você pode enviar vários tipos de mídia para seus contatos do WhatsApp:

- **Imagens, Vídeos, Documentos**: Use a ferramenta `send_file` para compartilhar qualquer tipo de mídia suportado.
- **Mensagens de Voz**: Use a ferramenta `send_audio_message` para enviar arquivos de áudio como mensagens de voz reproduzíveis do WhatsApp.
  - Para compatibilidade ideal, os arquivos de áudio devem estar no formato `.ogg` Opus.
  - Com o FFmpeg instalado, o sistema converterá automaticamente outros formatos de áudio (MP3, WAV, etc.) para o formato necessário.
  - Sem o FFmpeg, você ainda pode enviar arquivos de áudio brutos usando a ferramenta `send_file`, mas eles não aparecerão como mensagens de voz reproduzíveis.

#### Download de Mídia

Por padrão, apenas os metadados da mídia são armazenados no banco de dados local. A mensagem indicará que a mídia foi enviada. Para acessar essa mídia, você precisa usar a ferramenta download_media que recebe o `message_id` e `chat_jid` (que são mostrados ao imprimir mensagens contendo a mídia), isso baixa a mídia e então retorna o caminho do arquivo que pode ser aberto ou passado para outra ferramenta.

## Detalhes Técnicos

1. O Claude envia solicitações para o servidor MCP Python
2. O servidor MCP consulta a ponte Go para dados do WhatsApp ou diretamente o banco de dados SQLite
3. O Go acessa a API do WhatsApp e mantém o banco de dados SQLite atualizado
4. Os dados retornam pela cadeia para o Claude
5. Ao enviar mensagens, a solicitação flui do Claude através do servidor MCP para a ponte Go e para o WhatsApp

## Solução de Problemas

- Se você encontrar problemas de permissão ao executar o uv, talvez seja necessário adicioná-lo ao seu PATH ou usar o caminho completo para o executável.
- Certifique-se de que tanto o aplicativo Go quanto o servidor Python estejam em execução para que a integração funcione corretamente.

### Problemas de Autenticação

- **Código QR não está sendo exibido**: Se o código QR não aparecer, tente reiniciar o script de autenticação. Se os problemas persistirem, verifique se o seu terminal suporta a exibição de códigos QR.
- **WhatsApp já está conectado**: Se sua sessão já estiver ativa, a ponte Go reconectará automaticamente sem mostrar um código QR.
- **Limite de dispositivos atingido**: O WhatsApp limita o número de dispositivos vinculados. Se você atingir esse limite, precisará remover um dispositivo existente do WhatsApp no seu telefone (Configurações > Dispositivos vinculados).
- **Nenhuma mensagem sendo carregada**: Após a autenticação inicial, pode levar vários minutos para que seu histórico de mensagens seja carregado, especialmente se você tiver muitos chats.
- **WhatsApp fora de sincronização**: Se suas mensagens do WhatsApp ficarem fora de sincronização com a ponte, exclua ambos os arquivos de banco de dados (`whatsapp-bridge/store/messages.db` e `whatsapp-bridge/store/whatsapp.db`) e reinicie a ponte para autenticar novamente.

Para solução de problemas adicionais de integração com o Claude Desktop, consulte a [documentação MCP](https://modelcontextprotocol.io/quickstart/server#claude-for-desktop-integration-issues). A documentação inclui dicas úteis para verificar logs e resolver problemas comuns.

---

[English Version](README.md) | Versão em Português
