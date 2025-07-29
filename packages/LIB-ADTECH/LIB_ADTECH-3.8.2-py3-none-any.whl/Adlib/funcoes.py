import os
import re
import sys
import time
import msal
import shutil
import requests
import datetime
import platform
import subprocess
from pathlib import Path
from Adlib.api import EnumBanco, EnumProcesso
from Adlib.utils import chatIdMapping, meses
from urllib.parse import parse_qs, urlparse
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder


TOKEN_CAPTCHA = "7505814396:AAFEm1jwG3xwd8N41j_viCCxgZUBT-XhbbY"
CHAT_ID_CAPTCHA = "-4095757991"

# EXCLUDED_METHODS = ["close"]
EXCLUDED_ATTRIBUTES = []
from functools import wraps

class TabDriver:
    """
    A proxy class representing a single tab in a multi-tab Chrome instance.
    Ensures the correct tab is always active before any attribute or method is accessed.
    """
    def __init__(self, driver: Chrome, index: int):
        self.driver = driver
        self.index = index
        self.handle = driver.window_handles[index]

    def __getattribute__(self, name):
        attr = object.__getattribute__(self, name)
        if callable(attr) and not name.startswith("__"):
            @wraps(attr)
            def wrapped(*args, **kwargs):
                self.driver.switch_to.window(self.handle)
                return attr(*args, **kwargs)
            return wrapped
        return attr

    def __getattr__(self, name):
        
        self.autoSwitch()

        attr = getattr(self.driver, name)

        if callable(attr):
            @wraps(attr)
            def wrapped(*args, **kwargs):
                self.autoSwitch()
                return attr(*args, **kwargs)
            return wrapped
        
        return attr

    def autoSwitch(self):
        if self.driver.current_window_handle != self.handle:
            self.driver.switch_to.window(self.handle)

def setupDriver(
    webdriverPath: str = os.path.join(os.path.dirname(__file__), r"webdriver\chromedriver.exe"), 
    numTabs: int = 1,
    options: list[str] = [],
    experimentalOptions: dict[str, any] = dict(),
    autoSwitch: bool = False
) -> list[TabDriver] | Chrome:
    """
    Initializes a single Chrome instance with multiple tabs, then returns a list
    of TabDriver instances—one for each tab.
    """
    if platform.system() == "Linux":
        webdriverPath = os.path.join(os.path.dirname(__file__), r"webdriver\chromedriver")

    chrome_service = ChromeService(executable_path=webdriverPath)
    chrome_service.creation_flags = subprocess.CREATE_NO_WINDOW
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("log-level=3")

    # driver = Chrome(ChromeDriverManager().install())

    for option in options:
        chrome_options.add_argument(option)
    
    chrome_options.add_experimental_option("prefs", experimentalOptions)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    driver = Chrome(service=chrome_service, options=chrome_options)
    driver.maximize_window()

    # Open additional tabs
    for _ in range(numTabs - 1):
        driver.execute_script("window.open('');")

    # Return one TabDriver per tab.
    if autoSwitch:
        return TabDriver(driver, 0) if (numTabs == 1) else (TabDriver(driver, i) for i in range(numTabs))
    
    return driver


def setupDriverLinux(numTabs: int = 1, options: list[str] = [], experimentalOptions: dict[str, any] = {}):
    """
    Inicializa o Chrome no Linux, baixando automaticamente o WebDriver correto.
    """
    chrome_service = ChromeService(ChromeDriverManager().install())

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("log-level=3")

    for option in options:
        chrome_options.add_argument(option)

    chrome_options.add_experimental_option("prefs", experimentalOptions)

    driver = Chrome(service=chrome_service, options=chrome_options)
    driver.maximize_window()

    # Abrir abas adicionais
    for _ in range(numTabs - 1):
        driver.execute_script("window.open('');")

    return [TabDriver(driver, i) for i in range(numTabs)]


def getCredenciais(id: int) -> tuple[str, str] | tuple[None, None]:
    """
    Recupera as credenciais (login e senha) de uma API com base no ID fornecido.

    Esta função faz uma requisição `GET` para uma API REST usando o ID fornecido e tenta recuperar as credenciais de login e senha. Se a requisição for bem-sucedida (status code 200) e os dados estiverem presentes, ela retorna uma tupla contendo o login e a senha. Caso contrário, retorna uma tupla com `None` nos dois valores.

    Args:
        id (int): O ID utilizado para buscar as credenciais na API.

    Returns:
        tuple[str, str] | tuple[None, None]: 
            - Uma tupla contendo `login` e `senha` se a requisição for bem-sucedida e os dados estiverem presentes.
            - Uma tupla `(None, None)` se a requisição falhar ou os dados não estiverem disponíveis.
    """
    url = f"http://172.16.10.6:8080/credenciais/{id}"
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados = resposta.json()
            login = dados.get('login')
            senha = dados.get('senha')
            return login, senha
        return None, None
    except Exception as e:
        print(e)
        print("Não foi possível acessar a API")


def instalarPacote(pacote: str):
    """
    Instala uma biblioteca do python
    Arguments:
        pacote: nome do pacote disponível no PyPI
    """
    subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])
 
 
def getNumeroSolicitacao(virtaus: Chrome):
    time.sleep(5)

    urlAtual = virtaus.current_url
 
    parsed_url = urlparse(urlAtual)
    query_params = parse_qs(parsed_url.query)
 
    if 'app_ecm_workflowview_processInstanceId' in query_params:
        return query_params['app_ecm_workflowview_processInstanceId'][0]
    return None
 

def aguardarAlert(driver: Chrome | TabDriver) -> str:
    if isinstance(driver, TabDriver):
        driver = driver.driver
    try:
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert_text = alert.text
        try:
            alert.accept()
        except:
            alert.dismiss()
        return alert_text
    except:
        return ""


def selectOption(driver: Chrome, selectXpath: str, visibleText: str):
    select = Select(esperarElemento(driver, selectXpath))
    select.select_by_visible_text(visibleText)


def esperarElemento(driver: Chrome | TabDriver, xpath: str, tempo_espera=10, logLevel: int = 0):
    """
    Aguarda o elemento ser renderizado
    Arguments:
        driver: driver do site
        xpath: XPath do elemento
        tempo_espera: Tempo máximo de espera, em segundos
    Returns:
        Elemento
    """
    if isinstance(driver, TabDriver):
        driver = driver.driver
    try:
        return WebDriverWait(driver, tempo_espera).until(EC.visibility_of_element_located(('xpath', xpath)))
    except:
        if logLevel:
            print(f"Elemento não encontrado: {xpath}")
 
 
def esperarElementos(driver: Chrome, xpath: str, tempo_espera=10) -> list[WebElement]:
    """
    Aguarda todos os elementos serem renderizados.
    Arguments:
        driver: driver do site
        xpath: XPath dos elementos
        tempo_espera: Tempo máximo de espera, em segundos
    Returns:
        Lista de elementos
    """
    if isinstance(driver, TabDriver):
        driver = driver.driver
    try:
        return WebDriverWait(driver, tempo_espera).until(EC.presence_of_all_elements_located(('xpath', xpath)))
    except:
        return []
 

def clickarElemento(driver: Chrome, xpath: str, time_wait=10, logLevel: int = 0):
    """
    Retorna o elemento do Xpath de entrada
    Args:
        driver: driver do site
        xpath: XPath do elemento
    Returns:
        Elemento
    """
    if isinstance(driver, TabDriver):
        driver = driver.driver
    try:
        return WebDriverWait(driver, time_wait).until(EC.element_to_be_clickable(('xpath', xpath)))
    except:
        if logLevel:
            print(f"Elemento não encontrado: {xpath}")


def clickElement(driver: Chrome, xpath: str, tempoEspera: int = 20):
    """
        Aguarda o elemento entrar em estado clicável e executa um clique usando Javascript
    """
    if isinstance(driver, TabDriver):
        driver = driver.driver
    driver.execute_script("arguments[0].click();", WebDriverWait(driver, tempoEspera).until(EC.element_to_be_clickable((By.XPATH, xpath))))


def mensagemTelegram(token: str, chat_id: int, mensagem: str):
    """
    Envia uma mensagem pela API do Telegram
    Arguments:
        token: token do bot do Telegram
        chat_id: id do chat
        mensagem: mensagem a ser enviada
    Returns:
        JSON com a resposta da requisição
    """
    mensagem_formatada = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=HTML&text={mensagem}'
    resposta = requests.get(mensagem_formatada)
    return resposta.json()
 
 
       
def esperar_elemento(driver: Chrome, xpath: str, tempo_espera=10):
    
    if isinstance(driver, TabDriver):
        driver = driver.driver
    return WebDriverWait(driver, tempo_espera).until(EC.visibility_of_element_located(('xpath', xpath)))


def aguardarDownload(downloadsFolder: str, substringNomeArquivo: str, checkpoint: float = None, maxWaitTime: int = 60) -> str:
    """
    Aguarda o download de arquivos contendo uma substring específica no nome após um determinado ponto de verificação, se fornecido.

    Args:
        downloadsFolder (str): Caminho do diretório de download.
        substringNomeArquivo (str): Substring que o arquivo baixado deve conter no nome.
        checkpoint (float, optional): Marca de tempo (timestamp) para verificar os arquivos baixados após esse momento. Se não fornecido,
        modificados após a chamada da função serão verificados.
        maxWaitTime (int, optional): Tempo máximo de espera em segundos. O padrão é 60 segundos.
    Returns:
        str: Caminho completo do arquivo baixado, se encontrado.
    """
    if checkpoint is None:
        checkpoint = datetime.datetime.now().timestamp()

    if not os.path.exists(downloadsFolder):
        raise FileNotFoundError(f"A pasta de downloads não foi encontrada: {downloadsFolder}")

    t = 0
    
    while t <= maxWaitTime:
        matchingArquivos = [arquivo for arquivo in os.listdir(downloadsFolder) if substringNomeArquivo in arquivo]
        
        for arquivo in matchingArquivos:
            caminhoArquivo = os.path.join(downloadsFolder, arquivo)
            data_modificacao = os.path.getmtime(caminhoArquivo)
            if (data_modificacao > checkpoint) and not arquivo.endswith(".crdownload") and not arquivo.endswith(".tmp"):
                return caminhoArquivo

        time.sleep(1)
        t += 1



def solveReCaptcha(driver):
    
    from selenium_recaptcha_solver import RecaptchaSolver
    
    ffmpeg_dir = os.path.join(os.path.dirname(__file__), "ffmpeg", "bin")
    ffmpeg_path = os.path.join(ffmpeg_dir, "ffmpeg.exe" if sys.platform == "win32" else "ffmpeg")

    os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ["PATH"]

    solver = RecaptchaSolver(driver=driver)
    recaptcha_iframe = esperarElemento(driver, '//iframe[@title="reCAPTCHA"]')
    solver.click_recaptcha_v2(iframe=recaptcha_iframe)



def enviarCaptcha(imagePath: str | Path, enumBanco: EnumBanco, enumProcesso: EnumProcesso, token: str = TOKEN_CAPTCHA, chatId: str = CHAT_ID_CAPTCHA, tempoEspera: int = 60) -> str:
    """
    Envia uma imagem do captcha para um chat do Telegram e retorna uma resposta no intervalo de tempo.

    Args:
        chat_id (int): ID do chat do Telegram.
        imagePath (str | Path): Caminho da imagem do captcha.
    """

    baseUrl = f'https://api.telegram.org/bot{token}'
    
    chatId = chatIdMapping[enumProcesso]

    formatName = lambda x: (" ".join(c for c in x.split('_'))).upper()

    with open(imagePath, 'rb') as imageFile:
        parametros = {
            "chat_id": chatId,
            "caption": f"Realizar Captcha\n{formatName(enumBanco.name)} {formatName(enumProcesso.name)}"
        }

        files = {
            "photo": imageFile
        }

        resp = requests.post(f"{baseUrl}/sendPhoto", data=parametros, files=files).json()
        messageId = resp["result"]["message_id"]
        messageTimestamp = resp["result"].get("date", 0) - 5
    
    baseUrl = f"https://api.telegram.org/bot{token}"
    offset = 0
    tempoInicial = time.time()

    while (time.time() - tempoInicial) < tempoEspera:
        response = requests.get(
            f"{baseUrl}/getUpdates",
            params={"timeout": 20, "offset": offset},
            timeout=25
        )
        
        updates = response.json().get("result", [])
        
        for update in updates:
            offset = update["update_id"] + 1
            msg = update.get("message")
            
            if msg and msg.get("reply_to_message", {}).get("message_id") == messageId:
                if msg.get("date", 0) > messageTimestamp:
                    return msg["text"]

    return "123456"


def saveCaptchaImage(imgElement: WebElement, enumBanco: EnumBanco, enumProcesso: EnumProcesso):

    imgFolderPath = os.getcwd()
    imgName = f"Token_{enumBanco.name}_{enumProcesso.name}.png"
    
    imgPath = os.path.join(imgFolderPath, imgName)

    imgElement.screenshot(imgName)

    return imgPath


def clickCoordenada(driver: Chrome, x: int, y: int) -> None:
    """
    Clica em uma coordenada específica na tela.
    Args:
        driver: driver do site
        x: coordenada x
        y: coordenada y
    """

    action = ActionBuilder(driver)
    action.pointer_action.move_to_location(x, y)
    action.pointer_action.click()
    action.perform()
    

def rightClick(driver: Chrome, xpath: str):
    
    element = esperarElemento(driver, xpath)
    actions = ActionChains(driver)
    actions.context_click(element).perform()
    

def moveToElement(driver: Chrome, xpath: str):
    """
    Moves the mouse to the position where the element is located.

    Args:
        driver: The Chrome WebDriver instance.
        xpath: The XPath of the element to move to.
    """
    element = esperarElemento(driver, xpath)
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()


def importarPastaMonitoramento(filePathList: list[str], diretorioBase: str, data: datetime.datetime = None):
    try:
        if data:
            hoje = data
        else:
            hoje = datetime.datetime.now()
        pastaAno = str(hoje.year)
        pastaMes = f"{hoje.month:02d} - {meses[hoje.month]}"
        pastaDia = f"{hoje.day:02d}"
    
        caminho = os.path.join(diretorioBase, pastaAno, pastaMes, pastaDia)

        os.makedirs(caminho, exist_ok=True)

        for filePath in filePathList:
            
            nomeArquivo = os.path.basename(filePath)
            destino = os.path.join(caminho, nomeArquivo)

            shutil.copy(filePath, destino)
            os.remove(filePath)

        return caminho
    
    except Exception as e:
        print(e)


def coletarEmailEspecifico(email):
    CLIENT_ID = "d45fc956-3ea0-4c51-93be-c1ac46502c0d"
    CLIENT_SECRET = "oDm8Q~Wi2fH0fgc5xBqStZvBeAoDoKCwHjYyHbH0"
    TENANT_ID = "adaa0a29-8e4a-4216-8ac8-187b1608c2e1"
    USER_ID = email 
    AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
    SCOPES = ["https://graph.microsoft.com/.default"]  # Escopo adequado para client credentials

    # Configuração do fluxo de autenticação
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )

    # Solicitando o token com o client_credentials flow
    result = app.acquire_token_for_client(scopes=SCOPES)

    if "access_token" in result:
        print("Token obtido com sucesso!")
        access_token = result["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Passo 1: Acessar as mensagens sem filtro ou ordenação
        messages_url = f"https://graph.microsoft.com/v1.0/users/{USER_ID}/messages?$top=20"  # Recupera os 20 e-mails mais recentes
        
        # Recuperando as mensagens
        messages_response = requests.get(messages_url, headers=headers)
        
        if messages_response.status_code == 200:
            result_data = messages_response.json()
            messages = result_data.get("value", [])
            
            # Filtrando as mensagens pelo assunto e ordenando pelo recebimento
            filtered_messages = [
                msg for msg in messages
                if "BemWeb - Pin Autenticação" in msg['subject']
            ]
            sorted_messages = sorted(filtered_messages, key=lambda x: x['receivedDateTime'], reverse=True)

            if sorted_messages:
                email = sorted_messages[0]  # Pegando o primeiro e-mail após a ordenação
                subject = email['subject']
                sender = email['from']['emailAddress']['address']
                print(f"Assunto: {subject}")
                print(f"De: {sender}")
                
                # Extraindo o corpo do e-mail
                email_body = email['body']['content']
                print(f"Corpo do e-mail: {email_body}\n")
                
                # Usando regex para extrair o PIN
                pin_match = re.search(r"seguida:<br><br><b>(\d+)</b>", email_body)
                if pin_match:
                    pin = pin_match.group(1)  # O número encontrado
                    print(f"PIN encontrado: {pin}")
                    return pin


def dataEscolha(days: int, formato: str = '%d/%m/%Y') -> str:
    return (datetime.datetime.today() - datetime.timedelta(days=days)).strftime(formato)


def horaFinalizacao(hora=18, minuto=0):
    """
    Retorna True se já passou do horário especificado. 
    Default: 18:00
    """
    agora = datetime.datetime.now()
    horario_limite = agora.replace(hour=hora, minute=minuto)
    return agora >= horario_limite



def coletarEmail(
    user_email: str,
    subject_filter: str = None,
    content_regex: str = None, # This will now return the re.Match object(s)
    top_n_messages: int = 20,
    from_email_filter: str = None,
    received_after: datetime.datetime = None
) -> list[tuple[str, ...]] | list[str] | None: # Changed return type to list of tuples, list of strings or None
    """
    Coleta informações de e-mails específicos de uma caixa de entrada do Microsoft Graph.

    Args:
        user_email (str): O endereço de e-mail do usuário cuja caixa de entrada será acessada.
        subject_filter (str, optional): String para filtrar o assunto do e-mail (case-sensitive).
                                        Se None, não filtra por assunto.
        content_regex (str, optional): Expressão regular para extrair valores do corpo do e-mail.
                                       Se None, não tenta extrair e returns None.
        top_n_messages (int, optional): O número máximo de e-mails recentes a serem buscados. Padrão para 20.
        from_email_filter (str, optional): Filtra e-mails de um remetente específico. Se None, não filtra por remetente.
        received_after (datetime.datetime, optional): Filtra e-mails recebidos após esta data/hora.
                                                    Opcional. Deve ser um objeto datetime.datetime (UTC).

    Returns:
        list[tuple[str, ...]] | list[str] | None: A list of tuples (if regex has capturing groups) or a list of strings (if no capturing groups), or None if no match or error.
    """
    CLIENT_ID = "d45fc956-3ea0-4c51-93be-c1ac46502c0d"
    CLIENT_SECRET = "oDm8Q~Wi2fH0fgc5xBqStZvBeAoDoKCwHjYyHbH0"
    TENANT_ID = "adaa0a29-8e4a-4216-8ac8-187b1608c2e1"
    USER_ID = user_email 
    AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
    SCOPES = ["https://graph.microsoft.com/.default"]  # Escopo adequado para client credentials

    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )

    result = app.acquire_token_for_client(scopes=SCOPES)

    if "access_token" in result:
        access_token = result["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        messages_url = f"https://graph.microsoft.com/v1.0/users/{USER_ID}/messages?$top={top_n_messages}"

        try:
            messages_response = requests.get(messages_url, headers=headers)
            messages_response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
            result_data = messages_response.json()
            messages = result_data.get("value", [])

            filtered_messages = []
            for msg in messages:
                # Filtrar por assunto
                if subject_filter and subject_filter not in msg.get('subject', ''):
                    continue

                # Filtrar por remetente
                sender_address = msg.get('from', {}).get('emailAddress', {}).get('address', '')
                if from_email_filter and from_email_filter.lower() != sender_address.lower():
                    continue

                # Filtrar por data de recebimento
                if received_after:
                    received_date_str = msg.get('receivedDateTime')
                    if received_date_str:
                        try:
                            # Parse to timezone-aware datetime object (assuming Graph returns UTC)
                            # Use datetime.fromisoformat for Python 3.7+
                            received_date_obj = datetime.datetime.fromisoformat(received_date_str.replace('Z', '+00:00'))
                            if received_date_obj < received_after:
                                continue
                        except ValueError as e:
                            print(f"Warning: Could not parse receivedDateTime '{received_date_str}': {e}")
                            continue

                filtered_messages.append(msg)

            sorted_messages = sorted(filtered_messages, key=lambda x: x.get('receivedDateTime', ''), reverse=True)

            if sorted_messages:
                email_body = sorted_messages[0].get('body', {}).get('content', '')

                if content_regex:
                    # Find all non-overlapping matches for the regex
                    matches = re.finditer(content_regex, email_body)
                    extracted_data = []
                    for match in matches:
                        if match.groups(): # If there are capturing groups, return them
                            extracted_data.append(match.groups())
                        else: # If no capturing groups, return the whole match
                            extracted_data.append(match.group(0))

                    if not extracted_data:
                        print(f"Nenhum valor correspondente ao regex '{content_regex}' encontrado no corpo do e-mail.")
                        return None
                    else:
                        return extracted_data
                else:
                    return None
            else:
                print("Nenhum e-mail correspondente aos critérios de filtro foi encontrado.")
                return None
        except requests.exceptions.HTTPError as e:
            print(f"Erro HTTP ao acessar as mensagens: {e.response.status_code} - {e.response.text}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Erro de requisição ao acessar as mensagens: {e}")
            return None
    else:
        print(f"Erro ao obter o token: {result.get('error_description', result.get('error'))}")
        return None


if __name__=="__main__":
    
    email = "dannilo.costa@adpromotora.com.br"

    pin_data = coletarEmail(
        user_email=email,
        subject_filter="BemWeb - Pin Autenticação",
        content_regex=r"seguida:<br><br><b>(\d+)</b>"
    )
    print(pin_data)

    # while True:
    #     swagger, google = setupDriver(numTabs=2, autoSwitch=True)
        
    #     swagger.get("http://172.16.10.6:8080/swagger-ui/index.html#/credenciais-controller/getCredenciaisById")
    #     google.get("https://www.google.com.br/?hl=pt-BR")
        
    #     del swagger

    #     swagger: Chrome = TabDriver(google.driver, 0)
    #     print(swagger.title)
    #     searchbar = swagger.find_element('xpath', '//*[@id="swagger-ui"]/section/div[1]/div/div/form/input')
    #     searchbar.clear()
    #     searchbar.send_keys("I've found it")
    #     input("....")

    #     swagger.quit()

    #     input("....")