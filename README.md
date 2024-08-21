# Arthur English Chatbot

**Description:** This project is a chatbot integrated with audio recognition and generation functionalities, using various language models to offer interactions in different languages and voices.

## 🏆 Objective

The primary goal of the Arthur English Chatbot project is to provide an interactive chatbot experience that leverages advanced language models and audio technologies. This chatbot is designed to:

- **Facilitate Language Learning:** Help users practice and improve their English language skills through interactive conversations.
- **Provide Several Accents:** Offer interactions in different accents, catering to a diverse audience.
- **Generate and Play Audio:** Convert text responses into audio and play them back, enhancing the conversational experience.

## 🧠 Language Models Used

The chatbot leverages several state-of-the-art language models to deliver diverse and versatile interactions:

- **Llama 3.1 70B Versatile:** A powerful model known for its broad capabilities and flexibility in various conversational contexts.
- **Llama 3 70B 8192:** A large model with high performance, suited for detailed and nuanced conversations.
- **Mixtral 8x7B 32768:** A model designed for extensive context handling and complex interactions.
- **Gemma 2 9B IT:** Focused on specific tasks with refined capabilities in generating responses.
- **Llama 3 Groq 70B 8192 Tool Use Preview:** An advanced model with enhanced tool usage features for specific applications.

## 💻 Installation

### Clone the Repository

![GitHub](https://img.shields.io/badge/GitHub-Clone-blue)

```bash
git clone https://github.com/devarthurguilherme/arthurenglishchatbot.git
cd arthurenglishchatbot
```

### Install dependencies:

Create a virtual environment and install the required dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### Ensure `.env` File Configuration

Ensure that the `.env` file contains the necessary variables, including [**GROQ_API_KEY**](https://console.groq.com/keys).

## 🚀 Usage:

### Run the application:

```bash
streamlit run app.py
```

### Interact with the chatbot:

- Use the sidebar to record audio or select a model and voice.
- Type a message to start the conversation.
- The chatbot can generate and play audio based on your inputs and the model's responses.

## 💬 Feedback:

I am thrilled to have tested my skills with this project and excited to share it with you! I welcome any feedback, suggestions, or comments you may have. Your input is valuable and will help improve the project. Feel free to reach out with your thoughts or if you have any questions!

## 📧 Contact:

For questions or suggestions, please contact me on [LinkedIn](https://www.linkedin.com/in/arthurguilherme92/).
