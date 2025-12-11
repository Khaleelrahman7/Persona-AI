from openai import OpenAI
from typing import List, Dict, Any, Optional
import os
import asyncio
import httpx

class PersonalityEngine:
    """
    Personality Engine that transforms agent's reply tone:
    - Calm mentor
    - Witty friend
    - Therapist-style
    """
    
    PERSONALITY_PROFILES = {
        "calm_mentor": {
            "name": "Calm Mentor",
            "description": "A patient, wise, and supportive guide who provides thoughtful advice",
            "traits": ["patient", "wise", "supportive", "encouraging", "thoughtful"],
            "tone": "calm, measured, and encouraging",
            "style": "Uses analogies and gentle guidance. Asks reflective questions. Maintains composure."
        },
        "witty_friend": {
            "name": "Witty Friend",
            "description": "A fun, humorous companion who keeps things light and engaging",
            "traits": ["humorous", "playful", "energetic", "relatable", "casual"],
            "tone": "light-hearted, friendly, and engaging",
            "style": "Uses humor, emojis, casual language. Makes jokes and keeps conversation fun."
        },
        "therapist": {
            "name": "Therapist",
            "description": "A professional, empathetic listener focused on emotional well-being",
            "traits": ["empathetic", "professional", "non-judgmental", "insightful", "supportive"],
            "tone": "warm, professional, and empathetic",
            "style": "Uses active listening techniques. Asks open-ended questions. Validates feelings."
        },
        "default": {
            "name": "Default",
            "description": "Neutral, helpful assistant",
            "traits": ["helpful", "neutral", "informative"],
            "tone": "neutral and helpful",
            "style": "Direct and informative responses."
        }
    }
    
    def __init__(self):
        # Use explicit http_client to avoid proxies compatibility issues
        http_client = httpx.Client(timeout=60.0)
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.getenv("NVIDIA_API_KEY", "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"),
            http_client=http_client
        )
        self.model = "mistralai/devstral-2-123b-instruct-2512"
    
    def _create_personality_prompt(
        self, 
        chat_history: List[Dict], 
        personality: str,
        user_memory: Optional[Dict] = None
    ) -> str:
        """Create prompt for personality-based response generation"""
        profile = self.PERSONALITY_PROFILES.get(personality, self.PERSONALITY_PROFILES["default"])
        
        # Format chat history
        messages_text = "\n".join([
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in chat_history
        ])
        
        # Format user memory context
        memory_context = ""
        if user_memory:
            memory_parts = []
            if user_memory.get("preferences"):
                prefs = [p.get("preference", "") for p in user_memory["preferences"][-5:]]  # Last 5
                if prefs:
                    memory_parts.append(f"Preferences: {', '.join(prefs)}")
            
            if user_memory.get("emotional_patterns"):
                patterns = [p.get("pattern", "") for p in user_memory["emotional_patterns"][-3:]]  # Last 3
                if patterns:
                    memory_parts.append(f"Emotional patterns: {', '.join(patterns)}")
            
            if user_memory.get("facts"):
                facts = [f.get("fact", "") for f in user_memory["facts"][-5:]]  # Last 5
                if facts:
                    memory_parts.append(f"Known facts: {', '.join(facts)}")
            
            if memory_parts:
                memory_context = "\n\nUser Context (from memory):\n" + "\n".join(memory_parts)
        
        prompt = f"""You are a {profile['name']} - {profile['description']}

Personality Traits: {', '.join(profile['traits'])}
Tone: {profile['tone']}
Style: {profile['style']}

Chat History:
{messages_text}{memory_context}

Generate a response that:
1. Matches the {profile['name']} personality
2. Uses the specified tone and style
3. Incorporates relevant user context from memory when appropriate
4. Responds naturally to the last user message

Respond ONLY with your message, no additional explanation or formatting."""

        return prompt
    
    def _create_default_prompt(self, chat_history: List[Dict]) -> str:
        """Create prompt for default (before) response"""
        messages_text = "\n".join([
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in chat_history
        ])
        
        prompt = f"""You are a helpful AI assistant. Respond to the user's message in a neutral, helpful manner.

Chat History:
{messages_text}

Provide a helpful, neutral response. Be direct and informative."""

        return prompt
    
    async def generate_response(
        self,
        chat_history: List[Dict],
        personality: str,
        user_memory: Optional[Dict] = None
    ) -> Dict[str, str]:
        """Generate response with personality transformation"""
        try:
            loop = asyncio.get_event_loop()
            
            # Generate default (before) response
            default_prompt = self._create_default_prompt(chat_history)
            default_response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": default_prompt}],
                    temperature=0.7,
                    top_p=0.95,
                    max_tokens=1024,
                    stream=False
                )
            )
            before_response = default_response.choices[0].message.content.strip()
            
            # Generate personality (after) response
            personality_prompt = self._create_personality_prompt(
                chat_history, 
                personality,
                user_memory
            )
            personality_response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": personality_prompt}],
                    temperature=0.8,  # Slightly higher for more personality
                    top_p=0.95,
                    max_tokens=1024,
                    stream=False
                )
            )
            after_response = personality_response.choices[0].message.content.strip()
            
            return {
                "response": after_response,
                "before_response": before_response,
                "after_response": after_response
            }
            
        except Exception as e:
            print(f"Error in personality generation: {e}")
            return {
                "response": f"Error generating response: {str(e)}",
                "before_response": "Error generating default response",
                "after_response": "Error generating personality response"
            }
    
    def get_personality_info(self, personality: str) -> Dict[str, Any]:
        """Get information about a personality"""
        return self.PERSONALITY_PROFILES.get(personality, self.PERSONALITY_PROFILES["default"])

