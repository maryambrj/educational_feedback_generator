#!/usr/bin/env python3
"""
Test Script for Modular Model Configuration System

This script demonstrates the new modular system without circular import issues.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_model_registry():
    """Test the model registry functionality"""
    print("🧪 Testing Model Registry...")
    
    try:
        from config.model_config import ModelRegistry, ModelProvider, ModelCapability
        
        # Test listing all models
        all_models = ModelRegistry.list_all_models()
        print(f"✅ Total models available: {len(all_models)}")
        
        # Test provider listing
        providers = ModelRegistry.list_all_providers()
        print(f"✅ Total providers available: {len(providers)}")
        
        # Test capability-based model selection
        text_models = ModelRegistry.get_models_by_capability(ModelCapability.TEXT_ANALYSIS)
        print(f"✅ Models with text analysis: {text_models}")
        
        # Test cost optimization
        cost_models = ModelRegistry.get_cost_optimized_models(ModelCapability.TEXT_ANALYSIS)
        print(f"✅ Cost-optimized text analysis models: {cost_models}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing model registry: {e}")
        return False

def test_model_factory():
    """Test the model factory functionality"""
    print("\n🏭 Testing Model Factory...")
    
    try:
        from config.model_factory import ModelFactory
        
        # Test listing available models
        models = ModelFactory.list_available_models()
        print(f"✅ Available models: {models}")
        
        # Test model info retrieval
        if models:
            model_info = ModelFactory.get_model_info(models[0])
            print(f"✅ Model info for {models[0]}: {model_info['name']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing model factory: {e}")
        return False

def test_config_loader():
    """Test the configuration loader"""
    print("\n📥 Testing Configuration Loader...")
    
    try:
        from config.config_loader import ConfigLoader
        
        # Test configuration loading
        config = ConfigLoader()
        print("✅ Configuration loaded successfully")
        
        # Test LLM configuration
        llm_config = config.get_llm_config()
        print(f"✅ LLM config: {llm_config}")
        
        # Test model info
        model_info = config.get_model_info()
        print(f"✅ Model info: {model_info}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing config loader: {e}")
        return False

def test_model_creation():
    """Test actual model creation"""
    print("\n🤖 Testing Model Creation...")
    
    try:
        from config.model_factory import create_model
        
        # Test creating mock model (no API key needed)
        mock_llm = create_model("mock")
        print("✅ Mock model created successfully")
        
        # Test model response
        response = mock_llm.generate_response("Hello, test message", max_tokens=50)
        print(f"✅ Mock model response: {response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing model creation: {e}")
        return False

def main():
    """Main test function"""
    print("🎯 Testing Modular Model Configuration System")
    print("=" * 60)
    
    tests = [
        test_model_registry,
        test_model_factory,
        test_config_loader,
        test_model_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The modular system is working correctly.")
        print("\n🚀 Next steps:")
        print("1. Use the CLI tool: python -m src.config.model_cli list-models")
        print("2. Create configuration: python -m src.config.model_cli create-config")
        print("3. Test models: python -m src.config.model_cli test-model mock")
    else:
        print("❌ Some tests failed. Check the error messages above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
