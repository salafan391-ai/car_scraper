import asyncio
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_community.document_loaders.json_loader import JSONLoader
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
import json
from langchain_core.vectorstores import InMemoryVectorStore
from uuid import uuid4
from langchain_core.documents import Document


json_path = "/Users/amd/my_scrapping/autobell/autobell_data/final_json/detail_json_2024-11-12.json"
llm = OllamaLLM(model="llama3")
embed_model = OllamaEmbeddings(
    model="llama3",
)

# loader = JSONLoader(
#     file_path=json_path,
#     jq_schema=".[].title",
#     text_content=True,
#     # json_lines=True,
# )
# data = loader.load()
# print(data)


# vector_store = Chroma(
#     collection_name="example_collection",
#     embedding_function=embed_model,
#     persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
# )

# document_1 = Document(
#     page_content="I had chocolate chip pancakes and scrambled eggs for breakfast this morning.",
#     metadata={"source": "tweet"},
#     id=1,
# )

# document_2 = Document(
#     page_content="The weather forecast for tomorrow is cloudy and overcast, with a high of 62 degrees.",
#     metadata={"source": "news"},
#     id=2,
# )

# document_3 = Document(
#     page_content="Building an exciting new project with LangChain - come check it out!",
#     metadata={"source": "tweet"},
#     id=3,
# )

# document_4 = Document(
#     page_content="Robbers broke into the city bank and stole $1 million in cash.",
#     metadata={"source": "news"},
#     id=4,
# )

# document_5 = Document(
#     page_content="Wow! That was an amazing movie. I can't wait to see it again.",
#     metadata={"source": "tweet"},
#     id=5,
# )

# document_6 = Document(
#     page_content="Is the new iPhone worth the price? Read this review to find out.",
#     metadata={"source": "website"},
#     id=6,
# )

# document_7 = Document(
#     page_content="The top 10 soccer players in the world right now.",
#     metadata={"source": "website"},
#     id=7,
# )

# document_8 = Document(
#     page_content="LangGraph is the best framework for building stateful, agentic applications!",
#     metadata={"source": "tweet"},
#     id=8,
# )

# document_9 = Document(
#     page_content="The stock market is down 500 points today due to fears of a recession.",
#     metadata={"source": "news"},
#     id=9,
# )

# document_10 = Document(
#     page_content="I have a bad feeling I am going to get deleted :(",
#     metadata={"source": "tweet"},
#     id=10,
# )

# documents = [
#     document_1,
#     document_2,
#     document_3,
#     document_4,
#     document_5,
#     document_6,
#     document_7,
#     document_8,
#     document_9,
#     document_10,
# ]
# uuids = [str(uuid4()) for _ in range(len(documents))]

# vector_store.add_documents(documents=documents, ids=uuids)






# text = "LangChain is the framework for building context-aware reasoning applications"

# vectorstore = InMemoryVectorStore.from_texts(
#     [text],
#     embedding=embed_model,
# )

# # Use the vectorstore as a retriever
# retriever = vectorstore.as_retriever()
# # Retrieve the most similar text
# retrieved_documents = retriever.invoke("What is LangChain in Arabic?")

# # show the retrieved document's content
# print(retrieved_documents[0].page_content)
# single_vector = embed_model.embed_query(text)
# print(str(single_vector)[:100])  # Show the first 100 characters of the vector

# text2 = (
#     "LangGraph is a library for building stateful, multi-actor applications with LLMs"
# )
# two_vectors = embed_model.embed_documents([text, text2])
# for vector in two_vectors:
#     print(str(vector)[:100])  # Show the first 100 characters of the vector
