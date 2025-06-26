import streamlit as st
import requests
import json
import pandas as pd
import plotly.graph_objects as go  # <-- NOVA IMPORTAÇÃO

# --- Configuração da Página ---
st.set_page_config(page_title="Preditor de Aprovação", page_icon="🎓", layout="wide")


# --- Funções ---
def fazer_previsao(dados_aluno):
    """Envia os dados do aluno para a API Flask e retorna a resposta."""
    # (Esta função não muda)
    url_api = 'http://127.0.0.1:8000/predict'
    api_key = 'abexvi-chave-secreta-2024'
    headers = {'Content-Type': 'application/json', 'x-api-key': api_key}
    try:
        response = requests.post(url_api, headers=headers, data=json.dumps(dados_aluno))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}


# --- NOVA FUNÇÃO PARA CRIAR O GRÁFICO ---
def criar_grafico_contribuicao(contributions):
    """Cria um gráfico de barras Plotly para visualizar a contribuição das features."""
    df = pd.DataFrame(contributions)

    # Ordena as contribuições pela magnitude para o gráfico ficar mais intuitivo
    df = df.sort_values(by='contribution', ascending=True)

    # Define as cores: verde para positivo, vermelho para negativo
    colors = ['#28a745' if x > 0 else '#dc3545' for x in df['contribution']]

    fig = go.Figure(go.Bar(
        x=df['contribution'],
        y=df['feature'],
        orientation='h',
        marker_color=colors,
        text=df['contribution'].apply(lambda x: f'{x:.2f}'),
        textposition='auto'
    ))

    fig.update_layout(
        title_text='<b>O que mais pesou na decisão do modelo?</b>',
        title_x=0.5,
        xaxis_title="Contribuição (Negativa vs. Positiva)",
        yaxis_title="Fatores",
        yaxis=dict(tickfont=dict(size=12)),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500,
        margin=dict(l=50, r=50, t=50, b=50)
    )

    st.plotly_chart(fig, use_container_width=True)


# --- Interface do Usuário ---
# (Cabeçalho com logo não muda)
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    try:
        st.image("logo.png", width=150)
    except FileNotFoundError:
        st.markdown("🎓")
with col_titulo:
    st.title("Preditor de Aprovação de Alunos")
    st.markdown("Um projeto de Machine Learning para a disciplina AbexVI")

st.markdown("""
Esta aplicação utiliza um modelo de Machine Learning para prever se um aluno será **aprovado** ou **reprovado**. Preencha os dados abaixo e clique em 'Prever' para ver o resultado.
""")
st.divider()

# (Formulário não muda)
col1, col2 = st.columns(2)
with col1:
    st.subheader("Informações Pessoais")
    age = st.slider("Idade", 18, 30, 22)
    gender_display = st.selectbox("Gênero", ["Feminino", "Masculino"])
    stress_display = st.selectbox("Nível de Estresse", ["Baixo", "Médio", "Alto"])
    sleep_hours = st.slider("Horas de Sono por Noite", 4, 10, 7)
with col2:
    st.subheader("Mídia Social e Tecnologia")
    social_media_hours = st.slider("Horas em Mídia Social por Semana", 0, 30, 10)
    tech_display = st.radio("Usa Tecnologia Educacional?", ["Sim", "Não"])
    learning_style_display = st.selectbox("Estilo de Aprendizagem Preferido",
                                          options=["Prático", "Leitura/Escrita", "Visual", "Auditivo"])
st.divider()
st.subheader("Desempenho e Hábitos Acadêmicos")
col_a, col_b = st.columns(2)
with col_a:
    study_hours = st.slider("Horas de Estudo por Semana", 5, 50, 25)
    online_courses = st.slider("Cursos Online Completos", 0, 20, 10)
    discussions_display = st.radio("Participa de Discussões?", ["Sim", "Não"])
with col_b:
    assignment_rate = st.slider("Taxa de Conclusão de Tarefas (%)", 50, 100, 85)
    attendance_rate = st.slider("Taxa de Frequência (%)", 50, 100, 90)

# (Mapeamento não muda)
map_gender = {"Feminino": "Female", "Masculino": "Male"}
map_stress = {"Baixo": "Low", "Médio": "Medium", "Alto": "High"}
map_yes_no = {"Sim": "Yes", "Não": "No"}
map_learning_style = {"Prático": "Kinesthetic", "Leitura/Escrita": "Reading/Writing", "Visual": "Visual",
                      "Auditivo": "Auditory"}

if st.button("📊 Prever Aprovação", use_container_width=True, type="primary"):
    # (Montagem dos dados não muda)
    dados_entrada = {"Age": age, "Gender": map_gender[gender_display], "Study_Hours_per_Week": study_hours,
                     "Preferred_Learning_Style": map_learning_style[learning_style_display],
                     "Online_Courses_Completed": online_courses,
                     "Participation_in_Discussions": map_yes_no[discussions_display],
                     "Assignment_Completion_Rate (%)": assignment_rate, "Attendance_Rate (%)": attendance_rate,
                     "Use_of_Educational_Tech": map_yes_no[tech_display],
                     "Self_Reported_Stress_Level": map_stress[stress_display],
                     "Time_Spent_on_Social_Media (hours/week)": social_media_hours,
                     "Sleep_Hours_per_Night": sleep_hours}

    with st.spinner('Aguarde... Enviando dados para o modelo...'):
        resultado = fazer_previsao(dados_entrada)

        if 'error' in resultado:
            st.error(f"**Ocorreu um erro ao contatar a API:**\n\n{resultado['error']}")
        else:
            previsao = resultado.get('prediction')
            probabilidade = resultado.get('probability_of_passing', 'N/A')

            st.subheader("Resultado da Previsão:")
            if previsao == "APROVADO":
                st.success(f"🎉 **APROVADO!**")
            else:
                st.error(f"🚨 **REPROVADO!**")

            st.metric(label="Chance de Aprovação", value=probabilidade)

            # --- PARTE ATUALIZADA: EXIBIÇÃO DO GRÁFICO ---
            st.divider()
            contributions = resultado.get('feature_contributions')
            if contributions:
                criar_grafico_contribuicao(contributions)

