-- ══════════════════════════════════════════════════════════
-- GamSkillHub Payment System - Supabase Database Schema
-- Run this SQL in your Supabase SQL Editor
-- ══════════════════════════════════════════════════════════

-- ─── 1. Add payment columns to existing 'orders' table ───
ALTER TABLE orders
  ADD COLUMN IF NOT EXISTS payment_method TEXT DEFAULT 'cash',
  ADD COLUMN IF NOT EXISTS payment_status TEXT DEFAULT 'pending',
  ADD COLUMN IF NOT EXISTS payment_reference TEXT,
  ADD COLUMN IF NOT EXISTS service_fee NUMERIC(10,2) DEFAULT 500,
  ADD COLUMN IF NOT EXISTS commission NUMERIC(10,2) DEFAULT 25,
  ADD COLUMN IF NOT EXISTS total_amount NUMERIC(10,2) DEFAULT 525;

-- ─── 2. Create 'payments' table ───
CREATE TABLE IF NOT EXISTS payments (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  order_id UUID REFERENCES orders(id) ON DELETE SET NULL,
  
  -- Client info
  client_name TEXT,
  client_phone TEXT,
  
  -- Worker info
  worker_id UUID REFERENCES workers(id) ON DELETE SET NULL,
  worker_name TEXT,
  
  -- Amounts (in Dalasi)
  amount NUMERIC(10,2) NOT NULL DEFAULT 0,
  service_fee NUMERIC(10,2) DEFAULT 0,
  commission NUMERIC(10,2) DEFAULT 0,
  worker_payout NUMERIC(10,2) DEFAULT 0,
  
  -- Payment method: 'wave', 'bank', 'cash'
  method TEXT NOT NULL DEFAULT 'cash',
  
  -- Payment status: 'pending', 'escrow', 'released', 'refunded', 'unpaid', 'approved', 'rejected'
  status TEXT NOT NULL DEFAULT 'pending',
  
  -- Transaction reference
  reference TEXT UNIQUE,
  
  -- Payout fields (for worker payout requests)
  payout_to TEXT,
  type TEXT DEFAULT 'payment', -- 'payment' or 'payout'
  
  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT now(),
  released_at TIMESTAMPTZ,
  refunded_at TIMESTAMPTZ,
  approved_at TIMESTAMPTZ
);

-- ─── 3. Create indexes for performance ───
CREATE INDEX IF NOT EXISTS idx_payments_order_id ON payments(order_id);
CREATE INDEX IF NOT EXISTS idx_payments_worker_id ON payments(worker_id);
CREATE INDEX IF NOT EXISTS idx_payments_status ON payments(status);
CREATE INDEX IF NOT EXISTS idx_payments_type ON payments(type);
CREATE INDEX IF NOT EXISTS idx_payments_created_at ON payments(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_orders_payment_status ON orders(payment_status);
CREATE INDEX IF NOT EXISTS idx_orders_payment_method ON orders(payment_method);

-- ─── 4. Enable Row Level Security (RLS) ───
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;

-- Policy: Allow public read (anon key for the frontend)
CREATE POLICY "Payments are publicly readable"
  ON payments FOR SELECT
  USING (true);

-- Policy: Allow inserts from anon (frontend)
CREATE POLICY "Anyone can create payments"
  ON payments FOR INSERT
  WITH CHECK (true);

-- Policy: Allow updates from anon (frontend)
CREATE POLICY "Anyone can update payments"
  ON payments FOR UPDATE
  USING (true);

-- ─── 5. Update orders table RLS (add payment columns access) ───
-- These policies should already exist, but adding for completeness
CREATE POLICY "Anyone can update orders"
  ON orders FOR UPDATE
  USING (true);

CREATE POLICY "Anyone can insert orders"
  ON orders FOR INSERT
  WITH CHECK (true);

-- ══════════════════════════════════════════════════════════
-- NOTES:
-- 
-- Payment Flow:
-- 1. Client places order → payment_method, service_fee, commission, total_amount saved
-- 2. If Wave: payment_status = 'escrow' (money held securely)
-- 3. If Bank: payment_status = 'pending' (awaiting confirmation)  
-- 4. If Cash: payment_status = 'unpaid' (collected on-site)
-- 5. Admin marks job complete → can 'release' escrow to worker
-- 6. Worker requests payout → stored as type='payout' in payments table
-- 7. Admin approves payout → status changes to 'approved'
--
-- Commission: 5% of service fee goes to platform
-- Worker receives: service_fee - commission
--
-- Wave Integration (Future):
-- - Replace simulated flow with Wave Business API
-- - API endpoint: https://api.wave.com/v1/
-- - Uses OAuth 2.0 for authentication
-- - Supports mobile money collections & disbursements
-- ══════════════════════════════════════════════════════════
