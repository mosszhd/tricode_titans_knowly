from prompt_templates import templates
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts.prompt import PromptTemplate
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def get_conversation_chain(llm,selected_model):
    PROMPT = PromptTemplate(input_variables=['history', 'human_input'], template=templates[selected_model])
    conversation = ConversationChain(
        prompt=PROMPT,
        llm=llm,
        verbose=False,
        memory=ConversationBufferWindowMemory(k=2),
    )
    return conversation