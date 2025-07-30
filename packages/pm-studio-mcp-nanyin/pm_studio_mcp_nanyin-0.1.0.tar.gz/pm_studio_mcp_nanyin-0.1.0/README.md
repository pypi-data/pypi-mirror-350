# PM Studio MCP

PM Studio MCP is a Model Context Protocol (MCP) server for product management tasks. It provides a suite of tools and utilities to help product managers analyze user feedback, perform competitive analysis, generate data visualizations, and access structured data sources.

## Getting Started
### Set up MCP Runtime - Install uv

For windows: please refers to the [uv official site]https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_2
For macOS: run `brew install uv` (If you don't have Homebrew [click here](https://github.com/ai-microsoft/fsd/blob/main/private/DEVELOPER.md#install-homebrew-on-macos))


### Set up MCP server in your config file
   ```bash
   {
      "mcpServers": {
         "pm-studio-mcp": {
               "command": "uvx",
               "args": [
                  "pm-studio-mcp"
               ],
               "env": {
                  "WORKING_PATH": "{PATH_TO_YOUR_WORKSPACE}/working_dir/",
                  "AZURE_KEY_VAULT_CLIENT_SECRET":"{AZURE_KEY_VAULT_CLIENT_SECRET}",  // optional,this is the key to access all API keys in PM Studio, reach out to us to get the key
               },
               "disabled": false
         }
      }
   }
   ```
##PM Studio MCP Package 
