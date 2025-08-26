# 🎯 Modular Model Configuration System - Quick Usage Guide

All model configurations are centralized in a single file for easy management.

## 🚀 **Quick Start**

### 1. **View Available Models**
```bash
python simple_model_demo.py
```

### 2. **Using the System in Your Code**
```python
import sys
import os
sys.path.append(os.path.join('src', 'config'))

from model_config import ModelRegistry, ModelProvider, ModelCapability

# Get all models with text analysis capability
text_models = ModelRegistry.get_models_by_capability(ModelCapability.TEXT_ANALYSIS)
print(f"Text analysis models: {text_models}")

# Get cost-optimized models
cheap_models = ModelRegistry.get_cost_optimized_models(ModelCapability.TEXT_ANALYSIS)
print(f"Cheapest models: {cheap_models}")

# Get models from specific provider
openai_models = ModelRegistry.get_models_by_provider(ModelProvider.OPENAI)
print(f"OpenAI models: {list(openai_models.keys())}")

# Get detailed model info
model_info = ModelRegistry.get_model_config('gpt-4o-mini')
print(f"Model cost: ${model_info.cost_per_1k_tokens:.4f}/1K tokens")
```

## 📊 **Available Models**

### **OpenAI Models**
- **gpt-4o**: Latest GPT-4 ($0.005/1K tokens)
- **gpt-4o-mini**: Cost-effective GPT-4 ($0.0001/1K tokens) ⭐ **Best value**
- **gpt-3.5-turbo**: Fast and cheap ($0.0005/1K tokens)

### **Anthropic Models**
- **claude-3-5-sonnet**: Excellent reasoning ($0.003/1K tokens)
- **claude-3-haiku**: Fast Claude ($0.0003/1K tokens)

### **Mock Models**
- **mock**: For testing (free)

## 🎯 **Model Selection by Task**

### **For Cost-Sensitive Grading**
```python
# Get cheapest models that can do text analysis
cheap_models = ModelRegistry.get_cost_optimized_models(ModelCapability.TEXT_ANALYSIS)
selected_model = cheap_models[0]  # gpt-4o-mini ($0.0001/1K)
```

### **For Complex Code Analysis**
```python
# Get models that can analyze code
code_models = ModelRegistry.get_models_by_capability(ModelCapability.CODE_ANALYSIS)
# Returns: ['gpt-4o', 'gpt-4o-mini', 'claude-3-5-sonnet']
```

### **For Creative Feedback**
```python
# Get models with creativity capability
creative_models = ModelRegistry.get_models_by_capability(ModelCapability.CREATIVITY)
# Returns: ['gpt-4o', 'claude-3-5-sonnet']
```

## 🎯 **Single File Model Management**

**The key benefit**: All model configurations are in one file: `src/config/model_config.py`

### **To Add a New Model:**
1. Open `src/config/model_config.py`
2. Add your model to the appropriate provider section:
```python
"my-new-model": ModelConfig(
    name="my-new-model",
    provider=ModelProvider.OPENAI,  # or ANTHROPIC
    max_tokens=4096,
    temperature=0.3,
    capabilities=[
        ModelCapability.TEXT_ANALYSIS,
        ModelCapability.REASONING
    ],
    cost_per_1k_tokens=0.002,
    context_window=32000,
    description="My custom model for specific tasks",
    recommended_for=["specialized_grading", "custom_analysis"]
)
```
3. The model is now available everywhere in your system!

### **To Add a New Provider:**
```python
# Add to ModelProvider enum
class ModelProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    MOCK = "mock"
    MY_PROVIDER = "my_provider"  # Add this

# Add provider configuration
PROVIDERS = {
    ModelProvider.MY_PROVIDER: ProviderConfig(
        name="My Provider",
        provider=ModelProvider.MY_PROVIDER,
        api_key_env_var="MY_PROVIDER_API_KEY",
        base_url="https://api.myprovider.com",
        rate_limit_rpm=1000,
        rate_limit_tpm=50000
    )
}
```

## 💡 **Best Practices**

### **1. Cost Optimization**
```python
# Always consider cost for batch processing
cheap_models = ModelRegistry.get_cost_optimized_models(ModelCapability.TEXT_ANALYSIS)
# Use gpt-4o-mini for most grading tasks (97% cheaper than GPT-4)
```

### **2. Capability Matching**
```python
# Match model capabilities to your task
if task_requires_code_analysis:
    models = ModelRegistry.get_models_by_capability(ModelCapability.CODE_ANALYSIS)
else:
    models = ModelRegistry.get_models_by_capability(ModelCapability.TEXT_ANALYSIS)
```

### **3. Provider Preferences**
```python
# If you prefer OpenAI models
openai_models = ModelRegistry.get_models_by_provider(ModelProvider.OPENAI)
# If you prefer Anthropic models
anthropic_models = ModelRegistry.get_models_by_provider(ModelProvider.ANTHROPIC)
```

## 🎨 **Example: Smart Model Selection Function**

```python
def select_optimal_model(task_type, cost_sensitive=True, preferred_provider=None):
    """Select the optimal model for a given task"""
    
    # Map task to capability
    task_capability_map = {
        'grading': ModelCapability.TEXT_ANALYSIS,
        'code_review': ModelCapability.CODE_ANALYSIS,
        'creative_feedback': ModelCapability.CREATIVITY,
        'analysis': ModelCapability.REASONING
    }
    
    capability = task_capability_map.get(task_type, ModelCapability.TEXT_ANALYSIS)
    
    # Get models with the required capability
    if cost_sensitive:
        available_models = ModelRegistry.get_cost_optimized_models(capability)
    else:
        available_models = ModelRegistry.get_models_by_capability(capability)
    
    # Filter by preferred provider if specified
    if preferred_provider:
        provider_models = ModelRegistry.get_models_by_provider(preferred_provider)
        available_models = [m for m in available_models if m in provider_models]
    
    # Return the best option
    return available_models[0] if available_models else 'mock'

# Usage examples
best_for_grading = select_optimal_model('grading', cost_sensitive=True)
# Returns: 'gpt-4o-mini' (cheapest text analysis model)

best_for_code = select_optimal_model('code_review', cost_sensitive=False)
# Returns: 'gpt-4o' (most capable code analysis model)
```

## 🚀 **Integration with Your Grading System**

Instead of hardcoding model names in your grading code, you can now use:

```python
# OLD WAY (hardcoded)
llm_model = "gpt-4"

# NEW WAY (intelligent selection)
from model_config import ModelRegistry, ModelCapability

# For text grading (cost-optimized)
text_models = ModelRegistry.get_cost_optimized_models(ModelCapability.TEXT_ANALYSIS)
grading_model = text_models[0]  # gpt-4o-mini

# For code grading (performance-optimized)
code_models = ModelRegistry.get_models_by_capability(ModelCapability.CODE_ANALYSIS)
code_model = code_models[0]  # gpt-4o

print(f"Using {grading_model} for text grading")
print(f"Using {code_model} for code analysis")
```

## 🎉 **TL;DR**

✅ **Single file control**: `src/config/model_config.py`  
✅ **6 models available**: OpenAI, Anthropic, Mock  
✅ **4 capabilities**: Text, Code, Reasoning, Creativity  
✅ **Cost optimization**: Automatic cheapest model selection  
✅ **Easy extension**: Add models/providers with simple config  
✅ **Environment support**: `.env` file integration  
✅ **Zero code changes**: Switch models by updating config only  

