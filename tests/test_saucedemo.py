# tests/test_saucedemo.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Importamos la función auxiliar creada en utils/helpers.py
from utils.helpers import iniciar_sesion

@pytest.fixture
def driver():
    """Configura y abre el navegador Chrome antes de cada test, y lo cierra al finalizar."""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

# -------------------------------------------------------------
# CASO DE PRUEBA 1: Automatización de Login
# -------------------------------------------------------------
def test_login_exitoso(driver):
    iniciar_sesion(driver)
    
    # Validar que la URL contenga /inventory.html usando espera explícita
    WebDriverWait(driver, 10).until(EC.url_contains("/inventory.html"))
    assert "/inventory.html" in driver.current_url
    
    # Validar que el título o logo muestre "Swag Labs"
    logo = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "app_logo"))
    ).text
    assert "Swag Labs" in logo

# -------------------------------------------------------------
# CASO DE PRUEBA 2: Navegación y verificación del catálogo
# -------------------------------------------------------------
def test_verificacion_catalogo(driver):
    iniciar_sesion(driver)
    
    # 1. Verificar el título de la sección de inventario
    titulo_seccion = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "title"))
    ).text
    assert titulo_seccion == "Products"
    
    # 2. Comprobar que existan productos visibles (al menos uno)
    productos = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(productos) > 0
    
    # 3. Extraer e imprimir el nombre y precio del primer producto
    primer_nombre = productos[0].find_element(By.CLASS_NAME, "inventory_item_name").text
    primer_precio = productos[0].find_element(By.CLASS_NAME, "inventory_item_price").text
    print(f"\nProducto encontrado: {primer_nombre} - Precio: {primer_precio}")
    
    # 4. Validar la presencia del menú lateral
    menu_btn = driver.find_element(By.ID, "react-burger-menu-btn")
    assert menu_btn.is_displayed()

# -------------------------------------------------------------
# CASO DE PRUEBA 3: Interacción con el carrito
# -------------------------------------------------------------
def test_interaccion_carrito(driver):
    iniciar_sesion(driver)
    
    # 1. Añadir el primer producto al carrito
    boton_agregar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
    )
    boton_agregar.click()
    
    # 2. Verificar que el contador del carrito se incremente a 1
    contador_carrito = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    assert contador_carrito == "1"
    
    # 3. Navegar a la página del carrito
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    
    # 4. Comprobar que el producto añadido esté presente en la lista del carrito
    producto_en_carrito = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item_name"))
    ).text
    assert producto_en_carrito == "Sauce Labs Backpack"