# Multi-Chatbot Creation Platform

A streamlined platform for creating and managing multiple AI chatbots with customizable personalities and knowledge bases. This platform allows users to create, test, and manage multiple chatbots with different personalities and knowledge domains.

## 🌟 Features

### User Management
- User registration with email and password
- Secure login system with 24-hour session management
- Personal dashboard showing all created chatbots

### Chatbot Creation
- Step-by-step chatbot creation wizard
- Support for multiple document formats (PDF, TXT)
- Customizable chatbot personalities (Friendly, Formal, Witty)
- Real-time testing interface
- Document processing with semantic search capabilities

### Technical Features
- Document chunking and embedding generation
- Vector-based semantic search
- Personality-based response generation
- Session management and security features

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Tayyaba19/Multi-Chatbot-Creation-Platform.git
cd multi-chatbot-platform
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### Running the Application

1. Start the Streamlit server:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

## 📖 Usage

### Creating a New Chatbot
1. Register/Login to your account
2. Navigate to "Create Chatbot" tab
3. Fill in the chatbot details:
   - Name and description
   - Select personality type
   - Upload knowledge base document (PDF/TXT, max 5MB)
4. Click "Create Chatbot"

### Testing Your Chatbot
1. Go to the Dashboard tab
2. Find your chatbot in the list
3. Use the test interface to ask questions
4. Review responses and adjust as needed

## 🔧 Configuration

### Personality Types
- **Friendly**: Casual and approachable responses
- **Formal**: Professional and business-appropriate tone
- **Witty**: Includes appropriate humor and wordplay

### Document Processing
- Maximum file size: 5MB
- Supported formats: PDF, TXT
- Automatic text chunking for optimal processing

## 🛡️ Security Features
- Password hashing
- Session management
- Input validation
- File size and type validation

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Limitations
- Maximum file size of 5MB
- Requires OpenAI API key
- Session timeout after 24 hours
- Currently supports only PDF and TXT files

## 🔍 Troubleshooting

### Common Issues:
1. **OpenAI API Key Error**
   - Ensure your API key is correctly set in the `.env` file
   - Check API key permissions

2. **File Upload Issues**
   - Verify file size is under 5MB
   - Ensure file format is PDF or TXT

3. **Session Timeout**
   - Re-login required after 24 hours
   - Check internet connection

## 📮 Contact
For support or queries, please open an issue in the GitHub repository.