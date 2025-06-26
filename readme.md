🎓 Preditor de Aprovação de Alunos (Projeto AbexVI)
🎯 Objetivo
Este projeto foi desenvolvido para a disciplina AbexVI e consiste em um sistema completo de Machine Learning para prever a probabilidade de um aluno ser aprovado ou reprovado. A aplicação utiliza um modelo treinado a partir de dados demográficos e de hábitos de estudo, fornecendo uma previsão e, mais importante, uma explicação visual dos fatores que mais influenciaram naquela decisão.

O sistema é composto por:

Um notebook Jupyter (implícito): Para todo o processo de análise, limpeza, treinamento e avaliação dos modelos.

Uma API REST em Flask: Que serve o modelo treinado.

Um front-end interativo em Streamlit: Onde o usuário pode inserir dados e visualizar a previsão e a explicação do modelo em tempo real.


O desenvolvimento do modelo seguiu uma jornada iterativa, resultando em três versões distintas, cada uma mostrando uma questão em especifico

Versão 1: O Modelo "Perfeito"
Abordagem: Utilizou todas as features disponíveis, incluindo a Nota do Exame (%).

Resultado: Acurácia de 100%.

Diagnóstico: O modelo era perfeito, mas inútil na prática. Ele sofria de vazamento de dados (data leakage), pois a nota do exame é um preditor quase direto da nota final. Um modelo que precisa da nota da prova para prever a aprovação não tem utilidade prática para intervenção precoce.

Versão 2: O Modelo "paia"

Abordagem: Removeu-se a Nota do Exame e o modelo foi treinado novamente.

Resultado: Acurácia de ~75%. No entanto, a análise da Matriz de Confusão revelou que o modelo estava sempre prevendo "Aprovado".

Diagnóstico: O modelo identificou um desbalanceamento de classes (mais alunos aprovados do que reprovados) e, para maximizar sua acurácia, adotou a estratégia preguiçosa de sempre chutar a classe majoritária. Ele era incapaz de identificar alunos em risco.

Versão 3: O Modelo Final 
Abordagem: Foi introduzido o parâmetro class_weight='balanced' na LogisticRegression. Isso penaliza mais o modelo por errar a classe minoritária (os reprovados).

Resultado: Acurácia de ~50%.

Diagnóstico: Embora a acurácia tenha caído, o modelo se tornou imensamente mais útil. Ele agora consegue identificar corretamente cerca de 50% dos alunos que iriam reprovar, cumprindo seu objetivo de ser uma ferramenta de alerta precoce. O modelo prefere cometer o erro "seguro" (alertar um aluno que acabaria passando) do que o erro "perigoso" (dar um falso otimismo a um aluno que iria reprovar).

✨ Features Principais
API Robusta: Backend em Flask com endpoint de previsão e de saúde (/health).

Front-end Interativo: Interface amigável em Streamlit que consome a API em tempo real.

Explicabilidade do Modelo (XAI): A cada previsão, um gráfico de contribuição é gerado com Plotly, mostrando ao usuário quais fatores mais pesaram para o resultado (positiva ou negativamente).

Personalização: Interface totalmente em português e com identidade visual própria (logo).

🛠️ Tecnologias Utilizadas
Linguagem: Python 3

Análise e Modelo: Pandas, NumPy, Scikit-learn

API Backend: Flask

Front-end: Streamlit, Requests, Plotly

🚀 Como Executar o Projeto
Siga os passos abaixo para rodar a aplicação completa na sua máquina.

1. Pré-requisitos:

Ter o Python 3 instalado.

Ter o pip (gerenciador de pacotes do Python).

2. Crie e ative um ambiente virtual:

#### Criar o ambiente
python3 -m venv .venv

#### Ativar o ambiente (Linux/macOS)
source .venv/bin/activate

#### Ativar o ambiente (Windows)
#### .\.venv\Scripts\activate

3. Instale as dependências:
Com o ambiente virtual ativo, instale todas as bibliotecas necessárias.

pip install -r requirements.txt

4. Estrutura de Arquivos:
Garanta que a pasta do seu projeto tenha a seguinte estrutura:

.
├── .venv/

├── modelo_aprovacao.joblib

├── colunas_modelo.joblib

├── app.py                  # API Flask (backend)

├── frontend.py             # App Streamlit (frontend)

├── logo.png                # Sua logo

└── requirements.txt


5. Rode o Backend (API Flask):
Abra um terminal, ative o .venv e rode o servidor da API. Deixe este terminal aberto.

python3 app.py

6. Rode o Front-end (Streamlit):
Abra um segundo terminal, ative o .venv e rode a aplicação Streamlit.

streamlit run frontend.py

O Streamlit abrirá automaticamente uma aba no seu navegador com a aplicação pronta para uso!

📄 Documentação da API
Endpoint POST /predict
Descrição: Recebe os dados de um aluno e retorna a previsão de aprovação.

Headers:

Content-Type: application/json

x-api-key: abexvi-chave-secreta-2024

Exemplo de Corpo da Requisição (JSON):

{
    "Age": 22,
    "Gender": "Male",
    "Study_Hours_per_Week": 10,
    "Preferred_Learning_Style": "Kinesthetic",
    "Online_Courses_Completed": 5,
    "Participation_in_Discussions": "No",
    "Assignment_Completion_Rate (%)": 70,
    "Attendance_Rate (%)": 80,
    "Use_of_Educational_Tech": "Yes",
    "Self_Reported_Stress_Level": "High",
    "Time_Spent_on_Social_Media (hours/week)": 20,
    "Sleep_Hours_per_Night": 6
}

Exemplo de Resposta (JSON):

{
  "prediction": "REPROVADO",
  "probability_of_passing": "42.15%",
  "feature_contributions": [
    { "feature": "...", "contribution": -0.5 },
    { "feature": "...", "contribution": 0.2 }
  ]
}
