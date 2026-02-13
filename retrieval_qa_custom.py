"""
RAG System with Custom Prompt Template
Healthcare AI RAG System with LangChain LCEL (Modern Approach)
"""

import chromadb
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os

load_dotenv()


def create_custom_prompt():
    """
    Create a custom prompt template for healthcare AI queries
    """
    template = """You are a healthcare AI expert assistant. Use the following pieces of context to answer the question at the end.
    
Context from healthcare AI knowledge base:
{context}

Guidelines:
- Provide accurate, detailed answers based on the context
- If the context doesn't contain enough information, say so
- Cite specific details from the context when possible
- Focus on healthcare AI, payers, and health systems
- Be concise but comprehensive

Question: {question}

Answer:"""

    return ChatPromptTemplate.from_template(template)


def format_docs(docs):
    """Format retrieved documents into a single string"""
    return "\n\n".join(doc.page_content for doc in docs)


def create_rag_chain(
    collection_name="healthcare_ai_500_large",
    model_name="gpt-4o-mini",
    temperature=0,
    k=5
):
    """
    Create a RAG chain with custom prompt using LCEL
    
    Args:
        collection_name: ChromaDB collection name
        model_name: OpenAI model to use
        temperature: Model temperature (0 = deterministic)
        k: Number of documents to retrieve
    """
    # Initialize embeddings
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Connect to ChromaDB
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Create Chroma vectorstore from existing collection
    vectorstore = Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=embeddings
    )
    
    # Create retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )
    
    # Initialize LLM
    llm = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create custom prompt
    custom_prompt = create_custom_prompt()
    
    # Create RAG chain using LCEL
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | custom_prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain, retriever


def query_with_rag(question, rag_chain, retriever):
    """
    Query using the RAG chain
    
    Args:
        question: User's question
        rag_chain: RAG chain instance
        retriever: Retriever instance to get source docs
    """
    print(f"\n{'='*70}")
    print(f"🔍 Question: {question}")
    print(f"{'='*70}\n")
    
    # Get source documents
    source_docs = retriever.invoke(question)
    
    # Get response from RAG chain
    answer = rag_chain.invoke(question)
    
    # Display answer
    print(f"💡 Answer:\n{answer}\n")
    
    # Display source documents
    print(f"{'='*70}")
    print(f"📚 Source Documents (Top {len(source_docs)} chunks):\n")
    
    for i, doc in enumerate(source_docs, 1):
        metadata = doc.metadata
        content = doc.page_content
        
        print(f"[{i}] Chunk ID: {metadata.get('id', 'N/A')}")
        print(f"    Preview: {content[:200]}...")
        print()
    
    return {"answer": answer, "source_documents": source_docs}


def main():
    """
    Interactive RAG interface with custom prompt
    """
    print("="*70)
    print(" Healthcare AI RAG System with Custom Prompt (LCEL)")
    print("="*70)
    print()
    print("Configuration:")
    print("  - Collection: healthcare_ai_500_large")
    print("  - Model: gpt-4o-mini")
    print("  - Embeddings: text-embedding-3-large")
    print("  - Approach: LangChain Expression Language (LCEL)")
    print("  - Retrieved Docs: 5")
    print()
    print("="*70)
    
    # Create RAG chain
    print("\n⚙️  Initializing RAG chain...")
    try:
        rag_chain, retriever = create_rag_chain(
            collection_name="healthcare_ai_500_large",
            model_name="gpt-4o-mini",
            temperature=0,
            k=5
        )
        print("✅ RAG chain ready!\n")
    except Exception as e:
        print(f"❌ Error initializing chain: {e}")
        print("\nMake sure:")
        print("  1. Virtual environment is activated: source venv_py312/bin/activate")
        print("  2. ChromaDB has data in ./chroma_db/")
        print("  3. OPENAI_API_KEY is set in .env")
        return
    
    # Example queries
    example_queries = [
        "What is Elevance Health's AI strategy?",
        "How are payers using AI in 2025?",
        "What are the workforce challenges in healthcare?",
        "How is AI being used in utilization management?",
        "What are the cybersecurity concerns for health systems?",
    ]
    
    print("\n📚 Example Queries:")
    for i, q in enumerate(example_queries, 1):
        print(f"  {i}. {q}")
    
    print("\n" + "="*70)
    
    # Interactive mode
    while True:
        print("\nEnter your question (or 'quit' to exit, 'examples' to see list):")
        query = input("> ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if query.lower() == 'examples':
            for i, q in enumerate(example_queries, 1):
                print(f"  {i}. {q}")
            continue
        
        if query.lower().startswith('ex') and len(query) > 2 and query[2:].isdigit():
            # User typed "ex1", "ex2", etc.
            idx = int(query[2:]) - 1
            if 0 <= idx < len(example_queries):
                query = example_queries[idx]
            else:
                print("Invalid example number")
                continue
        
        if not query:
            continue
        
        try:
            result = query_with_rag(query, rag_chain, retriever)
        except Exception as e:
            print(f"❌ Error: {e}")
            print("\nTry a different question or check your configuration.")


if __name__ == "__main__":
    main()
