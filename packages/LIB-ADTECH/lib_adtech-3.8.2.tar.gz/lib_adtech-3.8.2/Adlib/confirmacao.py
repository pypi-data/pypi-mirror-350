import time
from selenium.webdriver import Chrome
from Adlib.api import EnumBanco, EnumStatus, EnumProcesso, putStatusRobo
from Adlib.funcoes import setupDriver, getCredenciais, mensagemTelegram
from Adlib.logins import loginVirtaus


token = '7519811574:AAGayFV_OReR-piS06_7APOgkWg9FZfwPSs'
chatId = '-1002420514126'


def importarArquivos(virtaus: Chrome, enumBanco: EnumBanco, codigoPasta: int, nomeBanco: str, filePathList: list):
    """
        Filtra arquivos na pasta de downloads do usuário e os envia para o sistema Virtaus.

        Parâmetros:
        - virtaus: Chrome - WebDriver do Selenium.
        - enumBanco: EnumBanco
        - codigoPasta: int - Código da pasta do banco no Virtaus (disponível na URL)
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
    
    virtaus.get('https://adpromotora.virtaus.com.br/portal/p/ad/ecmnavigation')
    time.sleep(5)

    try:
        putStatusRobo(EnumStatus.IMPORTANDO, EnumProcesso.CONFIRMACAO_CREDITO, enumBanco)

        virtaus.get(f'https://adpromotora.virtaus.com.br/portal/p/ad/ecmnavigation?app_ecm_navigation_doc={codigoPasta}')
        time.sleep(5)

        qntArquivos = len(filePathList)

        if qntArquivos == 0:
            #putStatusRobo(EnumStatus.SEM_ARQUIVOS, EnumProcesso.CONFIRMACAO_CREDITO, enumBanco)
            mensagem = f"Não haviam documentos para importar! ⚠️ <b>{nomeBanco}</b>"
            mensagemTelegram(token, chatId, mensagem)

        else:
            for i, caminho in enumerate(filePathList, start=1):
                
                # Envia o arquivo usando o elemento XPath
                try:

                    #importarMonitoramento(caminho, enumBanco)

                    # Simula o envio do arquivo
                    importarArquivo = virtaus.find_element('xpath', '//*[@id="ecm-navigation-inputFile-clone"]')
                    importarArquivo.send_keys(caminho)

                    print(f'Arquivo {caminho} enviado com sucesso')
                
                    # Aguarda o upload finalizar
                    time.sleep(10)

                    # Mensagem de sucesso
                    #arquivo = os.path.basename(caminho)
                    #mensagem = f"Arquivo importado: {arquivo} ({i}/{qntArquivos}) ✅"
                    mensagem = f"Arquivo importado: ({i}/{qntArquivos})"
                    mensagemTelegram(token, chatId, mensagem)

                except Exception as e:
                    print(e)
                    print(f"Erro ao processar o arquivo {caminho}: {e}")

            else:
                mensagem = f"Todos os documentos foram integrados com sucesso!\n<b>{nomeBanco}</b> ✅"
                mensagemTelegram(token, chatId, mensagem)
                putStatusRobo(EnumStatus.LIGADO, EnumProcesso.CONFIRMACAO_CREDITO, enumBanco)
                print("Todos os arquivos foram processados.")
    
    except Exception as erro:
        print(erro)
        print('Não deu certo')
        putStatusRobo(EnumStatus.ERRO, EnumProcesso.CONFIRMACAO_CREDITO, enumBanco)


def confirmacaoCredito(driver: Chrome, user: str, senha: str, codigoLoja: str, nomeProduto: str, filePaths: list[str], enumBanco: EnumBanco = None):

    def naoEstaLogado():
        return "https://adpromotora.fluigidentity.com" not in driver.current_url
    
    if naoEstaLogado():
        loginVirtaus(driver, user, senha)
    importarArquivos(driver, enumBanco, codigoLoja, nomeProduto, filePaths)


if __name__ == '__main__':

    virtaus = setupDriver(webdrivePath=r"C:\Users\dannilo.costa\Documents\chromedriver.exe")
    
    userVirtaus, senhaVirtaus = getCredenciais(168)
    usuarioWindows = "dannilo.costa"
    nomeBanco = "Pan"
    codigoPasta = 1836846
    substring = "teste"
    extensao = "pdf"

    loginVirtaus(virtaus, userVirtaus, senhaVirtaus)
    importarArquivos(virtaus, EnumBanco.PAN, codigoPasta, nomeBanco, substring, extensao, usuarioWindows)