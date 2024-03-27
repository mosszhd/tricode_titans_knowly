from prompt_templates import templates
from langchain.chains import LLMChain
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
import yaml
from accelerate import Accelerator

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def create_chat_memory(chat_history):
    return ConversationBufferWindowMemory(memory_key='history', chat_memory=chat_history, k=2)

def create_prompt_from_template(template):
    return PromptTemplate.from_template(template)

def create_llm_chain(llm, chat_prompt, memory):
    return LLMChain(llm=llm, prompt=chat_prompt, memory=memory, return_final_only=True)

def load_normal_chain(chat_history, model, selected_model):
    return chatChain(chat_history, model, selected_model)

class chatChain:
    def __init__(self, chat_history, model, selected_model):
        self.selected_model = selected_model
        self.memory = create_chat_memory(chat_history)
        llm = model
        chat_prompt = create_prompt_from_template(templates[selected_model])
        self.llm_chain = create_llm_chain(llm, chat_prompt, self.memory)

    def run(self, user_input):
        return self.llm_chain.run(human_input=user_input, history=self.memory.chat_memory.messages, stop=config[self.selected_model]["stop_tokens"])
    
