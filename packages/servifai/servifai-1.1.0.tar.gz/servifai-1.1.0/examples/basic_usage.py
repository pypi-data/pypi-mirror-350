"""Basic usage example for ServifAI"""

from servifai import ServifAI

def main():
    # Initialize client
    client = ServifAI()
    
    # Check subscription
    sub_info = client.get_subscription_info()
    print(f"Subscription: {sub_info.tier}")
    print(f"Document limit: {sub_info.document_limit}")
    print(f"Expires: {sub_info.expires_at}")
    
    # Create a session
    session_id = client.create_session()
    
    # Process PDFs
    result = client.process_pdfs(["document.pdf"], session_id=session_id)
    
    # Search documents
    search_result = client.search(
        "What are the key findings?", 
        session_id=session_id,
        top_k=5,
        include_assets=True
    )
    
    # Get LLM-ready context
    context = client.get_context_for_llm(search_result)
    citations = client.get_citations(search_result)
    
    print(f"Context length: {len(context)} characters")
    print(f"Citations: {len(citations)}")
    
    # Use with any LLM
    llm_prompt = f"""
    Context: {context}
    
    Question: What are the key findings?
    
    Answer based on the context above and cite your sources.
    """
    
    print("Ready for LLM processing!")

if __name__ == "__main__":
    main()
