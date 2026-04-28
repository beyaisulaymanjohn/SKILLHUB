-- ══════════════════════════════════════════════════════════
-- GamSkillHub — Workers Table RLS Fix
-- Run this SQL in your Supabase SQL Editor
-- 
-- PROBLEM: Approve/reject/restore workers fails because
-- the workers table has RLS enabled but no UPDATE/INSERT
-- policies for the anon (frontend) key.
-- ══════════════════════════════════════════════════════════

-- ─── 1. Workers table: full CRUD access for frontend ───
ALTER TABLE workers ENABLE ROW LEVEL SECURITY;

-- Allow anyone to read workers (needed for browse, admin, login)
CREATE POLICY "Workers are publicly readable"
  ON workers FOR SELECT
  USING (true);

-- Allow anyone to insert workers (needed for worker applications)
CREATE POLICY "Anyone can create workers"
  ON workers FOR INSERT
  WITH CHECK (true);

-- Allow anyone to update workers (needed for approve/reject/restore)
CREATE POLICY "Anyone can update workers"
  ON workers FOR UPDATE
  USING (true)
  WITH CHECK (true);

-- Allow anyone to delete workers (admin cleanup)
CREATE POLICY "Anyone can delete workers"
  ON workers FOR DELETE
  USING (true);

-- ─── 2. Worker skills table: full access ───
ALTER TABLE worker_skills ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Worker skills are publicly readable"
  ON worker_skills FOR SELECT USING (true);

CREATE POLICY "Anyone can create worker skills"
  ON worker_skills FOR INSERT WITH CHECK (true);

CREATE POLICY "Anyone can update worker skills"
  ON worker_skills FOR UPDATE USING (true) WITH CHECK (true);

CREATE POLICY "Anyone can delete worker skills"
  ON worker_skills FOR DELETE USING (true);

-- ─── 3. Work history table: full access ───
ALTER TABLE work_history ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Work history is publicly readable"
  ON work_history FOR SELECT USING (true);

CREATE POLICY "Anyone can create work history"
  ON work_history FOR INSERT WITH CHECK (true);

CREATE POLICY "Anyone can update work history"
  ON work_history FOR UPDATE USING (true) WITH CHECK (true);

CREATE POLICY "Anyone can delete work history"
  ON work_history FOR DELETE USING (true);
