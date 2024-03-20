from prompt_templates import memory_prompt_template
from langchain.chains import LLMChain
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def create_llm(model_path = config['model_path']['large'], model_type = config["model_type"], model_config = config["model_config"]):
    llm = CTransformers(model=model_path,model_type=model_type, config=model_config)
    return llm

def create_embeddings(embedding_path = config['embeddings_path']):
    return HuggingFaceInstructEmbeddings(embedding_path)

def create_chat_memory(chat_history):
    return ConversationBufferWindowMemory(memory_key='history', chat_memory=chat_history, k=2)

def create_prompt_from_template(template):
    return PromptTemplate.from_template(template)

def create_llm_chain(llm, chat_prompt,memory):
    return LLMChain(llm=llm, prompt=chat_prompt, memory=memory, return_final_only=True)

def load_normal_chain(chat_history):
    return chatChain(chat_history)

class chatChain:
    def __init__(self, chat_history):
        self.memory = create_chat_memory(chat_history)
        llm = create_llm()
        chat_prompt = create_prompt_from_template(memory_prompt_template)
        self.llm_chain = create_llm_chain(llm,chat_prompt,self.memory)

    def run(self, user_input):
        return self.llm_chain.run(human_input=user_input, history=self.memory.chat_memory.messages, stop="Human:")