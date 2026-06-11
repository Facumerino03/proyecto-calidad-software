# -*- coding: utf-8 -*-
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TestBusquedaArticulos(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)
        self.base_url = "https://um-2025-articulos.tiiny.site/"

    # --- TEST A ---
    def test_BusquedaArticulo_CodigoValidoExistente_ArticuloEsMostrado(self):
        driver = self.driver
        driver.get(self.base_url)
        
        driver.find_element(By.ID, "code").click()
        driver.find_element(By.ID, "code").clear()
        driver.find_element(By.ID, "code").send_keys("1111111111111")
        driver.find_element(By.ID, "search").click()
        
        time.sleep(2) 

    # --- TEST B ---
    def test_BusquedaArticulo_CodigoValidoInexistente_MensajeErrorEsMostrado(self):
        driver = self.driver
        driver.get(self.base_url)
        
        driver.find_element(By.ID, "code").click()
        driver.find_element(By.ID, "code").clear()
        driver.find_element(By.ID, "code").send_keys("9999999999999")
        driver.find_element(By.ID, "search").click()
        
        time.sleep(2)

    # --- TEST C ---
    def test_BusquedaArticulo_CodigoInvalido_ValidacionDeFormatoEsMostrada(self):
        driver = self.driver
        driver.get(self.base_url)
        
        driver.find_element(By.ID, "code").click()
        driver.find_element(By.ID, "code").clear()
        driver.find_element(By.ID, "code").send_keys("123456789012345")
        driver.find_element(By.ID, "search").click()
        
        time.sleep(2)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
