# MCP server for the `literature` skill (github.com/shutallbridge/skills).
# Runs on the host (not in a sandbox), so it has network access and local hardware.
#
# Tools to implement:
# - fetch_metadata(identifier): DOI or arXiv ID -> CSL-JSON-aligned frontmatter
#   (DOI content negotiation via doi.org; arXiv API for version dates/comments).
# - convert_pdf(key): papers/<key>/paper.pdf -> body of papers/<key>/paper.md,
#   written directly to disk (preserving frontmatter); returns only a short summary.
# - set_library_root(path): save the library folder to ~/.config/literature-tools/config.toml.
#   Works the same in every client (Cowork can't prompt for plugin settings).
#   If LITERATURE_ROOT is set, report that it takes precedence instead.
#
# Library folder lookup: LITERATURE_ROOT env var > saved config > ~/Literature (expanduser).
# Tools take paper keys, not paths.
#
# Tool descriptions must be usable without the skill (other MCP clients don't load it);
# the skill adds the full procedure on top.

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("literature-tools")
