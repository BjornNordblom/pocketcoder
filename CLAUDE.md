# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**PocketCoder** - an AI coding agent built using Cursor to demonstrate "agentic coding" principles. Implements a coding assistant that can read, edit, search, and navigate codebases through natural language commands.

### Architecture

**Python Backend (Main Agent)**: Uses the PocketFlow framework for LLM orchestration
- `main.py` - Entry point with CLI argument parsing
- `flow.py` - Main agent flow with decision nodes and action execution
- `utils/` - Utility functions for file operations, LLM calls, and search

### Key Design Patterns

- **Agent Pattern**: `MainDecisionAgent` makes decisions about which tools to use
- **Workflow Pattern**: Multi-step editing process (read → analyze → apply changes)
- **Batch Processing**: `ApplyChangesNode` processes multiple file edits in correct order

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the coding agent
python run.py --query "Your request here" --working-dir ./project

# Interactive mode (prompts for query)
python run.py --working-dir ./project

# Alternative: Run directly from src
python -m src.main --query "Your request here" --working-dir ./project
```

## Core Components

### Main Flow (`src/flow.py`)

The main agent operates through these key nodes:
1. **MainDecisionAgent** - Analyzes user requests and selects appropriate tools
2. **Action Nodes** - Execute specific operations (read, edit, search, list, delete)
3. **Edit Agent Sub-flow** - Specialized multi-step editing process
4. **FormatResponseNode** - Generates final user-facing responses

### Utility Functions (`src/utils/`)
- `call_llm.py` - Anthropic Claude API integration
- `read_file.py` - File reading operations
- `replace_file.py` - Line-based file editing
- `search_ops.py` - Grep-like search functionality
- `dir_ops.py` - Directory tree visualization
- `delete_file.py` - File deletion operations

### Shared Memory Structure
```python
shared = {
    "user_query": str,           # Original user request
    "working_dir": str,          # Base directory for operations
    "history": [                 # Action history with results
        {
            "tool": str,         # Tool used
            "reason": str,       # Why it was used
            "params": dict,      # Parameters passed
            "result": any,       # Operation result
            "timestamp": str     # When performed
        }
    ],
    "response": str             # Final response to user
}
```

## Development Guidelines

### File Operations
- All file paths are interpreted relative to `working_dir`
- Edit operations use line-based replacement (1-indexed, inclusive)
- Multiple edits are processed bottom-to-top to preserve line numbers

### LLM Integration
- Uses YAML for structured LLM outputs (more reliable than JSON)
- Implements retry logic through PocketFlow's node system
- Maintains conversation history for context-aware decisions

### Error Handling
- Each utility function returns `(success, result)` tuples
- Failed operations are logged and included in decision context
- The agent can adapt its strategy based on previous failures

## Important Notes
- This is an educational implementation - not production-ready
- Built following the [PocketFlow framework](https://github.com/The-Pocket/PocketFlow) principles
- Demonstrates meta-programming: using Cursor to build a Cursor-like agent
- The `.cursorrules` file contains extensive development guidance

## Embedded Documentation Summary

The original file contained several embedded documentation files which have been summarized below:

### Core Concepts
- **Node**: Basic building block with prep/exec/post methods
- **Flow**: Orchestrates nodes with action-based transitions
- **Batch**: Processes large inputs or reruns flows
- **Async**: For I/O-bound operations and parallel processing

### Design Patterns
- **Agent**: Dynamic action selection based on context
- **MapReduce**: For large-scale data processing
- **RAG**: Retrieval-augmented generation pipeline
- **Workflow**: Complex task decomposition

### Utility Functions
- LLM wrappers, embedding calls, vector databases
- PDF extraction, web crawling, search APIs
- Visualization and debugging tools

Full documentation available in the respective files under docs/ directory.
