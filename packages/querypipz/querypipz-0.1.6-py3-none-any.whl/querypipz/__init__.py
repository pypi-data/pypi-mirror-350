from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("BIANXIE_API_KEY")
api_base = os.getenv("BIANXIE_BASE")



Settings.embed_model = OpenAIEmbedding(api_key=api_key,api_base =api_base)
Settings.llm = OpenAI(model="gpt-4o",api_base=api_base,api_key=api_key)

