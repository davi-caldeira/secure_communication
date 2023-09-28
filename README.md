# Comunicação Segura entre Alice e Bob

Este projeto demonstra uma comunicação segura entre dois participantes, Alice (o servidor) e Bob (o cliente), usando Diffie-Hellman para troca de chaves e HMAC para garantir a integridade da mensagem.

## Como funciona?

### 1. Estabelecimento da Conexão
- Alice (o servidor) fica esperando por uma conexão.
- Bob (o cliente) se conecta a Alice.

### 2. Troca de Chaves Diffie-Hellman
- Alice envia sua chave pública Diffie-Hellman para Bob.
- Bob gera sua própria chave privada e pública Diffie-Hellman usando os parâmetros da chave pública de Alice.
- Bob envia sua chave pública Diffie-Hellman para Alice.
- Ambas as partes usam suas chaves privadas e a chave pública da outra parte para gerar uma chave compartilhada.

### 3. Derivação da Chave HMAC
- A chave compartilhada Diffie-Hellman é então usada para derivar uma chave HMAC. Isso é feito usando SHA-256.

### 4. Comunicação
- Bob envia uma mensagem para Alice. Ele anexa um HMAC da mensagem usando a chave HMAC derivada.
- Alice recebe a mensagem e verifica o HMAC usando sua própria chave HMAC derivada. Se o HMAC for verificado, Alice sabe que a mensagem não foi adulterada durante a transmissão.

## Como Executar

1. Execute o arquivo `Alice.py`.
2. Em outro terminal ou ambiente, execute o arquivo `Bob.py`.
3. Observe as saídas em ambos os terminais para entender o fluxo da comunicação e a verificação do HMAC.
