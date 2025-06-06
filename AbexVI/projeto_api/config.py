# Arquivo de Configuração Central da API

MODELO_PATH = 'modelo_final_xgboost.pkl'
SCALER_PATH = 'scaler_final.pkl'
SECRET_KEY = 'ixc-soft-analise-alunos-2025'

# ADICIONADO AQUI: O ponto de corte que o app.py precisa importar
PONTO_DE_CORTE = 0.75

# Lista exata das colunas que o modelo espera
COLUNAS_ESPERADAS = [
    'age',
    'study_hours_per_week',
    'online_courses_completed',
    'assignment_completion_rate_',
    'attendance_rate_',
    'time_spent_on_social_media_hoursweek',
    'sleep_hours_per_night',
    'assignment_study_ratio',
    'preferred_learning_style_Kinesthetic',
    'preferred_learning_style_Reading/Writing',
    'preferred_learning_style_Visual',
    'use_of_educational_tech_Yes',
    'participation_in_discussions_Yes',
    'self_reported_stress_level_Low',
    'self_reported_stress_level_Medium'
]