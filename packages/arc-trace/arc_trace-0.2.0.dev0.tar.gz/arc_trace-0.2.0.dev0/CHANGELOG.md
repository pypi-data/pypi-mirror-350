# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Integration-first architecture for modern AI frameworks
- OpenAI Agents SDK integration via built-in trace processors
- LangGraph integration with LangSmith observability extension
- LlamaIndex integration with observability handler registration
- Comprehensive examples and migration guides
- Production-ready configuration and error handling

### Changed
- **BREAKING**: Migrated from monkey patching to integration adapters
- Improved developer experience with single-line enablement
- Enhanced performance with zero overhead when tracing disabled
- Better compatibility with framework updates

### Deprecated
- Legacy monkey patching approach (still supported for backward compatibility)

### Removed
- Heavy framework instrumentation that conflicts with built-in tracing

### Fixed
- Framework compatibility issues with built-in tracing systems
- Performance overhead from excessive monkey patching
- Brittle behavior with framework version updates

### Security
- Improved handling of sensitive data in trace attributes
- Better error handling to prevent information leakage

## [0.1.0] - 2025-01-21

### Added
- Initial release of Arc Tracing SDK
- Core `@trace_agent` decorator functionality
- OpenTelemetry-based trace collection
- Framework detection for OpenAI, LangChain, LlamaIndex
- Arc platform integration with fallback mechanisms
- Configuration system with YAML and environment variable support
- Comprehensive test suite and examples

### Features
- Lightweight agent tracing with minimal code changes
- Framework-agnostic design supporting multiple AI frameworks
- Built-in exporters for Arc platform and local files
- Automatic framework detection and instrumentation
- Production-ready error handling and configuration