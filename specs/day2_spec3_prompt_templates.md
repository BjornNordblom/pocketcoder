# Day 2 Spec 3: Extract Prompt Templates & Centralized Management

**Task**: Extract and centralize prompt templates with validation and parameterization  
**Duration**: 2 hours  
**Priority**: Medium

## Context

Currently, LLM prompts are scattered throughout `flow.py` as hardcoded strings within node classes. This creates:
- **Maintenance Issues**: Difficult to update prompts across multiple locations
- **Testing Challenges**: Hard to test prompt variations and parameters
- **Inconsistency**: Different prompt styles and formatting across nodes
- **Localization Barriers**: Cannot easily support different languages or contexts

## Objectives

1. **Centralize Prompts**: Extract all prompts to dedicated module
2. **Template System**: Create parameterized, reusable prompt templates
3. **Validation**: Ensure prompt parameters are correctly formatted
4. **Testing**: Enable comprehensive prompt testing and validation

## Current Prompt Analysis

From `flow.py`, the following prompts need extraction:

### MainDecisionAgent Prompts
- Tool selection prompt with user query and history
- YAML response format specification
- Available tools and parameter descriptions

### Edit Agent Prompts
- File analysis and planning prompt
- Change application prompt with line-based editing
- Validation prompt for applied changes

### Response Formatting Prompts
- History summarization prompt
- Final response generation prompt

## Implementation Plan

### 1. Create `agents/prompts.py`

```python
from typing import Dict, Any, List
from string import Template
import yaml

class PromptTemplate:
    """A parameterized prompt template with validation"""
    
    def __init__(self, template: str, required_params: List[str]):
        self.template = Template(template)
        self.required_params = set(required_params)
    
    def format(self, **kwargs) -> str:
        """Format template with parameters and validation"""
        # Validate required parameters
        # Format and return prompt
        pass
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """Validate that all required parameters are present"""
        pass

class PromptManager:
    """Central management for all LLM prompts"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def get_prompt(self, prompt_name: str, **kwargs) -> str:
        """Get formatted prompt by name"""
        pass
    
    def _load_templates(self) -> Dict[str, PromptTemplate]:
        """Load all prompt templates"""
        pass

# Template definitions
DECISION_AGENT_PROMPT = PromptTemplate(
    template="""
    You are a coding assistant that helps users with file operations.
    
    User Query: $user_query
    Working Directory: $working_dir
    Recent Actions: $history_summary
    
    Available Tools:
    $available_tools
    
    Select the most appropriate tool and provide parameters in YAML format:
    
    tool: <tool_name>
    reason: <explanation>
    params:
      <parameter_name>: <value>
    """,
    required_params=["user_query", "working_dir", "history_summary", "available_tools"]
)

EDIT_ANALYSIS_PROMPT = PromptTemplate(
    template="""
    Analyze the following file and plan the requested changes:
    
    File: $file_path
    Content: $file_content
    User Request: $user_request
    
    Provide a detailed plan for the changes in YAML format:
    
    analysis: <file_analysis>
    changes:
      - line_start: <number>
        line_end: <number>
        new_content: <content>
        reason: <explanation>
    """,
    required_params=["file_path", "file_content", "user_request"]
)

# Additional template definitions...
```

### 2. Template Categories

#### Decision Making Prompts
- `decision_agent_main` - Primary tool selection
- `decision_agent_fallback` - When first attempt fails
- `decision_validation` - Validate tool selection

#### File Operation Prompts
- `edit_analysis` - Analyze file for changes
- `edit_application` - Apply specific changes
- `edit_validation` - Validate applied changes
- `search_refinement` - Refine search queries

#### Response Generation Prompts
- `response_formatting` - Format final responses
- `history_summarization` - Summarize action history
- `error_explanation` - Explain errors to users

### 3. Template Features

#### Parameter Validation
```python
def validate_params(self, params: Dict[str, Any]) -> bool:
    """Validate parameters with type checking and constraints"""
    missing = self.required_params - set(params.keys())
    if missing:
        raise ValueError(f"Missing required parameters: {missing}")
    
    # Type validation
    # Length constraints
    # Format validation
    return True
```

#### Template Inheritance
```python
class BasePromptTemplate(PromptTemplate):
    """Base template with common elements"""
    
    def __init__(self, template: str, required_params: List[str]):
        # Add common parameters like working_dir, timestamp
        base_params = ["working_dir", "timestamp"]
        super().__init__(template, required_params + base_params)
```

#### Context Management
```python
class ContextAwarePrompt(PromptTemplate):
    """Prompt template that adapts based on context"""
    
    def format(self, context: str = "default", **kwargs) -> str:
        """Format with context-specific variations"""
        # Load context-specific template variations
        # Apply appropriate formatting
        pass
```

## Testing Strategy

### 1. Template Validation Tests (`tests/test_agents/test_prompts.py`)

```python
class TestPromptTemplate:
    """Test individual prompt template functionality"""
    
    def test_template_formatting():
        """Test template parameter substitution"""
        
    def test_parameter_validation():
        """Test required parameter validation"""
        
    def test_invalid_parameters():
        """Test error handling for invalid parameters"""
        
    def test_template_inheritance():
        """Test base template functionality"""

class TestPromptManager:
    """Test prompt management functionality"""
    
    def test_prompt_loading():
        """Test loading all prompt templates"""
        
    def test_prompt_retrieval():
        """Test getting prompts by name"""
        
    def test_prompt_caching():
        """Test prompt caching for performance"""

class TestPromptIntegration:
    """Test prompts with actual LLM integration"""
    
    def test_prompt_with_mock_llm():
        """Test prompts generate expected LLM responses"""
        
    def test_yaml_response_parsing():
        """Test LLM responses can be parsed correctly"""
```

### 2. Template Content Tests

```python
class TestPromptContent:
    """Test prompt content and structure"""
    
    def test_all_prompts_load():
        """Test all defined prompts load without errors"""
        
    def test_prompt_yaml_format():
        """Test prompts produce valid YAML responses"""
        
    def test_prompt_parameter_coverage():
        """Test all required parameters are documented"""
        
    def test_prompt_consistency():
        """Test prompts follow consistent formatting"""
```

## Configuration Management

### 1. Environment-Specific Prompts

```python
# agents/prompts/environments.py
DEVELOPMENT_PROMPTS = {
    "decision_agent_main": "verbose development version...",
    "debug_mode": True,
    "include_reasoning": True
}

PRODUCTION_PROMPTS = {
    "decision_agent_main": "concise production version...",
    "debug_mode": False,
    "include_reasoning": False
}
```

### 2. Prompt Versioning

```python
class VersionedPromptManager(PromptManager):
    """Prompt manager with version support"""
    
    def __init__(self, version: str = "latest"):
        self.version = version
        super().__init__()
    
    def get_prompt(self, prompt_name: str, version: str = None, **kwargs) -> str:
        """Get prompt with specific version"""
        target_version = version or self.version
        # Load version-specific prompt
        pass
```

## File Structure

```
agents/
├── prompts/
│   ├── __init__.py
│   ├── templates.py         # Core template definitions
│   ├── manager.py          # PromptManager class
│   ├── validation.py       # Parameter validation
│   └── environments.py     # Environment-specific configs
└── prompts.py              # Main module interface

tests/test_agents/
├── test_prompts.py         # Core prompt testing
├── test_prompt_content.py  # Content validation tests
└── test_prompt_integration.py  # Integration with LLM
```

## Migration Strategy

### 1. Phase 1: Extract Templates
- Identify all hardcoded prompts in `flow.py`
- Create corresponding `PromptTemplate` objects
- Maintain backward compatibility

### 2. Phase 2: Replace Usage
- Update node classes to use `PromptManager`
- Replace hardcoded strings with template calls
- Add parameter validation

### 3. Phase 3: Enhance & Test
- Add advanced features (inheritance, versioning)
- Comprehensive testing suite
- Performance optimization

## Acceptance Criteria

1. **Complete Extraction**: All prompts removed from `flow.py`
2. **Template Coverage**: 100% of existing prompts converted to templates
3. **Parameter Validation**: All prompt parameters validated before use
4. **Test Coverage**: 95%+ coverage for prompt module
5. **Performance**: No measurable impact on response times
6. **Maintainability**: Easy to add new prompts and modify existing ones

## Success Metrics

- Number of prompts centralized (target: 8-10 prompts)
- Lines of code removed from `flow.py`
- Test coverage percentage
- Time to add new prompt (should be < 5 minutes)
- Prompt consistency score (manual review)

## Dependencies

- Day 1 testing framework
- Base classes from Spec 1 (for integration)
- Understanding of current prompt usage patterns

## Risks & Mitigation

**High Risk**: Breaking existing LLM interactions
- *Mitigation*: Careful extraction with exact string preservation
- *Validation*: Integration tests with mock LLM responses

**Medium Risk**: Over-engineered template system
- *Mitigation*: Start simple, add features incrementally
- *Validation*: Regular complexity review

**Low Risk**: Performance impact from template processing
- *Mitigation*: Template caching and optimization
- *Validation*: Performance benchmarks

## Deliverables

1. **`agents/prompts.py`** - Main prompt module with templates
2. **`tests/test_agents/test_prompts.py`** - Comprehensive prompt tests
3. **Prompt migration guide** - Documentation for updating node classes
4. **Template validation report** - Coverage and consistency analysis
5. **Performance benchmarks** - Before/after performance comparison