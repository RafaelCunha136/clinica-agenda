from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import pandas as pd
import json


# Acessa o site e faz login usando credenciais - *** IMPLEMENTAR GUI PARA DEMAIS USUÁRIOS ***

driver = webdriver.Chrome()
driver.get("URL")

wait = WebDriverWait(driver, 15)

email_input = wait.until(EC.presence_of_element_located((By.NAME, "identity")))
password_input = wait.until(
    EC.presence_of_element_located((By.NAME, "password")))

email_input.send_keys("EMAIL")
password_input.send_keys("PASSWORD")
password_input.send_keys(Keys.RETURN)

wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))

# Extrai cookies do Selenium e cria sessão requests

selenium_cookies = driver.get_cookies()
driver.quit()

session = requests.Session()
for cookie in selenium_cookies:
    session.cookies.set(cookie['name'], cookie['value'])

# Consume API da agenda
agenda_url = "URL AGENDA"
response = session.get(agenda_url)
data = response.json()

# Gera a lista em JSON
with open("agenda.json", "w", encoding="utf-8") as f:
   json.dump(data, f, ensure_ascii=False, indent=4)

# Processa eventos e aplica filtros
events = []
for item in data:
    title = item.get("title", "")
    description = item.get("description", "")
    sala = item.get("sala", "")

    # Filtros de negócio
    if "Desmarque pelo paciente" in description:
        continue
    if not sala:
        continue
    if "NÃO AGENDAR" in title.upper() or "NÃO AGENDAR" in description.upper():
        continue

    # Adiciona evento válido
    events.append({
        "Nome": title.replace("<br>", " ").strip(),
        "Data": item["start"].split(" ")[0],
        # "Hora Início": item["start"].split(" ")[1],
        # "Hora Fim": item["end"].split(" ")[1],
        # "Sala": sala
    })

# Cria e formata DataFrame
df = pd.DataFrame(events)

df["Data"] = pd.to_datetime(df["Data"])
df_sorted = df.sort_values(by=["Nome", "Data"], ascending=[True, True])
df_sorted["Data"] = df_sorted["Data"].dt.strftime("%d/%m/%Y")

# Exporta para Excel
df_sorted.to_excel("agenda_setembro_aline_yoshida.xlsx", index=False)
print("Arquivo gerado com sucesso!")
