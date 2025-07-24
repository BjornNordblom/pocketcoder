# Sprint 1: Flow Refactoring & Technical Debt Reduction

**Sprint Duration**: 5 days  
**Sprint Goal**: Refactor the monolithic `flow.py` file into maintainable, testable modules with comprehensive unit test coverage.

## 🚀 Current Status: Day 1 COMPLETED ✅

**Day 1 Progress**: ✅ **100% Complete** - Testing foundation established with comprehensive coverage
- Framework setup completed with pytest 8.4.1 configuration
- 131 test cases implemented across all utility functions
- 88% average test coverage for utility modules
- All acceptance criteria met and exceeded

## Current State Analysis

### Technical Debt Identified
- **Monolithic Architecture**: 785-line `flow.py` with 9 classes and multiple responsibilities
- **No Test Coverage**: Zero unit tests for critical business logic
- **Tight Coupling**: All nodes in single file with shared dependencies
- **Mixed Concerns**: History formatting, LLM prompts, and node logic intermingled
- **Code Duplication**: Similar patterns across action nodes (prep/exec/post)

### Current Structure
```
flow.py (785 lines)
├── format_history_summary() - Utility function
├── MainDecisionAgent - Core decision logic
├── 5 Action Nodes - File operations (read, edit, delete, search, list)
├── 3 Edit Agent Nodes - Multi-step editing workflow
├── FormatResponseNode - Response generation
└── Flow creation functions
```

## Sprint Backlog

### Day 1: Testing Foundation & Core Utilities
**Goal**: Establish testing infrastructure and test core utilities

#### Tasks
1. **Set up testing framework** (2 hours) - *See [`specs/day1_spec1_testing_framework.md`](specs/day1_spec1_testing_framework.md)*
   - Install pytest, pytest-mock, pytest-cov with comprehensive configuration
   - Create organized test directory structure with fixtures and shared utilities
   - Configure pytest.ini and coverage settings for CI-ready testing

2. **Test utility functions** (4 hours) - *See [`specs/day1_spec2_utility_testing.md`](specs/day1_spec2_utility_testing.md)*
   - Test all utility modules with mocked external dependencies (LLM APIs, file system)
   - Comprehensive coverage of file operations, search functionality, and directory operations
   - Focus on error handling, edge cases, and isolation between tests

3. **Test history formatter** (2 hours) - *See [`specs/day1_spec3_history_formatter.md`](specs/day1_spec3_history_formatter.md)*
   - Unit tests for `format_history_summary()` function with all action types
   - Edge case handling: empty history, malformed entries, performance with large datasets

#### Deliverables ✅ COMPLETED
- ✅ `tests/test_utils/` with full utility test coverage (88% average coverage)
- ✅ `tests/test_history_formatter.py` (12 comprehensive tests)
- ✅ CI-ready test configuration with pytest.ini and coverage reporting

#### Implementation Results
- **Framework Setup**: pytest 8.4.1 with comprehensive configuration
- **Test Coverage**: 131 tests across 8 test files, 49% total coverage
- **Utility Coverage**: 88% average across all utility modules
- **Performance**: All tests execute in <1 second
- **Quality**: Comprehensive mocking, edge case testing, and error handling

### Day 2: Node Base Classes & Shared Logic
**Goal**: Extract common patterns and create testable base classes

#### Tasks
1. **Create node base classes** (3 hours)
   - `agents/base.py` - BaseActionNode with common prep/post patterns
   - `agents/mixins.py` - HistoryMixin, ValidationMixin
   - Extract shared validation logic

2. **Test base classes** (3 hours)
   - Unit tests for BaseActionNode lifecycle
   - Test mixins with mock shared state
   - Validate error handling patterns

3. **Extract prompt templates** (2 hours)
   - `agents/prompts.py` - Centralized prompt management
   - Template validation and parameterization tests

#### Deliverables
- `agents/base.py` - Reusable node base classes
- `agents/prompts.py` - Centralized prompt templates
- Full test coverage for new modules

### Day 3: Decision Agent Refactoring
**Goal**: Refactor and test the core MainDecisionAgent

#### Tasks
1. **Refactor MainDecisionAgent** (4 hours)
   - Extract to `agents/decision_agent.py`
   - Separate tool selection logic from LLM interaction
   - Create `ToolSelector` class for decision logic

2. **Create comprehensive tests** (3 hours)
   - Test tool selection with various user queries
   - Mock LLM responses for different scenarios
   - Test error handling and edge cases

3. **Decision logic validation** (1 hour)
   - Test YAML parsing and validation
   - Test parameter extraction and validation

#### Deliverables
- `agents/decision_agent.py` - Refactored decision logic
- `tests/test_decision_agent.py` - Comprehensive test suite
- Tool selection validation framework

### Day 4: Action Nodes Modularization
**Goal**: Split action nodes into separate, testable modules

#### Tasks
1. **Create action node modules** (4 hours)
   - `agents/file_actions.py` - ReadFileAction, DeleteFileAction
   - `agents/search_actions.py` - GrepSearchAction, ListDirAction
   - `agents/edit_actions.py` - Edit workflow nodes
   - Inherit from BaseActionNode, use mixins

2. **Comprehensive action testing** (3 hours)
   - Test each action node with mocked utilities
   - Test shared state management
   - Test error propagation and history updates

3. **Integration testing** (1 hour)
   - Test action node interactions with decision agent
   - Validate workflow continuity

#### Deliverables
- Modularized action nodes in separate files
- Full test coverage for all action types
- Integration test framework

### Day 5: Flow Assembly & End-to-End Testing
**Goal**: Reassemble flows with new modules and validate complete system

#### Tasks
1. **Create flow factory** (2 hours)
   - `flows/factory.py` - FlowBuilder class
   - Configurable flow assembly
   - Environment-specific configurations

2. **Update main flow creation** (2 hours)
   - Refactor `create_main_flow()` and `create_edit_agent()`
   - Use new modular components
   - Maintain backward compatibility

3. **End-to-end testing** (3 hours)
   - Integration tests with real file operations
   - Test complete user workflows
   - Performance and reliability testing

4. **Documentation & cleanup** (1 hour)
   - Update CLAUDE.md with new architecture
   - Code cleanup and final refactoring
   - Sprint retrospective documentation

#### Deliverables
- `flows/factory.py` - Configurable flow assembly
- Updated `flow.py` as thin orchestration layer
- Complete end-to-end test suite
- Updated documentation

## New Architecture Overview

```
agents/
├── base.py              # BaseActionNode, BaseBatchNode
├── mixins.py            # HistoryMixin, ValidationMixin, LoggingMixin
├── prompts.py           # Centralized prompt templates
├── decision_agent.py    # MainDecisionAgent + ToolSelector
├── file_actions.py      # ReadFileAction, DeleteFileAction
├── search_actions.py    # GrepSearchAction, ListDirAction  
├── edit_actions.py      # ReadTargetFileNode, AnalyzeAndPlanNode, ApplyChangesNode
└── response_agent.py    # FormatResponseNode

flows/
├── factory.py           # FlowBuilder for configurable assembly
└── edit_flow.py         # Specialized edit workflow

tests/
├── test_utils/          # Utility function tests
├── test_agents/         # Individual agent tests
├── test_flows/          # Flow integration tests
└── test_integration/    # End-to-end system tests

flow.py                  # Thin orchestration layer (< 100 lines)
```

## Success Criteria

### Code Quality Metrics
- **Test Coverage**: 90%+ line coverage across all modules
- **File Size**: No single file > 200 lines
- **Cyclomatic Complexity**: Max 10 per function
- **Code Duplication**: < 5% duplicate code blocks

### Functional Requirements
- **Backward Compatibility**: All existing workflows continue to work
- **Performance**: No degradation in response times
- **Maintainability**: New features can be added without touching core logic
- **Testability**: Each component can be tested in isolation

### Technical Requirements
- **Modularity**: Clear separation of concerns
- **Extensibility**: Easy to add new action types
- **Configuration**: Environment-specific settings
- **Error Handling**: Comprehensive error propagation and logging

## Risk Mitigation

### High Risk
- **Breaking Changes**: Maintain interface compatibility during refactoring
- **Test Gaps**: Use mutation testing to validate test quality

### Medium Risk  
- **Performance Impact**: Profile before/after refactoring
- **Configuration Complexity**: Keep default configurations simple

### Low Risk
- **Learning Curve**: Document new architecture patterns
- **Tool Integration**: Validate with existing development tools

## Dependencies

### External
- pytest, pytest-mock, pytest-cov (testing framework)
- black, isort (code formatting)
- mypy (type checking)

### Internal
- PocketFlow framework compatibility
- Existing utility functions
- Current LLM integration patterns

## Sprint Retrospective Planning

### What to Measure
- Lines of code reduced in main files
- Test coverage improvement
- Time to add new action types
- Developer productivity metrics

### Review Questions
- Are the new modules intuitive to work with?
- Is the test suite comprehensive and maintainable?
- Can new team members understand the architecture quickly?
- What patterns should be applied to other parts of the system?