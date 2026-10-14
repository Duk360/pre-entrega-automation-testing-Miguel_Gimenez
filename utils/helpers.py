# utils/helpers.py
from selenium.webdriver.common.by import By

def iniciar_sesion(driver):
    """
    Función auxiliar para automatizar el ingreso a SauceDemo.
    Abre la página y completa el usuario y la contraseña.
    """
    # 1. Navegar a la página de inicio de sesión
    driver.get("https://www.saucedemo.com/")
    
    # 2. Localizar los campos de texto y el botón
    campo_usuario = driver.find_element(By.ID, "user-name")
    campo_contrasena = driver.find_element(By.ID, "password")
    boton_login = driver.find_element(By.ID, "login-button")
    
    # 3. Enviar los datos requeridos e ingresar
    campo_usuario.send_keys("standard_user")
    campo_contrasena.send_keys("secret_sauce")
    boton_login.click()