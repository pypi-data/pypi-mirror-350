# 🚀 Huuh MCP Server - Collaborative AI for everybody! 🎓

The **Huuh MCP Server** is your friendly neighborhood Model Context Protocol server that bridges the gap between AI applications and the [huuh.me](https://huuh.me) platform 🤖💝

With [huuh.me](https://huuh.me) you can:
- 📚 **AI-native knowledge** 
  - create knowledge bases 
  - retrieve and contribute content directly in chat
- 🫂 **shared AI for your team** 
  - share and collaborate on knowledge bases with others
  - let them retrieve and contribute
- 🎭 **better results with flexible usage** 
  - Build and share AI personas (system prompts) 
  - switch from your Research AI to your Marketing AI with in chat

## ✨ What Does This Server Do?

Our server is like a Swiss Army knife for collaboration in the era of AI! 🔧📚 You can:

- 🔍 **Explore Bases**: Search through marketplace public knowledge bases
- 📖 **Access Information**: Retrieve specific information from one of your bases or any public base
- 🎭 **Manage Personas**: Get and update AI personas to quickly apply system prompts in the chat
- 📝 **Contribute Content**: Add your own contributions to bases and help build the knowledge base
- 🛠️ **Contribute Personas**: Contribute personas you find useful to a public base

To use the server, please register on the [huuh.me](https://huuh.me) platform and get your API key. This server is designed to work with the huuh API, so you'll need an account to get started! 🌐

## 🛠️ Available Tools - Your AI Toolbox!

Our server comes packed with **7 incredible tools** that make working with educational content a breeze:

### 1. 🏠 `get_user_options`
**What it does:** Gets information about your available bases, modules, and files  
**Perfect for:** Starting your journey and understanding what's available to you!

### 2. 🛒 `search_marketplace`
**What it does:** Search for bases in the marketplace  
**Parameters:** 
- `query` (string) - Your search terms (max 150 characters)  
**Perfect for:** Discovering new bases and educational opportunities!

### 3. 🔍 `retrieve_information`
**What it does:** Retrieve specific information from base content  
**Parameters:**
- `query` (string) - What you're looking for (max 150 characters)
- `base_id` (string) - Which base to search in
- `relevant_modules` (array, optional) - Specific modules to focus on
- `relevant_groups` (array, optional) - Specific groups to include
- `relevant_file_ids` (array, optional) - Specific files to search  
**Perfect for:** Getting precise answers from base materials!

### 4. 📝 `contribute`
**What it does:** Add your own content contributions to bases  
**Parameters:**
- `base_id` (string) - Course to contribute to
- `folder_number` (string) - Which folder to add content to
- `contribution_title` (string) - Title of your contribution
- `contribution_content` (string) - Your amazing content (max 30,000 characters)  
**Perfect for:** Sharing knowledge and helping others learn!

### 5. 🎭 `get_persona`
**What it does:** Retrieve information about AI personas  
**Parameters:**
- `title` (string) - Name of the persona you want  
**Perfect for:** Applying your stored system prompts in your chat!

### 6. 🔄 `refresh_persona`
**What it does:** Update persona content and behavior  
**Parameters:**
- `title` (string) - Persona to update
- `new_content` (string) - Updated persona content
- `base_id` (string, optional) - Course-specific persona updates  
**Perfect for:** Iteratively improving system prompts for future use!

### 7. 🎁 `contribute_persona`
**What it does:** Add a brand new persona to a base (yours or public)
**Parameters:**
- `base_id` (string) - Course to add persona to
- `persona_title` (string) - Name of your new persona
- `persona_content` (string) - Persona description and behavior (max 150 characters)  
**Perfect for:** Storing system prompts to reapply them in the future!

## 🚀 Quick Start - Get Up and Running in Seconds!

### Claude Desktop Configuration

Add the following configuration to `claude-desktop.json`:

```json
{
  "mcpServers": {
    "linkedin-mcp": {
      "command": "uvx",
      "args": ["huuh-mcp"],
      "env": {
        "HUUH_APIK_KEY": "<yours>"
      }
    }
  }
}
```

## 🔧 Development Setup - For the Code Enthusiasts!

Want to contribute or customize? We love developers! 💻❤️

### Prerequisites
- Python 3.12+ 🐍
- [uv](https://docs.astral.sh/uv/) package manager ⚡

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/infolab-ai/mcp.git
cd mcp

# Install dependencies with uv (it's lightning fast!)
uv sync

# Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Set up your environment variables
cp .env.sample .env
# Edit .env with your API credentials

# Run the server in development mode
python -m huuh_mcp.server
```

### Environment Variables 📋

Create a `.env` file with:

```env
# Your HUUH API key (get this from your account settings)
HUUH_APIK_KEY=your_api_key_here

# Optional: Set logging level
LOG_LEVEL=INFO
```

## 🔐 Authentication - Secure and Simple!

The server uses API key authentication to keep your data safe! 🛡️

1. 🔑 Get your API key from the [huuh.me](https://huuh.me) platform
2. 🔒 Set it in your environment variables
3. ✨ The server handles the rest automatically!

## 📜 License - Freedom to Learn and Build!

This project is licensed under the **MIT License** 📄 - which means you're free to:

- ✅ Use it commercially
- ✅ Modify it however you want
- ✅ Distribute it to others
- ✅ Use it privately
- ✅ Contribute back to the community

The only requirement? Keep the license notice in derivative works. That's it! 🎉

## 🤝 [Contributing - Join our Discord Community!](https://discord.gg/6YypQX2F)

We'd love your help making this server even more awesome! 🌟

- 🐛 Found a bug? Open an issue!
- 💡 Have an idea? We want to hear it!
- 🔧 Want to contribute code? Send us a PR!
- 📚 Improve documentation? You're our hero!