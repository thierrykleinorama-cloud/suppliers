# Suppliers — TODO

## DONE

- [x] Database schema (supabase/schema_suppliers.sql) — suppliers + supplier_categories tables
- [x] Database connection (src/database.py) — singleton pattern from InstaHotel
- [x] Data models (src/models.py) — Pydantic Supplier model
- [x] Service layer (src/services/supplier_queries.py) — CRUD + smart search
- [x] Streamlit app entry (app/main.py) — navigation setup
- [x] UI components (app/components/ui.py) — CSS, helpers
- [x] List page (app/pages/1_Suppliers.py) — smart search, filters, clickable table
- [x] Detail page (app/pages/2_Supplier_Detail.py) — view/edit/new/delete
- [x] Config files (.env.example, requirements.txt, .streamlit/config.toml, .gitignore)
- [x] Table creation script (scripts/create_tables.py)
- [x] Create tables in Supabase via Management API
- [x] CRUD test passed: create, read, delete supplier + fetch categories
- [x] Categories updated: Upkeeping, Maintenance, Marketing/Advertising, Utilities, Admin, Financial, Renovation/Design, Other
- [x] Light theme, compact layout, dark readable text in all modes
- [x] Button alignment, mode indicators, hidden Save in view mode
- [x] Own GitHub repo (thierrykleinorama-cloud/suppliers, public)
- [x] Streamlit Cloud deployment configured

## BACKLOG

- [ ] Import/Export feature (CSV/Excel)
- [ ] Git setup: local branch for dev, main for deploy
