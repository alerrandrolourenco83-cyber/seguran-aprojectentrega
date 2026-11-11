import os
import json
import base64
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

PASTA = Path(__file__).resolve().parent
CHAVE_PUBLICA = PASTA / "chave_publica.pem"
CHAVE_PRIVADA = PASTA / "chave_privada.pem"
ARQUIVO_MENSAGEM = PASTA / "mensagem_criptografada.json"


def gerar_chaves():
    """Gera um par de chaves RSA e salva os arquivos PEM."""
    chave_privada = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    chave_publica = chave_privada.public_key()
    dados_privados = chave_privada.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    dados_publicos = chave_publica.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    CHAVE_PRIVADA.write_bytes(dados_privados)
    CHAVE_PUBLICA.write_bytes(dados_publicos)

    print("\nChaves geradas com sucesso!")
    print(f"Chave pública: {CHAVE_PUBLICA.name}")
    print(f"Chave privada: {CHAVE_PRIVADA.name}")
    print("Atenção: neste projeto acadêmico, a chave privada não tem senha.")
    print("Não use esse armazenamento simples em um sistema real.")


def carregar_chave_publica():
    if not CHAVE_PUBLICA.exists():
        raise FileNotFoundError("Gere as chaves primeiro (opção 1).")

    return serialization.load_pem_public_key(CHAVE_PUBLICA.read_bytes())


def carregar_chave_privada():
    if not CHAVE_PRIVADA.exists():
        raise FileNotFoundError("Gere as chaves primeiro (opção 1).")

    return serialization.load_pem_private_key(
        CHAVE_PRIVADA.read_bytes(),
        password=None
    )


def criar_padding_oaep():
    """Cria a configuração RSA usada para proteger e recuperar a chave AES."""
    return padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )


def criptografar_mensagem():
    """Usa AES-GCM para a mensagem e RSA-OAEP para proteger a chave AES."""
    chave_publica = carregar_chave_publica()
    mensagem = input("\nDigite a mensagem que deseja proteger: ")

    if not mensagem.strip():
        print("A mensagem não pode ficar vazia.")
        return

    # AES-256: chave aleatória de 32 bytes.
    chave_aes = AESGCM.generate_key(bit_length=256)
    aes = AESGCM(chave_aes)

    # O nonce de 12 bytes é recomendado para AES-GCM.
    nonce = os.urandom(12)
    texto_cifrado = aes.encrypt(nonce, mensagem.encode("utf-8"), None)

    # RSA-OAEP protege a chave AES, não a mensagem inteira.
    chave_aes_protegida = chave_publica.encrypt(
        chave_aes,
        criar_padding_oaep()
    )

    pacote = {
        "algoritmo_mensagem": "AES-256-GCM",
        "algoritmo_chave": "RSA-OAEP-SHA256",
        "nonce": base64.b64encode(nonce).decode("utf-8"),
        "chave_aes_protegida": base64.b64encode(chave_aes_protegida).decode("utf-8"),
        "mensagem_cifrada": base64.b64encode(texto_cifrado).decode("utf-8")
    }

    ARQUIVO_MENSAGEM.write_text(
        json.dumps(pacote, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    print("\nMensagem criptografada com sucesso!")
    print(f"Dados salvos em: {ARQUIVO_MENSAGEM.name}")


def ler_pacote():
    if not ARQUIVO_MENSAGEM.exists():
        raise FileNotFoundError("Ainda não existe mensagem criptografada. Use a opção 2.")

    return json.loads(ARQUIVO_MENSAGEM.read_text(encoding="utf-8"))


def recuperar_chave_aes(chave_privada, pacote):
    """Abre a chave AES usando a chave privada RSA."""
    chave_aes_protegida = base64.b64decode(pacote["chave_aes_protegida"])
    return chave_privada.decrypt(chave_aes_protegida, criar_padding_oaep())


def descriptografar_mensagem():
    """Recupera a chave AES com RSA e depois abre a mensagem com AES-GCM."""
    chave_privada = carregar_chave_privada()
    pacote = ler_pacote()

    nonce = base64.b64decode(pacote["nonce"])
    texto_cifrado = base64.b64decode(pacote["mensagem_cifrada"])
    chave_aes = recuperar_chave_aes(chave_privada, pacote)

    mensagem_original = AESGCM(chave_aes).decrypt(
        nonce,
        texto_cifrado,
        None
    ).decode("utf-8")

    print("\nMensagem descriptografada:")
    print(mensagem_original)


def menu():
    while True:
        print("\n========== CRIPTOGRAFIA HÍBRIDA ==========")
        print("1 - Gerar chaves RSA")
        print("2 - Criptografar mensagem")
        print("3 - Descriptografar mensagem")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                gerar_chaves()
            elif opcao == "2":
                criptografar_mensagem()
            elif opcao == "3":
                descriptografar_mensagem()
            elif opcao == "0":
                print("Programa encerrado.")
                break
            else:
                print("Opção inválida. Escolha uma opção do menu.")
        except FileNotFoundError as erro:
            print(f"\nAviso: {erro}")
        except (ValueError, KeyError, json.JSONDecodeError) as erro:
            print("\nNão foi possível concluir a operação.")
            print(f"Detalhe: {erro}")
        except Exception as erro:
            print("\nOcorreu um erro inesperado.")
            print(f"Detalhe: {erro}")


if __name__ == "__main__":
    menu()
