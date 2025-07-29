import os
import time
import datetime
import threading
from typing import Callable
from selenium.webdriver import Chrome
from selenium.common.exceptions import TimeoutException
from Adlib.api import EnumBanco, EnumStatus, EnumProcesso, putStatusRobo
from Adlib.funcoes import setupDriver, esperarElemento, esperarElementos, clickarElemento, selectOption
from Adlib.logins import loginVirtaus


def resetarTempoSessaoBMG(bmg: Chrome):
        bmg.switch_to.default_content()
        bmg.switch_to.frame("leftFrame")
        bmg.execute_script("document.getElementById('leftFrame').contentWindow.location.reload();")
        print('Refresh BMG com sucesso')
        time.sleep(10)


def resetarTempoSessaoC6(c6: Chrome):
    primeiroLinkToken = c6.current_url
    tokenc6 = primeiroLinkToken.split('=')[-1]
    print(tokenc6)
    time.sleep(5)
    linkGetEtapa = f'https://c6.c6consig.com.br/WebAutorizador/MenuWeb/Consulta/GeDoc/UI.CnAnexarDocumentacao.aspx?FISession={tokenc6}'
    time.sleep(5)


def resetarTempoSessaoFacta(facta: Chrome):
    facta.get('https://desenv.facta.com.br/sistemaNovo/andamentoPropostas.php')


class FiltrosSolicitacao:

    AGUARDANDO_AVERBACAO = "Aguardando Averbação | AnaliseAverbacao"
    AGUARDANDO_SENHA_BANCO = "Aguardando Senha do Banco | EmissaoDeNovaSenhaLoginExterno"
    AGUARDANDO_TERCEIROS = "Aguardando Terceiros | Notificacao Pagamento Devolvido"
    ANALISA_RECLAMACAO = "Analisa Reclamacao | Criacao de Eventos Reclamacao"
    ANALISAR_CONTRATO_NO_BANCO = "AnalisarContratoNoBanco | AnaliseDaMonitoria"
    ANALISE = "Analise | AnaliseAverbacao"
    ATENDE_AGUARDANDO_TERCEIROS = "Atende Aguardando Terceiros | Criacao de Eventos Reclamacao"
    ATENDIMENTO_ALTERACAO_STATUS_LOGIN = "Atendimento | AlteracaoDoStatusDeLogin"
    CRIACAO = "Atendimento | CriacaoDeLoginExternoParaParceiro"
    RESET = "Atendimento | EmissaoDeNovaSenhaLoginExterno"
    ATENDIMENTO_EMISSAO_NOVA_SENHA_FUNCIONARIO = "Atendimento | EmissaoDeNovaSenhaLoginExternoFuncionario"
    LIBERAR_PROPOSTA = "Liberar Proposta"
    AGUARDANDO_VIDEOCHAMADA = "Aguardando Videochamada | AnaliseDeEsteira"
    COLETAR_DOCUMENTOS = "Analisar Documentos"


mapping = {
    FiltrosSolicitacao.CRIACAO : EnumProcesso.CRIACAO,
    FiltrosSolicitacao.RESET : EnumProcesso.RESET,
    FiltrosSolicitacao.COLETAR_DOCUMENTOS : EnumProcesso.ANALISE_DOCUMENTOS, 
}


def assumirSolicitacao(virtaus: Chrome, nomeFerramenta: str, enumBanco: EnumBanco, tipoFiltro: FiltrosSolicitacao, localizacao: str = None, 
                       HORA_FINALIZACAO: str = 19, resetSessao: Callable[[Chrome], None] = None, driverReset: Chrome = None, resetEvent: threading.Event = None):
    """
        Função para assumir uma solicitação no sistema Virtaus com base em filtros específicos e nome da ferramenta.

        Esta função realiza o seguinte fluxo:
        - Navega para a página de tarefas centralizadas no sistema Virtaus.
        - Seleciona um filtro específico fornecido no parâmetro `tipoFiltro`.
        - Busca pelo nome da ferramenta no campo de pesquisa.
        - Seleciona o primeiro item correspondente à ferramenta.
        - Clica no botão "Assumir Tarefa" para iniciar o processamento.

        Parâmetros:
        - virtaus (Chrome): Instância do navegador Chrome controlada pelo Selenium.
        - nomeFerramenta (str): Nome da ferramenta para buscar nas solicitações.
        - enumBanco (EnumBanco): Enumeração que identifica o banco associado à solicitação.
        - tipoFiltro (FiltrosSolicitacao): Filtro a ser utilizado para categorizar as solicitações.
        - HORA_FINALIZACAO (str): Horário limite para finalizar a execução da função (padrão: "19:00").

        Exceções:
        - A função trata exceções durante a execução, exibindo mensagens informativas e aguardando para novas tentativas.
    """

    enumProcesso = mapping[tipoFiltro]
    
    putStatusRobo(EnumStatus.LIGADO, enumProcesso, enumBanco)

    while True:
        try:
            virtaus.get("https://adpromotora.virtaus.com.br/portal/p/ad/pagecentraltask")
            qntBotoes = len(esperarElementos(virtaus, '//*[@id="centralTaskMenu"]/li'))
            idxBtn = qntBotoes - 1
            
            clickarElemento(virtaus, f'//*[@id="centralTaskMenu"]/li[{idxBtn}]/a').click()

            # Seleciona o filtro de "Emissão De Nova Senha Login Externo"
            try:
                clickarElemento(virtaus, f'//*[@id="centralTaskMenu"]/li[{idxBtn}]/ul//a[contains(text(), "{tipoFiltro}")]').click()
            except:
                pass

            time.sleep(5)

            # Busca pelo nome da ferramenta
            esperarElemento(virtaus, '//*[@id="inputSearchFilter"]').send_keys(nomeFerramenta)
            
            time.sleep(5)

            if not localizacao:
                localizacao = nomeFerramenta

            # Clica no primeira item da lista de solicitações
            clickarElemento(virtaus, f'//td[@title="{localizacao}"]').click()
            break

        except Exception as e:
            hora = datetime.datetime.now()
            print(f"Não há solicitações do banco {nomeFerramenta.title()} no momento {hora.strftime('%H:%M')}")

            if HORA_FINALIZACAO < hora.hour:
                virtaus.quit()
                
                if driverReset:
                    driverReset.quit()

                putStatusRobo(EnumStatus.DESLIGADO, enumProcesso, enumBanco)
                os._exit(0)

            time.sleep(20)
                
            if resetSessao and driverReset:
                resetSessao(driverReset)

        except KeyboardInterrupt:
            putStatusRobo(EnumStatus.DESLIGADO, enumProcesso, enumBanco)
            break
        
        finally:
            if resetEvent:
                resetEvent.set()      # Reseta countdown de restart do bot
    try:
        print("Assumindo Tarefa")
        # Clica em Assumir Tarefa e vai para o menu de Cadastro de usuário
        clickarElemento(virtaus, '//*[@id="workflowActions"]/button[1]').click()
    
    except:
        print("Erro ao assumir tarefa")


def finalizarSolicitacao(virtaus: Chrome,  senha: str | None = None, usuario: str | None = None, codigoLoja: int | None = None, status: str = 'Finalizado com Sucesso'):

    try:

        virtaus.switch_to.default_content()

        menuFrame = esperarElemento(virtaus, '//*[@id="workflowView-cardViewer"]')
        virtaus.switch_to.frame(menuFrame)
 
        if usuario:
            elementoUsuario = esperarElemento(virtaus, '//*[@id="nomeLogin"]')
            if elementoUsuario:
                elementoUsuario.send_keys(usuario)
 
        if senha:
            elementoSenha = esperarElemento(virtaus, '//*[@id="senhaLogin"]')
            if elementoSenha:
                elementoSenha.clear()
                elementoSenha.send_keys(senha)
 
        if codigoLoja:
            elementoCodigoLoja = esperarElemento(virtaus, '//*[@id="groupCodigoDeLoja"]/span/span[1]/span/ul/li/input')
            if elementoCodigoLoja:
                elementoCodigoLoja.send_keys(codigoLoja)
                esperarElemento(virtaus, '//*[@id="select2-codigoDeLojaId-results"]/li[2]').click()
       
        try:
            esperarElemento(virtaus, '//*[@id="abaDadosGerais"]/div[4]/div[2]/div/div/div[3]/span/div/button').click()
            esperarElemento(virtaus, '//*[@id="abaDadosGerais"]/div[4]/div[2]/div/div/div[3]/span/div/ul/li[2]/a/label/input').click()
        except Exception as erro:
            pass
            #print('Não precisou escolher Tipo de Analise', erro)

        time.sleep(5)

        virtaus.switch_to.default_content()
        esperarElemento(virtaus, '//*[@id="send-process-button"]').click()

        selectOption(virtaus, '//*[@id="nextActivity"]', status)

        esperarElemento(virtaus, '//*[@id="moviment-button"]').click()
        time.sleep(5)

    except TimeoutException as e:
        print(f"Erro ao localizar elemento: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


if __name__=="__main__":
    
    userVirtaus, senhaVirtaus = "dannilo.costa@adpromotora.com.br", "Costa@36"
    
    driver = setupDriver(r"C:\Users\dannilo.costa\documents\chromedriver.exe")
    
    loginVirtaus(driver, userVirtaus, senhaVirtaus)

    assumirSolicitacao(driver, "BMG CONSIG", EnumBanco.CREFISA, FiltrosSolicitacao.RESET)