import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import pandas as pd
import json


def gerar_agenda(usuario, senha, data_inicio, data_fim, url_base, url_agenda_base):
   
    # Converte datas para YYYY-MM-DD conforme URL da API
    start_str = data_inicio.strftime("%Y-%m-%d")
    end_str = data_fim.strftime("%Y-%m-%d")

    # Selenium para login
    driver = webdriver.Chrome()
    driver.get(url_base)
    wait = WebDriverWait(driver, 15)

    email_input = wait.until(
        EC.presence_of_element_located((By.NAME, "identity")))
    password_input = wait.until(
        EC.presence_of_element_located((By.NAME, "password")))

    email_input.send_keys(usuario)
    password_input.send_keys(senha)
    password_input.send_keys(Keys.RETURN)

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))

    # Extrai cookies e cria sessão requests
    selenium_cookies = driver.get_cookies()
    driver.quit()
    session = requests.Session()
    for cookie in selenium_cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # Consome API da agenda
    agenda_url = f"{url_agenda_base}?start={start_str}&end={end_str}"
    response = session.get(agenda_url)
    data = response.json()

    # Salva JSON completo
    with open("agenda.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # Processa eventos e aplica filtros
    events = []
    for item in data:
        title = item.get("title", "")
        description = item.get("description", "")
        sala = item.get("sala", "")

        if "Desmarque pelo paciente" in description:
            continue
        if not sala:
            continue
        if "NÃO AGENDAR" in title.upper() or "NÃO AGENDAR" in description.upper():
            continue

        events.append({
            "Nome": title.replace("<br>", " ").strip(),
            "Data": item["start"].split(" ")[0],
        })

    # Cria DataFrame
    df = pd.DataFrame(events)
    df["Data"] = pd.to_datetime(df["Data"])
    df_sorted = df.sort_values(by=["Nome", "Data"], ascending=[True, True])
    df_sorted["Data"] = df_sorted["Data"].dt.strftime("%d/%m/%Y")

    # Exporta Excel e salva no Desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    nome_arquivo = f"agenda_{start_str}_ate_{end_str}.xlsx"
    caminho_completo = os.path.join(desktop_path, nome_arquivo)
    df_sorted.to_excel(caminho_completo, index=False)
    return nome_arquivo
