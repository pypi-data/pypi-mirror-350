Meta learn: keep CLAUDE.md up-to-date; When we discover a new way of working, a workflow, a tool to use, learning about the domain, the project, the environment, etc. please capture it in CLAUDE.md ASAP, commit and push it.
important! lint, commit, push very often
prefer `uv run` over running python directly
`./lint.sh` runs the linter, do it often please

# VS Code Python Environment Setup

To sync VS Code with uv dependencies:

```bash
uv venv .venv
. .venv/bin/activate
uv pip install -r <(uv pip compile pyproject.toml)
```

Then select the `.venv/bin/python` interpreter in VS Code to resolve import warnings.

# Shared Terminal with Claude via Tmux

Scripts for shared terminal workflow:

```bash
# Create session
./tmux-create-session.sh

# Human: attach to session
tmux attach-session -t excel-mcp

# Claude: send command and read result
./tmux-send-read.sh 'command'
```
