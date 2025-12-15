<!--
SYNC IMPACT REPORT
==================
Version Change: [INITIAL] → 1.0.0
Constitution Type: INITIAL_RATIFICATION
Date: 2025-12-14

Principles Defined:
  1. Code Quality & Architecture - Established modular, serverless-first design principles
  2. AI & Data Processing Standards - Cost-effective LLM usage with robust error handling
  3. User Experience Excellence - Mobile-first, <3s loads, regional separation
  4. Automation & Reliability - GitHub Actions with idempotent operations
  5. Performance & Cost Optimization - Static generation with self-hosted runners

Additional Sections:
  - Technology Stack Requirements (zero third-party dependencies mandate)
  - Quality Gates (constitution compliance checks required)

Templates Status:
  ✅ plan-template.md - Constitution Check section aligns with 5 principles
  ✅ spec-template.md - User story prioritization supports incremental delivery
  ✅ tasks-template.md - Task categorization reflects constitution principles
  ⚠️  No command templates found - no updates needed

Follow-up Actions:
  - None - all placeholders filled
  - Consider creating docs/quickstart.md for developer onboarding

Recommended Commit Message:
  docs: ratify constitution v1.0.0 for global news aggregation platform
  
  - Establish 5 core principles for code quality, AI processing, UX, automation, and performance
  - Define zero third-party dependency policy
  - Set mobile-first <3s page load requirements
  - Mandate GitHub self-hosted runners for cost optimization
-->

# Global News Aggregation Platform Constitution

## Core Principles

### I. Code Quality & Architecture

The platform MUST follow modular, maintainable, and scalable architectural patterns:

- **Agent Harness Pattern**: Memory and state management patterns from telugu_news project
  MUST be reused and extended for multi-regional news processing
- **Serverless & Cloud-Native First**: All components MUST be designed for serverless
  deployment (AWS Lambda, Google Cloud Functions) to minimize operational costs
- **Modular Regional Design**: Each region (India, USA, World) MUST be independently
  deployable and testable as separate modules with shared core libraries
- **Zero Third-Party Dependencies**: MUST minimize external dependencies to reduce
  supply chain risks, licensing concerns, and maintenance burden

**Rationale**: Proven patterns reduce development time; serverless architecture provides
automatic scaling at lowest cost; modular design enables parallel development and
independent regional rollouts; minimal dependencies reduce security surface area.

### II. AI & Data Processing Standards

All AI and data processing operations MUST prioritize cost-effectiveness and reliability:

- **Perplexity AI Preferred**: Use Perplexity AI as the primary LLM provider for
  cost-effective news summarization and processing
- **Robust Error Handling**: ALL API calls MUST implement exponential backoff retry
  logic with circuit breakers (max 3 retries, 1s/2s/4s delays)
- **Smart Caching**: MUST cache all LLM responses for 24 hours to minimize redundant
  processing; cache keys include content hash + timestamp
- **Multi-Language Support**: MUST support English, Hindi, and Telugu with proper
  Unicode handling and language-specific tokenization
- **Graceful Degradation**: If LLM service fails after retries, MUST fall back to
  extractive summarization or raw article display

**Rationale**: Perplexity AI offers competitive pricing; proper error handling ensures
reliability; caching reduces costs by 60-80%; multi-language support is core requirement;
graceful degradation maintains service availability.

### III. User Experience Excellence (NON-NEGOTIABLE)

User experience standards are strictly enforced and non-negotiable:

- **Mobile-First Design**: ALL interfaces MUST be designed for mobile first, then
  progressively enhanced for desktop (breakpoints: 320px, 768px, 1024px, 1440px)
- **Performance Budget**: Page load time MUST be <3 seconds on 3G connections
  (Lighthouse performance score >90)
- **Regional Separation**: Clear visual separation for India, USA, and World news
  sections with distinct color coding or tabs
- **Daily Bulletin Organization**: Each date page MUST display both Morning Bulletin
  (published before 12:00 UTC) and Evening Bulletin (published after 12:00 UTC)
- **Modern Aesthetic**: Clean, modern UI with dark mode and light mode support; MUST
  use system preference detection
- **Date Navigation**: Sidebar MUST provide calendar-style date picker for browsing
  historical bulletins (last 90 days accessible)
- **Pagination**: MUST support pagination for article lists (20 articles per page) with
  clear prev/next navigation

**Rationale**: Mobile-first matches global usage patterns; <3s loads prevent user
abandonment; regional separation improves content discovery; dual bulletins provide
morning/evening consumption patterns; modern design ensures competitive appeal.

### IV. Automation & Reliability

All automation MUST be idempotent, observable, and self-healing:

- **GitHub Actions Scheduled Workflows**: MUST use GitHub Actions for all scheduled
  tasks (news fetching, summarization, site generation) with cron expressions
- **Idempotent Operations**: ALL workflows MUST be safely re-runnable; duplicate
  executions MUST produce identical results (use content hashing for deduplication)
- **Source Failure Handling**: When news sources fail, MUST log error, alert via
  GitHub issue, and continue with available sources (minimum 3 sources per region)
- **Self-Hosted Runners**: MUST use GitHub self-hosted runners for workflow execution
  to eliminate per-minute charges (cost optimization requirement)
- **Monitoring & Alerts**: MUST implement health checks for all scheduled workflows;
  alert on 2 consecutive failures via GitHub issue auto-creation

**Rationale**: GitHub Actions provides free automation platform; idempotent operations
enable safe retries; graceful degradation maintains partial service; self-hosted runners
eliminate GitHub Actions costs; automated alerting enables rapid response.

### V. Performance & Cost Optimization

Cost and performance are first-class design constraints:

- **Static Site Generation**: MUST generate static HTML/CSS/JS for GitHub Pages
  deployment (zero hosting costs)
- **Self-Hosted Runners**: MUST use GitHub self-hosted runners for ALL workflow
  executions (eliminates $0.008/minute Linux runner costs)
- **Build-Time Rendering**: MUST perform all LLM processing, summarization, and
  rendering at build time; zero runtime compute costs
- **Asset Optimization**: MUST minify and compress all assets (CSS, JS, images);
  target <500KB total page weight
- **CDN-Friendly**: MUST generate cache-friendly URLs with content hashes; leverage
  GitHub Pages CDN for global distribution
- **Incremental Builds**: MUST implement incremental regeneration; only rebuild pages
  for new/updated bulletins (reduces build times by 90%)

**Rationale**: Static generation eliminates server costs; self-hosted runners eliminate
CI/CD costs; build-time processing amortizes LLM costs; GitHub Pages provides free global
CDN; incremental builds reduce processing time and LLM API usage.

## Technology Stack Requirements

The following technology constraints are mandatory for cost and maintenance optimization:

- **Static Site Generator**: Eleventy (11ty), Hugo, or Jekyll - MUST support incremental
  builds and data files
- **LLM Provider**: Perplexity AI (primary), with fallback to local summarization models
- **Version Control**: Git with GitHub for hosting, Actions, and Pages
- **Development Environment**: Docker or devcontainer for reproducible development
  (Alpine Linux preferred for minimal footprint)
- **Language Stack**: Python 3.11+ for data processing scripts; vanilla JavaScript
  (ES6+) for client-side interactions (NO frameworks like React/Vue to minimize bundle
  size)
- **Styling**: Vanilla CSS with CSS Grid and Flexbox OR Tailwind CSS (if inline/purged)
- **Storage**: Git repository for content versioning; JSON or YAML for structured data;
  NO external databases
- **CI/CD**: GitHub Actions with self-hosted runners (Linux/Docker-based)

**Constraint Rationale**: These choices collectively drive infrastructure costs to $0/month
while maintaining professional quality and scalability.

## Quality Gates

Before any PR merge or feature release, the following gates MUST pass:

1. **Constitution Compliance**: ALL code changes MUST be reviewed against these 5 core
   principles; violations MUST be explicitly justified with "Complexity Justification"
   section in PR description
2. **Performance Budget**: Lighthouse CI MUST show <3s page load on 3G; failing check
   blocks merge
3. **Mobile Responsiveness**: Visual regression tests MUST pass for 320px, 768px, 1024px
   viewports
4. **Accessibility**: WCAG 2.1 AA compliance MUST be maintained (automated with axe-core)
5. **Cost Impact**: PR MUST include cost impact statement (LLM API calls, build minutes,
   storage delta)
6. **Idempotency Test**: For automation changes, MUST demonstrate identical output on
   repeated runs

## Governance

This constitution establishes the foundational rules for all development on the Global
News Aggregation Platform:

- **Constitutional Supremacy**: This document supersedes all other development practices,
  coding standards, or architectural decisions
- **Amendment Process**: Constitutional amendments require:
  1. Written proposal with rationale in GitHub Discussion
  2. Approval from project maintainer
  3. Migration plan for existing code (if applicable)
  4. Version bump per semantic versioning rules below
- **Version Semantics**:
  - **MAJOR**: Backward-incompatible governance changes (principle removal/redefinition)
  - **MINOR**: New principle added or materially expanded guidance
  - **PATCH**: Clarifications, wording fixes, non-semantic refinements
- **Compliance Review**: ALL pull requests MUST include a Constitution Compliance
  checklist; reviewers MUST verify alignment
- **Complexity Justification**: Any deviation from constitutional principles MUST be
  explicitly justified in PR description under "Complexity Justification" section
- **Living Document**: This constitution should be reviewed quarterly; stale or
  conflicting guidance MUST be resolved

**Version**: 1.0.0 | **Ratified**: 2025-12-14 | **Last Amended**: 2025-12-14
