# MCP server for the `literature-*` skills (github.com/shutallbridge/skills).
# Runs on the host (not in a sandbox), so it has network access and local hardware.
#
# Tools to implement:
# - get_library(): {path, id, source: "env" | "config" | "default", initialized}.
#   initialized = folder has the .literature-library marker. Skills call this first.
# - init_library(path): create or adopt the library folder (papers/, index.md, and the
#   .literature-library marker with a random id), then save it to
#   ~/.config/literature-tools/config.toml. Safe to run again on the same folder.
#   Works the same in every client (Cowork can't prompt for plugin settings).
#   If LITERATURE_ROOT is set, report that it takes precedence instead.
# - fetch_metadata(identifier): DOI or arXiv ID -> CSL-JSON-aligned frontmatter
#   (DOI content negotiation via doi.org; arXiv API for version dates/comments).
# - convert_pdf(key): papers/<key>/paper.pdf -> body of papers/<key>/paper.md,
#   written directly to disk (preserving frontmatter); returns only a short summary.
#
# Library folder lookup: LITERATURE_ROOT env var > saved config > ~/Literature (expanduser).
# Tools take paper keys, not paths.
#
# Tool descriptions must be usable without the skills (other MCP clients don't load them);
# the skills add the full procedures on top.
#
# In Cowork the agent's shell sees the library at a VM mount path, not the host path
# get_library returns; the skills find it via the marker's id. Never exchange absolute paths.

import os
import platform
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

INSTRUCTIONS = """\
Manages a file-based library of academic papers on the user's machine.
Call get_library before touching the library; never assume its path.
If it isn't initialized, set it up first with init_library.
Tools take paper keys; refer to files only by library-relative paths.

Layout under the library root:
- index.md: one line per paper
- papers/<key>/paper.pdf: original PDF
- papers/<key>/paper.md: CSL-JSON-aligned frontmatter + converted full text
- papers/<key>/notes.md: the user's notes

Keys: {firstauthor-family}-{year}-{2-4 title words}, lowercase, hyphenated.
"""

mcp = MCPServer("literature-tools", instructions=INSTRUCTIONS)


# TEMPORARY: probe where the client runs this server (host vs. VM). Remove once answered.
@mcp.tool()
def debug_env() -> dict:
    """Diagnostic: report where this MCP server process runs (OS, host, user, paths).

    Temporary tool for testing client setups such as Claude Cowork.
    """
    home = Path.home()
    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "machine": platform.machine(),
        "hostname": platform.node(),
        "user": os.environ.get("USER") or os.environ.get("USERNAME"),
        "home": str(home),
        "cwd": os.getcwd(),
        "python": sys.executable,
        "literature_root_env": os.environ.get("LITERATURE_ROOT"),
        "home_literature_exists": (home / "Literature").exists(),
        "paths_exist": {p: Path(p).exists() for p in ["/Users", "/sessions", "/mnt"]},
        "env_names": sorted(
            k for k in os.environ if k.startswith(("CLAUDE", "COWORK", "MCP"))
        ),
    }
