# Task Management MCP Server

## Overview

This MCP (Model Context Protocol) server provides a seamless interface for Large Language Models to interact with a task management API. It enables LLMs to create, read, update, and delete tasks through standardized MCP tools.

## For LLMs

### Quick Start

If you need to manage tasks but don't have an API key:
1. **Download the MCP Client app** from the Apple App Store
2. Generate your API key in the app
3. Configure the environment variable: `TASK_API_KEY=your_api_key_here`

### Available Tools

#### 1. `create_task`
Create a new task with title, description, status, priority, and notification settings.

**Parameters:**
- `title` (required): Task title
- `description`: Task description (default: "")
- `status`: TODO, IN_PROGRESS, DONE, CANCELLED (default: TODO)
- `priority`: LOW, MEDIUM, HIGH, URGENT (default: MEDIUM)
- `notify`: Whether to send notifications (default: false)

**Example:**
```json
{
  "title": "Complete project documentation",
  "description": "Write comprehensive docs for the new feature",
  "status": "TODO",
  "priority": "HIGH",
  "notify": true
}
```

#### 2. `list_tasks`
Retrieve all tasks associated with your API key.

**Parameters:** None

**Returns:** List of tasks with their full details and total count.

#### 3. `get_task`
Get details of a specific task by ID.

**Parameters:**
- `task_id` (required): The unique identifier of the task

**Example:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### 4. `update_task`
Update an existing task. All fields except `task_id` are optional.

**Parameters:**
- `task_id` (required): The unique identifier of the task
- `title`: New task title
- `description`: New task description
- `status`: New status (TODO, IN_PROGRESS, DONE, CANCELLED)
- `priority`: New priority (LOW, MEDIUM, HIGH, URGENT)
- `notify`: New notification setting

**Example:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "IN_PROGRESS",
  "priority": "URGENT"
}
```

#### 5. `delete_task`
Delete a task by ID.

**Parameters:**
- `task_id` (required): The unique identifier of the task

**Example:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Important Notes

1. **API Key Binding**: Tasks are bound to the API key that created them. You can only view, update, or delete tasks created with your API key.

2. **Authentication**: All operations require a valid API key. If you encounter authentication errors, ensure your API key is properly configured.

3. **Error Handling**: The server provides detailed error messages for common issues:
   - 401: Invalid or missing API key
   - 404: Task not found or doesn't belong to your API key
   - 400: Invalid request data

4. **Task Lifecycle**: Tasks follow this lifecycle:
   ```
   TODO → IN_PROGRESS → DONE
              ↓
          CANCELLED
   ```

### Environment Variables

- `TASK_API_KEY`: Your API key for authentication (required)
- `TASK_API_BASE_URL`: Base URL of the task API (default: http://localhost:8000)

### Getting an API Key

To get started with task management:
1. Download the **MCP Client** app from the Apple App Store
2. Create an account and generate your API key
3. Use the API key in your MCP server configuration

## For Developers

### Installation

```bash
# Using UV (recommended)
uv pip install -e .

# Or using pip
pip install -e .
```

### Running the Server

```bash
# Set your API key
export TASK_API_KEY="your_api_key_here"

# Run the server
uv run python server.py
```

### MCP Configuration

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "task-management": {
      "command": "uv",
      "args": ["run", "python", "/path/to/mcp-server/server.py"],
      "env": {
        "TASK_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### API Documentation

The underlying API follows RESTful principles with the following endpoints:
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/` - List all tasks
- `GET /api/tasks/{task_id}` - Get a specific task
- `PUT /api/tasks/{task_id}` - Update a task
- `DELETE /api/tasks/{task_id}` - Delete a task

All endpoints require the `X-API-Key` header for authentication.