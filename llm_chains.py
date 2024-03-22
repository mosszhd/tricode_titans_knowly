from prompt_templates import templates
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
import yaml
from accelerate import Accelerator
from langchain_core.output_parsers import StrOutputParser


with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def create_embeddings(embedding_path = config['embeddings_path']):
    return HuggingFaceInstructEmbeddings(embedding_path)

def create_chat_memory(chat_history):
    return ConversationBufferWindowMemory(memory_key='history', chat_memory=chat_history, k=2)
    
class newChatChain:
    def __init__(self, llm, selected_model, chat_history):
        prompt = PromptTemplate.from_template(template=templates[selected_model])
        memory = ConversationBufferWindowMemory(memory_key='history', chat_memory=chat_history, k=2)
        self.llm_chain = prompt | llm | StrOutputParser()

    def run(self, user_input, chat_history):
        return self.llm_chain.stream(input={"human_input": user_input, "history": chat_history})