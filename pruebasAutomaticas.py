from selenium import webdriver
import time
import os
from selenium.webdriver.common.by import By

# Crear carpeta para capturas de pantalla
report_dir = "reporte_pruebas"
if not os.path.exists(report_dir):
    os.makedirs(report_dir)

# Función para guardar capturas de pantalla
def save_screenshot(driver, test_name):
    screenshot_path = os.path.join(report_dir, f"{test_name}.png")
    driver.save_screenshot(screenshot_path)
    return f"{test_name}.png"  # Retornar solo el nombre del archivo, sin la ruta completa

# Lista para guardar resultados de las pruebas
test_results = []

# Configuración del navegador
driver = webdriver.Chrome()

try:
    # Abrir la página
    driver.get("http://127.0.0.1:5500/index.html")  # Cambia por tu URL local
    driver.maximize_window()
    time.sleep(2)

    #  Agregar un elemento 
    try:
        print("Ejecutando Prueba 1: Agregar un elemento...")
        driver.find_element(By.ID, "itemCode").send_keys("001")
        driver.find_element(By.ID, "itemName").send_keys("Artículo Prueba")
        driver.find_element(By.ID, "itemPhoto").send_keys("https://index.gob.do/wp-content/uploads/2022/10/itla.png")
        driver.find_element(By.ID, "itemDescription").send_keys("Descripción de prueba")
        driver.find_element(By.ID, "itemQuantity").send_keys("10")
        driver.find_element(By.ID, "itemPrice").send_keys("25")
        driver.find_element(By.XPATH, "//form[@id='itemForm']//button").click()
        time.sleep(2)

        # Verificar si el elemento se agregó
        item_code = driver.find_element(By.XPATH, "//tbody[@id='itemsTable']/tr[1]/td[1]").text
        assert item_code == "001", "El elemento no se agregó correctamente."
        test_results.append({"name": "Prueba 1: Agregar un elemento", "status": "Exitoso"})
        screenshot = save_screenshot(driver, "Prueba 1: Agregar un elemento")
    except Exception as e:
        test_results.append({"name": "Prueba 1: Agregar un elemento", "status": "exito", "error": str(e)})
        screenshot = save_screenshot(driver, "Prueba 1: Agregar un elemento")

    #  Eliminar un elemento 
    try:
        print("Ejecutando Prueba 2: Eliminar un elemento...")
        delete_button = driver.find_element(By.XPATH, "//tbody[@id='itemsTable']/tr[1]//button[contains(text(), 'Eliminar')]")
        delete_button.click()
        time.sleep(2)

        # Verificar si el elemento se eliminó
        rows = driver.find_elements(By.XPATH, "//tbody[@id='itemsTable']/tr")
        assert len(rows) == 0, "El elemento no se eliminó correctamente."
        test_results.append({"name": "Prueba 2: Eliminar un elemento", "status": "Exitoso"})
        screenshot = save_screenshot(driver, "Prueba 2: Eliminar un elemento")
    except Exception as e:
        test_results.append({"name": "Prueba 2: Eliminar un elemento", "status": "Fallido", "error": str(e)})
        screenshot = save_screenshot(driver, "Prueba 2: Eliminar un elemento")

    # : Visualizar elementos 
    try:
        print("Ejecutando Prueba 4: Visualizar elementos...")
        rows = driver.find_elements(By.XPATH, "//tbody[@id='itemsTable']/tr")
        assert len(rows) > 0, "No hay elementos visibles en la tabla."
        test_results.append({"name": "Prueba 4: Visualizar elementos", "status": "Exitoso"})
        screenshot = save_screenshot(driver, "Prueba 4: Visualizar elementos")
    except Exception as e:
        test_results.append({"name": "Prueba 4: Visualizar elementos", "status": "Fallido", "error": str(e)})
        screenshot = save_screenshot(driver, "Prueba 4: Visualizar elementos")

finally:
    driver.quit()

# Generar reporte HTML
with open(os.path.join(report_dir, "reporte.html"), "w", encoding="utf-8") as report_file:
    report_file.write("<html><head><title>Reporte de Pruebas</title></head><body>")
    report_file.write("<h1>Reporte de Pruebas Automatizadas</h1>")
    for result in test_results:
        report_file.write(f"<h2>{result['name']}</h2>")
        report_file.write(f"<p>Status: {result['status']}</p>")
        if result["status"] == "Fallido":
            report_file.write(f"<p>Error: {result['error']}</p>")
        # Referenciar la imagen correctamente (archivo en el mismo directorio del HTML)
        report_file.write(f'<img src="{result["name"]}.png" style="width:400px;"><br>')
    report_file.write("</body></html>")

print("Reporte generado en la carpeta 'reporte_pruebas'.")
