import os
import base64
import requests
from Adlib.enums import EnumBanco, EnumStatus, EnumProcesso, EnumStatusSolicitacao, Enum, EnumTipoContrato
from requests.exceptions import RequestException, Timeout, ConnectionError

class IdSolicitacaoCriacaoBanco(Enum):
    BMG = 41
    C6 = 42
    DIGIO = 47
    BRADESCO = 47
    ITAU = 44
    VIRTAUS = 46

    @classmethod
    def getEnum(cls, key):
        try:
            return cls[key].value
        except KeyError:
            raise ValueError(f"Chave {key} não encontrada em {cls.__name__}.")


class IdSolicitacaoResetBanco(Enum):
    BMG = 48
    MASTER = 49
    CREDCESTA = 49
    ITAU = 50
    BANRISUL = 51
    FACTA = 52
    CREFISA = 53
    DIGIO = 54
    BRADESCO = 54

    @classmethod
    def getEnum(cls, key):
        try:
            return cls[key].value
        except KeyError:
            raise ValueError(f"Chave {key} não encontrada em {cls.__name__}.")



def putStatusRobo(status: EnumStatus, enumProcesso: EnumProcesso, enumBanco: EnumBanco):
    """
    Envia duas requisições HTTP PUT para atualizar o status de um processo e registrar o horário da atualização.

    Parâmetros:
    ----------
    status : IntegracaoStatus
        Um valor da enumeração `IntegracaoStatus` que representa o status do processo a ser atualizado.
    enumProcesso : int
        Um número inteiro que representa o ID do processo a ser atualizado.
    enumBanco : int
        Um número inteiro que representa o ID do banco a ser atualizado.
    """
    PORTA = 7118
    
    if enumProcesso in [EnumProcesso.INTEGRACAO, EnumProcesso.IMPORTACAO, EnumProcesso.APROVADORES]:
        PORTA = 8443

    horaFeita = f'http://172.16.10.6:{PORTA}/acompanhamentoTotal/horaFeita/{enumProcesso.value}/{enumBanco.value}'
    URLnovaApi = f'http://172.16.10.6:{PORTA}/acompanhamentoTotal/processoAndBancoStatus/{enumProcesso.value}/{enumBanco.value}'

    data = { "status": status.value }
    headers = { "Content-Type": "application/json" }
    try:
        response = requests.put(URLnovaApi, headers=headers, json=data)

    except requests.Timeout:
        print("A requisição expirou. Verifique sua conexão ou o servidor.")
    except ConnectionError:
        print("Erro de conexão. Verifique sua rede ou o servidor.")
    except requests.RequestException as e:
        print(f"Ocorreu um erro ao realizar a requisição: {e}")

    if status == EnumStatus.LIGADO:
        requests.put(horaFeita)

    if response.status_code == 200: 
        pass
        # print("Requisição PUT bem-sucedida!")
        # print("Resposta:", response.json())
    else:
        print(f"Falha na requisição PUT. Código de status: {response.status_code}")
        # print("Resposta:", response.text)


def putSolicitacaoStatus(idSolicitacao: int, enumStatus: EnumStatusSolicitacao, observacao: str = ""):
    data = {
        "enumDetalheSolicitacoesStatus": enumStatus.value,
        "observação": observacao
    }
    headers = {
        "Content-Type": "application/json"
    }

    URLChangeStatus = f'http://172.16.10.6:7118/detalhesSolicitacao/{idSolicitacao}'

    try:
        response = requests.put(URLChangeStatus, headers=headers, json=data)

        if response.status_code == 200:
            # print("Requisição PUT bem-sucedida!")
            requests.put(f'http://172.16.10.6:7118/detalhesSolicitacao/horaFim/{idSolicitacao}', headers=headers, json=data)
        else:
            print(f"Falha na requisição PUT. Código de status: {response.status_code}")
            print("Resposta:", response.text)
    except Timeout:
        print("A requisição expirou. Verifique sua conexão ou o servidor.")
    except ConnectionError:
        print("Erro de conexão. Verifique sua rede ou o servidor.")
    except RequestException as e:
        print(f"Ocorreu um erro ao realizar a requisição: {e}")


def postSolicitacao(enumStatusSolicitacao: EnumStatusSolicitacao, enumProcesso: EnumProcesso, solicitacao: int, enumBanco: EnumBanco) -> int:
    
    mapping =   {
                    EnumProcesso.CRIACAO : IdSolicitacaoCriacaoBanco,
                    EnumProcesso.RESET: IdSolicitacaoResetBanco
                }
    
    idBanco = mapping[enumProcesso].getEnum(enumBanco.name)
    
    data = {
        "enumDetalheSolicitacoesStatus": enumStatusSolicitacao.value,
        "numeroSolicitacao": solicitacao,
        "acompanhamentoDomain": {
            "acompanhamentoId": idBanco
        }
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post("http://172.16.10.6:7118/detalhesSolicitacao/", headers=headers, json=data)

    if response.status_code == 200:
        pass
        # print("Requisição POST bem-sucedida!")
        # print("Resposta:", response.json()) 
    
    else:
        print(f"Falha na requisição POST. Código de status: {response.status_code}")
        # print("Resposta:", response.text)

    dataApi = response.json()
    detalhesSolicitacaoId = dataApi['detalhesSolicitacaoId']

    return detalhesSolicitacaoId


def storeCaptcha(imagePath: str, enumBanco: EnumBanco = EnumBanco.VAZIO, enumProcesso: EnumProcesso = EnumProcesso.IMPORTACAO):

    url = "http://172.16.10.14:5000/storeCaptcha"

    name = os.path.basename(imagePath)
    captcha = name.split("_")[1].split(".")[0]
    processo = enumBanco.name
    banco = enumProcesso.name

    with open(imagePath, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

        document = {
            "nomeArquivo": name,
            "textoCaptcha": captcha,
            "processo": processo,
            "banco": banco,
            "imagem": f"data:image/png;base64,{base64_image}"
        }
    response = requests.post(url, json=document)
    os.remove(imagePath)
    # if response.status_code == 201:
        
        # print(response.json())


def putTicket(solicitacao: str, enumProcesso: EnumProcesso, enumBanco: EnumBanco):
    data = {
        "solicitacao": solicitacao
    }
    headers = {
        "Content-Type": "application/json"
    }

    URLChangeStatus = f'http://172.16.10.6:8443/acompanhamentoTotal/processoAndBancoSolicitacao/{enumProcesso.value}/{enumBanco.value}'

    try:
        response = requests.put(URLChangeStatus, headers=headers, json=data)

        if response.status_code == 200:
            # print("Requisição PUT bem-sucedida!")
            pass
        else:
            print(f"Falha na requisição PUT. Código de status: {response.status_code}")
            print("Resposta:", response.text)
    except Timeout:
        print("A requisição expirou. Verifique sua conexão ou o servidor.")
    except ConnectionError:
        print("Erro de conexão. Verifique sua rede ou o servidor.")
    except RequestException as e:
        print(f"Ocorreu um erro ao realizar a requisição: {e}")


dynamicFunctions = dict()

def createShutdownBotFunctions():
    from itertools import product

    for processo, banco in product(EnumProcesso, EnumBanco):
        func_name = f"desligar{processo.name.title()}{banco.name.title()}"
        
        def func(p=processo, b=banco):
            putStatusRobo(EnumStatus.DESLIGADO, p, b)

        dynamicFunctions[func_name] = func


def postReclamacao(contrato: int, enumBanco: EnumBanco, enumTipoContrato: EnumTipoContrato, observacao: str):
    
    url = "http://172.16.20.105:8080/contratos"

    data = {
        "contrato": contrato,
        "banco": enumBanco.name,
        "tipoContratoEnum": enumTipoContrato.value,
        "observacao": observacao,
        "notificado": False
    }
    headers = {
        "Content-Type": "application/json"
    }

    requests.post(url, headers=headers, json=data)


def putReclamacao(contrato: int):
    
    url = f"http://172.16.20.105:8080/contratos/notificado/{contrato}"

    requests.put(url)


def solveCaptcha(filepath: str) -> str | None:
    url = "http://172.16.20.221:9856/predict"
    try:
        with open(filepath, "rb") as img_file:
            files = {"image": img_file}
            response = requests.post(url, files=files)
        
        if response.status_code == 200:
            return response.json()["prediction"]
        else:
            return {"erro": f"Status {response.status_code}: {response.text}"}
    except Exception as e:
        return {'erro': str(e)}


if __name__=="__main__":
    
    print(solveCaptcha(r"C:\Users\dannilo.costa\Pictures\Imagens\Captchas\1737471966_5ak3.png"))


    # dynamicFunctions["desligarImportacaoNuvideo"]()

    # putStatusRobo(EnumStatus.LIGADO, EnumProcesso.RESET, EnumBanco.DIGIO)
    # putStatusRobo(EnumStatus.LIGADO, EnumProcesso.CRIACAO, EnumBanco.BMG)
    # putStatusRobo(EnumStatus.LIGADO, EnumProcesso.CRIACAO, EnumBanco.C6)
    # postSolicitacao(None, EnumProcesso.CRIACAO, 123345, EnumBanco.BANRISUL)
    # putStatusRobo(EnumStatus.LIGADO, EnumProcesso.IMPORTACAO, EnumBanco.MEU_CASH_CARD)
    # putStatusRobo(EnumStatus.LIGADO, EnumProcesso.RESET, EnumBanco.BANRISUL)
    #postSolicitacao(EnumStatusSolicitacao.EM_ATENDIMENTO, EnumProcesso.RESET, 123456, EnumBanco.DIGIO)
    pass