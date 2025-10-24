from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import chromedriver_autoinstaller

def setup():
    chromedriver_autoinstaller.install()
    # Configurações do Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")   # inicia maximizado
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--incognito")     
    driver = webdriver.Chrome(options=options)
    return driver


# Busca --- Pesquisar por nome de um produto e ter retornos em tela (nome pesquisado == nome de produtos em tela) 
def teste_busca():
    driver = setup()
    driver.get("https://www.amazon.com.br/")
    wait = WebDriverWait(driver, 30)

    produto_pesquisado = 'alqsnasnoqanqsojasjojoj'

    # Pesquisa o produto
    wait.until(EC.visibility_of_element_located((By.ID, "twotabsearchtextbox"))).send_keys(produto_pesquisado)
    wait.until(EC.element_to_be_clickable((By.ID, "nav-search-submit-button"))).click()

    # Espera os resultados ou a mensagem de "nenhum resultado"
    try:
        h2_elements = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "h2")))
    except TimeoutException:
        h2_elements = []

    # Verifica se há produtos compatíveis
    produto_encontrado = any(produto_pesquisado.strip().lower() in h2.text.lower() for h2 in h2_elements)

    # Tenta localizar a mensagem de "Nenhum resultado"
    try:
        sem_produto = driver.find_element(
            By.XPATH, "//span[contains(text(), 'Nenhum resultado para sua consulta de pesquisa')]"
        )
        sem_produto_visivel = sem_produto.is_displayed()
    except:
        sem_produto_visivel = False

    if produto_encontrado:
        print("✅ Encontrou produtos relacionados à pesquisa")
    elif sem_produto_visivel:
        print("✅ Informa corretamente que não há resultados para a pesquisa")
    else:
        print("❌ O sistema não funcionou conforme esperado")

    driver.quit()


# Busca --- ordenar itens de resultado pelos mais vendidos ou qualquer ordenador (verificar se tem resultados) 
def teste_busca_ordenada():
    driver = setup()
    driver.get("https://www.amazon.com.br/")
    wait = WebDriverWait(driver, 30)

    produto_pesquisado = 'Smart Tv'

    # Pesquisa o produto
    wait.until(EC.visibility_of_element_located((By.ID, "twotabsearchtextbox"))).send_keys(produto_pesquisado)
    wait.until(EC.element_to_be_clickable((By.ID, "nav-search-submit-button"))).click()

    botao_dropdown = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "span.a-button-text.a-declarative"))
)
    botao_dropdown.click()
    mais_vendidos = wait.until(
    EC.element_to_be_clickable((By.ID, "s-result-sort-select_5"))
    )
    mais_vendidos.click()

    try:
        h2_elements = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "h2")))
    except TimeoutException:
        h2_elements = []

    # Verifica se há produtos compatíveis
    produto_encontrado = any(produto_pesquisado.strip().lower() in h2.text.lower() for h2 in h2_elements)

    if produto_encontrado:
        print("✅ Encontrou produtos relacionados à pesquisa")
    else:
        print("❌ O sistema não funcionou conforme esperado")

    driver.quit()

# Busca --- verificar se o item entrou dentro do carrinho (se subiu o numero no canto)
def teste_adicionar_carrinho():
    driver = setup()
    driver.get("https://www.amazon.com.br/")
    wait = WebDriverWait(driver, 30)

    produto_pesquisado = 'Smart Tv'

    # Pesquisa o produto
    wait.until(EC.visibility_of_element_located((By.ID, "twotabsearchtextbox"))).send_keys(produto_pesquisado)
    wait.until(EC.element_to_be_clickable((By.ID, "nav-search-submit-button"))).click()

    valor_antigo_carrinho = wait.until(
        EC.visibility_of_element_located((By.ID, "nav-cart-count"))
    ).text

    # Clica no primeiro botão de add ao carrinho 
    adicionar_ao_carrinho = wait.until(
        EC.element_to_be_clickable((By.NAME, "submit.addToCart"))
    )
    adicionar_ao_carrinho.click()

    # espera até o valor do carrinho mudar (ou 10 segundos)
    WebDriverWait(driver, 10).until(
        lambda d: d.find_element(By.ID, "nav-cart-count").text.strip() != valor_antigo_carrinho
    )

    valor_novo_carrinho = wait.until(
        EC.visibility_of_element_located((By.ID, "nav-cart-count"))
    ).text


    print(f"Valor antigo carrinho: {int(valor_antigo_carrinho)} | Valor novo carrinho: {int(valor_novo_carrinho)}")


    if int(valor_novo_carrinho) == int(valor_antigo_carrinho) + 1:
        print("✅ Acrescentou o número de produtos no carrinho")
    else:
        print("❌ O sistema não funcionou conforme esperado")

    driver.quit()

# Produto - Clicar em um produto e abrir a página dele com imagem, descrição, preço e avaliações
def teste_clicar_produto():
    driver = setup()
    driver.get("https://www.amazon.com.br/")
    wait = WebDriverWait(driver, 30)

    produto_pesquisado = 'Smart Tv'

    # Pesquisa o produto
    wait.until(EC.visibility_of_element_located((By.ID, "twotabsearchtextbox"))).send_keys(produto_pesquisado)
    wait.until(EC.element_to_be_clickable((By.ID, "nav-search-submit-button"))).click()

    # Espera o primeiro título de produto aparecer
    primeiro_produto = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "h2.a-size-base-plus.a-spacing-none.a-color-base.a-text-normal"
        ))
    )

    # Clica no link dentro do título
    primeiro_produto.click()

    # Mapeamento dos elementos a verificar
    elementos = {
        "imagem": (By.ID, "landingImage"),
        "titulo": (By.ID, "productTitle"),
        "preco": (By.CSS_SELECTOR, "span.a-price-whole"),
        "avaliacao": (By.ID, "averageCustomerReviews_feature_div"),
    }

    nao_encontrados = []

    for nome, seletor in elementos.items():
        try:
            wait.until(EC.presence_of_element_located(seletor))
        except TimeoutException:
            nao_encontrados.append(nome)

    # Exibição de resultado final
    if not nao_encontrados:
        print("✅ Todos os elementos (imagem, título, preço e avaliações) foram encontrados com sucesso!")
    else:
        print("⚠️ Nem todos os elementos foram encontrados.")
        print("❌ Faltando:", ", ".join(nao_encontrados))

# Produto - Verificar se o item foi criado na tela do carrinho 
def teste_adicionar_e_conferir_carrinho():
    driver = setup()
    driver.get("https://www.amazon.com.br/")
    wait = WebDriverWait(driver, 30)

    produto_pesquisado = 'Smart Tv'

    # Pesquisa o produto
    wait.until(EC.visibility_of_element_located((By.ID, "twotabsearchtextbox"))).send_keys(produto_pesquisado)
    wait.until(EC.element_to_be_clickable((By.ID, "nav-search-submit-button"))).click()

    valor_antigo_carrinho = wait.until(
        EC.visibility_of_element_located((By.ID, "nav-cart-count"))
    ).text

    # Clica no primeiro botão de add ao carrinho 
    adicionar_ao_carrinho = wait.until(
        EC.element_to_be_clickable((By.NAME, "submit.addToCart"))
    )
    adicionar_ao_carrinho.click()

    # espera até o valor do carrinho mudar (ou 10 segundos)
    WebDriverWait(driver, 10).until(
        lambda d: d.find_element(By.ID, "nav-cart-count").text.strip() != valor_antigo_carrinho
    )

    # Sobe no DOM até o contêiner do produto
    produto_container = adicionar_ao_carrinho.find_element(By.XPATH, "./ancestor::div[@data-asin]")

    # Busca o nome do produto
    titulo_elemento = produto_container.find_element(By.CSS_SELECTOR, "h2 span")
    titulo_produto = titulo_elemento.text.strip()

    print(f"Produto identificado: {titulo_produto}")

    # Volta pro início da tela
    driver.execute_script("window.scrollTo(0, 0);")

    carrinho = wait.until(
        EC.visibility_of_element_located((By.ID, "nav-cart"))
    )

    carrinho.click()

    try:
        span_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.a-truncate-cut")))
    except TimeoutException:
        span_elements = []

    # Verifica se o produto adicionado está no carrinho
    produto_encontrado_carrinho = any(titulo_produto.strip().lower() in span.text.lower() for span in span_elements)


    if produto_encontrado_carrinho:
        print("✅ O produto adicionado ao carrinho foi encontrado na tela do carrinho")
    else:
        print("❌ O sistema não funcionou conforme esperado")

    driver.quit()

teste_adicionar_e_conferir_carrinho()