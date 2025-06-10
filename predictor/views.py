import pandas as pd
import numpy as np

from django.shortcuts import render
from sklearn.metrics import mean_squared_error
from scipy.spatial import cKDTree
from geopy.distance import geodesic

from .forms import WellPredictionForm
from .regressor import model
from .data import df_seismic, df_springs

FEATURES = [
    'latitude', 'longitude',
    'elevationgl_m', 'drillertotaldepth_m',
    'days_to_completion', 'year_spud', 'month_spud',
    'depth_per_day', 'is_production_well',
    'maxmeasuredtemp_c', 'bottommeasuredtemp_c',
    'closest_spring_mean_measuredtemp_c', 'avg_mag_within_100km'
]


def __compute_spring_temperature(data):

    # Coordenadas de pozos y manantiales
    well_coords = data[['latitude', 'longitude']].to_numpy()
    spring_coords = df_springs[['latdegree', 'longdegree']].to_numpy()

    # Crear árbol espacial
    tree = cKDTree(spring_coords)

    # Para cada pozo, obtener el índice del manantial más cercano
    distances, indices = tree.query(well_coords, k=1)

    # Obtener la temperatura del manantial más cercano
    closest_spring_temps = df_springs.iloc[indices]['spring_mean_measuredtemp_c'].values

    # Asignar la temperatura a df_wells
    data['closest_spring_mean_measuredtemp_c'] = closest_spring_temps


def __compute_seismic_info(data):

    import numpy as np

    # Crear KDTree con latitud y longitud de eventos sísmicos
    seismic_coords = df_seismic[['LAT', 'LON']].values
    tree = cKDTree(seismic_coords)

    approx_radius_deg = 100 / 111  # ~0.09 grados

    avg_mags = []

    for _, well in data.iterrows():
        well_coord = (well['latitude'], well['longitude'])

        # 1. Encontrar candidatos en un radio rápido (en grados)
        candidate_indices = tree.query_ball_point(
            [well_coord], r=approx_radius_deg)[0]

        if not candidate_indices:
            avg_mags.append(0)
            continue

        # 2. Calcular distancias geodésicas reales solo para los candidatos
        close_events = []
        for idx in candidate_indices:
            event_coord = (df_seismic.at[idx, 'LAT'],
                           df_seismic.at[idx, 'LON'])
            dist_km = geodesic(well_coord, event_coord).km
            if dist_km <= 100:
                close_events.append(idx)

        # 3. Promedio de magnitudes
        if close_events:
            avg_mag = df_seismic.loc[close_events, 'MAG_VALUE'].mean()
        else:
            avg_mag = 0

        avg_mags.append(avg_mag)

    data['avg_mag_within_100km'] = avg_mags


def __parse_to_dataframe(data):

    df = pd.DataFrame([{
        'latitude': data['latitude'],
        'longitude': data['longitude'],
        'elevationgl_m': data['elevationgl_m'],
        'drillertotaldepth_m': data['drillertotaldepth_m'],
        'maxmeasuredtemp_c': data['maxmeasuredtemp_c'],
        'bottommeasuredtemp_c': data['bottommeasuredtemp_c'],
        'function': data['function'],
        'spuddate': pd.to_datetime(data['spuddate']),
        'completiondate': pd.to_datetime(data['completiondate']),
    }])

    df['days_to_completion'] = (
        df['completiondate'] - df['spuddate']).dt.days + 1
    df['year_spud'] = df['spuddate'].dt.year
    df['month_spud'] = df['spuddate'].dt.month
    df['depth_per_day'] = df['drillertotaldepth_m'] / df['days_to_completion']
    df['is_production_well'] = (df['function'] == 'Production').astype(int)

    __compute_seismic_info(df)
    __compute_spring_temperature(df)

    return df[FEATURES]


def predict_view(request):
    prediction = None
    if request.method == 'POST':
        form = WellPredictionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            df_input = __parse_to_dataframe(data)

            # Si necesitas preprocesar function o fechas, hazlo aquí

            prediction = model.predict(df_input)[0]

    else:
        form = WellPredictionForm()
    return render(request, 'predict.html', {'form': form, 'prediction': prediction})
