-- Migration: add notes column to projects
-- Run once in Neon SQL Editor

ALTER TABLE projects
  ADD COLUMN IF NOT EXISTS notes TEXT;

-- Move legacy secondary code EPM-ECO into notes for project EPM-PSR
UPDATE projects
SET notes = 'Legacy secondary code: EPM-ECO'
WHERE code = 'EPM-PSR';

-- Verify
SELECT id, code, notes FROM projects WHERE notes IS NOT NULL;
