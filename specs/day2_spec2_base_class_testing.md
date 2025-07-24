# Day 2 Spec 2: Base Class Testing & Validation

**Task**: Create comprehensive unit tests for base classes and mixins  
**Duration**: 3 hours  
**Priority**: High

## Context

Following the creation of base classes and mixins in Spec 1, we need comprehensive test coverage to ensure:
- Base class lifecycle works correctly
- Mixins provide expected functionality
- Integration between base classes and mixins is seamless
- Error handling and edge cases are covered

## Objectives

1. **Unit Test BaseActionNode**: Test lifecycle and state management
2. **Unit Test Mixins**: Test each mixin independently and in combination
3. **Integration Testing**: Test base classes with mock shared state
4. **Error Handling**: Test failure scenarios and error propagation

## Implementation Plan

### 1. BaseActionNode Testing (`tests/test_agents/test_base.py`)

```python
class TestBaseActionNode:
    """Test suite for BaseActionNode lifecycle and functionality"""
    
    def test_node_initialization():
        """Test node creation and basic properties"""
        
    def test_prep_method_validation():
        """Test prep method with various shared state configurations"""
        
    def test_exec_method_abstract():
        """Test that exec method raises NotImplementedError in base class"""
        
    def test_post_method_history_update():
        """Test post method updates history correctly"""
        
    def test_lifecycle_integration():
        """Test complete prep → exec → post lifecycle"""
        
    def test_error_handling():
        """Test error handling in each lifecycle phase"""

class TestBaseBatchNode:
    """Test suite for BaseBatchNode functionality"""
    
    def test_batch_processing_patterns():
        """Test batch processing capabilities"""
        
    def test_batch_error_handling():
        """Test error handling in batch operations"""
```

### 2. Mixin Testing (`tests/test_agents/test_mixins.py`)

```python
class TestHistoryMixin:
    """Test suite for HistoryMixin functionality"""
    
    def test_add_to_history():
        """Test adding actions to shared history"""
        
    def test_get_recent_actions():
        """Test retrieving recent actions with various counts"""
        
    def test_history_with_empty_state():
        """Test history operations with empty shared state"""
        
    def test_history_formatting():
        """Test consistent history entry formatting"""

class TestValidationMixin:
    """Test suite for ValidationMixin functionality"""
    
    def test_validate_working_dir():
        """Test working directory validation"""
        
    def test_validate_required_fields():
        """Test required field validation with various scenarios"""
        
    def test_validation_error_messages():
        """Test clear error messages for validation failures"""

class TestLoggingMixin:
    """Test suite for LoggingMixin functionality"""
    
    def test_log_action_start():
        """Test action start logging"""
        
    def test_log_action_result():
        """Test action result logging"""
        
    def test_logging_with_sensitive_data():
        """Test logging excludes sensitive information"""

class TestMixinComposition:
    """Test mixins working together"""
    
    def test_multiple_mixins():
        """Test class using multiple mixins simultaneously"""
        
    def test_mixin_method_resolution():
        """Test method resolution order with multiple mixins"""
```

### 3. Integration Testing (`tests/test_agents/test_base_integration.py`)

```python
class TestBaseClassIntegration:
    """Integration tests for base classes with mock utilities"""
    
    def test_base_node_with_mock_utilities():
        """Test base node integration with mocked utility functions"""
        
    def test_shared_state_management():
        """Test shared state passing between lifecycle methods"""
        
    def test_error_propagation():
        """Test error propagation through base class methods"""
        
    def test_backward_compatibility():
        """Test base classes maintain existing interface contracts"""
```

### 4. Mock Framework Integration

```python
@pytest.fixture
def mock_shared_state():
    """Fixture providing mock shared state for testing"""
    return {
        "user_query": "test query",
        "working_dir": "/test/dir",
        "history": [],
        "response": ""
    }

@pytest.fixture
def sample_node_class():
    """Fixture providing a concrete implementation of BaseActionNode for testing"""
    class TestActionNode(BaseActionNode, HistoryMixin, ValidationMixin):
        def exec(self, shared: dict) -> dict:
            return {"success": True, "result": "test"}
    return TestActionNode
```

## Testing Scenarios

### Happy Path Testing
- Normal lifecycle execution
- Successful validation
- Proper history updates
- Correct logging behavior

### Edge Case Testing
- Empty shared state
- Missing required fields
- Invalid working directory
- Malformed history entries

### Error Handling Testing
- Invalid parameters
- File system errors
- Network failures (for LLM calls)
- Memory/resource constraints

### Performance Testing
- Large shared state objects
- High-frequency operations
- Memory usage patterns
- Execution time benchmarks

## Test Coverage Requirements

### Minimum Coverage Targets
- **BaseActionNode**: 98% line coverage
- **BaseBatchNode**: 95% line coverage
- **All Mixins**: 95% line coverage each
- **Integration Tests**: 90% coverage of interaction paths

### Coverage Analysis
```bash
pytest --cov=agents.base --cov=agents.mixins --cov-report=html
```

## Mock Strategy

### External Dependencies
- File system operations → `unittest.mock.patch`
- LLM API calls → Mock responses from `fixtures/mock_responses/`
- Time-dependent operations → `freezegun` or time mocks

### Internal Dependencies
- Utility functions → Mock return values
- Shared state → Controlled fixtures
- Configuration → Environment variable mocks

## Acceptance Criteria

1. **Test Coverage**: 95%+ line coverage for all base classes and mixins
2. **Test Speed**: All tests execute in < 5 seconds
3. **Test Reliability**: 100% pass rate across 20 consecutive runs
4. **Error Coverage**: All exception paths tested
5. **Documentation**: Each test method has clear docstring explaining purpose

## Success Metrics

- Number of test cases (target: 50+ tests)
- Code coverage percentage
- Test execution time
- Number of bugs found during testing
- Mutation testing score (if applicable)

## Tools & Configuration

### Required Tools
```python
# requirements-dev.txt additions
pytest-mock==3.12.0
pytest-benchmark==4.0.0
freezegun==1.2.2
mutmut==2.4.3  # for mutation testing
```

### Pytest Configuration
```ini
# Additional pytest.ini settings for base class testing
[tool:pytest]
testpaths = tests/test_agents
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers = 
    unit: Unit tests for individual components
    integration: Integration tests between components
    slow: Tests that take longer than 1 second
```

## Deliverables

1. **`tests/test_agents/test_base.py`** - BaseActionNode and BaseBatchNode tests
2. **`tests/test_agents/test_mixins.py`** - Comprehensive mixin tests
3. **`tests/test_agents/test_base_integration.py`** - Integration test suite
4. **Test fixtures** - Mock shared state and sample implementations
5. **Coverage report** - HTML coverage report showing 95%+ coverage
6. **Performance benchmarks** - Baseline performance metrics for base classes

## Dependencies

- Spec 1 completion (base classes and mixins created)
- Existing test framework from Day 1
- Mock response fixtures
- Access to current `flow.py` for backward compatibility testing

## Risks & Mitigation

**High Risk**: Tests don't catch real-world usage patterns
- *Mitigation*: Include integration tests with realistic scenarios
- *Validation*: Test against actual node implementations

**Medium Risk**: Over-mocking leading to false confidence
- *Mitigation*: Balance unit tests with integration tests
- *Validation*: Include end-to-end tests in later specs

**Low Risk**: Test maintenance overhead
- *Mitigation*: Use fixtures and helper functions for common patterns
- *Validation*: Regular test suite review and refactoring