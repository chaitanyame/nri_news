---
description: "Task breakdown for Global News Brief implementation"
created: 2025-12-15
---

# Tasks: Global News Brief

**Feature Branch**: `1-global-news-brief`  
**Input Documents**: [plan.md](plan.md), [spec.md](spec.md), [data-model.md](data-model.md), [contracts/](contracts/), [research.md](research.md), [quickstart.md](quickstart.md)

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1, US2, US3, US4)
- All file paths are absolute from repository root

## Implementation Strategy

**MVP Scope**: User Story 1 (US1) + User Story 4 (US4) = Regional morning news with automation  
**Incremental Delivery**: US1 → US4 → US2 → US3  
**Parallel Opportunities**: Backend models + Frontend components + GitHub workflows can be built simultaneously after foundational phase

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend directory structure at `/workspaces/us_ind_world_news/backend/` with `src/fetchers/`, `src/models/`, `src/utils/`, `scripts/`, `tests/` subdirectories
- [ ] T002 Create frontend directory structure at `/workspaces/us_ind_world_news/frontend/` with `css/`, `js/`, `assets/` subdirectories
- [ ] T003 Create data directory structure at `/workspaces/us_ind_world_news/data/` with `usa/`, `india/`, `world/` subdirectories
- [ ] T004 Initialize Python virtual environment and create `/workspaces/us_ind_world_news/backend/requirements.txt` with `openai>=1.0.0`, `pydantic>=2.0.0`, `python-dotenv>=1.0.0`, `pytest>=7.0.0`
- [ ] T005 [P] Create `.env.example` at `/workspaces/us_ind_world_news/backend/.env.example` with `PERPLEXITY_API_KEY=your_api_key_here`
- [ ] T006 [P] Create `.gitignore` at `/workspaces/us_ind_world_news/.gitignore` to exclude `venv/`, `*.pyc`, `__pycache__/`, `.env`, `.pytest_cache/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 Implement Pydantic data models in `/workspaces/us_ind_world_news/backend/src/models/bulletin.py` (Bulletin entity with id, region enum [usa|india|world], date, period enum [morning|evening], generated_at, version, articles[], metadata)
- [ ] T008 [P] Implement Pydantic data models in `/workspaces/us_ind_world_news/backend/src/models/article.py` (Article entity with title max 120 chars, summary 40-500 chars, category enum, source, citations[], article_id)
- [ ] T009 [P] Implement exponential backoff retry logic in `/workspaces/us_ind_world_news/backend/src/utils/retry_logic.py` (3 retries with 1s, 2s, 4s delays, handle rate limit errors)
- [ ] T010 [P] Implement structured logger in `/workspaces/us_ind_world_news/backend/src/utils/logger.py` (JSON format with timestamp, level, message, context fields)
- [ ] T011 Create Perplexity API client wrapper in `/workspaces/us_ind_world_news/backend/src/fetchers/perplexity_client.py` (OpenAI client with base_url='https://api.perplexity.ai', sonar model, temp=0.3, max_tokens=1000, search_recency_filter='day', integrate retry logic from T009)
- [ ] T012 Implement JSON formatter in `/workspaces/us_ind_world_news/backend/src/fetchers/json_formatter.py` (convert Perplexity API response to Bulletin/Article schema, validate with Pydantic models)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Regional Morning News Catchup (Priority: P1) 🎯 MVP

**Goal**: Users can view morning news summaries for a single region in a responsive card layout

**Independent Test**: Visit site at 8 AM, select USA region, verify 5-10 news cards appear with titles, summaries, citations, and categories; test on mobile (320px) to confirm vertical card stacking

### Implementation for User Story 1

- [ ] T013 [P] [US1] Create HTML structure in `/workspaces/us_ind_world_news/frontend/index.html` with header (logo, region filter buttons), main (bulletin cards container), footer (attribution)
- [ ] T014 [P] [US1] Add Tailwind CSS via CDN in `/workspaces/us_ind_world_news/frontend/index.html` `<head>` with SRI integrity hash
- [ ] T015 [P] [US1] Add custom CSS overrides in `/workspaces/us_ind_world_news/frontend/css/styles.css` for card hover states, category badge colors (politics: blue, economy: green, technology: purple, etc.)
- [ ] T016 [US1] Implement bulletin loader in `/workspaces/us_ind_world_news/frontend/js/bulletin-loader.js` (async fetch from `/data/{region}/{date}-morning.json`, parse JSON, validate schema, handle 404 errors)
- [ ] T017 [US1] Implement card rendering logic in `/workspaces/us_ind_world_news/frontend/js/app.js` (loop through articles, create card DOM elements with title, summary, category badge, source link, citation links)
- [ ] T018 [US1] Add region filter functionality in `/workspaces/us_ind_world_news/frontend/js/app.js` (USA/India/World buttons, update active state, reload bulletin for selected region)
- [ ] T019 [US1] Add responsive breakpoints in `/workspaces/us_ind_world_news/frontend/css/styles.css` (mobile 320px: vertical stack, tablet 768px: 2 columns, desktop 1440px: 3 columns)
- [ ] T020 [US1] Add loading state UI in `/workspaces/us_ind_world_news/frontend/js/app.js` (skeleton cards, spinner, "Loading news..." message while fetching data)
- [ ] T021 [US1] Add error state UI in `/workspaces/us_ind_world_news/frontend/js/app.js` (show "Unable to load bulletin" message on fetch failure, retry button)

**Checkpoint**: User Story 1 complete - users can view morning regional news with responsive design

---

## Phase 4: User Story 4 - Automated Fresh Content (Priority: P1) 🎯 MVP

**Goal**: News bulletins are automatically fetched and published without manual intervention

**Independent Test**: Observe GitHub Actions workflows at 7 AM EST/IST/UTC, verify new JSON files appear in `data/{region}/`, confirm Perplexity API integration works end-to-end

### Implementation for User Story 4

- [ ] T022 [P] [US4] Implement CLI script in `/workspaces/us_ind_world_news/backend/scripts/fetch_news.py` with argparse for `--region` [usa|india|world] and `--period` [morning|evening] flags
- [ ] T023 [US4] Integrate Perplexity prompt templates in `/workspaces/us_ind_world_news/backend/scripts/fetch_news.py` (load prompt from `specs/1-global-news-brief/contracts/perplexity-prompt-{region}-{period}.md`, inject date/timezone, send to API)
- [ ] T024 [US4] Add JSON file writing logic in `/workspaces/us_ind_world_news/backend/scripts/fetch_news.py` (format filename as `data/{region}/{YYYY-MM-DD}-{period}.json`, ensure directory exists, write Bulletin JSON with atomic file operations)
- [ ] T025 [US4] Add error handling and logging in `/workspaces/us_ind_world_news/backend/scripts/fetch_news.py` (log start/end timestamps, API response status, file write success, handle API errors with retry logic)
- [ ] T026 [P] [US4] Create USA morning workflow at `/workspaces/us_ind_world_news/.github/workflows/fetch-usa-morning.yml` (cron: '55 11 * * *' for 7 AM EST, run on self-hosted runner, execute `python backend/scripts/fetch_news.py --region usa --period morning`, commit new JSON to main branch)
- [ ] T027 [P] [US4] Create USA evening workflow at `/workspaces/us_ind_world_news/.github/workflows/fetch-usa-evening.yml` (cron: '55 1 * * *' for 9 PM EST, run on self-hosted runner, execute `python backend/scripts/fetch_news.py --region usa --period evening`)
- [ ] T028 [P] [US4] Create India morning workflow at `/workspaces/us_ind_world_news/.github/workflows/fetch-india-morning.yml` (cron: '25 1 * * *' for 7 AM IST, run on self-hosted runner, execute `python backend/scripts/fetch_news.py --region india --period morning`)
- [ ] T029 [P] [US4] Create India evening workflow at `/workspaces/us_ind_world_news/.github/workflows/fetch-india-evening.yml` (cron: '25 15 * * *' for 9 PM IST, run on self-hosted runner, execute `python backend/scripts/fetch_news.py --region india --period evening`)
- [ ] T030 [P] [US4] Create World morning workflow at `/workspaces/us_ind_world_news/.github/workflows/fetch-world-morning.yml` (cron: '55 6 * * *' for 7 AM UTC, run on self-hosted runner, execute `python backend/scripts/fetch_news.py --region world --period morning`)
- [ ] T031 [P] [US4] Create World evening workflow at `/workspaces/us_ind_world_news/.github/workflows/fetch-world-evening.yml` (cron: '55 20 * * *' for 9 PM UTC, run on self-hosted runner, execute `python backend/scripts/fetch_news.py --region world --period evening`)
- [ ] T032 [US4] Add workflow error notification logic in all 6 workflow files (create GitHub issue on 2 consecutive failures with workflow name, error log, timestamp)
- [ ] T033 [P] [US4] Create GitHub Pages deployment workflow at `/workspaces/us_ind_world_news/.github/workflows/deploy-pages.yml` (trigger on push to main, deploy `frontend/` directory to GitHub Pages)
- [ ] T034 [US4] Add `PERPLEXITY_API_KEY` to GitHub repository secrets (navigate to Settings → Secrets → Actions, add new secret)

**Checkpoint**: User Story 4 complete - automated workflows fetch and publish news twice daily for all regions

---

## Phase 5: User Story 2 - Evening News & Multi-Region (Priority: P2)

**Goal**: Users can toggle between morning/evening bulletins and switch regions without page reload

**Independent Test**: Visit site at 9 PM, toggle between morning/evening periods, switch between USA/India/World regions, verify distinct news appears for each combination without page refresh

### Implementation for User Story 2

- [ ] T035 [P] [US2] Add morning/evening toggle UI in `/workspaces/us_ind_world_news/frontend/index.html` (two radio buttons or toggle switch in header, default to current time period)
- [ ] T036 [US2] Implement period toggle functionality in `/workspaces/us_ind_world_news/frontend/js/app.js` (detect toggle change, update `currentPeriod` state, reload bulletin with new period parameter)
- [ ] T037 [US2] Update bulletin loader in `/workspaces/us_ind_world_news/frontend/js/bulletin-loader.js` to accept `period` parameter (construct URL as `/data/{region}/{date}-{period}.json`)
- [ ] T038 [US2] Add auto-detection of current period in `/workspaces/us_ind_world_news/frontend/js/app.js` (get current hour, if 7 AM - 8 PM → morning, if 9 PM - 6 AM → evening)
- [ ] T039 [US2] Add region transition animation in `/workspaces/us_ind_world_news/frontend/css/styles.css` (fade-out old cards, fade-in new cards, 200ms duration)
- [ ] T040 [US2] Update region filter buttons in `/workspaces/us_ind_world_news/frontend/js/app.js` to preserve period selection when switching regions (maintain `currentPeriod` state across region changes)

**Checkpoint**: User Story 2 complete - users can view evening bulletins and switch between all regions seamlessly

---

## Phase 6: User Story 3 - Historical Browsing & Dark Mode (Priority: P3)

**Goal**: Users can browse past 7 days of bulletins and toggle between light/dark themes

**Independent Test**: Select yesterday's date in sidebar, verify historical bulletins load correctly, toggle dark mode, confirm all UI elements adapt with proper contrast, test system preference detection

### Implementation for User Story 3

- [ ] T041 [P] [US3] Add sidebar with date picker in `/workspaces/us_ind_world_news/frontend/index.html` (vertical list of past 7 days, formatted as "Mon, Dec 15", highlight current date)
- [ ] T042 [P] [US3] Implement date navigation logic in `/workspaces/us_ind_world_news/frontend/js/date-navigator.js` (generate array of past 7 dates using DayJS, render date buttons, handle click events)
- [ ] T043 [US3] Update bulletin loader in `/workspaces/us_ind_world_news/frontend/js/bulletin-loader.js` to accept `date` parameter (construct URL as `/data/{region}/{date}-{period}.json`, validate date is within 7-day window)
- [ ] T044 [US3] Add "data not available" handling in `/workspaces/us_ind_world_news/frontend/js/bulletin-loader.js` (show message "Bulletin not found for {date}" when 404 occurs, distinguish between missing file vs network error)
- [ ] T045 [P] [US3] Add DayJS library via CDN in `/workspaces/us_ind_world_news/frontend/index.html` `<head>` with SRI integrity hash
- [ ] T046 [P] [US3] Create dark theme CSS variables in `/workspaces/us_ind_world_news/frontend/css/styles.css` (define `--bg-dark`, `--text-dark`, `--card-bg-dark`, `--border-dark` with 4.5:1 contrast ratio)
- [ ] T047 [P] [US3] Create light theme CSS variables in `/workspaces/us_ind_world_news/frontend/css/styles.css` (define `--bg-light`, `--text-light`, `--card-bg-light`, `--border-light` with 4.5:1 contrast ratio)
- [ ] T048 [US3] Implement theme manager in `/workspaces/us_ind_world_news/frontend/js/theme-manager.js` (detect system preference with `window.matchMedia('prefers-color-scheme: dark')`, load saved preference from localStorage, apply theme by adding/removing `dark` class on `<html>`)
- [ ] T049 [US3] Add theme toggle button in `/workspaces/us_ind_world_news/frontend/index.html` header (sun/moon icon, positioned in top-right corner)
- [ ] T050 [US3] Add theme toggle functionality in `/workspaces/us_ind_world_news/frontend/js/theme-manager.js` (handle toggle button click, swap theme, save preference to localStorage as `theme: 'light'|'dark'`)

**Checkpoint**: User Story 3 complete - users can browse historical bulletins and customize theme preference

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Cleanup, optimization, testing, and deployment readiness

- [ ] T051 [P] Implement 7-day retention cleanup script in `/workspaces/us_ind_world_news/backend/scripts/cleanup_old_data.py` (scan `data/` directories, parse filenames, delete files older than 7 days from current date)
- [ ] T052 [P] Create cleanup workflow at `/workspaces/us_ind_world_news/.github/workflows/cleanup-old-data.yml` (cron: '0 0 * * *' for midnight UTC, run on self-hosted runner, execute cleanup script, commit deletions to main branch)
- [ ] T053 [P] Create `data/index.json` generation logic in `/workspaces/us_ind_world_news/backend/scripts/fetch_news.py` (after writing bulletin, update index with list of available bulletins for fast frontend navigation)
- [ ] T054 [P] Add Lighthouse performance testing script in `/workspaces/us_ind_world_news/backend/tests/test_performance.py` (use `playwright` to audit page, assert score >90, check page weight <500KB)
- [ ] T055 Add comprehensive error messages in `/workspaces/us_ind_world_news/frontend/js/app.js` (network timeout: "Connection slow - retrying...", 404: "Bulletin not published yet", 500: "Service temporarily unavailable")
- [ ] T056 [P] Add meta tags in `/workspaces/us_ind_world_news/frontend/index.html` for SEO (title: "Global News Brief", description: "AI-summarized news from India, USA, and World", og:image, viewport)
- [ ] T057 [P] Add favicon and Apple touch icon in `/workspaces/us_ind_world_news/frontend/assets/` (newspaper icon, 32×32 and 180×180 sizes)
- [ ] T058 Add accessibility attributes in `/workspaces/us_ind_world_news/frontend/index.html` (ARIA labels for region buttons, alt text for icons, role attributes for interactive elements)
- [ ] T059 Optimize CSS in `/workspaces/us_ind_world_news/frontend/css/styles.css` (remove unused styles, minify for production, ensure <10KB file size)
- [ ] T060 Add README.md at `/workspaces/us_ind_world_news/README.md` with project description, setup instructions (link to quickstart.md), screenshot, GitHub Pages URL

**Checkpoint**: All polish tasks complete - platform ready for production deployment

---

## Dependencies & Parallel Execution

### User Story Completion Order

```
Phase 1 (Setup) → Phase 2 (Foundation) → Phase 3 (US1) + Phase 4 (US4) → Phase 5 (US2) → Phase 6 (US3) → Phase 7 (Polish)
                                              ↓                   ↓
                                           Frontend           Backend + Workflows
                                        (T013-T021)           (T022-T034)
```

**Critical Path**: T001-T012 (Foundation) → T022-T025 (Backend fetch script) → T026-T031 (Workflows) → T033 (Pages deployment)

**MVP Delivery**: Complete T001-T034 for functioning single-region morning news with automation

### Parallel Execution Opportunities

**After Phase 2 Foundation (T012 complete)**:

**Group A - Frontend (US1)**: T013, T014, T015 can run in parallel (HTML, CSS, Tailwind CDN)  
**Group B - Backend (US4)**: T022, T026, T027, T028, T029, T030, T031 can run in parallel (script + workflows)  
**Group C - Workflows (US4)**: T026-T031 can run in parallel (6 workflow files)

**After US1 + US4 complete**:

**Group D - US2 Features**: T035, T039 can run in parallel (UI + CSS)  
**Group E - US3 Features**: T041, T042, T045, T046, T047 can run in parallel (sidebar HTML, JS, DayJS, CSS)

**During Polish Phase**:

**Group F - Final Tasks**: T051, T052, T053, T054, T056, T057, T058, T059, T060 can run in parallel (different files)

---

## Task Summary

**Total Tasks**: 60  
**Parallelizable Tasks**: 28 (47%)  
**Tasks per User Story**:
- Setup: 6 tasks
- Foundation: 6 tasks
- US1 (Regional Morning News): 9 tasks
- US4 (Automated Workflows): 13 tasks
- US2 (Evening & Multi-Region): 6 tasks
- US3 (Historical & Dark Mode): 10 tasks
- Polish: 10 tasks

**MVP Scope (US1 + US4)**: Tasks T001-T034 (34 tasks)  
**Estimated MVP Timeline**: 3-4 days with parallel execution  
**Full Feature Timeline**: 6-7 days with polish phase

---

## Validation Checklist

✅ All tasks follow checklist format: `- [ ] [ID] [P?] [Story?] Description with file path`  
✅ Tasks organized by user story (Phase 3-6 match spec.md user stories)  
✅ Each user story has independent test criteria  
✅ Foundation phase clearly marked as blocking prerequisite  
✅ Parallel opportunities identified with [P] markers  
✅ File paths are absolute and specific  
✅ Dependencies section shows completion order  
✅ MVP scope clearly defined (US1 + US4)  
✅ Task count per story documented
