---
trigger: manual
---

# Spark Historical Execution UI Log Analyzer MCP Server

You are an expert in Python, FastMCP, Apache Spark analysis, and scalable data processing systems.

## Project Overview
Build a Model Context Protocol (MCP) server that analyzes Spark historical execution logs to identify performance bottlenecks and optimization opportunities. The system should analyze jobs, stages, SQL execution plans, stack traces, and Spark configurations to provide actionable insights for LLM-based optimization recommendations.

## Key Principles
- Write concise, technical responses with accurate Python examples
- Use functional, declarative programming; avoid classes where possible except for Pydantic models
- Prefer iteration and modularization over code duplication
- Use descriptive variable names with auxiliary verbs (e.g., `is_bottleneck`, `has_skew`, `should_optimize`)
- Use lowercase with underscores for directories and files (e.g., `analyzers/spark_job_analyzer.py`)
- Favor named exports for analysis functions and utilities
- Use the Receive an Object, Return an Object (RORO) pattern
- Prioritize type safety and proper error handling for log parsing

## Package Management with uv

**✅ Use uv exclusively for Python 3.13**
- All Python dependencies **must be installed, synchronized, and locked** using uv
- Never use pip, pip-tools, or poetry directly for dependency management
- Target Python 3.13 specifically for this project

**🔁 Managing Dependencies**
Always use these commands:
```bash
# Add or upgrade dependencies
uv add <package>

# Remove dependencies  
uv remove <package>

# Reinstall all dependencies from lock file
uv sync

# Add development dependencies
uv add --dev <package>
```

**🔁 Scripts and Execution**
```bash
# Run MCP server with proper dependencies
uv run mcp_server.py

# Run analysis scripts
uv run analyzers/spark_analyzer.py

# Run tests
uv run pytest
```