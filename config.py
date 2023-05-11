from langchain.chat_models import ChatOpenAI
import os
OPENAI_API_KEY = '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'
VECTORSTORE_DIRECTORY = './data/vectorstore/'

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
CHAT_MODEL = ChatOpenAI(temperature=.25)