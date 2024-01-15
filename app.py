import os
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from components.st_custom_components import st_audiorec
from tts.polly import synthesize_speech
from templates.maps import language_map,emojis,scen_emoj
import info.text
from utils.process import main
from chain.llms import runllm
from utils.styles import styles

from IPython.display import Audio

 

### STYLES

### MISC
def chatclear():
    if msgs.messages:
        msgs.clear()
        print("clear")

### MESSAGE MEMORY  
msgs = StreamlitChatMessageHistory(key="langchain_messages")
memory = ConversationBufferMemory(chat_memory=msgs,memory_key="history",input_key="human_input")

### VIEW
buff, col, buff2 = st.columns([30,6,1])

current_lang = col.selectbox('Language',(None,'fr','ja',"zh"))

st.title("CONVO.AI 🗺")

scenario = st.selectbox("Pick a scenario",
(None,"Introduce Yourself - Speaking","Answer questions on a piece of text - Reading")
)
### STATE

if "load_state" not in st.session_state or st.session_state.load_state != [scenario,current_lang]:
    chatclear()
    st.session_state.load_state = [scenario,current_lang]

### SIDEBAR 
if scenario and current_lang:
    titletext = scenario
else:
    titletext = "Pick a language and scenario"


st.sidebar.title(titletext + " " + scen_emoj[titletext])
if scenario == "Introduce Yourself - Speaking":
    st.sidebar.subheader("Conversation starters")
    st.sidebar.text(info.text.intro[current_lang])

if scenario == "Answer questions on a piece of text - Reading":
    st.sidebar.subheader("Read")
    st.sidebar.text("hello")



### AUDIO COMPONENT  
if scenario == "Introduce Yourself - Speaking" and current_lang:
    _wav_audio_data = st_audiorec(scenario=scenario,lang=current_lang)


### MESSAGES
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)


#### SCENARIOS
if scenario == "Introduce Yourself - Speaking" and current_lang:

    if "audio" not in st.session_state or st.session_state["audio"] == [scenario,current_lang]:
        data = main(_wav_audio_data,current_lang)
    else:
        data = None
    
    st.session_state["audio"]= [scenario,current_lang]
    
    if data:
        st.chat_message("Human").write(data)
        response = runllm(lang=language_map[current_lang],data=data,memory=memory)
        st.chat_message("Ai").write(response)
        if response:
            st.write(Audio(synthesize_speech(response,current_lang),autoplay=True))
###
if scenario == "Answer questions on a piece of text - Reading" and current_lang:
    pass




