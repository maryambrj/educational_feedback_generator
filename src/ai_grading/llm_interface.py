# llm_interface.py
"""
LLM interface and implementations for different providers
"""

import json
from abc import ABC, abstractmethod

# ============================================================================
# Abstract LLM Interface
# ============================================================================

class LLMInterface(ABC):
    """Abstract interface for different LLM providers"""
    
    @abstractmethod
    def generate_response(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate response from the LLM"""
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """Return the model name/identifier"""
        pass

# ============================================================================
# Mock LLM for Testing
# ============================================================================

class MockLLM(LLMInterface):
    """Mock LLM for testing purposes"""
    
    def generate_response(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate a mock response with realistic structure"""
        return json.dumps({
            "scores": {
                "insight_quality": 12,
                "code_quality": 8,
                "visualization": 4
            },
            "total_score": 24,
            "percentage": 80.0,
            "feedback": "Good analysis with clear insights. Code implementation is solid but could use more comments. Visualizations are appropriate but labels could be clearer.",
            "suggestions": [
                "Add more detailed comments to your code",
                "Include axis labels and titles in your plots",
                "Consider discussing limitations of your analysis"
            ],
            "confidence": 0.85
        })
    
    def get_model_name(self) -> str:
        return "MockLLM-v1.0"

# ============================================================================
# OpenAI GPT Implementation
# ============================================================================

class OpenAIGPT(LLMInterface):
    """OpenAI GPT integration"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self._client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client"""
        try:
            import openai
            self._client = openai.OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        except Exception as e:
            raise Exception(f"Error initializing OpenAI client: {e}")
    
    def generate_response(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate response using OpenAI API"""
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            # Fallback to mock response
            return MockLLM().generate_response(prompt, max_tokens)
    
    def get_model_name(self) -> str:
        return f"OpenAI-{self.model}"

# ============================================================================
# Anthropic Claude Implementation
# ============================================================================

class AnthropicClaude(LLMInterface):
    """Anthropic Claude integration"""
    
    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229"):
        self.api_key = api_key
        self.model = model
        self._client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Anthropic client"""
        try:
            import anthropic
            self._client = anthropic.Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError("Anthropic package not installed. Run: pip install anthropic")
        except Exception as e:
            raise Exception(f"Error initializing Anthropic client: {e}")
    
    def generate_response(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate response using Anthropic API"""
        try:
            response = self._client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Error calling Anthropic API: {e}")
            # Fallback to mock response
            return MockLLM().generate_response(prompt, max_tokens)
    
    def get_model_name(self) -> str:
        return f"Anthropic-{self.model}"