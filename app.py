import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Carregamento dos Artefatos ---
try:
    model = joblib.load('modelo_aprovacao.joblib')
    model_columns = joblib.load('colunas_modelo.joblib')
    print("Modelo e colunas carregados com sucesso.")
except FileNotFoundError:
    print("ERRO: Arquivos de modelo não encontrados.")
    model = None
    model_columns = None

class_names = {0: 'REPROVADO', 1: 'APROVADO'}
SECRET_KEY = 'abexvi-chave-secreta-2024'


def check_api_key(req):
    key = req.headers.get('x-api-key')
    return key == SECRET_KEY


@app.route('/predict', methods=['POST'])
def predict():
    if not check_api_key(request):
        return jsonify({'error': 'Acesso não autorizado'}), 401

    if model is None or model_columns is None:
        return jsonify({'error': 'Serviço indisponível, modelo não carregado'}), 503

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    try:
        input_df = pd.DataFrame([data])
        processed_df = pd.get_dummies(input_df)
        final_df = processed_df.reindex(columns=model_columns, fill_value=0)

        prediction_code = model.predict(final_df)
        prediction_name = class_names[prediction_code[0]]

        probabilities = model.predict_proba(final_df)
        probability_of_passing = probabilities[0][1]

        # --- NOVA PARTE: CÁLCULO DA CONTRIBUIÇÃO DAS FEATURES ---
        # Multiplicamos os coeficientes do modelo pelos valores das features do usuário
        contributions = model.coef_[0] * final_df.iloc[0]

        # Criamos uma lista de dicionários para enviar ao front-end
        feature_contributions = []
        for feature, contribution in contributions.items():
            # Ignoramos features com contribuição zero para um gráfico mais limpo
            if contribution != 0:
                feature_contributions.append({
                    "feature": feature.replace("_", " ").replace(" per ", "/"),  # Deixa o nome mais bonito
                    "contribution": contribution
                })

        # --- FIM DA NOVA PARTE ---

        # Adicionamos a lista de contribuições à resposta da API
        return jsonify({
            'prediction': prediction_name,
            'probability_of_passing': f"{probability_of_passing * 100:.2f}%",
            'feature_contributions': feature_contributions  # <-- NOVO DADO ENVIADO
        })

    except Exception as e:
        return jsonify({'error': f'Ocorreu um erro interno: {str(e)}'}), 500


@app.route('/health', methods=['GET'])
def health():
    if model is not None and model_columns is not None:
        return jsonify({'status': 'OK'}), 200
    else:
        return jsonify({'status': 'ERROR'}), 503


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host="0.0.0.0", port=port, debug=True)

