# Patronus Prompt Management System Overview

## Core Concepts

The Patronus prompt management system is built around two primary concepts:

1. **Prompt Definitions** - The metadata container for a prompt
2. **Prompt Revisions** - The versioned content of a prompt

### Prompt Definition

A Prompt Definition represents the metadata and identity of a prompt. It includes:

- **ID**: Unique identifier
- **Name**: User-friendly name for the prompt
- **Description**: Optional description of the prompt's purpose
- **Project**: Every prompt belongs to a project (identified by ID and name)
- **Latest Revision**: Reference to the most recent revision number

Prompt definitions act as containers that organize and identify prompts within the system. They provide a stable reference point while the actual content can evolve over time through revisions.

### Prompt Revision

A Prompt Revision represents a specific version of a prompt's content. Each revision includes:

- **ID**: Unique identifier for the revision
- **Revision Number**: Sequential version number (starting from 1)
- **Body**: The actual prompt template text
- **Normalized Body Hash**: SHA-256 hash of the normalized prompt body
- **Labels**: Optional tags that can be applied to specific revisions
- **Metadata**: Optional JSON data associated with the revision
- **Creation Timestamp**: When the revision was created

Each prompt definition can have multiple revisions, representing the evolution of the prompt over time. Only one revision can be the "latest" at any given time.

### Labels

Labels provide a way to tag specific revisions with meaningful identifiers. Common use cases include:

- Marking a specific revision as "production" or "staging"
- Tagging revisions for specific use cases or experiments
- Creating stable references to important revisions

Labels can be moved between revisions, allowing for semantic versioning practices.

## System Architecture

The prompt management system is implemented across three main components:

1. **Internal API** (`patronus-evaluation-api`)
2. **Public API** (`patronus-backend`)
3. **SDK** (`patronus-py`)

### Internal API

The internal API (`evaluation_api/transport/prompts/`) defines the core data models and operations for prompt definitions and revisions:

- CRUD operations for prompt definitions
- CRUD operations for prompt revisions
- Label management
- Filtering and retrieval operations

This API serves as the implementation layer for prompt storage and management.

### Public API

The public API (`backend_api/transport/prompts/handlers.py`) exposes the prompt management functionality to clients. It acts as a thin wrapper around the internal API, handling authentication and request validation before delegating to the evaluation API client.

### SDK

The SDK (`patronus/prompts/`) provides a high-level interface for working with prompts in Python applications. It abstracts away the details of API communication, caching, and template rendering.

## SDK Design

The SDK is designed around a few key abstractions:

### Prompt Providers

Prompt providers are responsible for retrieving prompts from different sources:

- `APIPromptProvider`: Retrieves prompts from the Patronus API
- `LocalPromptProvider`: (Placeholder) Will support local prompt files

The provider pattern allows for flexibility in how prompts are sourced, with potential for additional providers in the future.

### Template Engines

The SDK supports multiple template engines for rendering prompts:

- `FStringTemplateEngine`: Python's format string syntax
- `MustacheTemplateEngine`: Mustache templates (requires 'chevron' package)
- `Jinja2TemplateEngine`: Jinja2 templates (requires 'jinja2' package)

This allows for flexibility in template syntax and capabilities.

### Prompt Models

The SDK defines two main models:

- `Prompt`: A simple model for client-side prompt creation
- `LoadedPrompt`: A comprehensive model representing a prompt retrieved from a provider

Both models inherit from `BasePrompt`, which provides common functionality like template rendering.

### Client Interface

The SDK exposes two primary functions for retrieving prompts:

- `load_prompt`: Synchronous prompt loading
- `aload_prompt`: Asynchronous prompt loading

These functions provide a simple interface while handling the complexities of provider selection, caching, and template engine configuration.

```python
# Example usage
from patronus.prompts import load_prompt

# Load latest revision of a prompt
prompt = load_prompt(name="my-prompt", project="my-project")

# Load a specific revision
prompt = load_prompt(name="my-prompt", revision=3, project="my-project")

# Load a labeled revision
prompt = load_prompt(name="my-prompt", label="production", project="my-project")

# Render the prompt with variables
rendered = prompt.render(user="John", query="How does this work?")
```

## Relationship Between Definitions and Revisions

The relationship between prompt definitions and revisions in the SDK is somewhat abstracted. When a user loads a prompt, they receive a `LoadedPrompt` object that contains both definition metadata (name, description, project) and revision data (body, revision number, labels).

The SDK hides the two-step retrieval process:

1. Finding the appropriate revision based on parameters (name, revision, label)
2. Loading the corresponding definition metadata

This abstraction simplifies the user experience but means that the distinction between definitions and revisions is less visible to SDK users.

## Caching Strategy

The SDK implements a caching strategy to minimize API calls:

- Prompts are cached by their lookup parameters (name, project, revision, label)
- Cache is thread-safe for synchronous operations and lock-protected for async operations
- Users can disable caching for specific lookups if needed

This improves performance for frequently used prompts while allowing for cache invalidation when necessary.

## Potential Improvements

Based on the current implementation, potential improvements could include:

1. Implementing the `LocalPromptProvider` to support offline development
2. Adding methods to create and update prompts through the SDK
3. Providing utilities for common prompt management workflows
4. Enhancing the caching strategy with time-based invalidation
5. Support for more advanced template features (partials, includes, etc.)
6. More explicit handling of the definition/revision relationship in the SDK

## Conclusion

The Patronus prompt management system provides a robust foundation for versioning, retrieving, and rendering prompts. The separation of definitions and revisions allows for effective version control, while the SDK abstracts away the complexity to provide a simple interface for application developers.
