from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from skimage import io
import json

print('Running...')

#Prepara ambiente de execução
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--headless")

s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=options)
wait = WebDriverWait(driver, 10)

#Site request
driver.get("http://www.institucional.jucesp.sp.gov.br")

#Fecha popup do site
close_button = driver.find_element(By.CLASS_NAME, 'close')
close_button.click()

#Clica no botão de pesquisar empresas
search_button = wait.until(presence_of_element_located((By.LINK_TEXT, 'Pesquisa de empresas no banco de dados da Junta Comercial do Estado de São Paulo.')))
search_button.click()

#User request nome empresa
nome_empresa = input("Entre com o nome da empresa: ")

#Pesquisa com o nome da empresa inserido
input_text = wait.until(presence_of_element_located((By.ID, "ctl00_cphContent_frmBuscaSimples_txtPalavraChave")))
input_text.send_keys(nome_empresa + Keys.RETURN)

#Encontra e salva link da imagem captcha
form = wait.until(presence_of_element_located((By.ID, "formBuscaAvancada")))
link_image_captcha = form.find_element(By.CSS_SELECTOR, "img").get_attribute("src")

#Usa a lib skimage para ler a imagem
imagem_captcha = io.imread(link_image_captcha)
io.imshow(imagem_captcha)
io.show()

#User request captcha
captcha_value = input("Entre com o captcha: ")

#Insere o captcha e pesquisa
input_text = wait.until(presence_of_element_located((By.NAME, "ctl00$cphContent$gdvResultadoBusca$CaptchaControl1")))
input_text.send_keys(captcha_value + Keys.RETURN)

#Tenta encontrar algum resultado, caso não encontrar o programa não faz nada; Se encontrar, salva o resultado em um arquivo json
try:
    #Percorre a tabela procurando pelas informações nas trs
    result_table = wait.until(presence_of_element_located((By.ID,"ctl00_cphContent_gdvResultadoBusca_gdvContent")))
    rows = result_table.find_elements(By.TAG_NAME, "tr")
    #Flag para ignorar o cabeçalho da tabela
    is_header = True
    empresas = []
    for row in rows:
        if(is_header):
            pass
        else:
            #Tratamento das strings para ser formatado em formato de dicionário
            dados_empresa = row.text.split('\n')
            dados_empresa = [x for x in dados_empresa if x]
            empresa = {'Empresa': dados_empresa[1], 'NIRE': int(dados_empresa[0]), 'Municipio': dados_empresa[2]}
            empresas.append(empresa)

        is_header = False
except:
    print('Nenhuma empresa encontrada')
else:
    #Transforma em JSON
    resultado_json = json.dumps(empresas)
    print('-----------------Resultado-------------------')
    print(resultado_json)
    print('---------------------------------------------')
    #Salva arquivo na pasta
    with open('output/empresas_output.json', 'w') as f:
        f.write(resultado_json)