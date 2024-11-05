# Persona Creator & Chat Application

A Streamlit application that allows users to create and chat with custom personas using OpenAI's Assistant API.

## Features

- Create detailed personas with customizable traits, backgrounds, and expertise
- Upload reference documents to enhance persona knowledge
- Chat with created personas in real-time
- Download chat history and summaries
- Manage multiple personas
- Secure API key handling through Streamlit secrets

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd persona-creator-chat
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure Secrets in Streamlit Cloud:
   - Go to your Streamlit Cloud dashboard
   - Navigate to "Settings" > "Secrets"
   - Add your secrets in the following format:
     ```toml
     OPENAI_API_KEY = "your-api-key-here"
     OPENAI_ORGANIZATION = "your-org-id-here"  # Optional
     ```

4. Deploy on Streamlit Cloud:
   - Add the secrets in the Streamlit Cloud dashboard under "Settings" > "Secrets"
   - Connect your GitHub repository to Streamlit Cloud
   - Deploy the application

## Project Structure

```
.
├── requirements.txt          # Python dependencies
├── src/
├── src/
│   ├── main.py             # Application entry point
│   ├── config.py           # Configuration settings
│   ├── utils/              # Utility functions
│   ├── services/           # Business logic and API interactions
│   ├── components/         # UI components
│   └── pages/             # Application pages
└── README.md              # Project documentation
```

## Usage

1. Start the application:
```bash
streamlit run src/main.py
```

2. Creating a Persona:
   - Click "Create New Persona" in the sidebar
   - Fill in the persona details
   - Upload any reference documents
   - Click "Create Persona"

3. Chatting with a Persona:
   - Select a persona from the sidebar
   - Type your message in the chat input
   - Download chat history or get summaries using the buttons below

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

