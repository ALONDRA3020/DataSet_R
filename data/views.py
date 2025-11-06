import base64
import io
import requests
from django.shortcuts import render
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split




def train_val_test_split(df, stratify=None, test_size=0.2, val_size=0.2):
    """Divide un DataFrame en train, val y test, con estratificación opcional"""
    strat = df[stratify] if stratify else None
    train_df, temp_df = train_test_split(df, test_size=(test_size + val_size), stratify=strat)
    strat_temp = temp_df[stratify] if stratify else None
    val_df, test_df = train_test_split(temp_df, test_size=test_size / (test_size + val_size), stratify=strat_temp)
    return train_df, val_df, test_df


def index(request):
    context = {}

    if request.method == 'POST':
        dataset_url = request.POST.get('dataset_url', '').strip()

        try:
            # Leer CSV desde GitHub o URL
            df = pd.read_csv(dataset_url)

            # Verificar columna 'protocol_type'
            if 'protocol_type' not in df.columns:
                context['error'] = "El dataset no contiene la columna 'protocol_type'."
                return render(request, 'index.html', context)

            # Dividir dataset
            train_set, val_set, test_set = train_val_test_split(df, stratify='protocol_type')

            # Calcular longitudes
            context['data_info'] = {
                'dataset_len': len(df),
                'train_len': len(train_set),
                'val_len': len(val_set),
                'test_len': len(test_set),
            }

            # Función auxiliar para convertir gráficas a base64
            def plot_to_base64(data, title):
                fig, ax = plt.subplots()
                data['protocol_type'].hist(ax=ax)
                ax.set_title(title)
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                image_png = buffer.getvalue()
                buffer.close()
                plt.close(fig)
                return base64.b64encode(image_png).decode('utf-8')

            # Crear imágenes
            context['df_img'] = plot_to_base64(df, 'Dataset completo')
            context['train_img'] = plot_to_base64(train_set, 'Training Set')
            context['val_img'] = plot_to_base64(val_set, 'Validation Set')
            context['test_img'] = plot_to_base64(test_set, 'Test Set')

        except Exception as e:
            context['error'] = f"Ocurrió un error al procesar el dataset: {e}"

    return render(request, 'index.html', context)