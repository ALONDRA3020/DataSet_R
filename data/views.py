# views.py
from django.shortcuts import render
import pandas as pd

def dataset_upload_view(request):
    df_html = None
    error = None

    if request.method == 'POST':
        url = request.POST.get('url')

        # Si es GitHub, convertir a RAW
        if 'github.com' in url:
            url = url.replace('github.com', 'raw.githubusercontent.com')\
                     .replace('/blob/', '/')

        try:
            # Leer CSV y manejar posibles líneas problemáticas
            df = pd.read_csv(url, on_bad_lines='skip')

            # Si no existe columna 'id', agregarla al inicio
            if 'id' not in df.columns:
                df.insert(0, 'id', range(len(df)))

            # Reordenar para que 'id' esté al inicio (por si acaso)
            cols = df.columns.tolist()
            if cols[0] != 'id':
                cols.remove('id')
                cols = ['id'] + cols
                df = df[cols]

            # Mostrar solo las primeras 20 filas
            df_html = df.head(20).to_html(classes='table table-striped', index=False)
        except Exception as e:
            error = f"Error al cargar los datos: {e}"

    return render(request, 'index.html', {'df_html': df_html, 'error': error})