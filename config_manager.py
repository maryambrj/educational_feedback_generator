# config_manager.py
"""
Configuration management for the AI grading system
"""

import os
import yaml
from llm_interface import MockLLM, OpenAIGPT, AnthropicClaude

class ConfigManager:
    """Manages configuration loading and validation"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self) -> dict:
        """Load configuration from YAML file"""
        
        if not os.path.exists(self.config_path):
            print(f"Warning: Config file {self.config_path} not found. Using defaults.")
            return self.get_default_config()
        
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except Exception as e:
            print(f"Error loading config: {e}. Using defaults.")
            return self.get_default_config()
    
    def get_default_config(self) -> dict:
        """Return default configuration"""
        return {
            'llm_settings': {
                'provider': 'mock',
                'model': 'gpt-4',
                'max_tokens': 1500,
                'temperature': 0.3,
                'api_key': ''
            },
            'grading_settings': {
                'confidence_threshold': 0.7,
                'auto_flag_low_confidence': True,
                'enable_detailed_feedback': True,
                'max_suggestions': 5
            },
            'output_settings': {
                'generate_html_report': True,
                'export_detailed_feedback': True,
                'create_flagged_report': True,
                'save_grading_history': True
            },
            'system_settings': {
                'rubrics_directory': 'rubrics',
                'output_directory': 'ai_grading_results',
                'log_level': 'INFO'
            }
        }
    
    def get(self, key_path: str, default=None):
        """Get configuration value using dot notation (e.g., 'llm_settings.provider')"""
        
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def validate_config(self) -> bool:
        """Validate configuration completeness"""
        
        required_keys = [
            'llm_settings.provider',
            'grading_settings.confidence_threshold',
            'system_settings.rubrics_directory'
        ]
        
        for key in required_keys:
            if self.get(key) is None:
                print(f"Warning: Required config key missing: {key}")
                return False
        
        return True

class LLMFactory:
    """Factory for creating LLM instances based on configuration"""
    
    @staticmethod
    def create_llm(config: ConfigManager):
        """Create LLM instance based on configuration"""
        
        provider = config.get('llm_settings.provider', 'mock')
        api_key = config.get('llm_settings.api_key', '')
        model = config.get('llm_settings.model', 'gpt-4')
        
        print(f"LLMFactory: Creating LLM with provider='{provider}', model='{model}'")
        
        if provider == 'openai':
            if not api_key:
                print("Warning: No OpenAI API key provided. Using mock LLM.")
                return MockLLM()
            if not api_key.startswith('sk-'):
                print("Warning: Invalid OpenAI API key format. Using mock LLM.")
                return MockLLM()
            try:
                print("✅ Creating OpenAI LLM")
                return OpenAIGPT(api_key, model)
            except ImportError:
                print("❌ OpenAI package not installed. Run: pip install openai")
                print("Using mock LLM instead.")
                return MockLLM()
            except Exception as e:
                print(f"❌ Error creating OpenAI LLM: {e}")
                return MockLLM()
        
        elif provider == 'anthropic':
            if not api_key:
                print("Warning: No Anthropic API key provided. Using mock LLM.")
                return MockLLM()
            try:
                print("✅ Creating Anthropic LLM")
                return AnthropicClaude(api_key, model)
            except ImportError:
                print("❌ Anthropic package not installed. Run: pip install anthropic")
                print("Using mock LLM instead.")
                return MockLLM()
            except Exception as e:
                print(f"❌ Error creating Anthropic LLM: {e}")
                return MockLLM()
        
        else:  # Default to mock or explicit mock
            print("Using Mock LLM for testing")
            return MockLLM()