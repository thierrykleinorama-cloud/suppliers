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
- [x] Create tables in Supabase via Management API — both suppliers + supplier_categories created
- [x] CRUD test passed: create, read, delete supplier + fetch categories

## BACKLOG

- [ ] Test full UI flow in browser (create, list, search, edit, delete)
- [ ] Import/Export feature (CSV/Excel)
- [ ] Deploy to Streamlit Cloud
- [ ] Git setup: local branch for dev, main for deploy
