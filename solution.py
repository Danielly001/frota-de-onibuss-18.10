import os
import requests
from dotenv import load_dotenv
from folium import Map, Marker, Icon

load_dotenv(".env")

s = requests.Session()
res = s.post(
    f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={os.getenv('SPTRANS_TOKEN')}"
)

#Busca por linhas 
linhas_lapa = s.get(
    "http://api.olhovivo.sptrans.com.br/v2.1/Linha/Buscar?termosBusca=Lapa"
)
linhas_lapa = linhas_lapa.json()

#Busca por paradas
res = s.get(
    "http://api.olhovivo.sptrans.com.br/v2.1/Parada/BuscarParadasPorLinha?codigoLinha=1273"
)
paradas = res.json()

# Busca pelas posições dos ônibus em tempo real
pos = s.get(
    "http://api.olhovivo.sptrans.com.br/v2.1/Posicao/Linha?codigoLinha=1273"
)
posicoes = pos.json()

#criação do mapa
mapa = Map(location=[-23.525799, -46.679251], zoom_start=13, tiles="OpenTopoMap")

for parada in paradas:                         #adicionando marcadores no mapa
    Marker(location=[parada["py"], parada["px"]], icon=Icon(color="blue")).add_to(mapa)

for posicao in posicoes["vs"]:
    Marker(location=[posicao["py"], posicao["px"]], icon=Icon(color="red")).add_to(mapa)

#salvar so quando houver dados
if paradas and posicoes["vs"]:
    mapa.save("mapa.html")
else:
    print("Sem dados suficientes para atualizar o mapa.")


    



