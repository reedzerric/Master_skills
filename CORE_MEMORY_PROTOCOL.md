# 🧠 Core Memory: Operating Protocols

## 🏷️ Standard 1: YAML & Metadata
Every memory file (skills, knowledge, testing) MUST include a YAML header. 
- Use the `.templates/standard-memory.md` as a baseline.
- `confidence_score` (0.0 to 1.0) reflects how battle-tested the knowledge is.

## 🔗 Standard 2: Cross-Linking & Graphing
Use Obsidian-style `[[path/to/file]]` links to connect related memories.
- **Rules:** 
  - Skills should link to their corresponding Knowledge Base facts.
  - Knowledge Base entries should link to the Testing rules that validate them.

## 🔄 Standard 3: The Active Recall Loop (Maintenance)
Every 10 tasks, or when a major feature is complete, I MUST:
1.  **Garbage Collection:** Delete duplicate or obsolete memory files.
2.  **Synthesis:** If multiple "Skills" are related, merge them into a single, clean "Pattern" file.
3.  **Audit:** Verify that all links are still valid and headers are up to date.

## 📁 Standard 4: The "Git-Tag" Memory History
When requested to commit, I will use a specific tag `[MEM]` for any changes involving the memory folders. This allows us to filter the Git history to see how the project's knowledge evolved.

## 🛠️ Implementation of Git Hooks
*Recommendation: If using Git, run `git config core.hooksPath .githooks` and create a post-commit script to auto-tag memory changes.*
