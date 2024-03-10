from django.shortcuts import render
import folium


def route(request):

    m = folium.Map(location=[-10.430347, -45.174076], zoom_start=14)

    rota_saida = f"geojson/saida.geojson"
    rota_retorno = f"geojson/retorno.geojson"

    paradas_saida = f"geojson/paradas-saida.geojson"
    paradas_retorno = f"geojson/paradas-retorno.geojson"

    paradas_saida_labels = [
        "Posto de Combustível Primavera", "Praça Principal do Vermelhão", "Supermercado Rocha",
        "Praça da Igreja Batista", "15ª Regional de Educação", "Posto de Combustível do Aeroporto",
        "Escola Municipal Orley Cavalcante Pacheco",
    ]
    paradas_retorno_labels = [
        "15ª Regional de Educação", "APAE", "SAMU", "Caixa D'Agua da Agespisa",
        "Trevo da Entrada do Moro do Pequi", "IFPI-Campus Corrente",
    ]

    folium.GeoJson(rota_saida, name="Rota de Saída", style_function=lambda x: {'color': 'blue'}).add_to(m)
    folium.GeoJson(rota_retorno, name="Rota de Retorno", style_function=lambda x: {'color': 'red'}).add_to(m)
    
    paradas_saida_geojson = folium.GeoJson(paradas_saida, name="Paradas de Saída", style_function=lambda x: {'color': 'blue'}).add_to(m)
    paradas_retorno_geojson = folium.GeoJson(paradas_retorno, name="Paradas de Retorno", style_function=lambda x: {'color': 'red'}).add_to(m)
    
    for i, parada in enumerate(paradas_saida_geojson.data['features']):
        folium.Marker(
            location=parada['geometry']['coordinates'][::-1],
            popup=paradas_saida_labels[i],
            icon=folium.Icon(color='blue', icon='bus', prefix='fa')
        ).add_to(m)

    for i, parada in enumerate(paradas_retorno_geojson.data['features']):
        folium.Marker(
            location=parada['geometry']['coordinates'][::-1],
            popup=paradas_retorno_labels[i],
            icon=folium.Icon(color='red', icon='bus', prefix='fa')
        ).add_to(m)

    m = m._repr_html_()

    return render(request, 'index.html', {'mapa': m, 'saida': paradas_saida_labels, 'retorno': paradas_retorno_labels})