-- Suppliers Database Schema
-- Project: Suppliers Directory for Hotel Noucentista
-- Supabase project: lngrockgpnwaizzyvwsk

CREATE TABLE IF NOT EXISTS suppliers (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company         TEXT NOT NULL,
    category        TEXT,
    sex             TEXT,          -- 'Mr' or 'Mrs'
    last_name       TEXT,
    first_name      TEXT,
    phone1          TEXT,
    phone2          TEXT,
    email           TEXT,
    website         TEXT,
    facebook        TEXT,
    instagram       TEXT,
    address         TEXT,
    city            TEXT,
    country         TEXT DEFAULT 'Spain',
    vat_number      TEXT,          -- Company VAT (NIF/CIF or foreign)
    payment_terms   TEXT,
    iban            TEXT,
    hotels          TEXT[],        -- e.g. {'MIAOU','COIN','WOUAF'}
    rating          INTEGER CHECK (rating >= 1 AND rating <= 5),
    notes           TEXT,
    tags            TEXT[],
    created_at      TIMESTAMPTZ DEFAULT now(),
    updated_at      TIMESTAMPTZ DEFAULT now()
);

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION update_suppliers_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_suppliers_updated_at
    BEFORE UPDATE ON suppliers
    FOR EACH ROW
    EXECUTE FUNCTION update_suppliers_updated_at();

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_suppliers_category ON suppliers(category);
CREATE INDEX IF NOT EXISTS idx_suppliers_city ON suppliers(city);
CREATE INDEX IF NOT EXISTS idx_suppliers_country ON suppliers(country);
CREATE INDEX IF NOT EXISTS idx_suppliers_hotels ON suppliers USING GIN(hotels);

-- Preset categories table (extensible by users)
CREATE TABLE IF NOT EXISTS supplier_categories (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL UNIQUE,
    sort_order  INTEGER DEFAULT 0,
    created_at  TIMESTAMPTZ DEFAULT now()
);

-- Seed preset categories
INSERT INTO supplier_categories (name, sort_order) VALUES
    ('Upkeeping', 1),
    ('Maintenance', 2),
    ('Marketing / Advertising', 3),
    ('Utilities', 4),
    ('Admin', 5),
    ('Financial', 6),
    ('Renovation / Design', 7),
    ('Other', 99)
ON CONFLICT (name) DO NOTHING;
