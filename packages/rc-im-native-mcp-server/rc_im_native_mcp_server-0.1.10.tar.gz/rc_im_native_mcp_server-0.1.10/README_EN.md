# Rongcloud Native MCP Server (Rust)

Rongcloud IM Service based on MCP Protocol (Rust SDK Wrapper)

[中文文档](README.md)

## Usage

### Prerequisites - Install UV Package Manager

```bash
 pip install uv 
```

UV is a Python package installation and dependency management tool written in Rust, offering faster and more efficient experience than traditional tools (like pip). It focuses on two core objectives:

Speed: UV is optimized for package installation, dependency resolution, and virtual environment creation, providing significant performance improvements.
Efficiency: UV reduces resource consumption, especially in large projects.

The UVX command we'll use later means "download if not local, then run", and it runs in a separate virtual environment each time, making it ideal for large model/Agent-related scenarios.

### Using in Cursor (Similar for Cline / Claude)

Configuration path: Cursor -> Preferences -> Cursor Settings -> MCP -> Add new global MCP server
Configuration content:

```json
{
  "mcpServers": {
    "rc_im_native_mcp": {
      "name": "rc-im-native-mcp-server",
      "type": "stdio",
      "command": "uvx",
      "args": [
        "rc-im-native-mcp-server"
      ],
      "env": {
          "APP_KEY": "Your Rongcloud App Key",
          "TOKEN": "Your Rongcloud SDK Token (from Server API)",
          "NAVI_HOST": "Your Rongcloud SDK Nav URL"
      }
    }
  }
}
```

### Using in Cherry Studio

First install both UV and Bun (both required), then restart Cherry Studio. Configure as shown in the images below:
![Cherry Studio Interface Example](readme_img/cherry-studio-0.png)
![Cherry Studio Interface Example](readme_img/cherry-studio.png)

## Main Features and Tools Description (Continuously Updated)

The server exposes the following tools through the MCP protocol:

### 1. `init_and_connect`

- **Function**: Initialize IM engine and connect to IM server
- **Parameters**:
  - `timeout_sec` (int, default 30): Connection timeout in seconds
- **Returns**:
  - `code` (int): 0 for success, non-zero for failure
  - `message` (str): Result description
  - `init_success` (bool): Whether initialization was successful
  - `connect_success` (bool): Whether connection was successful

### 2. `send_message`

- **Function**: Send IM message to specified user (supports private/group chat)
- **Parameters**:
  - `receiver` (str): Recipient ID
  - `content` (str): Message content
  - `conversation_type` (int, default 1): Conversation type, 1=private chat, 2=group chat
- **Returns**:
  - Failure: `code`, `message`
  - Success: `code`, `message_id`, `message`

### 3. `get_history_messages`

- **Function**: Get historical messages with specified user
- **Parameters**:
  - `target_id` (str): Target ID (User_ID or Group_ID)
  - `conversation_type` (int, default 1): Conversation type, 1=private chat, 3=group chat
  - `order_asc` (bool, default False): Sort order, False=descending, True=ascending
  - `count` (int, default 10): Number of messages to retrieve
- **Returns**:
  - Failure: `code`, `message`
  - Success: `code`, `messages` (message array)

### 4. `disconnect`

- **Function**: Disconnect from IM server
- **Parameters**: None
- **Returns**:
  - `code` (int): 0 for success, non-zero for failure
  - `message` (str): Result description

## Common Issues

### Q: Why does the server list show a yellow dot in Cursor even after configuration?

A: If the server list shows a yellow dot, try installing the UV command first, then restart Cursor and re-enable the service switch.

### Q: Why does Cherry Studio keep reporting errors?

A: Make sure both UV and Bun are installed successfully, restart Cherry Studio, and then re-enable the service switch.

### Q: Why do tool calls return errors?

A: Make sure environment variables (APP_KEY, TOKEN, NAVI_HOST) are correctly set, restart the service, and try calling the tools again.

## Technical Support

If you encounter issues, please:

1. Check if environment variables are correctly set
2. Check log output for specific error messages
3. Create an issue in the open source project
