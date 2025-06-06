# 🎓 Projeto de Previsão de Desempenho Acadêmico

Bem-vindo! Esta é uma ferramenta de Inteligência Artificial projetada para ajudar educadores a identificar e apoiar estudantes.

## 🎯 Qual o Objetivo Deste Projeto?

O principal objetivo desta ferramenta é prever, com base em diversas características, se um aluno tem um perfil de risco para ser **reprovado**. Ao identificar esses alunos proativamente, é possível oferecer apoio pedagógico direcionado (como aulas de reforço, tutoria ou acompanhamento psicopedagógico) antes que as dificuldades se tornem irreversíveis, aumentando as chances de sucesso do estudante.

## 🤔 Como Funciona?

Pense neste sistema como um **detetive experiente**.

1.  **Treinamento:** O "detetive" (nosso modelo de Machine Learning) analisou o histórico de 10.000 alunos para aprender quais padrões de comportamento, estudo e bem-estar estão mais associados à aprovação e à reprovação.
2.  **Análise:** Ao receber os dados de um novo aluno, ele usa toda essa experiência para encontrar "pistas" e fazer uma previsão sobre o resultado final daquele aluno.
3.  **Explicação:** Além de dar o palpite final, o sistema também mostra quais foram as **5 principais pistas** que o levaram àquela conclusão, tornando o processo transparente.

## 🚀 Como Usar a Ferramenta

Para executar a aplicação no seu computador, siga estes passos:

### Pré-requisitos
* Ter o [Python](https://www.python.org/downloads/) instalado no seu computador.
* Ter baixado a pasta completa deste projeto.

### Passo 1: Instalar as Dependências
Abra um terminal ou prompt de comando, navegue até a pasta principal do projeto (`/AbexVI/`) e execute o seguinte comando para instalar todas as bibliotecas necessárias de uma só vez:
```bash
pip install -r requirements.txt