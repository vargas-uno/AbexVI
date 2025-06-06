import requests
import json

url = 'http://127.0.0.1:5000/predict'

headers = {
    'Content-Type': 'application/json',
    'x-api-key': 'ixc-soft-analise-alunos-2025'
}

# ALTERAÇÃO FINAL: Chaves do dicionário corrigidas para bater 100% com o modelo.
dados_aluno = {
    'age': 21,
    'study_hours_per_week': 2,
    'online_courses_completed': 1,
    'assignment_completion_rate_': 30,
    'attendance_rate_': 40,
    'time_spent_on_social_media_hoursweek': 15, # Corrigido
    'sleep_hours_per_night': 5,
    'gender_Male': 1,
    'gender_Other': 0,
    'preferred_learning_style_Kinesthetic': 1,
    'preferred_learning_style_Reading/Writing': 0, # Adicionado
    'preferred_learning_style_Visual': 0,
    'use_of_educational_tech_Yes': 0,
    'participation_in_discussions_Yes': 0,
    'self_reported_stress_level_Low': 0,
    'self_reported_stress_level_Medium': 1
}
# Note que 'previous_failures' não está na lista final do seu modelo, então foi removido.

print("Enviando dados para a API (com a estrutura final e correta)...")
response = requests.post(url, data=json.dumps(dados_aluno), headers=headers)

print("\n--- Resposta da API ---")
if response.status_code == 200:
    print("Dados Recebidos:")
    print(response.json())
else:
    print(f"Erro ao chamar a API: {response.status_code}")
    print(f"Detalhes: {response.text}")