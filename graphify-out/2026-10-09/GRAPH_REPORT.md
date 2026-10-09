# Graph Report - iwb-demo  (2026-10-09)

## Corpus Check
- 113 files · ~27,346 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 7, .ini 2, .tsbuildinfo 2)

## Summary
- 883 nodes · 1758 edges · 65 communities (33 shown, 32 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 86 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `72e67776`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- package.json
- compilerOptions
- Product Learning Studio
- devDependencies
- compilerOptions
- errors.py
- conftest.py
- schemas/story.py
- login
- WorkspaceService
- Settings
- core/__init__.py
- docker-entrypoint.sh
- iwb-demo-backend
- schemas/workspace.py
- routes/workspace.py
- workspaceApi.ts
- ReadinessService
- sqlalchemy_orm
- ReviewService
- UserRepository
- schemas/__init__.py
- VisionFields
- log_auth_event
- ReviewPage.tsx
- database.py
- WorkspacePage.tsx
- pydantic
- StoryService
- Workspace
- User
- WorkspaceRepository
- useAuth.ts
- ReadinessPage.tsx
- env.py
- utils.ts
- Story
- dependencies
- scripts
- App.tsx
- app/config.py
- @vitejs/plugin-react
- router.tsx
- get_db
- health
- start.sh
- api.ts
- BacklogPage.tsx
- authStore
- stop.sh

## God Nodes (most connected - your core abstractions)
1. `Workspace` - 71 edges
2. `User` - 45 edges
3. `Story` - 34 edges
4. `WorkspaceRepository` - 25 edges
5. `WorkspaceService` - 25 edges
6. `StoryService` - 22 edges
7. `ReadinessService` - 21 edges
8. `get_db()` - 20 edges
9. `AcceptanceCriterion` - 20 edges
10. `AuthService` - 19 edges

## Surprising Connections (you probably didn't know these)
- `get_current_user()` --uses--> `User`  [INFERRED]
  backend/app/api/deps.py → backend/app/models/user.py
- `login()` --uses--> `AuthService`  [INFERRED]
  backend/app/api/routes/auth.py → backend/app/services/auth_service.py
- `logout()` --uses--> `User`  [INFERRED]
  backend/app/api/routes/auth.py → backend/app/models/user.py
- `get_review_snapshot()` --uses--> `ReviewSnapshotResponse`  [INFERRED]
  backend/app/api/routes/review.py → backend/app/schemas/review.py
- `create_review_note()` --uses--> `ReviewNoteCreateRequest`  [INFERRED]
  backend/app/api/routes/review.py → backend/app/schemas/review.py

## Import Cycles
- None detected.

## Communities (65 total, 32 thin omitted)

### Community 0 - "package.json"
Cohesion: 0.12
Nodes (15): engines, node, name, private, type, version, autoprefixer, jsdom (+7 more)

### Community 1 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, isolatedModules, jsx, lib, module, moduleResolution, noEmit (+11 more)

### Community 2 - "Product Learning Studio"
Cohesion: 0.06
Nodes (31): API Routes, Authentication, Backend Tests, Build Verification, Contributing, Database Migration Issues, Default Credentials, Deployment Notes (+23 more)

### Community 3 - "devDependencies"
Cohesion: 0.14
Nodes (14): devDependencies, autoprefixer, jsdom, postcss, tailwindcss, @testing-library/jest-dom, @testing-library/react, @testing-library/user-event (+6 more)

### Community 4 - "compilerOptions"
Cohesion: 0.18
Nodes (10): compilerOptions, allowSyntheticDefaultImports, composite, lib, module, moduleResolution, skipLibCheck, strict (+2 more)

### Community 5 - "errors.py"
Cohesion: 0.14
Nodes (10): ApiError, ApiErrorResponse, create_error_response(), ErrorDetail, http_401_handler(), http_403_handler(), http_404_handler(), http_422_handler() (+2 more)

### Community 6 - "conftest.py"
Cohesion: 0.06
Nodes (12): ReviewNote, ReviewShare, ReviewRepository, mock_log_auth_event(), mock_log_authorization_failure(), mock_log_review_action(), mock_log_save_event(), mock_logging() (+4 more)

### Community 7 - "schemas/story.py"
Cohesion: 0.16
Nodes (6): AcceptanceCriterionItem, Config, StoryDraft, StorySaveResponse, StorySetUpdateRequest, ValidationSummary

### Community 8 - "login"
Cohesion: 0.11
Nodes (7): login(), logout(), AuthResponse, AuthTokenPayload, Config, LoginRequest, UserSummary

### Community 9 - "WorkspaceService"
Cohesion: 0.08
Nodes (6): get_readiness(), get_workspace(), update_stories(), update_workspace(), WorkspaceService, TestWorkspaceService

### Community 11 - "core/__init__.py"
Cohesion: 0.13
Nodes (5): create_access_token(), decode_access_token(), get_current_user(), get_password_hash(), verify_password()

### Community 23 - "schemas/workspace.py"
Cohesion: 0.15
Nodes (8): CompletenessInfo, Config, ReviewSummary, StoryResponse, WorkspaceAggregate, WorkspaceAggregateResponse, WorkspaceSaveResponse, WorkspaceUpdateRequest

### Community 24 - "routes/workspace.py"
Cohesion: 0.24
Nodes (4): Config, GapItem, ReadinessResponse, ReadinessSummary

### Community 25 - "workspaceApi.ts"
Cohesion: 0.17
Nodes (15): ReviewWorkspaceSnapshot, AcceptanceCriterionItem, StoryDraft, StorySaveResponse, StorySetUpdateRequest, ValidationSummary, VisionFields, AcceptanceCriterionItem (+7 more)

### Community 26 - "ReadinessService"
Cohesion: 0.13
Nodes (3): AcceptanceCriterion, ReadinessService, TestReadinessService

### Community 28 - "ReviewService"
Cohesion: 0.06
Nodes (10): create_review_note(), get_review_snapshot(), evaluate_readiness(), GapCode, _is_vision_complete(), ReadinessStatus, generate_share_token(), validate_share_token() (+2 more)

### Community 30 - "schemas/__init__.py"
Cohesion: 0.21
Nodes (7): Config, ReviewNoteCreateRequest, ReviewNoteResponse, ReviewReadinessSummary, ReviewSnapshotResponse, ReviewStoryResponse, ReviewWorkspaceSnapshot

### Community 31 - "VisionFields"
Cohesion: 0.18
Nodes (4): CompletenessInfo, Config, VisionFields, VisionSaveResponse

### Community 32 - "log_auth_event"
Cohesion: 0.24
Nodes (4): get_logger(), log_auth_event(), log_authorization_failure(), log_review_action()

### Community 33 - "ReviewPage.tsx"
Cohesion: 0.21
Nodes (12): createReviewNote(), getReviewSnapshot(), ReviewNoteForm(), ReviewNoteFormProps, ReviewWorkspaceSnapshot(), ReviewWorkspaceSnapshotProps, ReviewPage(), ReviewNoteCreateRequest (+4 more)

### Community 34 - "database.py"
Cohesion: 0.11
Nodes (6): upgrade(), create_db_engine(), get_database_url(), get_engine(), get_session_factory(), init_db()

### Community 35 - "WorkspacePage.tsx"
Cohesion: 0.27
Nodes (9): request(), getWorkspace(), updateWorkspace(), AppShell(), AppShellProps, Navbar(), VisionSection(), VisionSectionProps (+1 more)

### Community 36 - "pydantic"
Cohesion: 0.25
Nodes (3): ApiError, Config, ErrorDetail

### Community 39 - "User"
Cohesion: 0.11
Nodes (3): User, AuthService, TestAuthService

### Community 41 - "useAuth.ts"
Cohesion: 0.26
Nodes (11): login(), logout(), clearAuthToken(), setAuthToken(), useAuth(), AuthState, Listener, AuthResponse (+3 more)

### Community 42 - "ReadinessPage.tsx"
Cohesion: 0.21
Nodes (10): getReadiness(), GapItem, GapList(), GapListProps, ReadinessSummaryCard(), ReadinessSummaryCardProps, ReadinessPage(), GapItem (+2 more)

### Community 47 - "dependencies"
Cohesion: 0.33
Nodes (6): dependencies, clsx, react, react-dom, react-router-dom, tailwind-merge

### Community 48 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, preview, test

### Community 49 - "App.tsx"
Cohesion: 0.31
Nodes (5): App(), Providers(), ProvidersProps, router, react-dom

### Community 53 - "router.tsx"
Cohesion: 0.23
Nodes (9): getAuthToken(), RequireAuth(), RequireAuthProps, SignInPage(), mockLogin, mockNavigate, react-router-dom, @testing-library/react (+1 more)

### Community 54 - "get_db"
Cohesion: 0.10
Nodes (4): get_current_user(), get_db(), lifespan(), seed_data()

### Community 58 - "start.sh"
Cohesion: 0.47
Nodes (4): check_prerequisites(), DATABASE_URL, find_available_port(), start.sh script

### Community 60 - "BacklogPage.tsx"
Cohesion: 0.24
Nodes (9): updateStories(), StoryCard(), StoryCardProps, StoryEditorDrawer(), StoryEditorDrawerProps, StoryList(), StoryListProps, BacklogPage() (+1 more)

## Knowledge Gaps
- **120 isolated node(s):** `Config`, `docker-entrypoint.sh script`, `iwb-demo-backend`, `name`, `private` (+115 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 452 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **32 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Workspace` connect `Workspace` to `database.py`, `StoryService`, `conftest.py`, `WorkspaceRepository`, `WorkspaceService`, `get_db`, `ReadinessService`, `sqlalchemy_orm`, `ReviewService`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `Workspace` (e.g. with `WorkspaceRepository` and `ReadinessService`) actually correct?**
  _`Workspace` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `docker-entrypoint.sh script`, `iwb-demo-backend` to the rest of the system?**
  _120 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.11764705882352941 - nodes in this community are weakly interconnected._
- **Why does `User` connect `User` to `database.py`, `conftest.py`, `login`, `WorkspaceService`, `core/__init__.py`, `get_db`, `routes/workspace.py`, `ReadinessService`, `sqlalchemy_orm`, `UserRepository`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `User` (e.g. with `get_current_user()` and `logout()`) actually correct?**
  _`User` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Should `compilerOptions` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._