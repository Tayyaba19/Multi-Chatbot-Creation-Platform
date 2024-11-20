import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import streamlit as st
from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
import hashlib
from PyPDF2 import PdfReader

# Load environment variables
load_dotenv()

# Initialize session state
def init_session_state():
    if 'users' not in st.session_state:
        st.session_state['users'] = {}
    if 'user_chatbots' not in st.session_state:
        st.session_state['user_chatbots'] = []
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'login_time' not in st.session_state:
        st.session_state['login_time'] = None

class UserManager:
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def validate_email(email: str) -> bool:
        import re
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def register_user(username: str, email: str, password: str) -> tuple[bool, str]:
        if not username or not email or not password:
            return False, "All fields are required"
        
        if not UserManager.validate_email(email):
            return False, "Invalid email format"
            
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
            
        if username in st.session_state['users']:
            return False, "Username already exists"
            
        st.session_state['users'][username] = {
            'email': email,
            'password': UserManager.hash_password(password),
            'created_at': datetime.now()
        }
        return True, "Registration successful"

    @staticmethod
    def login_user(username: str, password: str) -> tuple[bool, str]:
        if username not in st.session_state['users']:
            return False, "Invalid credentials"
            
        if st.session_state['users'][username]['password'] != UserManager.hash_password(password):
            return False, "Invalid credentials"
            
        st.session_state['logged_in'] = True
        st.session_state['username'] = username
        st.session_state['login_time'] = datetime.now()
        return True, "Login successful"

class ChatbotManager:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
        self.llm = ChatOpenAI(temperature=0.4)

    def process_document(self, file) -> Optional[str]:
        try:
            if file.type == "application/pdf":
                pdf_reader = PdfReader(file)
                return "\n".join([page.extract_text() for page in pdf_reader.pages])
            elif file.type == "text/plain":
                return file.getvalue().decode("utf-8")
            else:
                return None
        except Exception as e:
            st.error(f"Error processing document: {e}")
            return None

    def create_chatbot(self, name: str, description: str, personality: str, 
                      file_content: str, creator: str) -> tuple[bool, str]:
        try:
            # Process document
            chunks = self.text_splitter.split_text(file_content)
            documents = [Document(page_content=chunk) for chunk in chunks]
            
            # Create vector store
            vectorstore = FAISS.from_documents(documents, self.embeddings)
            
            # Create personality prompt template
            personality_prompts = {
                "Friendly": "You are a friendly and helpful assistant. Respond in a casual, approachable manner.",
                "Formal": "You are a professional and formal assistant. Maintain a business-appropriate tone.",
                "Witty": "You are a witty and clever assistant with a good sense of humor. Include appropriate jokes or wordplay."
            }
            
            # Updated prompt template with better formatting
            prompt_template = f"""{personality_prompts.get(personality, personality_prompts["Formal"])}

Using the following context information, please answer the question. If the answer cannot be found in the context, say so.

Context:
{{context}}

Question: {{question}}

Answer: """
            
            # Create chatbot object
            chatbot = {
                'name': name,
                'description': description,
                'personality': personality,
                'created_at': datetime.now(),
                'creator': creator,
                'embeddings': vectorstore,
                'prompt_template': prompt_template
            }
            
            st.session_state['user_chatbots'].append(chatbot)
            return True, "Chatbot created successfully"
            
        except Exception as e:
            return False, f"Error creating chatbot: {e}"

    def get_chatbot_response(self, chatbot: Dict, question: str) -> str:
        try:
            retriever = chatbot['embeddings'].as_retriever(
                search_type="similarity", 
                search_kwargs={"k": 3}
            )
            
            # Get relevant documents
            docs = retriever.get_relevant_documents(question)
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Construct the full prompt
            full_prompt = (
                chatbot['prompt_template'].format(
                    context=context,
                    question=question
                )
            )
            
            # Generate response using the LLM
            response = self.llm.invoke(full_prompt)
            
            return response.content if hasattr(response, 'content') else str(response)
            
        except Exception as e:
            return f"Error generating response: {e}"

def main():
    st.title("Multi-Chatbot Creation Platform")
    
    init_session_state()
    user_manager = UserManager()
    chatbot_manager = ChatbotManager()
    
    # Check session timeout
    if st.session_state.get('login_time'):
        if datetime.now() - st.session_state['login_time'] > timedelta(hours=24):
            st.session_state['logged_in'] = False
            st.warning("Session expired. Please login again.")
    
    # Authentication sidebar
    with st.sidebar:
        if not st.session_state['logged_in']:
            st.title("Authentication")
            tab1, tab2 = st.tabs(["Login", "Register"])
            
            with tab1:
                login_username = st.text_input("Username", key="login_username")
                login_password = st.text_input("Password", type="password", key="login_password")
                if st.button("Login"):
                    success, message = user_manager.login_user(login_username, login_password)
                    st.write(message)
            
            with tab2:
                reg_username = st.text_input("Username", key="reg_username")
                reg_email = st.text_input("Email", key="reg_email")
                reg_password = st.text_input("Password", type="password", key="reg_password")
                if st.button("Register"):
                    success, message = user_manager.register_user(reg_username, reg_email, reg_password)
                    st.write(message)
        else:
            st.write(f"Logged in as {st.session_state['username']}")
            if st.button("Logout"):
                st.session_state['logged_in'] = False
                st.session_state['login_time'] = None
    
    # Main content
    if st.session_state['logged_in']:
        tab1, tab2 = st.tabs(["Dashboard", "Create Chatbot"])
        
        with tab1:
            st.header("Your Chatbots")
            user_bots = [bot for bot in st.session_state['user_chatbots'] 
                        if bot['creator'] == st.session_state['username']]
            
            if user_bots:
                for bot in user_bots:
                    with st.expander(f"{bot['name']} - Created: {bot['created_at'].strftime('%Y-%m-%d %H:%M')}"):
                        st.write(f"Description: {bot['description']}")
                        st.write(f"Personality: {bot['personality']}")
                        
                        # Test interface
                        user_input = st.text_input("Ask a question:", key=f"input_{bot['name']}")
                        if st.button("Send", key=f"send_{bot['name']}"):
                            if user_input:
                                response = chatbot_manager.get_chatbot_response(bot, user_input)
                                st.write("Response:", response)
            else:
                st.info("You haven't created any chatbots yet.")
        
        with tab2:
            st.header("Create a New Chatbot")
            
            name = st.text_input("Chatbot Name")
            description = st.text_area("Description")
            personality = st.selectbox("Personality", ["Friendly", "Formal", "Witty"])
            
            uploaded_file = st.file_uploader("Upload Knowledge Base (PDF/TXT)", 
                                           type=['pdf', 'txt'])
            
            if st.button("Create Chatbot"):
                if name and description and uploaded_file:
                    if uploaded_file.size > 5 * 1024 * 1024:  # 5MB limit
                        st.error("File size exceeds 5MB limit")
                    else:
                        file_content = chatbot_manager.process_document(uploaded_file)
                        if file_content:
                            success, message = chatbot_manager.create_chatbot(
                                name, description, personality, 
                                file_content, st.session_state['username']
                            )
                            if success:
                                st.success(message)
                            else:
                                st.error(message)
                else:
                    st.warning("Please fill in all fields and upload a document")

if __name__ == "__main__":
    main()