import os
## import API keys
### streamlit
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from components.st_custom_components import st_audiorec
from pydub import AudioSegment
from io import BytesIO
import assemblyai as aai
from tts.polly import synthesize_speech


## llm imports
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
os.environ["OPENAI_API_KEY"] = st.secrets["openAiKey"]



### memory 
msgs = StreamlitChatMessageHistory(key="langchain_messages")
memory = ConversationBufferMemory(chat_memory=msgs,
                                  memory_key="history",
    input_key="human_input")

buff, col, buff2 = st.columns([30,6,1])


option = col.selectbox(
    'Language',
    (None,'en', 'ja', 'fr',"es","ko"))


## Language select

st.title("CONVO.AI")


scenario = st.selectbox(
    "Pick a scenario",
    (None,"buy a train ticket","hello")
)



current_lang = option    



language_map = {"en": "English 💂🏼‍♂️","ja":"Japanese 🎌","fr":"French 🥐","es":"Spanish 🐂","ko":"Korean"}


if option:
    st.text(f"Converse in {language_map[current_lang]}")

#### AUDIO

wav_audio_data = st_audiorec(scenario=scenario,lang=current_lang)


def preprocess():
    if wav_audio_data is not None:
        audio = AudioSegment.from_wav(BytesIO(wav_audio_data))
        audio.export("./temp/file.wav", format="wav")


def transcribe():
    config = aai.TranscriptionConfig(language_code=current_lang)

    aai.settings.api_key = st.secrets["auth_key"]

    transcriber = aai.Transcriber()

    transcript = transcriber.transcribe("./temp/file.wav", config=config)


    return transcript.text


def main():
    if wav_audio_data is not None:
        preprocess()
        ans = transcribe()
        return ans



### Main app

scenario = None


llm = OpenAI(temperature=0.9)


template = """I am trying to learn {language}, you are a ticket seller at a train station and i am the user buying the ticket.

{history}
Human: {human_input}
You: """
prompt = PromptTemplate(input_variables=["history","language", "human_input"], template=template)

llm_chain = LLMChain(llm=llm, prompt=prompt, memory=memory, verbose=True)

for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

if prompt := main():
    st.chat_message("human").write(prompt)
    response = llm_chain.run({"language":language_map[current_lang],"human_input":prompt})
    st.chat_message("ai").write(response)
    if response:
        st.audio(synthesize_speech(response),format="mp3")


    





