import os
import requests

# URL fixa da API
URL_API = "http://172.16.20.50:9022/classificarDocumentos"

def enviarDocumentos(pasta_documentos):
    """
    Envia todos os documentos de uma pasta para um endpoint fixo em uma única requisição.

    :param pasta_documentos: Caminho da pasta contendo os documentos.
    :return: Código de status, resposta da API e lista de arquivos com resposta True.
    """
    # Lista todos os arquivos na pasta
    file_paths = [os.path.join(pasta_documentos, f) for f in os.listdir(pasta_documentos) if os.path.isfile(os.path.join(pasta_documentos, f))]

    if not file_paths:
        return "Nenhum arquivo encontrado na pasta.", []

    # Criando o dicionário de arquivos
    files = [("files", (os.path.basename(path), open(path, "rb"))) for path in file_paths]

    try:
        # Enviando todos os arquivos de uma vez para a URL fixa
        response = requests.post(URL_API, files=files)
        response_json = response.json()

        # Filtrando os documentos que tiveram resposta "true"
        documentos_true = [nome for nome, resultado in response_json.items() if resultado is True]

        return response.status_code, response_json, documentos_true
    except Exception as e:
        return f"Erro ao enviar documentos: {str(e)}", [], []
    finally:
        # Fechando os arquivos
        for _, file_obj in files:
            file_obj[1].close()


def main():
    # Caminho da pasta com os documentos
    pasta_documentos = r"C:\Users\yan.fontes\Dropbox\PC\Downloads\ImportarDocumento-importar-documento-c6\ImportarDocumento-importar-documento-c6\C6 Importar Documneto\Documentos"

    # Chama o método para enviar os documentos
    status_code, resposta_api, documentos_true = enviarDocumentos(pasta_documentos)

    # Exibindo o resultado
    print(f"Código de status: {status_code}")
    print(f"Resposta da API: {resposta_api}")
    print(f"Documentos com resposta True: {documentos_true}")

# Chamando a função main quando o script for executado
if __name__ == "__main__":
    main()