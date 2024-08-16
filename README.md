### **APIs**

**Groq API:**

- Utilizado no cliente `client = Groq(api_key=os.environ.get("GROQ_API_KEY"))`. Este cliente é usado para interagir com o serviço Groq, que provavelmente fornece acesso a modelos de linguagem para completar tarefas de NLP.

**Edge TTS API:**

- Utilizado para gerar áudio a partir de texto. O módulo `edge_tts` é usado para criar e salvar o áudio a partir do texto fornecido, utilizando a função `generateAudio`.

**SpeechRecognition Library (Google Speech-to-Text API):**

- Usado na função `transcribeAudio` para converter áudio em texto. Utiliza o serviço de reconhecimento de fala do Google.

### **LLMs (Modelos de Linguagem de Grande Escala)**

**Llama Models:**

- Vários modelos de linguagem do Llama são utilizados no código, como:
  - `"llama-3.1-70b-versatile"`
  - `"llama3-70b-8192"`
  - `"llama-3.1-8b-instant"`
  - `"llama3-8b-8192"`
  - `"llama3-groq-70b-8192-tool-use-preview"`
  - `"llama3-groq-8b-8192-tool-use-preview"`
  - `"llama-guard-3-8b"`

**Groq Models:**

- Inclui modelos como:
  - `"mixtral-8x7b-32768"`
  - `"gemma2-9b-it"`
  - `"gemma-7b-it"`
