#!/usr/bin/env python3
"""
Auto-fix metadata in all project files based on content analysis.
"""

import os
import re
from pathlib import Path

KB_DIR = Path("digital-avatar/backend/knowledge_base/3. projects-eng")

ROLE_MAP = {
    'Enterprise Architect': 'enterprise-architect',
    'Chief Architect': 'enterprise-architect',
    'Domain Architect': 'domain-architect',
    'Solution Architect': 'solution-architect',
    'Business Analyst': 'business-analyst',
    'Lead Business Analyst': 'business-analyst',
    'Project Manager': 'project-manager',
    'Product Manager': 'product-manager',
    'Product Portfolio Lead': 'product-manager',
    'IT Strategy Consultant': 'consultant',
    'Consultant': 'consultant'
}

def parse_frontmatter(content):
    """Extract YAML frontmatter."""
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None, 0
    
    fm_text = match.group(1)
    fm_end = match.end()
    
    frontmatter = {}
    for line in fm_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            if value.startswith('[') and value.endswith(']'):
                value = [v.strip() for v in value[1:-1].split(',') if v.strip()]
            frontmatter[key] = value
    
    return frontmatter, fm_end

def extract_roles_from_content(content):
    """Extract roles from Role(s): field."""
    match = re.search(r'\*\*Role\(s\):\*\*\s*(.+?)(?:\n|$)', content)
    if not match:
        return []
    
    roles_text = match.group(1).strip()
    roles = []
    
    for key, value in ROLE_MAP.items():
        if key in roles_text:
            if value not in roles:
                roles.append(value)
    
    return roles

def update_frontmatter(filepath):
    """Update frontmatter in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    frontmatter, fm_end = parse_frontmatter(content)
    
    if frontmatter is None:
        print(f"⚠️  {filepath.name}: No frontmatter found, skipping")
        return False
    
    # Extract roles from content
    content_roles = extract_roles_from_content(content)
    
    # Check if roles need to be added/updated
    current_roles = frontmatter.get('roles', [])
    if isinstance(current_roles, str):
        current_roles = [current_roles]
    
    needs_update = False
    
    # Add missing roles
    if content_roles and not current_roles:
        frontmatter['roles'] = content_roles
        needs_update = True
        print(f"✅ {filepath.name}: Adding roles {content_roles}")
    elif content_roles and set(content_roles) != set(current_roles):
        # Update if different
        frontmatter['roles'] = content_roles
        needs_update = True
        print(f"📝 {filepath.name}: Updating roles from {current_roles} to {content_roles}")
    
    if not needs_update:
        return False
    
    # Rebuild frontmatter
    new_fm_lines = ['---']
    
    # Order: industries, functional, roles
    for key in ['industries', 'functional', 'roles']:
        if key in frontmatter:
            value = frontmatter[key]
            if isinstance(value, list):
                value_str = '[' + ', '.join(value) + ']'
            else:
                value_str = value
            new_fm_lines.append(f'{key}: {value_str}')
    
    new_fm_lines.append('---')
    new_fm = '\n'.join(new_fm_lines) + '\n'
    
    # Replace frontmatter
    new_content = new_fm + content[fm_end:]
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    """Main function."""
    print("Analyzing and fixing metadata...\n")
    print("=" * 80)
    
    updated = 0
    skipped = 0
    
    for filepath in sorted(KB_DIR.glob("*.md")):
        if update_frontmatter(filepath):
            updated += 1
        else:
            skipped += 1
    
    print("\n" + "=" * 80)
    print(f"\n✅ Updated: {updated} files")
    print(f"⏭️  Skipped: {skipped} files (already complete or no frontmatter)")
    print(f"\n📊 Total: {updated + skipped} files processed")

if __name__ == "__main__":
    main()
