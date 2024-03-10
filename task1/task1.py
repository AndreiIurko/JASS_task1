import os
from langchain_community.document_loaders import JSONLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_together import Together
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")

llm = Together(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    temperature=0,
    top_k=1,
    together_api_key=TOGETHER_API_KEY
)

loader = JSONLoader(
    file_path='./data.json',
    jq_schema='.[]',
    text_content=False)

docs = loader.load()
vectorstore = Chroma.from_documents(documents=docs, embedding=HuggingFaceEmbeddings())
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 1})

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)
contextualize_q_chain = contextualize_q_prompt | llm | StrOutputParser()

qa_system_prompt = """You are a Paphos city travel assistant for question-answering tasks. \
Use the following pieces of retrieved context to answer the question. \
If the context is insufficient use your own knowledge. \
Use as little sentences as possible and keep the answer concise.\
DO NOT refer to context.

{context}"""
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)

def contextualized_question(input: dict):
    if input.get("chat_history"):
        return contextualize_q_chain
    else:
        return input["question"]

rag_chain = (
    RunnablePassthrough.assign(
        context=contextualized_question | retriever | format_docs
    )
    | qa_prompt
    | llm
)

if __name__ == "__main__":
    chat_history = []
    print("Hello and welcome dear user! I am an AI travel assistant and I am happy to provide you any information" \
        "about Pafos city. Print \"exit\" in case you want to end our conversation."
    )
    while(True):
        question = input("User: ")
        if question == "exit":
            break
        ai_response = rag_chain.invoke({"question": question, "chat_history": chat_history})
        print(f"Assistant: {ai_response}")
        chat_history.extend([HumanMessage(content=question), ai_response])
