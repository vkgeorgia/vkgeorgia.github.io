"""
Knowledge Base Metadata Fix Script
Automatically adds missing 'roles' tags to project files based on content analysis
"""

import os
import re
from pathlib import Path

# Role mapping based on project content keywords
ROLE_KEYWORDS = {
    'business-analyst': [
        'business analyst', 'requirements', 'gathered requirements',
        'business needs', 'stakeholder', 'functional requirements'
    ],
    'enterprise-architect': [
        'enterprise architect', 'ea', 'enterprise architecture',
        'strategic', 'enterprise strategy', 'transformation'
    ],
    'solution-architect': [
        'solution architect', 'architecture', 'designed solution',
        'technical architecture', 'platform', 'integration'
    ],
    'project-manager': [
        'project manager', 'managed project', 'project management',
        'team', 'timeline', 'budget', 'delivery'
    ],
    'product-manager': [
        'product manager', 'product', 'roadmap', 'feature',
        'user stories', 'backlog'
    ]
}

# Functional domain corrections
FUNCTIONAL_CORRECTIONS = {
    'e-commerce': 'data-analytics',  # or 'retail' depending on context
    'crm': 'data-analytics'
}

def extract_frontmatter_and_content(file_path):
    """Extract YAML frontmatter and content from markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Match YAML frontmatter
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        return None, content
    
    frontmatter = match.group(1)
    body = match.group(2)
    
    metadata = {}
    for line in frontmatter.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # Parse array values
            if value.startswith('[') and value.endswith(']'):
                items = value[1:-1].split(',')
                metadata[key] = [item.strip() for item in items if item.strip()]
            else:
                metadata[key] = value
    
    return metadata, body

def detect_roles_from_content(content):
    """Detect likely roles based on content keywords"""
    content_lower = content.lower()
    detected_roles = []
    
    for role, keywords in ROLE_KEYWORDS.items():
        # Count keyword matches
        matches = sum(1 for keyword in keywords if keyword in content_lower)
        if matches >= 2:  # Require at least 2 keyword matches
            detected_roles.append(role)
    
    # If no roles detected, check for explicit role mentions in content
    if not detected_roles:
        if 'role(s):' in content_lower or 'role:' in content_lower:
            # Extract roles from "Role(s): ..." line
            role_match = re.search(r'role\(s\)?:\s*\*\*(.+?)\*\*', content_lower, re.IGNORECASE)
            if role_match:
                role_text = role_match.group(1)
                if 'business analyst' in role_text:
                    detected_roles.append('business-analyst')
                if 'project manager' in role_text:
                    detected_roles.append('project-manager')
                if 'solution architect' in role_text:
                    detected_roles.append('solution-architect')
                if 'enterprise architect' in role_text:
                    detected_roles.append('enterprise-architect')
    
    return detected_roles if detected_roles else ['solution-architect']  # Default

def fix_functional_domains(metadata):
    """Fix invalid functional domain tags"""
    if 'functional' in metadata:
        fixed = []
        for domain in metadata['functional']:
            if domain in FUNCTIONAL_CORRECTIONS:
                fixed.append(FUNCTIONAL_CORRECTIONS[domain])
            else:
                fixed.append(domain)
        metadata['functional'] = fixed
    return metadata

def update_project_file(file_path, dry_run=True):
    """Update a project file with missing roles tag"""
    metadata, body = extract_frontmatter_and_content(file_path)
    
    if metadata is None:
        print(f"⚠️  {file_path.name}: No frontmatter, skipping")
        return False
    
    # Fix functional domains
    metadata = fix_functional_domains(metadata)
    
    # Add roles if missing
    if 'roles' not in metadata or not metadata['roles']:
        detected_roles = detect_roles_from_content(body)
        metadata['roles'] = detected_roles
        print(f"✅ {file_path.name}: Adding roles: {detected_roles}")
    else:
        print(f"ℹ️  {file_path.name}: Already has roles: {metadata['roles']}")
        return False
    
    if dry_run:
        print(f"   [DRY RUN] Would update file")
        return True
    
    # Reconstruct file with updated frontmatter
    frontmatter_lines = ['---']
    for key, value in metadata.items():
        if isinstance(value, list):
            value_str = '[' + ', '.join(value) + ']'
        else:
            value_str = value
        frontmatter_lines.append(f'{key}: {value_str}')
    frontmatter_lines.append('---')
    
    new_content = '\n'.join(frontmatter_lines) + '\n\n' + body
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"   ✓ File updated")
    return True

def fix_all_projects(kb_dir, dry_run=True):
    """Fix all project files in knowledge base"""
    projects_dir = kb_dir / '3. projects-eng'
    
    if not projects_dir.exists():
        print(f"❌ Projects directory not found: {projects_dir}")
        return
    
    print(f"\n🔧 Fixing project metadata...")
    print(f"   Mode: {'DRY RUN' if dry_run else 'LIVE UPDATE'}\n")
    
    updated_count = 0
    
    for md_file in sorted(projects_dir.glob('*.md')):
        if update_project_file(md_file, dry_run):
            updated_count += 1
    
    print(f"\n{'='*60}")
    print(f"📊 SUMMARY")
    print(f"{'='*60}")
    print(f"Files that would be updated: {updated_count}")
    
    if dry_run:
        print(f"\n💡 This was a DRY RUN. To apply changes, run:")
        print(f"   python fix_kb_metadata.py --apply")
    else:
        print(f"\n✅ All changes applied!")

if __name__ == '__main__':
    import sys
    
    # Check for --apply flag
    dry_run = '--apply' not in sys.argv
    
    # Find knowledge base directory
    script_dir = Path(__file__).parent
    kb_dir = script_dir / 'knowledge-base'
    
    if not kb_dir.exists():
        print(f"❌ Knowledge base not found at: {kb_dir}")
        exit(1)
    
    fix_all_projects(kb_dir, dry_run)
    
    if dry_run:
        print(f"\n⚠️  No files were modified (dry run mode)")
