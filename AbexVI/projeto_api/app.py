import os
import joblib
import pandas as pd
import shap
from flask import Flask, request, jsonify

# CORREÇÃO AQUI: Adicionamos PONTO_DE_CORTE à lista de importação
from config import MODELO_PATH, SCALER_PATH, COLUNAS_ESPERADAS, SECRET_KEY, PONTO_DE_CORTE

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Carrega os artefatos
model = joblib.load(MODELO_PATH)
scaler = joblib.load(SCALER_PATH)
explainer = shap.TreeExplainer(model)
print("Modelo, Scaler e Explicador SHAP carregados.")


# Função para verificar a chave de API
def check_api_key(req):
    return req.headers.get('x-api-key') == SECRET_KEY


# Endpoint para verificar a saúde da aplicação
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'OK'}), 200


# Endpoint para predição
@app.route('/predict', methods=['POST'])
def predict():
    if not check_api_key(request):
        return jsonify({'erro': 'Acesso não autorizado'}), 401

    dados_entrada = request.get_json()

    if not dados_entrada or not all(coluna in dados_entrada for coluna in COLUNAS_ESPERADAS):
        return jsonify({'erro': 'Uma ou mais colunas necessárias estão faltando no JSON'}), 400

    try:
        df_para_prever = pd.DataFrame([dados_entrada], columns=COLUNAS_ESPERADAS)
        dados_scaled = scaler.transform(df_para_prever)

        previsao = model.predict(dados_scaled)
        probabilidades = model.predict_proba(dados_scaled)

        prob_aprovacao = float(probabilidades[0][1])
        previsao_final = "Aprovado" if prob_aprovacao >= PONTO_DE_CORTE else "Reprovado"

        shap_values = explainer.shap_values(dados_scaled)
        feature_names = df_para_prever.columns
        contribuições = {name: float(val) for name, val in zip(feature_names, shap_values[0])}
        fatores_influentes = sorted(contribuições.items(), key=lambda item: abs(item[1]), reverse=True)[:5]

        resposta = {
            'previsao': previsao_final,
            'status_de_risco': 'Aluno em Risco' if previsao_final == 'Reprovado' else 'Baixo Risco',
            'probabilidade_de_aprovacao': f'{prob_aprovacao:.2%}',
            'ponto_de_corte_usado': PONTO_DE_CORTE,
            'explicacao': fatores_influentes
        }

        return jsonify(resposta), 200

    except Exception as e:
        return jsonify({'erro': 'Ocorreu um erro durante a predição.', 'detalhes': str(e)}), 500


# Executa a aplicação
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)