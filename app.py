from flask import Flask, jsonify, render_template_string
import folium
from geopy.geocoders import Nominatim

app = Flask()

# Coordenadas das cidades
city_coordinates = {
    'Patrocinio': (-18.9433, -46.9922),
    'Araxa': (-19.5902, -46.9433),
    'Uberlandia': (-18.9128, -48.2755),
    'Serra do Salitre': (-19.1081, -46.6961),
    'Monte Carmelo': (-18.7247, -47.4985),
    'Coromandel': (-18.4733, -47.1987),
    'Carmo do Paranaiba': (-19.0004, -46.3165),
    'Rio Paranaiba': (-19.1868, -46.2456),
    'Guimarania': (-18.8426, -47.1067),
    'Perdizes': (-19.3435, -47.2902),
    'Patos de Minas': (-18.5789, -46.5143),
}

# Saída JSON simulada pelo back-end
data = {
    "melhor_custo": [
        ["Patrocinio", "Serra do Salitre", "Monte Carmelo", "Carmo do Paranaiba", "Coromandel", "Araxa", "Uberlandia", "Rio Paranaiba", "Perdizes", "Guimarania", "Patos de Minas", "Patrocinio"],
        740,
        197,
        13.8
    ],
    "melhor_distancia": [
        ["Patrocinio", "Serra do Salitre", "Monte Carmelo", "Carmo do Paranaiba", "Coromandel", "Araxa", "Uberlandia", "Rio Paranaiba", "Perdizes", "Guimarania", "Patos de Minas", "Patrocinio"],
        740,
        197,
        13.8
    ],
    "melhor_tempo": [
        ["Patrocinio", "Serra do Salitre", "Monte Carmelo", "Carmo do Paranaiba", "Coromandel", "Araxa", "Uberlandia", "Rio Paranaiba", "Perdizes", "Guimarania", "Patos de Minas", "Patrocinio"],
        740,
        197,
        13.8
    ]
}

@app.route('/')
def home():
    # Inicializa o mapa centralizado em Patrocínio
    folium_map = folium.Map(location=[-18.9433, -46.9922], zoom_start=8)

    # Adiciona marcadores das cidades no mapa
    for city, coord in city_coordinates.items():
        folium.Marker(
            location=coord,
            popup=city,
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(folium_map)

    # Desenha as rotas com base nos dados do back-end
    rotas = [
        {"cities": data["melhor_custo"][0], "color": 'red'},
        {"cities": data["melhor_distancia"][0], "color": 'blue'},
        {"cities": data["melhor_tempo"][0], "color": 'green'}
    ]

    # Desenha as rotas
    for route in rotas:
        points = [city_coordinates[city] for city in route['cities']]
        folium.PolyLine(
            locations=points,
            color=route['color'],
            weight=5,
            opacity=0.8
        ).add_to(folium_map)

    # Renderiza o mapa como HTML
    map_html = folium_map._repr_html_()
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rotas Otimizadas</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            #map {
                width: 100%;
                height: 80vh;
                margin: 20px 0;
            }
            #details {
                width: 80%;
                max-width: 800px;
                background: #f9f9f9;
                border: 1px solid #ccc;
                padding: 10px;
                border-radius: 5px;
            }
            .route-details {
                margin-bottom: 15px;
            }
        </style>
    </head>
    <body>
        <h1>Rotas Otimizadas</h1>
        <div id="map">{{ map_html|safe }}</div>
        <div id="details">
            <h3>Detalhes das Rotas</h3>
            {% for route in routes %}
                <div class="route-details">
                    <strong>Rota:</strong> {{ route.cities|join(' → ') }}<br>
                    <strong>Cor:</strong> {{ route.color }}
                </div>
            {% endfor %}
        </div>
    </body>
    </html>
    ''', map_html=map_html, routes=rotas)
