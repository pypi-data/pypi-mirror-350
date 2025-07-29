"""Main client for ServifAI API"""

import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
import httpx
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from .config import ServifAIConfig, SubscriptionTier
from .models import ProcessingResult, SearchResult, SubscriptionInfo
from .exceptions import (
    ServifAIException, AuthenticationError, RateLimitError, 
    ProcessingError, APIError, TimeoutError
)
from .utils import (
    validate_pdf_files, format_citations, format_context_for_llm,
    display_processing_results, display_search_results, console
)

logger = logging.getLogger(__name__)

class ServifAI:
    """
    ServifAI client for AI-powered PDF parsing and retrieval
    
    Supports three subscription tiers:
    - QUICKEST: Fastest processing
    - BALANCED: Optimal speed/accuracy balance
    - SECURED: Enterprise security
    """
    
    def __init__(
        self,
        config: Optional[ServifAIConfig] = None,
        config_file: str = ".env"
    ):
        """Initialize ServifAI client"""
        
        if config:
            self.config = config
        else:
            self.config = ServifAIConfig.from_env(config_file)
        
        self.client = httpx.AsyncClient(
            base_url=self.config.api_url,
            timeout=httpx.Timeout(self.config.timeout),
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "User-Agent": "ServifAI-Python/1.0.0",
                "Content-Type": "application/json"
            }
        )
        
        logging.basicConfig(level=getattr(logging, self.config.log_level.upper()))
        logger.info("ServifAI client initialized")
    
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make authenticated API request with error handling"""
        
        for attempt in range(self.config.max_retries + 1):
            try:
                response = await self.client.request(method, endpoint, **kwargs)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    raise AuthenticationError("Invalid or expired API key")
                elif response.status_code == 429:
                    raise RateLimitError("Rate limit exceeded")
                elif response.status_code >= 400:
                    raise APIError(f"API error: {response.status_code}", response.status_code)
                    
            except httpx.TimeoutException:
                if attempt == self.config.max_retries:
                    raise TimeoutError("Request timed out")
                await asyncio.sleep(2 ** attempt)
    
    def get_subscription_info(self) -> SubscriptionInfo:
        """Get current subscription information"""
        
        async def _get_info():
            response = await self._make_request("GET", "/api/v1/auth/subscription")
            return SubscriptionInfo(**response)
        
        return asyncio.run(_get_info())
    
    def create_session(self, session_id: Optional[str] = None) -> str:
        """Create a new processing session"""
        
        async def _create():
            data = {"session_id": session_id} if session_id else {}
            response = await self._make_request("POST", "/api/v1/sessions/create", json=data)
            return response["session_id"]
        
        session_id = asyncio.run(_create())
        console.print(f"✅ Created session: [bold]{session_id}[/bold]")
        return session_id
    
    def process_pdfs(
        self,
        pdf_files: Union[str, Path, List[Union[str, Path]]],
        session_id: Optional[str] = None,
        tier: Optional[SubscriptionTier] = None,
        show_progress: bool = True
    ) -> ProcessingResult:
        """Process PDF files with AI parsing"""
        
        async def _process():
            # Validate files
            if isinstance(pdf_files, (str, Path)):
                files = [pdf_files]
            else:
                files = pdf_files
            
            validated_files = validate_pdf_files(files)
            
            # Create session if needed
            if not session_id:
                session_response = await self._make_request("POST", "/api/v1/sessions/create")
                current_session = session_response["session_id"]
            else:
                current_session = session_id
            
            # Prepare file data
            files_data = []
            for file_path in validated_files:
                with open(file_path, 'rb') as f:
                    import base64
                    files_data.append({
                        "filename": file_path.name,
                        "content": base64.b64encode(f.read()).decode(),
                        "size": file_path.stat().st_size
                    })
            
            # Start processing
            process_data = {
                "session_id": current_session,
                "tier": tier.value if tier else None,
                "files": files_data
            }
            
            response = await self._make_request("POST", "/api/v1/documents/process", json=process_data)
            processing_id = response["processing_id"]
            
            # Poll for completion with progress
            if show_progress:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    TimeElapsedColumn(),
                    console=console
                ) as progress:
                    task = progress.add_task("Processing PDFs...", total=None)
                    
                    while True:
                        status_response = await self._make_request(
                            "GET", f"/api/v1/documents/status/{processing_id}"
                        )
                        
                        if status_response["status"] == "completed":
                            break
                        elif status_response["status"] == "failed":
                            raise ProcessingError(status_response.get("error", "Processing failed"))
                        
                        await asyncio.sleep(2)
            
            # Get results
            result_response = await self._make_request("GET", f"/api/v1/documents/result/{processing_id}")
            return ProcessingResult(**result_response)
        
        result = asyncio.run(_process())
        if show_progress:
            display_processing_results(result)
        return result
    
    def search(
        self,
        query: str,
        session_id: Optional[str] = None,
        top_k: int = 5,
        include_assets: bool = True,
        tier: Optional[SubscriptionTier] = None,
        show_results: bool = True
    ) -> SearchResult:
        """Search documents with AI-powered retrieval"""
        
        async def _search():
            search_data = {
                "query": query,
                "session_id": session_id,
                "top_k": top_k,
                "include_assets": include_assets,
                "tier": tier.value if tier else None
            }
            
            response = await self._make_request("POST", "/api/v1/search", json=search_data)
            return SearchResult(**response)
        
        result = asyncio.run(_search())
        if show_results:
            display_search_results(result)
        return result
    
    def get_citations(self, search_result: SearchResult) -> List[str]:
        """Format search results as citation strings"""
        return format_citations(search_result.citations)
    
    def get_context_for_llm(
        self,
        search_result: SearchResult,
        max_length: int = 8000
    ) -> str:
        """Format search results as context for LLM consumption"""
        return format_context_for_llm(search_result, max_length)
    
    def cleanup_session(self, session_id: str):
        """Clean up session and all associated data"""
        
        async def _cleanup():
            await self._make_request("DELETE", f"/api/v1/sessions/{session_id}")
        
        asyncio.run(_cleanup())
        console.print(f"🗑️  Cleaned up session: [bold]{session_id}[/bold]")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        asyncio.run(self.client.aclose())
