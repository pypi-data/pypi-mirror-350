import os
import time
import shutil
import datetime
from Adlib.funcoes import mensagemTelegram, setupDriver
from Adlib.logins import loginVirtaus
from Adlib.utils import meses
from Adlib.api import EnumBanco, EnumProcesso, putStatusRobo, EnumStatus

global NUM_TABS

baseFolderMapping = {
    EnumBanco.VAZIO: 0,
    EnumBanco.PAN: r"Z:\Arquivos de Integração\02 - Pan",
    EnumBanco.OLE: r"Z:\Arquivos de Integração\05 - Bonsucesso",
    EnumBanco.MEU_CASH_CARD: "Meu CashCard",
    EnumBanco.BMG: r"Z:\Arquivos de Integração\04 - BMG",
    EnumBanco.DIGIO: r"Z:\Arquivos de Integração\29 - Digio",
    EnumBanco.BANRISUL: "Banrisul",
    EnumBanco.BANCO_DO_BRASIL: "Banco do Brasil",
    EnumBanco.C6: r"Z:\Arquivos de Integração\08 - C6 Bank",
    EnumBanco.ITAU: r"Z:\Arquivos de Integração\03 - Itau",
    EnumBanco.MASTER: r"Z:\Arquivos de Integração\21 - Master_Consig_e_FGTS",
    EnumBanco.PAULISTA: r"Z:\Arquivos de Integração\23 - Paulista",
    EnumBanco.CREFAZ: r"Z:\Arquivos de Integração\15 - Crefaz",
    EnumBanco.CCB: 13,
    EnumBanco.DAYCOVAL: r"Z:\Arquivos de Integração\07 - Daycoval",
    EnumBanco.ICRED: 15,
    EnumBanco.HAPPY_AMIGOZ: 16,
    EnumBanco.SAFRA: r"Z:\Arquivos de Integração\18 - Safra",
    EnumBanco.SANTANDER: 18,
    EnumBanco.CREFISA: 20,
    EnumBanco.FACTA: r"Z:\Arquivos de Integração\12 - Facta",
    EnumBanco.SABEMI: r"Z:\Arquivos de Integração\13 - Sabemi",
    EnumBanco.FUTURO_PREVIDENCIA: 23,
    EnumBanco.CREFISA_CP: 24,
    EnumBanco.PAN_CARTAO: 25,
    EnumBanco.PAN_PORT: 26,
    EnumBanco.HAPPY_PORT: 27,
    EnumBanco.NUVIDEO: 28,
    EnumBanco.PROMOBANK: 29,
    EnumBanco.GETDOC: 31,
}


def importarMonitoramento(filePath: str, enumBanco: EnumBanco, data: datetime.datetime = None):

    diretorioBase = baseFolderMapping[enumBanco] #os.path.join(filePath, )
    hoje = datetime.datetime.now()
    
    if data:
        hoje = data
    
    pastaAno = str(hoje.year)
    pastaMes = f"{hoje.month:02d} - {meses[hoje.month]}" # 01 - Janeiro
    pastaDia = f"{hoje.day:02d}"

    caminho = os.path.join(diretorioBase, pastaAno, pastaMes, pastaDia)

    os.makedirs(caminho, exist_ok=True)

    nomeArquivo = os.path.basename(filePath)

    destino = os.path.join(caminho, nomeArquivo)

    shutil.copy(filePath, destino)

    print(f"Arquivo salvo na pasta de monitoramento: {destino}")

    return destino


def importarArquivos(virtaus, enumBanco: EnumBanco, codigoBanco: int, nomeBanco: str, filepaths: list):
    """
        Filtra arquivos na pasta de downloads do usuário e os envia para o sistema Virtaus.

        Parâmetros:
        - virtaus: webdriver.Chrome - WebDriver do Selenium.
        - enumBanco: EnumBanco
        - codigoBanco: int - Código do banco no Virtaus (disponível na URL de integração do banco)
        - nomeBanco: str - Nome descritivo do banco (usado para gerar mensagens de feedback).
        - substring: str - Substring para filtrar os arquivos na pasta de downloads.
        - formatoArquivo: str - Extensão dos arquivos a serem filtrados (por exemplo, 'pdf').
        - usuarioWindows: str - Nome de usuário do sistema Windows (usado para localizar a pasta de downloads).

        Fluxo:
        1. Acessa a URL específica do banco no sistema Virtaus.
        2. Filtra os arquivos na pasta de downloads com base na substring e na extensão fornecida.
        3. Faz o upload de cada arquivo filtrado para o sistema Virtaus.
        4. Remove o arquivo da pasta de downloads após o upload bem-sucedido.
        5. Exibe uma mensagem de sucesso ou erro no console.
    """
    token = '7506259919:AAEpbbkg5Xu7YXK0T8IVM76LM23pzIvt6wY'
    chatId = '-4579971115'

    virtaus.get('https://adpromotora.virtaus.com.br/portal/p/ad/ecmnavigation')
    time.sleep(5)

    try:
        putStatusRobo(EnumStatus.IMPORTANDO, EnumProcesso.INTEGRACAO, enumBanco)

        virtaus.get(f'https://adpromotora.virtaus.com.br/portal/p/ad/ecmnavigation?app_ecm_navigation_doc={codigoBanco}')
        time.sleep(5)
        
        qntArquivos = len(filepaths)

        if qntArquivos == 0:
            putStatusRobo(EnumStatus.SEM_ARQUIVOS, EnumProcesso.INTEGRACAO, enumBanco)
            mensagem = f"Não haviam documentos para integrar! ⚠️ <b>{nomeBanco}</b>"
            mensagemTelegram(token, chatId, mensagem)

        else:
            for i, filepath in enumerate(filepaths, start=1):
                try:
                    importarMonitoramento(filepath, enumBanco)

                    # Simula o envio do arquivo
                    importarArquivo = virtaus.find_element('xpath', '//*[@id="ecm-navigation-inputFile-clone"]')
                    importarArquivo.send_keys(filepath)

                    print(f'Arquivo {filepath} enviado com sucesso')
                
                    time.sleep(10)

                    os.remove(filepath)
                    print(f'Arquivo {filepath} removido da pasta de downloads')

                    # Mensagem de sucesso
                    mensagem = f"Documento integrado!  <b>{nomeBanco}</b> \nDocumentos importados: {i}/{qntArquivos}"
                    mensagemTelegram(token, chatId, mensagem)

                except Exception as e:
                    print(e)
                    print(f"Erro ao processar o arquivo {filepath}: {e}")

            else:
                mensagem = f"Todos os documentos foram integrados com sucesso!\n<b>{nomeBanco}</b> ✅"
                mensagemTelegram(token, chatId, mensagem)
                putStatusRobo(EnumStatus.LIGADO, EnumProcesso.INTEGRACAO, enumBanco)
                print("Todos os arquivos foram processados.")
    
    except Exception as erro:
        print(erro)
        print('Não deu certo')
        putStatusRobo(EnumStatus.ERRO, EnumProcesso.INTEGRACAO, enumBanco)


def integracaoVirtaus(driver, usuario: str, senha: str, enumBanco: EnumBanco, codigoBanco: int, nomeBanco: str, filepaths: list):
    """
        Função principal que coordena a automação de login e importação de arquivos para o Virtaus.

        Parâmetros:
        - driver: webdriver.Chrome - WebDriver do Selenium
        - usuario: str - Nome de usuário para o login no Virtaus.
        - senha: str - Senha para o login no Virtaus.
        - codigoBanco: int - Código do banco no Virtaus (disponível na URL de integração do banco)
        - nomeBanco: str - Nome do banco para gerar mensagens de log e feedback.
        - substring: str - Substring usada para filtrar os arquivos na pasta de downloads.
        - formatoArquivo: str - Extensão dos arquivos a serem filtrados (por exemplo, 'xlsx', 'csv').
        - usuarioWindows: str - Nome de usuário no Windows para acessar a pasta de downloads (por exemplo, 'yan.fontes').

        Fluxo:
        1. Realiza o login no sistema Virtaus usando a função loginVirtaus.
        2. Filtra e envia arquivos da pasta de downloads para o sistema Virtaus utilizando a função importarArquivos.
    """

    driver.execute_script("window.open('');")
    NUM_TABS = len(driver.window_handles) - 1
    driver.switch_to.window(driver.window_handles[NUM_TABS])
    
    loginVirtaus(driver, usuario, senha)
    importarArquivos(driver, enumBanco, codigoBanco, nomeBanco, filepaths)


if __name__=="__main__":

    driver = setupDriver()

    nomeBanco = "Paulista"
    codigoBanco = 2865957
    userVirtaus = "dannilo.costa@adpromotora.com.br"
    senhaVirtaus = "Costa@36"
    substringNomeArquivo = "FE361338-299B-429B-8F57-79B0AA2D872A"
    formatoArquivo = "xlsx"
    usuarioWindows = "dannilo.costa"

    integracaoVirtaus(driver, userVirtaus, senhaVirtaus, EnumBanco.PAULISTA, codigoBanco, nomeBanco, [])