# Filtered Allstacks API Endpoints (Non-Admin, Non-Destructive)

## Exclusions Applied:
- ❌ All `/api/v1/iadmin/*` endpoints (admin only)
- ❌ DELETE endpoints for: organizations, services, projects (highly destructive)
- ❌ DELETE endpoints for: service users, core data (irreversible)
- ✅ INCLUDED: DELETE for soft-deletable items (invites, widgets, configs, labels, reports)

## Total Endpoints After Filtering: ~270

---

## Phase 1 (Option B): Critical Endpoints (~100 tools)

### Fix Existing 54 + Add 46 Most Critical

#### 1. Metrics & Analytics (20 tools)
- Fix GMDTS endpoint
- Fix Metrics V2 endpoints
- Add insight configs
- Add population benchmarks

#### 2. Service Items (12 tools)
- Fix service items endpoint
- Fix parent service items
- Add property keys lookup

#### 3. Organization (15 tools)
- Fix existing org tools
- Add org settings management
- Add company metrics CRUD

#### 4. Users & Teams (15 tools)
- Add full user CRUD
- Add invited users CRUD
- Add role management

#### 5. Labels & Tags (12 tools)
- Add label families
- Add bulk operations
- Fix service user tags

#### 6. Dashboards (10 tools)
- Complete dashboard CRUD
- Complete widget CRUD
- Shared links

#### 7. AI Reports (7 tools)
- List, create, get, update, delete, cancel

#### 8. Risk Definitions (6 tools)
- Full CRUD for risk definitions

#### 9. Personal Access Tokens (6 tools)
- Full CRUD for PATs

**Subtotal: ~103 tools**

---

## Phase 2 (Option A): Remaining Endpoints (~170 tools)

#### 10. Projects (40 tools)
- Project CRUD operations
- Project settings
- Project dashboards
- Project service links
- Project slots
- Project tags
- Autopin messages
- Deploy filters
- Data ingest dates

#### 11. Employee (5 tools)
- Employee metrics
- Employee periods
- Employee users
- Employee metric data

#### 12. Forecasting (10 tools)
- Forecast V3
- Item types for forecasting
- Forecasting properties

#### 13. Capitalization (12 tools)
- Generate capitalization
- Capitalization reports
- Upload reports
- Report configs

#### 14. Work Bundles (15 tools)
- Selectable work bundles (org)
- Selectable work bundles (project)
- Toggle operations
- Work bundle types
- Initial work bundles
- Estimation methods

#### 15. Service Items Extended (10 tools)
- Service item types
- Initial service items
- Estimation methods
- Service item notes

#### 16. Milestones & Portfolio (10 tools)
- Pinned milestones
- Pin/unpin operations
- Custom sort
- Enabled portfolio columns
- Dynamic filter sets

#### 17. Filter Sets & Saved Views (8 tools)
- Metrics filter sets CRUD
- Saved service item views
- Saved work bundle views
- Pin/unpin metrics

#### 18. Slots & Templates (12 tools)
- Organization slots
- Project slots
- Slot configs
- Templates

#### 19. Charts & Analysis (3 tools)
- Chart analysis
- Chart analyze

#### 20. Action AI (8 tools)
- AI metric builder
- Code query
- Code query JSON
- AI auth tokens

#### 21. External AI Services (5 tools)
- Cursor usage data
- Q usage config
- Q usage data

#### 22. Surveys & Developer Experience (10 tools)
- Survey CRUD
- Survey themes
- Survey items
- Survey responses
- Notification preferences

#### 23. Subscriptions (5 tools)
- Dashboard subscriptions
- Alert subscriptions
- Send subscriptions

#### 24. Configs (6 tools)
- Organization configs CRUD

#### 25. Team Management (8 tools)
- Team categories CRUD
- Service user info
- Service issue states
- Manageable roles

#### 26. User Operations (5 tools)
- Favorite workspace
- Get organization
- Save welcome info
- Apply promo code

#### 27. Visualization & Reporting (3 tools)
- Tree visualization
- Service properties

#### 28. Utilities (2 tools)
- Generate RSA key pair

**Subtotal: ~167 tools**

---

## Grand Total: ~270 Tools Across 28 Categories


