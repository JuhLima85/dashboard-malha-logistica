import requests

url = "https://raw.githubusercontent.com/Mcelli/Municipios-Brasileiros/master/csv/municipios.csv"

print("Baixando base de municípios...")

resposta = requests.get(url, timeout=60)
resposta.raise_for_status()

with open("municipios.csv", "wb") as arquivo:
    arquivo.write(resposta.content)

print("Download concluído!")
print("Arquivo criado: municipios.csv")