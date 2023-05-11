from langchain.chat_models import ChatOpenAI
import os
from SECRET_API_KEY import KEY
OPENAI_API_KEY = KEY
VECTORSTORE_DIRECTORY = './data/vectorstore/'

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
CHAT_MODEL = ChatOpenAI(temperature=.25)