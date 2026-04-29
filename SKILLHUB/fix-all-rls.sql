-- ══════════════════════════════════════════════════════════════
-- GamSkillHub — COMPLETE RLS Fix for ALL Tables
-- Run this ENTIRE SQL in your Supabase SQL Editor
-- 
-- PROBLEM: Approve/reject/restore workers, place orders, 
-- accept orders, rate workers — ALL fail because the tables
-- have RLS enabled but no UPDATE/INSERT policies for the
-- anon (frontend) key used by the GitHub Pages app.
--
-- SOLUTION: This script adds full CRUD policies for every table.
-- ══════════════════════════════════════════════════════════════

-- ─── 1. Workers table ───
ALTER TABLE workers ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Workers are publicly readable"
  ON workers FOR SELECT USING (true);

CREATE POLICY "Anyone can create workers"
  ON workers FOR INSERT WITH CHECK (true);

CREATE POLICY "Anyone can update workers"
  ON workers FOR UPDATE USING (true) WITH CHECK (true);

CREATE POLICY "Anyone can delete workers"
  ON workers FOR DELETE USING (true);

-- ─── 2. Worker skills table ───
ALTER TABLE worker_skills ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Worker skills are publicly readable"
  ON worker_skills FOR SELECT USING (true);

CREATE POLICY "Anyone can create worker skills"
  ON worker_skills FOR INSERT WITH CHECK (true);

CREATE POLICY "Anyone can update worker skills"
  ON worker_skills FOR UPDATE USING (true) WITH CHECK (true);

CREATE POLICY "Anyone can delete worker skills"
  ON worker_skills FOR DELETE USING (true);

-- ─── 3. Work history table ───
ALTER TABLE work_history ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Work history is publicly readable"
  ON work_history FOR SELECT USING (true);

CREATE POLICY "Anyone can create work history"
  ON work_history FOR INSERT WITH CHECK (true);

CREATE POLICY "Anyone can update work history"
  ON work_history FOR UPDATE USING (true) WITH CHECK (true);

CREATE POLICY "Anyone can delete work history"
  ON work_history FOR DELETE USING (true);

-- ─── 4. Orders table ───
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Orders are publicly readable"
  ON orders FOR SELECT USING (true);

CREATE POLICY "Anyone can create orders"
  ON orders FOR INSERT WITH CHECK (true);

CREATE POLICY "Anyone can update orders"
  ON orders FOR UPDATE USING (true) WITH CHECK (true);

CREATE POLICY "Anyone can delete orders"
  ON orders FOR DELETE USING (true);

-- ─── 5. Payments table ───
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Payments are publicly readable"
  ON payments FOR SELECT USING (true);

CREATE POLICY "Anyone can create payments"
  ON payments FOR INSERT WITH CHECK (true);

CREATE POLICY "Anyone can update payments"
  ON payments FOR UPDATE USING (true) WITH CHECK (true);

CREATE POLICY "Anyone can delete payments"
  ON payments FOR DELETE USING (true);

-- ─── 6. Ratings table ───
ALTER TABLE ratings ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Ratings are publicly readable"
  ON ratings FOR SELECT USING (true);

CREATE POLICY "Anyone can create ratings"
  ON ratings FOR INSERT WITH CHECK (true);

CREATE POLICY "Anyone can update ratings"
  ON ratings FOR UPDATE USING (true) WITH CHECK (true);

CREATE POLICY "Anyone can delete ratings"
  ON ratings FOR DELETE USING (true);

-- ─── 7. Admin users table ───
ALTER TABLE admin_users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Admin users are readable"
  ON admin_users FOR SELECT USING (true);

CREATE POLICY "Anyone can create admin users"
  ON admin_users FOR INSERT WITH CHECK (true);

CREATE POLICY "Anyone can update admin users"
  ON admin_users FOR UPDATE USING (true) WITH CHECK (true);

CREATE POLICY "Anyone can delete admin users"
  ON admin_users FOR DELETE USING (true);

-- ─── 8. Skill categories table ───
ALTER TABLE skill_categories ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Skill categories are publicly readable"
  ON skill_categories FOR SELECT USING (true);

CREATE POLICY "Anyone can create skill categories"
  ON skill_categories FOR INSERT WITH CHECK (true);

CREATE POLICY "Anyone can update skill categories"
  ON skill_categories FOR UPDATE USING (true) WITH CHECK (true);

CREATE POLICY "Anyone can delete skill categories"
  ON skill_categories FOR DELETE USING (true);

-- ─── 9. Escrow transactions table ───
ALTER TABLE escrow_transactions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Escrow transactions are publicly readable"
  ON escrow_transactions FOR SELECT USING (true);

CREATE POLICY "Anyone can create escrow transactions"
  ON escrow_transactions FOR INSERT WITH CHECK (true);

CREATE POLICY "Anyone can update escrow transactions"
  ON escrow_transactions FOR UPDATE USING (true) WITH CHECK (true);

CREATE POLICY "Anyone can delete escrow transactions"
  ON escrow_transactions FOR DELETE USING (true);

-- ══════════════════════════════════════════════════════════════
-- DONE! All tables now have full CRUD access from the frontend.
-- If you get "policy already exists" errors, that's fine —
-- it means the policies are already in place from a previous run.
-- ══════════════════════════════════════════════════════════════
