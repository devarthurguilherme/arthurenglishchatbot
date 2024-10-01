import streamlit as st

# Título do manual
st.title("📚 Arthur's English Teacher")

# Introdução
st.markdown("""
Bem-vindo ao manual de instruções do seu app English Teacher! Este aplicativo é uma ferramenta poderosa para praticar e aprender inglês com diversas funcionalidades. Abaixo, você encontrará uma descrição detalhada de cada página do app 🚀
""")

# Seção: Página do Chatbot
st.header("🤖 English Teacher Chatbot")

st.markdown("""
Nesta página, você pode conversar com o Chatbot, que atua como seu professor de inglês. Aqui estão as funcionalidades principais:

- **Selecionar um Modelo LLM**: 🧠 Escolha entre 5 modelos disponíveis para testar e ver qual se adapta melhor ao seu estilo de aprendizado.

- **Gravação de Áudio**: 🎙️ 
  - Grave sua voz e envie como input para o chatbot.
  - Selecione a linguagem antes de gravar para ajudar o reconhecimento de áudio a captar melhor suas palavras.

- **Ouvir Respostas**: 🔊
  - Ouça a resposta do modelo apertando o botão de play logo abaixo da resposta em texto.
  
- **Seleção de Sotaque**: 🌍
  - Personalize a experiência escolhendo o sotaque que o modelo de LLM irá usar nas respostas faladas.
""")

# Seção: Página de Conversação
st.header("💬 Conversação")

st.markdown("""
Nesta página, você pode treinar suas habilidades de conversação em inglês com um chat simples. Aqui está o que você pode fazer:

- **Conversar com o Chatbot**: 🗣️
  - Utilize um script simples com frases e perguntas básicas para praticar suas habilidades de conversação.
  - O chatbot responderá com frases simples, ajudando você a melhorar seu entendimento e fluência.

- **Gravação e Transcrição**: 🎙️
  - Grave suas respostas e veja como elas são transcritas para texto.
  - Compare suas respostas faladas com as transcritas para avaliar sua pronúncia e clareza.

- **Feedback e Prática**: 🔍
  - Receba feedback com base nas respostas do chatbot e use isso para ajustar e melhorar sua prática.
""")


st.header("🔄 From Portuguese to English")
"""
- **Tradução Português-Inglês**: 🌐
  - Traduza frases do português para o inglês de maneira natural, com foco em expressões e termos do dia a dia.
  - O Chatbot ajudará você a compreender por que certas expressões são usadas, oferecendo dicas de uso apropriado.
"""

# Seção: Página Text to Speech
st.header("🔡 Text to Speech")

st.markdown("""
Na página Text to Speech, você pode converter texto em áudio. As funcionalidades incluem:

- **Converter Texto em Áudio**: 🗣️
  - Cole o texto que você deseja ouvir e o app irá converter para áudio.

- **Ouvir e Repetir**: 🔄
  - Ouça o áudio quantas vezes quiser para melhorar sua compreensão auditiva.

- **Controle de Velocidade**: ⏩
  - Ajuste a velocidade de reprodução do áudio para acompanhar no seu próprio ritmo.

- **Download de Áudio**: 📥
  - Faça o download do áudio gerado para ouvir offline e praticar em qualquer lugar.
""")


# Seção: Página Speech to Text
st.header("🗣️ Speech to Text")

st.markdown("""
A página Speech to Text é ideal para treinar a sua dicção e fala. Confira o que você pode fazer:

- **Treinar Pronúncia**: 🎤 
  - Fale em inglês e veja a transcrição automática da sua fala.
  - Verifique se a sua pronúncia está correta e identifique áreas para melhorar.

- **Verificação de Pronúncia**: 📝
  - Compare o texto transcrito com o que você pretendia dizer para avaliar a precisão da sua pronúncia.
""")

# Conclusão
st.markdown("""
Esperamos que este manual ajude você a tirar o máximo proveito do seu app English Teacher. Explore cada página e aproveite as ferramentas para aprimorar suas habilidades em inglês! 🌟
""")
