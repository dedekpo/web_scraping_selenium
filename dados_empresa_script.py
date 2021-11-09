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

#User request nire
nire_code = input("Entre com o NIRE: ") #35218345517

#Pesquisa com o nire da empresa inserido
input_text = wait.until(presence_of_element_located((By.ID, "ctl00_cphContent_frmBuscaSimples_txtPalavraChave")))
input_text.send_keys(nire_code + Keys.RETURN)

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
    nome = wait.until(presence_of_element_located((By.ID, "ctl00_cphContent_frmPreVisualiza_lblEmpresa"))).text
    tipo_de_empresa = wait.until(presence_of_element_located((By.ID, "ctl00_cphContent_frmPreVisualiza_lblDetalhes"))).text
    inicio_atividade = wait.until(presence_of_element_located((By.ID, "ctl00_cphContent_frmPreVisualiza_lblAtividade"))).text
    cnpj = wait.until(presence_of_element_located((By.ID, "ctl00_cphContent_frmPreVisualiza_lblCnpj"))).text
    nire = wait.until(presence_of_element_located((By.ID, "ctl00_cphContent_frmPreVisualiza_lblNire"))).text
    data_constituicao = wait.until(presence_of_element_located((By.ID, "ctl00_cphContent_frmPreVisualiza_lblConstituicao"))).text
    inscricao_estadual = wait.until(presence_of_element_located((By.ID, "ctl00_cphContent_frmPreVisualiza_lblInscricao"))).text
    objeto = wait.until(presence_of_element_located((By.ID, "ctl00_cphContent_frmPreVisualiza_lblObjeto"))).text
    capital = wait.until(presence_of_element_located((By.ID, "ctl00_cphContent_frmPreVisualiza_lblCapital"))).text
    logradouro = wait.until(presence_of_element_located((By.ID, "ctl00_cphContent_frmPreVisualiza_lblLogradouro"))).text
    numero = wait.until(presence_of_element_located((By.ID, "ctl00_cphContent_frmPreVisualiza_lblNumero"))).text
    bairro = wait.until(presence_of_element_located((By.ID, "ctl00_cphContent_frmPreVisualiza_lblBairro"))).text
    complemento = wait.until(presence_of_element_located((By.ID, "ctl00_cphContent_frmPreVisualiza_lblComplemento"))).text
    municipio = wait.until(presence_of_element_located((By.ID, "ctl00_cphContent_frmPreVisualiza_lblMunicipio"))).text
    cep = wait.until(presence_of_element_located((By.ID, "ctl00_cphContent_frmPreVisualiza_lblCep"))).text
    uf = wait.until(presence_of_element_located((By.ID, "ctl00_cphContent_frmPreVisualiza_lblUf"))).text
except:
    print('Nenhuma empresa encontrada')

else:
    #Transforma em JSON
    dados_empresa = {'nome': nome,'tipo de empresa': tipo_de_empresa,'inicio de atividade': inicio_atividade,'cnpj': cnpj,'nire': nire,'data da constituicao': data_constituicao,'inscricao estadual': inscricao_estadual,'objeto': objeto,'capital': capital,'logradouro': logradouro,'numero': numero,'bairro': bairro,'complemento': complemento,'municipio': municipio,'cep': cep,'uf': uf}
    dados_empresa = json.dumps(dados_empresa)
    print('-----------------Resultado-------------------')
    print(dados_empresa)
    print('---------------------------------------------')
    #Salva arquivo na pasta
    with open('output/dados_empresa_output.json', 'w') as f:
        f.write(dados_empresa)