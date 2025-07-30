import os

import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from fast_deploy.loaders.sklearn_loader import SklearnModelLoader

app = FastAPI()

model_loader = SklearnModelLoader()
model = None


@app.post('/upload-model')
async def upload_model(file: UploadFile = File(...)):
    """Endpoint para upload e carregamento de um modelo de machine learning.

    Parameters:
        file (UploadFile): Arquivo do modelo enviado pelo usuário para ser carregado

    Returns:
        dict: Mensagem de sucesso indicando que o modelo foi carregado com sucesso

    Raises:
        HTTPException: Lança uma exceção com status 500 em caso de erro durante o
        upload ou carregamento do modelo
    """
    global model

    try:
        tmp_file_path = f'./{file.filename}'
        with open(tmp_file_path, 'wb') as f:
            content = await file.read()
            f.write(content)

        model = model_loader.load_model(tmp_file_path)

        os.remove(tmp_file_path)

        return {'message': 'Modelo carregado com sucesso!'}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class PredictionInput(BaseModel):
    features: list[float]


@app.post('/predict')
async def predict(input_data: PredictionInput):
    """Realiza a previsão com base nos dados de entrada usando o modelo carregado.

    Esta função utiliza o modelo de machine learning carregado para gerar uma previsão
    e a probabilidade associada para os dados fornecidos.

    Parameters:
        input_data (PredictionInput): Dados de entrada para a previsão, incluindo as
         variáveis (features) necessárias

    Returns:
        dict: Um dicionário contendo a probabilidade da previsão (`prediction_proba`)
        e o valor previsto (`predicted`)

    Raises:
        HTTPException: Lança uma exceção com status 400 se o modelo não estiver carregado,
        ou com status 500 se ocorrer um erro durante a previsão.
    """
    if model is None:
        raise HTTPException(
            status_code=400,
            detail='Modelo não carregado. Faça o upload primeiro.',
        )

    try:
        features = np.array([input_data.features])
        probabilities = model.predict_proba(features).tolist()
        prediction = model.predict(features).tolist()

        return {
            'prediction_proba': probabilities[0][1],
            'predicted': prediction[0],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
