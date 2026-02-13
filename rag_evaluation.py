"""
RAG Pipeline Evaluation Script
Tests retrieval quality, faithfulness, and correctness
"""

import chromadb
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()


# ============================================================================
# EVALUATION TEST SET
# ============================================================================

EVAL_QUESTIONS = [
    {
        "id": 1,
        "question": "What is Elevance Health's AI strategy?",
        "expected_answer": "Elevance Health has developed a comprehensive AI strategy that includes building a unified AI platform, implementing responsible AI practices, focusing on member-centered approaches, and deploying AI tools across the enterprise including ChatGPT.",
        "expected_keywords": ["Elevance", "AI strategy", "responsible AI", "unified platform", "member-centered"],
        "expected_sources": ["Fierce Healthcare", "Elevance"]
    },
    {
        "id": 2,
        "question": "How are payers using AI in 2025?",
        "expected_answer": "Payers are using AI in 2025 for various applications including prior authorization, utilization management, claims processing, fraud detection, member engagement, and predictive analytics. Multiple payer organizations made significant AI moves in 2025.",
        "expected_keywords": ["payers", "AI", "2025", "utilization management", "prior authorization"],
        "expected_sources": ["Becker's", "payer"]
    },
    {
        "id": 3,
        "question": "What are the top workforce challenges in healthcare for 2026?",
        "expected_answer": "The top workforce challenges include attracting and retaining clinical staff, addressing workforce shortages, managing burnout, and competing for talent in a tight labor market. Deloitte identifies workforce challenges as a top concern for 2026.",
        "expected_keywords": ["workforce", "challenges", "clinical staff", "retention", "2026", "Deloitte"],
        "expected_sources": ["Deloitte", "workforce"]
    },
    {
        "id": 4,
        "question": "How is AI being used in utilization management?",
        "expected_answer": "AI is being used in utilization management (UM) to automate prior authorization decisions, review medical necessity, predict utilization patterns, and streamline approval processes. NORC research discusses AI tools in utilization management.",
        "expected_keywords": ["AI", "utilization management", "UM", "prior authorization", "NORC"],
        "expected_sources": ["NORC", "utilization"]
    },
    {
        "id": 5,
        "question": "What cybersecurity concerns do health systems face?",
        "expected_answer": "Health systems face cybersecurity concerns including data breaches, ransomware attacks, protecting patient data, securing medical devices, and ensuring compliance with privacy regulations. These are ongoing challenges as healthcare becomes more digital.",
        "expected_keywords": ["cybersecurity", "health systems", "data breach", "security", "patient data"],
        "expected_sources": ["security", "cybersecurity", "health system"]
    }
]


# ============================================================================
# RAG PIPELINE SETUP
# ============================================================================

def format_docs(docs):
    """Format retrieved documents into a single string"""
    return "\n\n".join(doc.page_content for doc in docs)


def create_rag_chain(
    collection_name="healthcare_ai_500_large",
    model_name="gpt-4o-mini",
    temperature=0,
    k=5
):
    """Create RAG chain with custom prompt"""
    
    # Initialize embeddings
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Connect to ChromaDB
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Create Chroma vectorstore
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
    
    custom_prompt = ChatPromptTemplate.from_template(template)
    
    # Create RAG chain using LCEL
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | custom_prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain, retriever


# ============================================================================
# EVALUATION FUNCTIONS
# ============================================================================

def evaluate_retrieval(retrieved_docs, expected_keywords, expected_sources):
    """
    Evaluate if retrieval found relevant documents
    
    Checks:
    - Are expected keywords present in retrieved docs?
    - Are expected source types present?
    """
    # Combine all retrieved text
    retrieved_text = " ".join([doc.page_content.lower() for doc in retrieved_docs])
    
    # Check for expected keywords
    keyword_matches = sum(1 for keyword in expected_keywords if keyword.lower() in retrieved_text)
    keyword_score = keyword_matches / len(expected_keywords)
    
    # Check for expected sources
    source_matches = sum(1 for source in expected_sources if source.lower() in retrieved_text)
    source_score = source_matches / len(expected_sources) if expected_sources else 0
    
    # Overall retrieval quality
    overall_score = (keyword_score + source_score) / 2
    
    return {
        "passed": overall_score >= 0.5,  # Pass if 50%+ criteria met
        "keyword_score": keyword_score,
        "source_score": source_score,
        "overall_score": overall_score,
        "keyword_matches": keyword_matches,
        "total_keywords": len(expected_keywords)
    }


def evaluate_faithfulness(answer, retrieved_docs):
    """
    Evaluate if answer is grounded in context (not hallucinated)
    
    Checks:
    - Does answer contain information from retrieved docs?
    - Are there unsupported claims?
    """
    retrieved_text = " ".join([doc.page_content.lower() for doc in retrieved_docs])
    answer_lower = answer.lower()
    
    # Simple heuristic: check if answer mentions things from context
    # A more sophisticated approach would use an LLM to judge
    
    # Red flags for hallucination
    hallucination_flags = [
        "I don't have specific information" in answer,
        "the context doesn't mention" in answer,
        "not provided in the context" in answer
    ]
    
    if any(hallucination_flags):
        # Answer admits lack of information - that's actually good (not hallucinating)
        return {"passed": True, "reason": "Answer acknowledges limitations"}
    
    # Check if answer uses content from context
    # Extract key phrases from answer (simple approach)
    answer_phrases = answer.split(".")[:3]  # First 3 sentences
    
    grounded_sentences = 0
    for phrase in answer_phrases:
        if len(phrase.strip()) < 10:
            continue
        # Check if key words from phrase appear in context
        words = [w for w in phrase.lower().split() if len(w) > 4][:3]
        if any(word in retrieved_text for word in words):
            grounded_sentences += 1
    
    passed = grounded_sentences >= len([p for p in answer_phrases if len(p.strip()) >= 10]) * 0.7
    
    return {
        "passed": passed,
        "reason": f"Grounded sentences: {grounded_sentences}/{len(answer_phrases)}"
    }


def evaluate_correctness(answer, expected_answer, expected_keywords):
    """
    Evaluate if answer is correct based on expected answer
    
    Checks:
    - Does answer contain expected key information?
    - Does it align with expected answer?
    """
    answer_lower = answer.lower()
    
    # Check for expected keywords in answer
    keyword_matches = sum(1 for keyword in expected_keywords if keyword.lower() in answer_lower)
    keyword_score = keyword_matches / len(expected_keywords)
    
    # Simple correctness heuristic
    passed = keyword_score >= 0.4  # At least 40% of key concepts present
    
    return {
        "passed": passed,
        "keyword_score": keyword_score,
        "keyword_matches": keyword_matches,
        "total_keywords": len(expected_keywords),
        "reason": f"Contains {keyword_matches}/{len(expected_keywords)} key concepts"
    }


# ============================================================================
# MAIN EVALUATION RUNNER
# ============================================================================

def run_evaluation():
    """Run full evaluation on test set"""
    
    print("="*80)
    print(" RAG PIPELINE EVALUATION")
    print("="*80)
    print(f"\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Test Questions: {len(EVAL_QUESTIONS)}")
    print(f"Evaluation Criteria: Retrieval Quality, Faithfulness, Correctness")
    print("\n" + "="*80)
    
    # Initialize RAG chain
    print("\n⚙️  Initializing RAG chain...")
    try:
        rag_chain, retriever = create_rag_chain(
            collection_name="healthcare_ai_500_large",
            model_name="gpt-4o-mini",
            temperature=0,
            k=5
        )
        print("✅ RAG chain initialized\n")
    except Exception as e:
        print(f"❌ Error initializing RAG chain: {e}")
        return
    
    # Track results
    results = []
    retrieval_passes = 0
    faithfulness_passes = 0
    correctness_passes = 0
    
    # Run each test
    for i, test in enumerate(EVAL_QUESTIONS, 1):
        print("\n" + "="*80)
        print(f"TEST {test['id']}/{len(EVAL_QUESTIONS)}")
        print("="*80)
        print(f"\n❓ Question: {test['question']}")
        print(f"\n📋 Expected Answer: {test['expected_answer'][:150]}...")
        
        try:
            # Get retrieved documents
            retrieved_docs = retriever.invoke(test['question'])
            
            # Get answer from RAG
            answer = rag_chain.invoke(test['question'])
            
            print(f"\n💡 Generated Answer:\n{answer}")
            
            # Evaluate retrieval
            print(f"\n{'─'*80}")
            print("📊 EVALUATION RESULTS:")
            print(f"{'─'*80}")
            
            retrieval_eval = evaluate_retrieval(
                retrieved_docs,
                test['expected_keywords'],
                test['expected_sources']
            )
            retrieval_pass = retrieval_eval['passed']
            retrieval_passes += retrieval_pass
            
            print(f"\n1️⃣  RETRIEVAL QUALITY: {'✅ PASS' if retrieval_pass else '❌ FAIL'}")
            print(f"   - Overall Score: {retrieval_eval['overall_score']:.1%}")
            print(f"   - Keywords Found: {retrieval_eval['keyword_matches']}/{retrieval_eval['total_keywords']}")
            print(f"   - Keyword Score: {retrieval_eval['keyword_score']:.1%}")
            print(f"   - Source Score: {retrieval_eval['source_score']:.1%}")
            
            # Evaluate faithfulness
            faithfulness_eval = evaluate_faithfulness(answer, retrieved_docs)
            faithfulness_pass = faithfulness_eval['passed']
            faithfulness_passes += faithfulness_pass
            
            print(f"\n2️⃣  FAITHFULNESS (Grounded): {'✅ PASS' if faithfulness_pass else '❌ FAIL'}")
            print(f"   - Reason: {faithfulness_eval['reason']}")
            
            # Evaluate correctness
            correctness_eval = evaluate_correctness(
                answer,
                test['expected_answer'],
                test['expected_keywords']
            )
            correctness_pass = correctness_eval['passed']
            correctness_passes += correctness_pass
            
            print(f"\n3️⃣  CORRECTNESS: {'✅ PASS' if correctness_pass else '❌ FAIL'}")
            print(f"   - {correctness_eval['reason']}")
            
            # Store results
            results.append({
                'question': test['question'],
                'answer': answer,
                'retrieval': retrieval_pass,
                'faithfulness': faithfulness_pass,
                'correctness': correctness_pass,
                'retrieval_eval': retrieval_eval,
                'faithfulness_eval': faithfulness_eval,
                'correctness_eval': correctness_eval
            })
            
            print(f"\n📚 Top 3 Retrieved Sources:")
            for j, doc in enumerate(retrieved_docs[:3], 1):
                print(f"   [{j}] {doc.page_content[:100]}...")
            
        except Exception as e:
            print(f"\n❌ Error processing question: {e}")
            results.append({
                'question': test['question'],
                'error': str(e),
                'retrieval': False,
                'faithfulness': False,
                'correctness': False
            })
    
    # ============================================================================
    # FINAL SUMMARY
    # ============================================================================
    
    print("\n\n" + "="*80)
    print(" 📊 FINAL EVALUATION SUMMARY")
    print("="*80)
    
    total_tests = len(EVAL_QUESTIONS)
    
    print(f"\n🎯 ACCURACY SCORES:")
    print(f"   • Retrieval Quality:  {retrieval_passes}/{total_tests} ({retrieval_passes/total_tests:.1%})")
    print(f"   • Faithfulness:       {faithfulness_passes}/{total_tests} ({faithfulness_passes/total_tests:.1%})")
    print(f"   • Correctness:        {correctness_passes}/{total_tests} ({correctness_passes/total_tests:.1%})")
    
    overall_score = (retrieval_passes + faithfulness_passes + correctness_passes) / (total_tests * 3)
    print(f"\n   📈 Overall Score:     {overall_score:.1%}")
    
    print(f"\n{'='*80}")
    print("Individual Test Results:")
    print(f"{'='*80}\n")
    
    for i, result in enumerate(results, 1):
        if 'error' in result:
            print(f"Test {i}: ❌ ERROR - {result['error']}")
        else:
            r = '✅' if result['retrieval'] else '❌'
            f = '✅' if result['faithfulness'] else '❌'
            c = '✅' if result['correctness'] else '❌'
            print(f"Test {i}: Retrieval {r} | Faithfulness {f} | Correctness {c}")
            print(f"         Q: {result['question'][:60]}...")
    
    print(f"\n{'='*80}")
    print("Evaluation Complete!")
    print(f"{'='*80}\n")
    
    return results


if __name__ == "__main__":
    run_evaluation()
