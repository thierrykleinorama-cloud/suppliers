# Suppliers — Lessons Learned

## Lesson — Supabase PostgREST can't run DDL
**Rule**: Cannot CREATE TABLE via the PostgREST API (supabase-py client). Must use Management API with SUPABASE_ACCESS_TOKEN or paste SQL directly in Supabase Dashboard SQL Editor.

## Lesson — Same Supabase project across hotel apps
**Rule**: InstaHotel, hotelPandL, and Suppliers all share the same Supabase project (lngrockgpnwaizzyvwsk). Same SUPABASE_URL and SUPABASE_KEY. Copy from any sibling project's .env.
