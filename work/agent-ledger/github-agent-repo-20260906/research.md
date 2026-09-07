run_id: github-agent-repo-20260906
question: "Should MOSAIK split main back into long-lived branches by agent or workstream, and what does GitHub recommend for agent-enabled repositories in 2026?"
decision: pending
scope: "Current GitHub guidance for branch protection, pull requests, agent instructions, agentic workflows, and repository organization; local MOSAIK structure and branch history."
acceptance_criteria:
  - "Use current primary GitHub sources."
  - "Distinguish documented guidance from recommendations inferred for MOSAIK."
  - "Produce an actionable branch and repository model without mutating the repository."
effort_budget: "Bounded research: local audit plus focused official-source web search."
status: decided

concepts:
  - id: C-001
    term: "protected integration branch"
    meaning: "A stable branch receiving reviewed pull requests and required checks."
    related_to: [C-002, C-003]
    origin: inference
    next_query: "GitHub protected branches rulesets pull request required reviews"
  - id: C-002
    term: "short-lived agent branch"
    meaning: "An isolated branch created for one task and merged through a pull request."
    related_to: [C-001, C-004]
    origin: inference
    next_query: "GitHub coding agent pull request branch workflow"
  - id: C-003
    term: "repository agent instructions"
    meaning: "Versioned instructions and scoped guidance that agents read before changing code."
    related_to: [C-005]
    origin: source
    next_query: "GitHub Copilot custom instructions AGENTS.md repository instructions"
  - id: C-004
    term: "agentic workflow"
    meaning: "A GitHub Actions workflow that uses an agent to inspect or change repository state."
    related_to: [C-001, C-002, C-005]
    origin: source
    next_query: "GitHub agentic workflows security human approval"
  - id: C-005
    term: "least privilege and human gate"
    meaning: "Restrict agent permissions and require human review for consequential changes."
    related_to: [C-001, C-004]
    origin: source
    next_query: "GitHub Actions security permissions pull request approval agentic workflows"

queries:
  - id: QRY-001
    text: "GitHub Flow separate branches unrelated changes pull requests delete after merge"
    channel: web
    reason: "Determine the current baseline branch lifecycle."
    expected_gain: "Evidence for short-lived versus long-lived branches."
    result: "GitHub Flow recommends a separate branch per unrelated change, review through a pull request, and deletion after merge while preserving PR and commit history."
    next_action: "Use as baseline against permanent per-agent branches."
  - id: QRY-002
    text: "GitHub Copilot cloud agent branch pull request human review"
    channel: web
    reason: "Understand how GitHub's coding agents are expected to work with branches."
    expected_gain: "Evidence for agent-created task branches and review gates."
    result: "Copilot cloud agent researches and edits on a branch, can open one pull request per task, cannot merge it, and requires human review."
    next_action: "Recommend one branch per agent task, not one permanent branch per agent."
  - id: QRY-003
    text: "GitHub rulesets required pull request reviews status checks code owners protected default branch"
    channel: web
    reason: "Identify controls that replace branch proliferation with review and ownership."
    expected_gain: "Actionable repository governance for main."
    result: "Rulesets can require pull requests, approvals, code-owner reviews, status checks, linear history, and deployment checks."
    next_action: "Recommend protecting main with a ruleset."
  - id: QRY-004
    text: "GitHub Copilot repository instructions AGENTS.md path-specific instructions custom agents"
    channel: web
    reason: "Find the supported way to encode domain expertise for intelligent agents."
    expected_gain: "Agent specialization without long-lived branches."
    result: "GitHub supports repository-wide and path-specific instructions, AGENTS.md, and repository custom agents under .github/agents."
    next_action: "Map MOSAIK domains to scoped instructions and custom agents."
  - id: QRY-005
    text: "GitHub Agentic Workflows permissions safe outputs human approval"
    channel: web
    reason: "Assess automation patterns and safety boundaries for agentic repository work."
    expected_gain: "Avoid granting agents direct write or secret access."
    result: "Agentic Workflows use minimal permissions/read-only agent jobs by default, separate safe outputs, sandboxing, and optional human approval."
    next_action: "Keep deterministic CI separate from agentic workflows and gate writes."

sources:
  - id: S-001
    title: "GitHub flow"
    author_or_org: "GitHub"
    date: "2026"
    accessed: "2026-09-06"
    type: official
    url_or_path: "https://docs.github.com/en/get-started/using-github/github-flow"
    supports: [CL-001]
    contradicts: []
    quality: "Primary product documentation; current page crawled last month."
    limitations: "A lightweight baseline, not a complete multi-agent operating model."
  - id: S-002
    title: "About GitHub Copilot cloud agent"
    author_or_org: "GitHub"
    date: "2026"
    accessed: "2026-09-06"
    type: official
    url_or_path: "https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent"
    supports: [CL-002]
    contradicts: []
    quality: "Primary GitHub documentation; current page crawled yesterday."
    limitations: "Describes Copilot cloud agent, not every third-party agent."
  - id: S-003
    title: "Available rules for rulesets"
    author_or_org: "GitHub"
    date: "2026"
    accessed: "2026-09-06"
    type: official
    url_or_path: "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets"
    supports: [CL-003]
    contradicts: []
    quality: "Primary GitHub documentation; current page crawled today."
    limitations: "Feature availability depends on repository plan and organization settings."
  - id: S-004
    title: "About code owners"
    author_or_org: "GitHub"
    date: "2026"
    accessed: "2026-09-06"
    type: official
    url_or_path: "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners"
    supports: [CL-003]
    contradicts: []
    quality: "Primary GitHub documentation; current page crawled two days ago."
    limitations: "Required review needs repository permissions and an enabled rule."
  - id: S-005
    title: "Adding custom instructions for GitHub Copilot CLI"
    author_or_org: "GitHub"
    date: "2026"
    accessed: "2026-09-06"
    type: official
    url_or_path: "https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions"
    supports: [CL-004]
    contradicts: []
    quality: "Primary GitHub documentation; current page crawled today."
    limitations: "Instruction discovery and precedence vary by client."
  - id: S-006
    title: "Invoking custom agents"
    author_or_org: "GitHub"
    date: "2026"
    accessed: "2026-09-06"
    type: official
    url_or_path: "https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/invoke-custom-agents"
    supports: [CL-004]
    contradicts: []
    quality: "Primary GitHub documentation; current page crawled today."
    limitations: "Custom-agent feature availability and syntax can change."
  - id: S-007
    title: "How Agentic Workflows Work"
    author_or_org: "GitHub Agentic Workflows"
    date: "2026"
    accessed: "2026-09-06"
    type: official
    url_or_path: "https://github.github.com/gh-aw/introduction/how-they-work/"
    supports: [CL-005]
    contradicts: []
    quality: "GitHub-maintained project documentation; current page crawled today."
    limitations: "Agentic Workflows are a distinct product path and public-preview details may change."
  - id: S-008
    title: "Local MOSAIK branch and repository audit"
    author_or_org: "Codex local inspection"
    date: "2026-09-06"
    accessed: "2026-09-06"
    type: local
    url_or_path: "C:/IA/VJ/.git and repository tree"
    supports: [CL-006, CL-007]
    contradicts: []
    quality: "Direct inspection of the working repository."
    limitations: "Does not establish organization-level GitHub settings or hidden open pull requests."

claims:
  - id: CL-001
    statement: "GitHub's lightweight flow favors a short-lived branch per unrelated change, a pull request, review/checks, and deletion after merge."
    status: supported
    evidence: [S-001]
    inference_notes: "Directly documented by GitHub Flow."
    confidence: high
  - id: CL-002
    statement: "GitHub's coding-agent workflow is task-oriented: an agent works on a branch and produces a pull request that a human reviews and merges."
    status: supported
    evidence: [S-002]
    inference_notes: "The task branch is the unit of isolation; agent specialization is configured separately."
    confidence: high
  - id: CL-003
    statement: "Rulesets and CODEOWNERS can provide governance and domain review without requiring one permanent branch per domain."
    status: supported
    evidence: [S-003, S-004]
    inference_notes: "The no-permanent-branch conclusion is an application of the documented controls to MOSAIK."
    confidence: high
  - id: CL-004
    statement: "Repository-wide/path-specific instructions and custom agents are the supported mechanism for encoding specialist agent behavior."
    status: supported
    evidence: [S-005, S-006]
    inference_notes: "This supports specialization by domain while keeping code integrated in one default branch."
    confidence: high
  - id: CL-005
    statement: "Agentic automation should separate read-only reasoning from controlled writes, use minimal permissions, and keep human approval for consequential changes."
    status: supported
    evidence: [S-007]
    inference_notes: "Applies especially to workflows that create PRs, issues, or touch protected files."
    confidence: high
  - id: CL-006
    statement: "MOSAIK currently has one default branch, no .github directory, no tracked GitHub Actions workflow, and no CODEOWNERS file."
    status: supported
    evidence: [S-008]
    inference_notes: "Observed from the current working tree after branch consolidation."
    confidence: high
  - id: CL-007
    statement: "MOSAIK already has coherent domain boundaries in code and documentation: INSTAR, NAYADE, IMAGO, LUCIDA, and adapters/vj."
    status: supported
    evidence: [S-008]
    inference_notes: "The former branches are better represented as paths, instructions, agents, and CODEOWNERS scopes than as permanent branch lines."
    confidence: high

models:
  - id: M-001
    kind: thesis
    statement: "Keep one protected main and recreate permanent branches for INSTAR, NAYADE, IMAGO, LUCIDA, and VJ adapters."
    assumptions: ["Workstreams must evolve independently for long periods.", "Cross-domain integration cost is acceptable."]
    predictions: ["More branch drift and integration overhead.", "Agent context is implied by branch names rather than explicitly versioned instructions."]
    evidence_for: []
    evidence_against: [CL-001, CL-002, CL-004, CL-007]
    status: "rejected as default; retain only for genuinely independent release trains"
  - id: M-002
    kind: thesis
    statement: "Keep one protected main, use short-lived task branches and PRs, and specialize agents/instructions by path and responsibility."
    assumptions: ["The domains share one product and are integrated regularly.", "Main can be protected with CI and review rules."]
    predictions: ["Less drift, clearer PRs, and parallel agent work with controlled integration.", "The repository gains explicit, auditable agent context."]
    evidence_for: [CL-001, CL-002, CL-003, CL-004, CL-005, CL-007]
    evidence_against: []
    status: "preferred"

open_questions:
  - id: OQ-001
    question: "What GitHub plan and organization/team structure does ligereza/mosaik use?"
    why_it_matters: "It determines which rulesets, team-based CODEOWNERS, and Copilot controls are available."
    next_test: "Inspect repository settings or ask the repository owner."
    stop_condition: "Do not block the branch recommendation; use the strongest available subset."
  - id: OQ-002
    question: "Will INSTAR, NAYADE, IMAGO, and LUCIDA ever ship as independently versioned products?"
    why_it_matters: "Independent release trains could justify a small number of long-lived release branches."
    next_test: "Decide based on release cadence and compatibility policy."
    stop_condition: "Until such a need exists, use task branches and tags."

decision:
  recommendation: "Do not recreate the 14 permanent branches. Keep main as the integration branch, create one short-lived branch per issue/agent task, and encode specialization in .github/instructions, .github/agents, CODEOWNERS, and CI/rulesets."
  rationale: "The former branches were implementation milestones that are already integrated; the current GitHub agent model treats a task branch plus reviewed PR as the unit of work, while custom agents and path-specific instructions carry domain expertise."
  risks:
    - "Without branch protection and required CI, main can still be changed too directly."
    - "Large cross-domain changes may produce oversized pull requests."
    - "Agent instructions can conflict if scopes are not clearly assigned."
  reversibility: "High: branches can be recreated from tags/commits, and custom agents/instructions are versioned files."
  confidence: high
  unresolved_but_accepted:
    - "Exact GitHub plan and organization ownership model."
    - "Whether any domain will need independent release branches later."
  next_review_trigger: "A domain needs independent versioning, release cadence, access control, or rollback policy."
