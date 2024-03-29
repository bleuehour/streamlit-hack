import os
import streamlit as st
from templates.prompts import template
## llm imports
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAIChat
from templates.prompts import template
os.environ["OPENAI_API_KEY"] = st.secrets["openAiKey"]

llm = ChatOpenAI(temperature=0.5,model_name="gpt-3.5-turbo")


def runllm(lang,data,memory):
    prompt = PromptTemplate(input_variables=["history","language", "human_input"], template=template)

    llm_chain = LLMChain(llm=llm, prompt=prompt, memory=memory, verbose=True)

    res = llm_chain.run({"language":lang,"human_input":data})

    return res


