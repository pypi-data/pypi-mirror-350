"""LLM integration examples"""

from servifai import ServifAI, SubscriptionTier

class LLMIntegration:
    
    def __init__(self):
        self.servifai = ServifAI()
    
    def openai_example(self, query: str, pdf_files: list):
        """OpenAI integration example"""
        
        # Process documents
        result = self.servifai.process_pdfs(pdf_files, tier=SubscriptionTier.BALANCED)
        
        # Search for context
        search_result = self.servifai.search(query, top_k=5)
        context = self.servifai.get_context_for_llm(search_result)
        citations = self.servifai.get_citations(search_result)
        
        # OpenAI prompt
        prompt = f"""
        Based on the following context, answer the question with citations.
        
        Context:
        {context}
        
        Citations:
        {chr(10).join(citations)}
        
        Question: {query}
        
        Provide a comprehensive answer with proper citations.
        """
        
        # Use with OpenAI (uncomment when you have API key)
        import openai
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
        
        #return {"prompt": prompt, "context": context, "citations": citations}
    
    def anthropic_example(self, query: str, pdf_files: list):
        """Anthropic Claude integration"""
        
        # Process with secured tier for enterprise use
        self.servifai.process_pdfs(pdf_files, tier=SubscriptionTier.SECURED)
        search_result = self.servifai.search(query, top_k=7)
        context = self.servifai.get_context_for_llm(search_result, max_length=10000)
        
        prompt = f"""Human: Based on the document context, answer this question: {query}

Context:
{context}

Please provide a detailed answer with citations.
"""

        # Use with Anthropic (uncomment when you have API key)
        import anthropic
        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
        
        #return {"prompt": prompt, "context": context}
    
    def local_llm_example(self, query: str, pdf_files: list):
        """Local LLM (Ollama/LlamaCpp) integration"""
        
        # Process with quickest tier for local processing
        self.servifai.process_pdfs(pdf_files, tier=SubscriptionTier.QUICKEST)
        search_result = self.servifai.search(query, top_k=3)
        context = self.servifai.get_context_for_llm(search_result, max_length=4000)
        
        # Shorter context for local models
        prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
        
        # Use with Ollama (uncomment when available)
        import ollama
        response = ollama.chat(model='llama2', messages=[
            {'role': 'user', 'content': prompt}
        ])
        return response['message']['content']
        
        #return {"prompt": prompt, "ready_for_local_llm": True}

# Usage example
def main():
    integration = LLMIntegration()
    pdf_files = ["document.pdf"]
    query = "What are the main conclusions?"
    
    # Try different LLM integrations
    openai_result = integration.openai_example(query, pdf_files)
    # anthropic_result = integration.anthropic_example(query, pdf_files)
    # local_result = integration.local_llm_example(query, pdf_files)
    
    print("All integrations ready!")

if __name__ == "__main__":
    main()
