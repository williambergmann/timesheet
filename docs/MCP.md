# MCP Integration Guide

> **Purpose:** Document Model Context Protocol (MCP) servers used to enhance development and operations of the Northstar Timesheet application.
>
> **Status:** ✅ Active (Antigravity IDE)
>
> **Last Updated:** January 20, 2026

---

## ✅ Current MCP Configuration

MCP servers are configured in Antigravity IDE to provide AI-assisted development capabilities.

| MCP Server              | Status    | Description                                        |
| ----------------------- | --------- | -------------------------------------------------- |
| **GitKraken**           | ✅ Active | Git operations, GitHub integration (pre-installed) |
| **Context7**            | ✅ Active | Up-to-date library documentation                   |
| **DBHub**               | ✅ Active | PostgreSQL database access (Render production)     |
| **Filesystem**          | ✅ Active | File access to project directory                   |
| **Sequential-Thinking** | ✅ Active | Enhanced reasoning for complex problems            |

---

## 🚀 Setting Up MCP Servers in Antigravity

### Prerequisites

1. **Node.js 18+** (required for MCP servers)

   ```bash
   node --version  # Should be v18+ or v20+
   ```

2. **Antigravity IDE** installed and running

### Step 1: Check Node.js Version

MCP servers require Node.js 18 or newer. If you have an older version:

```bash
# Check current version
node --version

# If older than v18, upgrade via Homebrew (macOS)
brew install node@20
brew link --overwrite node@20

# May need permissions fix
sudo chown -R $(whoami) /usr/local/lib/node_modules
```

### Step 2: Fix npm Cache (if needed)

If you see `npm ERR! cb() never called!` errors:

```bash
sudo chown -R $(whoami) ~/.npm
npm cache clean --force
```

### Step 3: Locate the MCP Config File

Antigravity stores MCP configuration at:

```
~/Library/Application Support/Antigravity/User/mcp.json
```

You can also find this by:

1. Go to **Extensions** → **MCP Servers - Installed**
2. Click on any server → ⚙️ → **Show Configuration (JSON)**

### Step 4: Configure MCP Servers

Edit the `mcp.json` file with the following configuration:

```json
{
  "servers": {
    "GitKraken": {
      "command": "/Users/YOUR_USERNAME/Library/Application Support/Antigravity/User/globalStorage/eamodio.gitlens/gk",
      "type": "stdio",
      "args": [
        "mcp",
        "--host=antigravity",
        "--source=gitlens",
        "--scheme=antigravity"
      ]
    },
    "context7": {
      "command": "npx",
      "type": "stdio",
      "args": [
        "--package",
        "@upstash/context7-mcp",
        "context7-mcp",
        "--api-key",
        "YOUR_CONTEXT7_API_KEY"
      ]
    },
    "dbhub": {
      "command": "npx",
      "type": "stdio",
      "args": [
        "--package",
        "@bytebase/dbhub",
        "dbhub",
        "--dsn",
        "postgresql://USER:PASSWORD@HOST:5432/DATABASE?sslmode=require"
      ]
    },
    "filesystem": {
      "command": "npx",
      "type": "stdio",
      "args": [
        "--package",
        "@modelcontextprotocol/server-filesystem",
        "mcp-server-filesystem",
        "/Users/YOUR_USERNAME/Developer/northstar"
      ]
    },
    "sequential-thinking": {
      "command": "npx",
      "type": "stdio",
      "args": [
        "--package",
        "@modelcontextprotocol/server-sequential-thinking",
        "mcp-server-sequential-thinking"
      ]
    }
  },
  "inputs": []
}
```

### Step 5: Get Required Credentials

#### Context7 API Key

1. Go to https://context7.com/dashboard
2. Sign up for a free account
3. Copy your API key

#### Database Connection String (DBHub)

1. Go to Render Dashboard → Your Database
2. Click **Connect** → **External**
3. Copy the connection string
4. Add `?sslmode=require` to the end

Example:

```
postgresql://timesheet:PASSWORD@dpg-xxx.oregon-postgres.render.com/timesheet_db?sslmode=require
```

### Step 6: Restart Antigravity

After editing `mcp.json`:

1. Close Antigravity completely
2. Reopen it
3. Go to **Extensions** → **MCP Servers - Installed**
4. Click ⚙️ → **Start Server** for each server

### Step 7: Verify Servers Are Running

Click ⚙️ → **Show Output** for each server. You should see:

**Context7:**

```
Context7 Documentation MCP Server v2.1.0 running on stdio
Discovered 2 tools
```

**DBHub:**

```
DBHub v0.15.0 - Minimal Database MCP Server
MCP server running on stdio
Discovered 2 tools
```

---

## 🔌 What is MCP?

The **Model Context Protocol (MCP)** is an open standard that connects AI assistants to external tools and data sources. MCP servers provide structured access to APIs, databases, and services, allowing AI agents to perform actions on your behalf.

**Benefits for Development:**

- AI can directly interact with git, databases, cloud services
- Reduces context-switching between tools
- Enables automated workflows
- Provides real-time data access

---

## 🧩 Available MCP Servers

### Context7 (Library Documentation)

**Purpose:** Fetches up-to-date documentation for libraries and frameworks.

**Usage:** Add `use context7` to your prompts:

```
How do I set up Flask-Migrate? use context7
```

**Package:** `@upstash/context7-mcp`

**API Key:** Get free at https://context7.com/dashboard

---

### DBHub (Database Access)

**Purpose:** Direct PostgreSQL database access for queries and schema inspection.

**Tools Available:**

- `execute_sql` - Run SQL queries
- `search_objects` - Search database objects

**Package:** `@bytebase/dbhub`

**Connection String Format:**

```
postgresql://USER:PASSWORD@HOST:5432/DATABASE?sslmode=require
```

**Note:** For Render.com databases, you MUST add `?sslmode=require` to the connection string.

---

### Filesystem (File Access)

**Purpose:** Controlled file system access for the AI assistant.

**Package:** `@modelcontextprotocol/server-filesystem`

**Configuration:** Specify the directory path the AI can access.

---

### Sequential-Thinking (Enhanced Reasoning)

**Purpose:** Enables step-by-step reasoning for complex problems.

**Package:** `@modelcontextprotocol/server-sequential-thinking`

---

## 🔧 Troubleshooting

### "You must supply a command" Error

**Cause:** Old npx version (< 7.0) doesn't support `-y` flag.

**Solution:** Use the `--package` syntax instead:

```json
"args": ["--package", "@package/name", "binary-name"]
```

### "SSL/TLS required" Error (DBHub)

**Cause:** Render.com requires SSL connections.

**Solution:** Add `?sslmode=require` to the connection string.

### "cb() never called" Error

**Cause:** Corrupted npm cache or permissions issues.

**Solution:**

```bash
sudo chown -R $(whoami) ~/.npm
npm cache clean --force
```

### "ESM module loader is experimental" Error

**Cause:** Node.js version is too old.

**Solution:** Upgrade to Node.js 18+:

```bash
brew install node@20
brew link --overwrite node@20
```

### Server Not Found in Agent Tools

**Note:** User-configured MCP servers may not be accessible through the agent's internal `list_resources` tool, but they still work for interactive sessions in Antigravity.

---

## 🔒 Security Best Practices

1. **Never commit credentials to git**
   - The `mcp.json` file contains API keys and database passwords
   - It's stored in your user profile, not in the project directory

2. **Use read-only credentials when possible**

   ```sql
   CREATE USER mcp_readonly WITH PASSWORD 'secure_password';
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO mcp_readonly;
   ```

3. **Rotate credentials regularly**

4. **Use SSL for database connections**
   - Always include `?sslmode=require` for cloud databases

---

## 📚 Resources

- [MCP Specification](https://modelcontextprotocol.io/)
- [MCP Server Registry](https://github.com/mcp)
- [Context7 Documentation](https://context7.com/docs)
- [DBHub Documentation](https://github.com/bytebase/dbhub)
- [Antigravity IDE](https://antigravity.ai/)

---

## 📋 Quick Reference

### MCP Config File Location

```
~/Library/Application Support/Antigravity/User/mcp.json
```

### Start/Stop Servers

Extensions → MCP Servers → ⚙️ → Start/Stop Server

### View Server Output

Extensions → MCP Servers → ⚙️ → Show Output

### Required Node.js Version

Node.js 18+ (v20 LTS recommended)

---

_Document updated January 20, 2026_
