# Projeto de Criptografia Híbrida

## O que o programa faz
- Gera um par de chaves RSA de 2048 bits.
- Criptografa uma mensagem com AES-256-GCM.
- Protege a chave AES usando RSA-OAEP com SHA-256.
- Descriptografa a mensagem.

## Requisitos
- Python 3.9 ou superior.
- Biblioteca `cryptography`.

## Como executar no VS Code
1. Extraia a pasta do projeto.
2. Abra a pasta no VS Code.
3. Abra o terminal do VS Code.
4. Instale a dependência:

   ```bash
   pip install -r requirements.txt
   ```

5. Execute:

   ```bash
   python main.py
   ```

## Como testar
1. Escolha `1` para gerar as chaves.
2. Escolha `2` e digite uma mensagem.
3. Escolha `3` para recuperar a mensagem original.

## Algoritmos utilizados
- **AES-256-GCM:** criptografa a mensagem e verifica se o conteúdo foi alterado.
- **RSA-OAEP com SHA-256:** protege a chave AES usando a chave pública RSA.
- **Base64:** representa os dados binários em texto para armazená-los no arquivo JSON.

## Conceitos importantes
- **Confidencialidade:** impede que pessoas sem a chave adequada leiam a mensagem.
- **Integridade:** permite detectar alterações nos dados.
- **Autenticidade:** trata de confirmar quem enviou a mensagem. O AES-GCM, neste exemplo, verifica a integridade usando a chave secreta compartilhada, mas não comprova sozinho a identidade do remetente.
- **Certificado digital:** documento eletrônico que associa uma chave pública a uma identidade, emitido por uma autoridade certificadora.
- **PKI:** conjunto de regras, processos e entidades usados para emitir, validar e gerenciar certificados e chaves públicas.

## Limitações e cuidados
- A chave privada é salva sem senha para simplificar a demonstração acadêmica. Em um sistema real, ela deve ser protegida adequadamente.
- O programa não cria nem valida certificados digitais e não implementa uma PKI.
- O programa não usa assinatura digital. Portanto, não comprova a identidade de quem criou a mensagem.
- O nonce não deve ser reutilizado com a mesma chave AES. O programa gera uma chave AES nova para cada mensagem.
- Use apenas mensagens de teste e ambiente próprio ou autorizado.
