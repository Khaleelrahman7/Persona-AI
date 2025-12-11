from openai import OpenAI
from typing import List, Dict, Any
import json
import os
import asyncio
import httpx

class MemoryExtractor:
    """
    Memory Extraction Module that identifies:
    - User preferences
    - User emotional patterns
    - Facts worth remembering
    """
    
    def __init__(self):
        # Initialize NVIDIA API client
        # Use explicit http_client to avoid proxies compatibility issues
        http_client = httpx.Client(timeout=60.0)
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.getenv("NVIDIA_API_KEY", "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"),
            http_client=http_client
        )
        self.model = "mistralai/devstral-2-123b-instruct-2512"
    
    def _create_extraction_prompt(self, chat_history: List[Dict]) -> str:
        """Create structured prompt for memory extraction"""
        messages_text = "\n".join([
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in chat_history
        ])
        
        prompt = f"""Analyze the following chat conversation and extract structured memory information.

Chat History:
{messages_text}

Extract and return a JSON object with the following structure:
{{
    "preferences": [
        {{"preference": "description", "confidence": "high/medium/low", "context": "relevant quote"}}
    ],
    "emotional_patterns": [
        {{"pattern": "description", "emotion": "emotion_type", "triggers": ["trigger1", "trigger2"], "context": "relevant quote"}}
    ],
    "facts": [
        {{"fact": "description", "category": "personal/professional/other", "importance": "high/medium/low", "context": "relevant quote"}}
    ]
}}

Guidelines:
- Preferences: Extract likes, dislikes, habits, interests, values, goals
- Emotional patterns: Identify recurring emotional states, triggers, coping mechanisms, mood patterns
- Facts: Extract important personal information, relationships, achievements, constraints, commitments

Only include new information not already known. Be specific and include context quotes when possible.
Return ONLY valid JSON, no additional text."""

        return prompt
    
    async def extract(self, chat_history: List[Dict]) -> Dict[str, Any]:
        """Extract memory from chat history"""
        try:
            prompt = self._create_extraction_prompt(chat_history)
            
            # Run synchronous OpenAI call in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.15,
                    top_p=0.95,
                    max_tokens=4096,
                    stream=False
                )
            )
            
            content = response.choices[0].message.content.strip()
            
            # Try to extract JSON from response
            # Handle cases where response might have markdown code blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            # Parse JSON
            try:
                memory_data = json.loads(content)
            except json.JSONDecodeError:
                # Fallback: try to extract JSON object from text
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    memory_data = json.loads(json_match.group())
                else:
                    # Return empty structure if parsing fails
                    memory_data = {"preferences": [], "emotional_patterns": [], "facts": []}
            
            # Validate structure
            result = {
                "preferences": memory_data.get("preferences", []),
                "emotional_patterns": memory_data.get("emotional_patterns", []),
                "facts": memory_data.get("facts", [])
            }
            
            return result
            
        except Exception as e:
            print(f"Error in memory extraction: {e}")
            # Return empty structure on error
            return {
                "preferences": [],
                "emotional_patterns": [],
                "facts": []
            }
    
    def format_memory_summary(self, memory: Dict[str, Any]) -> str:
        """Format memory for display"""
        summary_parts = []
        
        if memory.get("preferences"):
            summary_parts.append("Preferences:")
            for pref in memory["preferences"]:
                summary_parts.append(f"  - {pref.get('preference', 'N/A')}")
        
        if memory.get("emotional_patterns"):
            summary_parts.append("\nEmotional Patterns:")
            for pattern in memory["emotional_patterns"]:
                summary_parts.append(f"  - {pattern.get('pattern', 'N/A')} ({pattern.get('emotion', 'N/A')})")
        
        if memory.get("facts"):
            summary_parts.append("\nFacts:")
            for fact in memory["facts"]:
                summary_parts.append(f"  - {fact.get('fact', 'N/A')}")
        
        return "\n".join(summary_parts) if summary_parts else "No new memory extracted."

