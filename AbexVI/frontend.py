import streamlit as st
import requests
import json
import pandas as pd

# --- Configuração da Página ---
st.set_page_config(
    page_title="Previsão de Desempenho de Alunos",
    page_icon="🎓",
    layout="centered"
)

# --- Título e Descrição da Aplicação ---
st.title("🎓 Previsão de Desempenho Acadêmico")
st.write(
    "Esta interface interage com um modelo de Machine Learning (XGBoost Otimizado) "
    "para prever o desempenho de um aluno. Preencha os campos na barra lateral "
    "para realizar uma nova análise."
)

# --- Barra Lateral com os Inputs do Usuário ---
st.sidebar.header("Insira os Dados do Aluno")

age = st.sidebar.slider("Idade", 15, 30, 20)
study_hours_per_week = st.sidebar.slider("Horas de Estudo / Semana", 1, 40, 10)
assignment_completion_rate = st.sidebar.slider("Taxa de Conclusão de Tarefas (%)", 0, 100, 85)
attendance_rate = st.sidebar.slider("Taxa de Frequência (%)", 0, 100, 90)
online_courses_completed = st.sidebar.number_input("Cursos Online Completos", min_value=0, max_value=20, value=2)
time_spent_on_social_media = st.sidebar.slider("Tempo em Redes Sociais (horas/semana)", 0, 30, 5)
sleep_hours_per_night = st.sidebar.slider("Horas de Sono / Noite", 4, 12, 7)
learning_style_pt = st.sidebar.selectbox("Estilo de Aprendizagem", ('Visual', 'Cinestésico', 'Leitura/Escrita'))
tech_usage_pt = st.sidebar.radio("Usa Ferramentas de TI para Estudo?", ('Sim', 'Não'))
discussion_participation_pt = st.sidebar.radio("Participa de Discussões em Aula?", ('Sim', 'Não'))
stress_level_pt = st.sidebar.selectbox("Nível de Estresse", ('Baixo', 'Médio', 'Alto'))

if st.sidebar.button("Fazer Previsão"):
    # --- Preparação dos Dados para a API ---
    learning_style_Kinesthetic = 1 if learning_style_pt == 'Cinestésico' else 0
    learning_style_Reading_Writing = 1 if learning_style_pt == 'Leitura/Escrita' else 0
    learning_style_Visual = 1 if learning_style_pt == 'Visual' else 0
    tech_usage_Yes = 1 if tech_usage_pt == 'Sim' else 0
    discussion_participation_Yes = 1 if discussion_participation_pt == 'Sim' else 0
    stress_level_Low = 1 if stress_level_pt == 'Baixo' else 0
    stress_level_Medium = 1 if stress_level_pt == 'Médio' else 0
    assignment_study_ratio = assignment_completion_rate / (study_hours_per_week + 1)

    # --- Montagem do Payload para a API ---
    dados_aluno = {
        'age': age, 'study_hours_per_week': study_hours_per_week, 'online_courses_completed': online_courses_completed,
        'assignment_completion_rate_': assignment_completion_rate, 'attendance_rate_': attendance_rate,
        'time_spent_on_social_media_hoursweek': time_spent_on_social_media,
        'sleep_hours_per_night': sleep_hours_per_night, 'assignment_study_ratio': assignment_study_ratio,
        'preferred_learning_style_Kinesthetic': learning_style_Kinesthetic,
        'preferred_learning_style_Reading/Writing': learning_style_Reading_Writing,
        'preferred_learning_style_Visual': learning_style_Visual,
        'use_of_educational_tech_Yes': tech_usage_Yes,
        'participation_in_discussions_Yes': discussion_participation_Yes,
        'self_reported_stress_level_Low': stress_level_Low,
        'self_reported_stress_level_Medium': stress_level_Medium
    }

    # --- Chamada da API e Exibição do Resultado ---
    with st.spinner("Analisando com o modelo XGBoost..."):
        try:
            url = 'http://127.0.0.1:5000/predict'
            headers = {'Content-Type': 'application/json', 'x-api-key': 'ixc-soft-analise-alunos-2025'}
            response = requests.post(url, data=json.dumps(dados_aluno), headers=headers)

            if response.status_code == 200:
                resultado = response.json()
                st.subheader("Resultado da Previsão")
                if resultado['previsao'] == "Aprovado":
                    st.success(f"**Previsão:** {resultado['previsao']}")
                    st.balloons()
                else:
                    st.error(f"**Previsão:** {resultado['previsao']}")
                st.metric(label="Status de Risco", value=resultado['status_de_risco'])
                st.metric(label="Confiança na Aprovação", value=resultado['probabilidade_de_aprovacao'])

                st.subheader("🔍 Fatores que Influenciaram a Decisão")
                explicacao = resultado.get('explicacao', [])

                if explicacao:
                    # --- NOVIDADE: Traduzindo os nomes das features para o gráfico ---
                    traducoes = {
                        'assignment_completion_rate_': 'Taxa de Entrega de Tarefas',
                        'attendance_rate_': 'Taxa de Frequência',
                        'study_hours_per_week': 'Horas de Estudo / Semana',
                        'age': 'Idade',
                        'time_spent_on_social_media_hoursweek': 'Tempo em Redes Sociais',
                        'sleep_hours_per_night': 'Horas de Sono',
                        'assignment_study_ratio': 'Eficiência de Entregas',
                        'online_courses_completed': 'Cursos Online Concluídos',
                        'self_reported_stress_level_Medium': 'Nível de Estresse: Médio',
                        'preferred_learning_style_Visual': 'Estilo de Aprend.: Visual',
                        'use_of_educational_tech_Yes': 'Usa Tec. Educacional: Sim',
                        'participation_in_discussions_Yes': 'Participa de Discussões: Sim',
                        'self_reported_stress_level_Low': 'Nível de Estresse: Baixo',
                        'preferred_learning_style_Kinesthetic': 'Estilo de Aprend.: Cinestésico',
                        'preferred_learning_style_Reading/Writing': 'Estilo de Aprend.: Leitura/Escrita'
                    }

                    df_explicacao = pd.DataFrame(explicacao, columns=['Fator', 'Impacto'])
                    # Aplica a tradução. Se um fator não estiver no dicionário, mantém o original.
                    df_explicacao['Fator'] = df_explicacao['Fator'].map(traducoes).fillna(df_explicacao['Fator'])

                    df_plot = df_explicacao.set_index('Fator')
                    st.bar_chart(df_plot['Impacto'])
                    st.caption(
                        "O gráfico mostra os 5 principais fatores e o impacto de cada um. "
                        "Barras para a direita (positivas) empurram a previsão para 'Aprovado'. "
                        "Barras para a esquerda (negativas) empurram para 'Reprovado'."
                    )
            else:
                st.error(f"Erro ao chamar a API: {response.status_code}")
                st.json(response.json())
        except requests.exceptions.ConnectionError:
            st.error(
                "Falha na Conexão: Não foi possível conectar à API. Verifique se o servidor `app.py` está rodando.")

else:
    st.info("Aguardando a inserção dos dados na barra lateral para fazer a previsão.")