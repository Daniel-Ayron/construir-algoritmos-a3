import os
import requests
from dotenv import load_dotenv
from folium import Map, Marker, Icon, folium

load_dotenv(".env")
# Troquei o código de 2506 para este abaixo
codigo_linha = 32813

s = requests.Session()
res = s.post(
    f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={os.getenv('SPTRANS_TOKEN')}"
)

res = s.get(
    f"http://api.olhovivo.sptrans.com.br/v2.1/Parada/BuscarParadasPorLinha?codigoLinha={codigo_linha}"
)
paradas = res.json()
paradas[:3]
print(res.text)

res_onibus = s.get(
    f"http://api.olhovivo.sptrans.com.br/v2.1//Posicao/Linha?codigoLinha={codigo_linha}"
    )
dados_onibus = res_onibus.json() 

m = Map(location=[paradas[3]["py"], paradas[3]["px"]], zoom_start=14)
for i in paradas:
    Marker(location=[i["py"], i["px"]], popup=i["np"]).add_to(m)

if "vs" in dados_onibus and dados_onibus["vs"]:
    for onibus in dados_onibus["vs"]:
        acessivel = "Sim" if onibus.get("a") else "Não"
        
        Marker(
            location=[onibus["py"], onibus["px"]],
            popup=f"<b>Prefixo:</b> {onibus.get('p')}<br><b>Acessível:</b> {acessivel}",
            tooltip="Ônibus em Movimento",
            icon=Icon(color="red", icon="bus", prefix="fa")
        ).add_to(m)

legenda_html = """
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 150px; height: 75px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white;
     opacity: 0.8;
     padding: 10px;
     border-radius: 5px;">
     &nbsp; <b>Legenda:</b> <br>
     &nbsp; <i class="fa fa-map-marker" style="color:blue"></i>&nbsp; Parada Fixa <br>
     &nbsp; <i class="fa fa-bus" style="color:red"></i>&nbsp; Ônibus Real
     </div>
     """
m.get_root().html.add_child(folium.Element(legenda_html))
# Professor, aqui optei por utilizar o m.save(index.html) pois o m.show_in_browser estava dando erro.
# Nesse caso, ao rodar esse codigo ele gera um arquivo html que ao ser rodado via Live Server ou semelhante
# irá exibir o mapa.
m.save("index.html")
