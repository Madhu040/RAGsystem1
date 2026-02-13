"""
RAG System - Healthcare AI Documents
Clean version for production use

This module provides the complete pipeline for:
1. Loading documents from web URLs
2. Splitting into chunks
3. Creating embeddings with OpenAI
4. Storing in ChromaDB vector database
"""

import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
import chromadb
import pickle
import time

# Load environment variables
load_dotenv()


class RAGSystem:
    """
    Complete RAG system for healthcare AI documents
    """
    
    def __init__(self, chunk_size=500, chunk_overlap=100, embedding_model="text-embedding-3-large"):
        """
        Initialize RAG system
        
        Args:
            chunk_size: Size of text chunks (default: 500)
            chunk_overlap: Overlap between chunks (default: 100)
            embedding_model: OpenAI embedding model (default: text-embedding-3-large)
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in .env file")
        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model_name = embedding_model
        
        # Initialize components
        self.embeddings = OpenAIEmbeddings(
            model=embedding_model,
            openai_api_key=self.api_key
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=self.api_key
        )
        
        print(f"✅ RAG System initialized")
        print(f"   • Embedding model: {embedding_model}")
        print(f"   • Chunk size: {chunk_size}")
        print(f"   • Chunk overlap: {chunk_overlap}")
    
    
    def load_documents_from_urls(self, urls):
        """
        Load documents from web URLs
        
        Args:
            urls: List of URLs or single URL string
            
        Returns:
            List of loaded documents
        """
        if isinstance(urls, str):
            urls = [urls]
        
        print(f"\n📄 Loading {len(urls)} document(s)...")
        
        documents = []
        for i, url in enumerate(urls, 1):
            try:
                print(f"   [{i}/{len(urls)}] Loading: {url[:60]}...")
                loader = WebBaseLoader(url)
                docs = loader.load()
                documents.extend(docs)
                print(f"      ✅ Loaded {len(docs[0].page_content):,} characters")
            except Exception as e:
                print(f"      ❌ Failed: {e}")
        
        print(f"\n✅ Loaded {len(documents)} document(s)")
        total_chars = sum(len(doc.page_content) for doc in documents)
        print(f"   Total content: {total_chars:,} characters")
        
        return documents
    
    
    def add_document(self, content, metadata=None):
        """
        Add a custom document
        
        Args:
            content: Document text content
            metadata: Optional metadata dict
            
        Returns:
            Document object
        """
        return Document(page_content=content, metadata=metadata or {})
    
    
    def create_chunks(self, documents):
        """
        Split documents into chunks
        
        Args:
            documents: List of Document objects
            
        Returns:
            List of chunked documents
        """
        print(f"\n✂️  Splitting into chunks...")
        chunks = self.text_splitter.split_documents(documents)
        
        chunk_sizes = [len(chunk.page_content) for chunk in chunks]
        print(f"✅ Created {len(chunks)} chunks")
        print(f"   • Smallest: {min(chunk_sizes)} characters")
        print(f"   • Largest: {max(chunk_sizes)} characters")
        print(f"   • Average: {sum(chunk_sizes)/len(chunk_sizes):.1f} characters")
        
        return chunks
    
    
    def create_embeddings(self, chunks, save_backup=True):
        """
        Create embeddings for chunks
        
        Args:
            chunks: List of Document chunks
            save_backup: Save embeddings to pickle file (default: True)
            
        Returns:
            List of embeddings
        """
        print(f"\n🔄 Creating embeddings...")
        print(f"   Model: {self.embedding_model_name}")
        print(f"   Processing {len(chunks)} chunks...")
        
        start_time = time.time()
        
        # Extract texts
        texts = [chunk.page_content for chunk in chunks]
        
        # Create embeddings
        embeddings_list = self.embeddings.embed_documents(texts)
        
        elapsed = time.time() - start_time
        print(f"✅ Created {len(embeddings_list)} embeddings in {elapsed:.1f}s")
        
        # Save backup
        if save_backup:
            data = {
                'chunks': chunks,
                'embeddings': embeddings_list,
                'metadata': [chunk.metadata for chunk in chunks],
                'embedding_model': self.embedding_model_name,
                'chunk_size': self.chunk_size,
                'chunk_overlap': self.chunk_overlap
            }
            with open('embeddings_backup.pkl', 'wb') as f:
                pickle.dump(data, f)
            print(f"💾 Backup saved to: embeddings_backup.pkl")
        
        return embeddings_list
    
    
    def store_in_chromadb(self, chunks, collection_name="healthcare_ai_docs"):
        """
        Store chunks in ChromaDB
        
        Args:
            chunks: List of Document chunks
            collection_name: Name for the collection
            
        Returns:
            ChromaDB collection object
        """
        print(f"\n💾 Storing in ChromaDB...")
        print(f"   Collection: {collection_name}")
        
        # Connect to ChromaDB
        client = chromadb.PersistentClient(path="./chroma_db")
        
        # Delete existing collection if it exists
        try:
            client.delete_collection(name=collection_name)
            print(f"   Deleted existing collection")
        except:
            pass
        
        # Create new collection
        collection = client.create_collection(
            name=collection_name,
            metadata={
                "description": f"Healthcare AI documents - {self.embedding_model_name}",
                "chunk_size": self.chunk_size,
                "chunk_overlap": self.chunk_overlap
            }
        )
        
        # Prepare data
        ids = [f"doc_{i}" for i in range(len(chunks))]
        texts = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        
        # Create embeddings
        embeddings_list = self.embeddings.embed_documents(texts)
        
        # Add to collection in batches
        batch_size = 50
        for i in range(0, len(chunks), batch_size):
            end_idx = min(i + batch_size, len(chunks))
            collection.add(
                ids=ids[i:end_idx],
                embeddings=embeddings_list[i:end_idx],
                documents=texts[i:end_idx],
                metadatas=metadatas[i:end_idx]
            )
            print(f"   Added batch {i//batch_size + 1}/{(len(chunks)-1)//batch_size + 1}")
        
        print(f"✅ Stored {len(chunks)} chunks in ChromaDB")
        print(f"   Location: ./chroma_db/")
        
        return collection
    
    
    def query(self, collection_name, query_text, n_results=5):
        """
        Query the ChromaDB collection
        
        Args:
            collection_name: Name of the collection
            query_text: Query string
            n_results: Number of results to return
            
        Returns:
            Query results
        """
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_collection(collection_name)
        
        # Embed query
        query_embedding = self.embeddings.embed_query(query_text)
        
        # Query collection
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        return results


def main():
    """
    Example usage
    """
    # Healthcare AI URLs
    urls = [
        "https://www.beckerspayer.com/virtual-care/14-payer-ai-moves-in-2025/",
        "https://www.deloitte.com/us/en/insights/industry/health-care/life-sciences-and-health-care-industry-outlooks/2026-global-health-care-outlook.html",
        "https://www.norc.org/research/projects/use-ai-utilization-management.html"
    ]
    
    print("="*70)
    print(" RAG System - Healthcare AI Documents")
    print("="*70)
    
    # Initialize system
    rag = RAGSystem(chunk_size=500, chunk_overlap=100)
    
    # Load documents
    documents = rag.load_documents_from_urls(urls)
    
    # Add custom document (Fierce Healthcare)
    fierce_content = """
    A look inside Elevance Health's artificial intelligence strategy
    
    The pace of digital innovation in healthcare is rapidly accelerating, and, for the team at Elevance Health, 
    a simple mantra remains at the heart of its efforts: Keep the member at the center.
    
    Ratnakar Lavu, executive vice president and chief digital information officer at Elevance, told Fierce Healthcare 
    in an interview that the perspective is born from his experience in consumer industries like retail, where many 
    patients form their expectations for digital experiences.
    """
    
    fierce_doc = rag.add_document(
        content=fierce_content,
        metadata={
            "source": "https://www.fiercehealthcare.com/payers/look-inside-elevance-healths-artificial-intelligence-strategy",
            "title": "Elevance Health AI Strategy"
        }
    )
    documents.append(fierce_doc)
    
    # Create chunks
    chunks = rag.create_chunks(documents)
    
    # Store in ChromaDB
    collection = rag.store_in_chromadb(chunks, collection_name="healthcare_ai_500_large")
    
    print("\n" + "="*70)
    print("✅ RAG System Ready!")
    print("="*70)
    print(f"\nTo query:")
    print(f"  results = rag.query('healthcare_ai_500_large', 'your question', n_results=5)")


if __name__ == "__main__":
    main()
