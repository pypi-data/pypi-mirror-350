"""Basic usage example for ServifAI"""

from servifai import ServifAI, SubscriptionTier

def main():
    # Initialize client
    client = ServifAI()
    
    # Check subscription
    sub_info = client.get_subscription_info()
    print(f"Subscription: {sub_info.tier}")
    
    # Process PDFs
    result = client.process_pdfs(["document.pdf"], tier=SubscriptionTier.BALANCED)
    
    # Search documents
    search_result = client.search("What are the key findings?", top_k=5)
    
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
