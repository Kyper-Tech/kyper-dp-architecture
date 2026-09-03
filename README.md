# kyper-architecture

Architecture-as-code for the Kyper industrial AI platform.
Start with CLAUDE.md, then [docs/design-brief.md](docs/design-brief.md).

## First session in VS Code + Claude Code
Open this folder, open the Claude Code panel, and start with:

1. "Read CLAUDE.md, [docs/design-brief.md](docs/design-brief.md) and adr/. Summarize the architecture
    in 10 lines and list anything in the model that contradicts the brief."
2. "Set up package.json with a pinned likec4 version, verify the LikeC4
    constructs used in architecture/model against the current docs, fix syntax
    only, and run the gate."
3. "Run scripts/check_adr_links.py and resolve every failure without changing
    decisions."
4. "Generate docs/arc42/ skeleton (12 sections) and fill sections 1, 3, 5, 9
    from the brief and ADRs."

Then work the Linear project from [docs/analysis-plan.md](docs/analysis-plan.md), one issue per branch.
