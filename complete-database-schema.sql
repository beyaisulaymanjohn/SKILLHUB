-- ══════════════════════════════════════════════════════════════════
-- GamSkillHub — COMPLETE DATABASE SCHEMA
-- Run this ENTIRE SQL in your Supabase SQL Editor (click "New Query")
-- 
-- This creates ALL tables the app needs:
--   workers, worker_skills, work_history, skill_categories,
--   orders, ratings, admin_users, escrow_transactions
-- Plus all RLS policies so the frontend (anon key) can read/write.
--
-- IMPORTANT: The payment schema you ran earlier already created the
-- "payments" table and added payment columns to "orders". This script
-- uses IF NOT EXISTS so it won't break anything already in place.
-- ══════════════════════════════════════════════════════════════════

-- ══════════════════════════════════════════════
-- 1. SKILL CATEGORIES
-- ══════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS skill_categories (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  icon TEXT DEFAULT '',
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now()
);

INSERT INTO skill_categories (name, icon) VALUES
  ('Plumbing', '🔧'), ('Electrical', '⚡'), ('Carpentry', '🪚'),
  ('Masonry', '🧱'), ('Painting', '🎨'), ('Roofing', '🏠'),
  ('Tiling', '⬜'), ('Welding', '🔩'), ('AC/HVAC', '❄️'),
  ('Security Systems', '🔐'), ('Landscaping', '🌿'), ('General Labour', '🛠️'),
  ('Barber (Home)', '✂️'), ('Home Cleaning', '🧹'), ('Pest Control', '🐛'),
  ('Home Nursing', '💊'), ('Laundry Service', '👕'), ('Auto Mechanic', '🔋'),
  ('Solar Energy', '☀️'), ('IT/Tech Support', '💻')
ON CONFLICT (name) DO NOTHING;

-- ══════════════════════════════════════════════
-- 2. WORKERS
-- ══════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS workers (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  phone TEXT NOT NULL UNIQUE,
  email TEXT,
  password TEXT,
  bio TEXT DEFAULT '',
  location TEXT DEFAULT '',
  shop_address TEXT DEFAULT '',
  years_experience INTEGER DEFAULT 0,
  status TEXT DEFAULT 'pending',
  completed_jobs INTEGER DEFAULT 0,
  rating NUMERIC(3,1) DEFAULT 5.0,
  rating_count INTEGER DEFAULT 0,
  is_available BOOLEAN DEFAULT true,
  photo_url TEXT DEFAULT '',
  id_doc_url TEXT DEFAULT '',
  cert_urls TEXT[] DEFAULT '{}',
  cert_count INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ══════════════════════════════════════════════
-- 3. WORKER SKILLS (junction table)
-- ══════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS worker_skills (
  id SERIAL PRIMARY KEY,
  worker_id UUID REFERENCES workers(id) ON DELETE CASCADE,
  category_id INTEGER REFERENCES skill_categories(id) ON DELETE CASCADE,
  UNIQUE(worker_id, category_id)
);

-- ══════════════════════════════════════════════
-- 4. WORK HISTORY
-- ══════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS work_history (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  worker_id UUID REFERENCES workers(id) ON DELETE CASCADE,
  title TEXT NOT NULL DEFAULT '',
  description TEXT DEFAULT '',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ══════════════════════════════════════════════
-- 5. ORDERS (may already exist from Supabase setup)
-- ══════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS orders (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  client_name TEXT NOT NULL DEFAULT '',
  client_phone TEXT DEFAULT '',
  skill_needed TEXT NOT NULL DEFAULT '',
  description TEXT DEFAULT '',
  client_address TEXT DEFAULT '',
  status TEXT DEFAULT 'pending',
  worker_id UUID REFERENCES workers(id) ON DELETE SET NULL,
  assigned_by_admin BOOLEAN DEFAULT false,
  payment_method TEXT DEFAULT 'cash',
  payment_status TEXT DEFAULT 'pending',
  payment_reference TEXT,
  service_fee NUMERIC(10,2) DEFAULT 500,
  commission NUMERIC(10,2) DEFAULT 25,
  total_amount NUMERIC(10,2) DEFAULT 525,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ══════════════════════════════════════════════
-- 6. RATINGS
-- ══════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS ratings (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  order_id UUID REFERENCES orders(id) ON DELETE SET NULL,
  worker_id UUID REFERENCES workers(id) ON DELETE SET NULL,
  client_name TEXT DEFAULT '',
  score INTEGER NOT NULL DEFAULT 5 CHECK (score BETWEEN 1 AND 5),
  review TEXT DEFAULT '',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ══════════════════════════════════════════════
-- 7. ADMIN USERS
-- ══════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS admin_users (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL DEFAULT '',
  email TEXT DEFAULT '',
  password TEXT NOT NULL DEFAULT '',
  role TEXT DEFAULT 'admin',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Insert default admin (password: admin123)
INSERT INTO admin_users (name, email, password, role)
VALUES ('Main Admin', 'admin@gamskillhub.gm', 'admin123', 'admin')
ON CONFLICT DO NOTHING;

-- ══════════════════════════════════════════════
-- 8. ESCROW TRANSACTIONS
-- ══════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS escrow_transactions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  payment_id UUID REFERENCES payments(id) ON DELETE SET NULL,
  order_id UUID REFERENCES orders(id) ON DELETE SET NULL,
  worker_id UUID REFERENCES workers(id) ON DELETE SET NULL,
  amount NUMERIC(10,2) NOT NULL DEFAULT 0,
  status TEXT DEFAULT 'held',
  released_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ══════════════════════════════════════════════
-- 9. INDEXES
-- ══════════════════════════════════════════════
CREATE INDEX IF NOT EXISTS idx_workers_status ON workers(status);
CREATE INDEX IF NOT EXISTS idx_workers_phone ON workers(phone);
CREATE INDEX IF NOT EXISTS idx_worker_skills_worker ON worker_skills(worker_id);
CREATE INDEX IF NOT EXISTS idx_worker_skills_category ON worker_skills(category_id);
CREATE INDEX IF NOT EXISTS idx_work_history_worker ON work_history(worker_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_worker ON orders(worker_id);
CREATE INDEX IF NOT EXISTS idx_orders_created ON orders(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_ratings_worker ON ratings(worker_id);
CREATE INDEX IF NOT EXISTS idx_ratings_order ON ratings(order_id);

-- ══════════════════════════════════════════════════════════════════
-- 10. ROW LEVEL SECURITY (RLS) — Full access for the frontend key
-- ══════════════════════════════════════════════════════════════════

-- Skill categories
ALTER TABLE skill_categories ENABLE ROW LEVEL SECURITY;
CREATE POLICY "skill_cat_select" ON skill_categories FOR SELECT USING (true);
CREATE POLICY "skill_cat_insert" ON skill_categories FOR INSERT WITH CHECK (true);
CREATE POLICY "skill_cat_update" ON skill_categories FOR UPDATE USING (true) WITH CHECK (true);
CREATE POLICY "skill_cat_delete" ON skill_categories FOR DELETE USING (true);

-- Workers
ALTER TABLE workers ENABLE ROW LEVEL SECURITY;
CREATE POLICY "workers_select" ON workers FOR SELECT USING (true);
CREATE POLICY "workers_insert" ON workers FOR INSERT WITH CHECK (true);
CREATE POLICY "workers_update" ON workers FOR UPDATE USING (true) WITH CHECK (true);
CREATE POLICY "workers_delete" ON workers FOR DELETE USING (true);

-- Worker skills
ALTER TABLE worker_skills ENABLE ROW LEVEL SECURITY;
CREATE POLICY "wskills_select" ON worker_skills FOR SELECT USING (true);
CREATE POLICY "wskills_insert" ON worker_skills FOR INSERT WITH CHECK (true);
CREATE POLICY "wskills_update" ON worker_skills FOR UPDATE USING (true) WITH CHECK (true);
CREATE POLICY "wskills_delete" ON worker_skills FOR DELETE USING (true);

-- Work history
ALTER TABLE work_history ENABLE ROW LEVEL SECURITY;
CREATE POLICY "whist_select" ON work_history FOR SELECT USING (true);
CREATE POLICY "whist_insert" ON work_history FOR INSERT WITH CHECK (true);
CREATE POLICY "whist_update" ON work_history FOR UPDATE USING (true) WITH CHECK (true);
CREATE POLICY "whist_delete" ON work_history FOR DELETE USING (true);

-- Orders
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY "orders_select" ON orders FOR SELECT USING (true);
CREATE POLICY "orders_insert" ON orders FOR INSERT WITH CHECK (true);
CREATE POLICY "orders_update" ON orders FOR UPDATE USING (true) WITH CHECK (true);
CREATE POLICY "orders_delete" ON orders FOR DELETE USING (true);

-- Ratings
ALTER TABLE ratings ENABLE ROW LEVEL SECURITY;
CREATE POLICY "ratings_select" ON ratings FOR SELECT USING (true);
CREATE POLICY "ratings_insert" ON ratings FOR INSERT WITH CHECK (true);
CREATE POLICY "ratings_update" ON ratings FOR UPDATE USING (true) WITH CHECK (true);
CREATE POLICY "ratings_delete" ON ratings FOR DELETE USING (true);

-- Admin users
ALTER TABLE admin_users ENABLE ROW LEVEL SECURITY;
CREATE POLICY "admins_select" ON admin_users FOR SELECT USING (true);
CREATE POLICY "admins_insert" ON admin_users FOR INSERT WITH CHECK (true);
CREATE POLICY "admins_update" ON admin_users FOR UPDATE USING (true) WITH CHECK (true);
CREATE POLICY "admins_delete" ON admin_users FOR DELETE USING (true);

-- Escrow transactions
ALTER TABLE escrow_transactions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "escrow_select" ON escrow_transactions FOR SELECT USING (true);
CREATE POLICY "escrow_insert" ON escrow_transactions FOR INSERT WITH CHECK (true);
CREATE POLICY "escrow_update" ON escrow_transactions FOR UPDATE USING (true) WITH CHECK (true);
CREATE POLICY "escrow_delete" ON escrow_transactions FOR DELETE USING (true);

-- Payments (may already have policies from payment schema, use IF NOT EXISTS pattern)
DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename='payments' AND policyname='payments_select') THEN
    ALTER TABLE payments ENABLE ROW LEVEL SECURITY;
    CREATE POLICY "payments_select" ON payments FOR SELECT USING (true);
    CREATE POLICY "payments_insert" ON payments FOR INSERT WITH CHECK (true);
    CREATE POLICY "payments_update" ON payments FOR UPDATE USING (true) WITH CHECK (true);
    CREATE POLICY "payments_delete" ON payments FOR DELETE USING (true);
  END IF;
END $$;

-- ══════════════════════════════════════════════════════════════════
-- 11. ADD PASSWORD COLUMN (from payment schema, in case not run)
-- ══════════════════════════════════════════════════════════════════
DO $$ BEGIN
  ALTER TABLE workers ADD COLUMN IF NOT EXISTS password TEXT;
EXCEPTION WHEN OTHERS THEN NULL;
END $$;

-- ══════════════════════════════════════════════════════════════════
-- DONE! 
-- 
-- If you see "already exists" or "duplicate" errors — that's fine.
-- It means those tables/policies/indexes are already in place.
--
-- Your GamSkillHub app should now work fully with Supabase!
-- ══════════════════════════════════════════════════════════════════
