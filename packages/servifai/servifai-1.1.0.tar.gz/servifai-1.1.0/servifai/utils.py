"""Utility functions for ServifAI"""

import logging
from pathlib import Path
from typing import List, Union
from rich.console import Console
from rich.table import Table

console = Console()
logger = logging.getLogger(__name__)

def validate_pdf_files(pdf_files: List[Union[str, Path]]) -> List[Path]:
    """Validate PDF file paths"""
    validated_files = []
    
    for pdf_file in pdf_files:
        path = Path(pdf_file)
        
        if not path.exists():
            raise FileNotFoundError(f"PDF file not found: {path}")
        
        if path.suffix.lower() != '.pdf':
            raise ValueError(f"File is not a PDF: {path}")
        
        if path.stat().st_size > 100 * 1024 * 1024:  # 100MB limit
            raise ValueError(f"PDF file too large (max 100MB): {path}")
        
        validated_files.append(path)
    
    return validated_files

def format_citations(citations: List) -> List[str]:
    """Format citations as readable strings"""
    formatted = []
    for citation in citations:
        text = f"[{citation.id}] {citation.source_document}"
        if citation.page_number:
            text += f", page {citation.page_number}"
        text += f" (relevance: {citation.relevance_score:.3f})"
        formatted.append(text)
    return formatted

def format_context_for_llm(search_result, max_length: int = 8000) -> str:
    """Format search results as context for LLM"""
    context_parts = [f"Query: {search_result.query}\n\nRelevant Information:\n"]
    current_length = len(context_parts[0])
    
    for citation in search_result.citations:
        if current_length >= max_length:
            break
        
        header = f"\n[Source {citation.id}] {citation.source_document}"
        if citation.page_number:
            header += f" (Page {citation.page_number})"
        header += f"\nRelevance: {citation.relevance_score:.3f}\n"
        
        available_length = max_length - current_length - len(header) - 50
        text = citation.text_preview
        if len(text) > available_length:
            text = text[:available_length] + "..."
        
        part = f"{header}Content: {text}\n"
        
        if current_length + len(part) > max_length:
            break
            
        context_parts.append(part)
        current_length += len(part)
    
    return "".join(context_parts)

def display_processing_results(result):
    """Display processing results in a table"""
    table = Table(title=f"Processing Results - {result.subscription_tier.title()}")
    
    table.add_column("Metric", style="cyan")
    table.add_column("Count", style="magenta")
    
    table.add_row("Documents", str(len(result.processed_documents)))
    table.add_row("Pages", str(result.total_pages))
    table.add_row("Text Chunks", str(result.total_text_chunks))
    table.add_row("Images", str(result.total_images))
    table.add_row("Tables", str(result.total_tables))
    table.add_row("Time", f"{result.processing_time_seconds:.2f}s")
    
    console.print(table)

def display_search_results(search_result):
    """Display search results"""
    console.print(f"\n🔍 Query: [bold]{search_result.query}[/bold]")
    console.print(f"📊 Found {search_result.total_results} results")
    
    for i, citation in enumerate(search_result.citations[:3]):
        console.print(f"\n[{i+1}] [bold]{citation.source_document}[/bold]")
        console.print(f"    ⭐ Score: {citation.relevance_score:.3f}")
        console.print(f"    📝 {citation.text_preview[:100]}...")

def create_env_file(file_path: str = ".env") -> None:
    """Create example .env file"""
    env_content = '''# ServifAI Configuration
SERVIFAI_API_KEY=sai_your_api_key_here
SERVIFAI_API_URL=https://api.syntheialabs.ai
SERVIFAI_TIMEOUT=300
SERVIFAI_LOG_LEVEL=INFO
'''
    
    with open(file_path, 'w') as f:
        f.write(env_content)
    
    console.print(f"✅ Created .env file: [bold]{file_path}[/bold]")

