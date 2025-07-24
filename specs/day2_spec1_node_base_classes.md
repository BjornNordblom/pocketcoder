# Day 2 Spec 1: Node Base Classes & Common Patterns

**Task**: Create node base classes with common prep/post patterns and shared logic extraction  
**Duration**: 3 hours  
**Priority**: High

## Context

Currently all 9 node classes in `flow.py` share similar patterns:
- Common prep/exec/post lifecycle methods
- Shared state management through `shared` parameter
- History tracking and validation logic
- Similar error handling patterns

## Objectives

1. **Extract BaseActionNode**: Common lifecycle and state management
2. **Create Mixins**: Reusable functionality components
3. **Reduce Code Duplication**: DRY principle implementation
4. **Improve Testability**: Isolated, mockable components

## Implementation Plan

### 1. Create `agents/base.py`

```python
class BaseActionNode:
    """Base class for all action nodes with common lifecycle patterns"""
    
    def __init__(self, name: str):
        self.name = name
    
    def prep(self, shared: dict) -> bool:
        """Common preparation logic"""
        # Validation, state setup
        pass
    
    def exec(self, shared: dict) -> dict:
        """Override in subclasses for specific action logic"""
        raise NotImplementedError
    
    def post(self, shared: dict, result: dict) -> dict:
        """Common post-processing logic"""
        # History updates, response formatting
        pass

class BaseBatchNode:
    """Base class for batch processing nodes"""
    # Similar pattern for batch operations
```

### 2. Create `agents/mixins.py`

```python
class HistoryMixin:
    """Mixin for history management functionality"""
    
    def add_to_history(self, shared: dict, action_data: dict):
        """Add action to shared history"""
        pass
    
    def get_recent_actions(self, shared: dict, count: int = 5):
        """Get recent actions from history"""
        pass

class ValidationMixin:
    """Mixin for common validation patterns"""
    
    def validate_working_dir(self, shared: dict) -> bool:
        """Validate working directory exists"""
        pass
    
    def validate_required_fields(self, shared: dict, fields: list) -> bool:
        """Validate required fields in shared state"""
        pass

class LoggingMixin:
    """Mixin for consistent logging patterns"""
    
    def log_action_start(self, action_name: str, params: dict):
        """Log action start with parameters"""
        pass
    
    def log_action_result(self, action_name: str, success: bool, result: any):
        """Log action completion"""
        pass
```

### 3. Extract Common Patterns

From existing nodes in `flow.py`, identify and extract:

- **State Validation**: Common checks for working_dir, user_query
- **History Management**: Consistent history entry creation
- **Error Handling**: Standard error response formatting
- **Parameter Extraction**: Common parameter parsing patterns

## File Structure

```
agents/
├── __init__.py
├── base.py              # BaseActionNode, BaseBatchNode
└── mixins.py            # HistoryMixin, ValidationMixin, LoggingMixin
```

## Testing Requirements

### Unit Tests for Base Classes
- Test BaseActionNode lifecycle (prep → exec → post)
- Test state validation and error handling
- Test history management integration
- Mock shared state for isolation

### Mixin Testing
- Test each mixin independently
- Test mixin composition with base classes
- Validate shared state interactions
- Test error propagation

### Integration Testing
- Test base classes with existing utility functions
- Validate backward compatibility
- Test with mock LLM responses

## Acceptance Criteria

1. **Code Reduction**: Remove 200+ lines of duplicated code from `flow.py`
2. **Test Coverage**: 95%+ coverage for base classes and mixins
3. **Backward Compatibility**: Existing functionality unchanged
4. **Documentation**: Clear docstrings and usage examples
5. **Performance**: No measurable performance degradation

## Success Metrics

- Lines of code reduced in `flow.py`
- Test coverage percentage
- Number of code duplication violations (should be 0)
- Time to understand new node structure (< 10 minutes for new developer)

## Dependencies

- Day 1 testing framework (completed)
- Access to current `flow.py` structure
- Understanding of existing node patterns

## Risks & Mitigation

**High Risk**: Breaking existing node functionality
- *Mitigation*: Maintain exact interface compatibility
- *Validation*: Run existing tests after extraction

**Medium Risk**: Over-abstraction leading to complexity
- *Mitigation*: Keep base classes simple and focused
- *Validation*: Code review for clarity

## Deliverables

1. `agents/base.py` - Base classes with common patterns
2. `agents/mixins.py` - Reusable functionality mixins
3. `tests/test_agents/test_base.py` - Comprehensive base class tests
4. `tests/test_agents/test_mixins.py` - Mixin functionality tests
5. Documentation updates in base class docstrings