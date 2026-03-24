-- Migration: add client_public flag to projects
-- Run once in Neon SQL Editor
-- Source of truth: client_name_visibility field in _projects/*.md frontmatter
--
-- client_public = true  → client name may be shown publicly
-- client_public = false → client name is confidential (show as "Confidential client" or omit)

-- Step 1: add column (default true = public)
ALTER TABLE projects
  ADD COLUMN IF NOT EXISTS client_public BOOLEAN NOT NULL DEFAULT true;

-- Step 2: set false for hidden projects (23 projects)
UPDATE projects SET client_public = false
WHERE code IN (
  'GAM-NAMOS',
  'GAM-CAR5',
  'GAM-X5',
  'GAM-VTB',
  'GAM-ZG',
  'DME-25',
  'DME-26',
  'DME-27',
  'DME-28',
  'DME-29',
  'EPM-HRMS',
  'EPM-SPC',
  'EPM-PSR',
  'EPM-ECO',
  'DELB-CRP',
  'DANF-ACO',
  'DANF-L2C',
  'ADNO-BCP',
  'EPM-AST',
  'ADNO-TRMS',
  'TRANS-AIPOC',
  'TRANS-EAM',
  'HR-BOT'
);

-- Verify
SELECT code, client, client_public
FROM projects
ORDER BY client_public, code;
