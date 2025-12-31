"""
Knowledge Base Metadata Audit Script
Analyzes all project files and reports missing/incomplete tags
"""

import os
import re
from pathlib import Path
from collections import defaultdict

# Define valid tag values
VALID_INDUSTRIES = {
    'oil-gas', 'telecom', 'retail', 'finance', 'healthcare', 
    'aviation', 'consulting', 'transport'
}

VALID_ROLES = {
    'business-analyst', 'enterprise-architect', 'solution-architect',
    'project-manager', 'product-manager'
}

VALID_FUNCTIONAL = {
    'architecture', 'erp', 'data-analytics', 'finance', 'hr',
    'loyalty', 'payment-systems', 'workflow-automation', 'ai'
}

def extract_frontmatter(file_path):
    """Extract YAML frontmatter from markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Match YAML frontmatter
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None
    
    frontmatter = match.group(1)
    metadata = {}
    
    # Extract tags
    for line in frontmatter.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # Parse array values [item1, item2]
            if value.startswith('[') and value.endswith(']'):
                items = value[1:-1].split(',')
                metadata[key] = [item.strip() for item in items if item.strip()]
            else:
                metadata[key] = value
    
    return metadata

def audit_project_files(kb_dir):
    """Audit all project files in knowledge base"""
    projects_dir = kb_dir / '3. projects-eng'
    
    if not projects_dir.exists():
        print(f"❌ Projects directory not found: {projects_dir}")
        return
    
    results = {
        'total': 0,
        'complete': 0,
        'missing_industries': [],
        'missing_roles': [],
        'missing_functional': [],
        'invalid_industries': [],
        'invalid_roles': [],
        'invalid_functional': [],
        'no_frontmatter': []
    }
    
    print(f"\n📊 Auditing projects in: {projects_dir}\n")
    
    for md_file in sorted(projects_dir.glob('*.md')):
        results['total'] += 1
        file_name = md_file.name
        
        metadata = extract_frontmatter(md_file)
        
        if metadata is None:
            results['no_frontmatter'].append(file_name)
            print(f"⚠️  {file_name}: No frontmatter")
            continue
        
        # Check for required tags
        has_industries = 'industries' in metadata and metadata['industries']
        has_roles = 'roles' in metadata and metadata['roles']
        has_functional = 'functional' in metadata and metadata['functional']
        
        issues = []
        
        if not has_industries:
            results['missing_industries'].append(file_name)
            issues.append('missing industries')
        else:
            # Validate industries
            invalid = [i for i in metadata['industries'] if i not in VALID_INDUSTRIES]
            if invalid:
                results['invalid_industries'].append((file_name, invalid))
                issues.append(f'invalid industries: {invalid}')
        
        if not has_roles:
            results['missing_roles'].append(file_name)
            issues.append('missing roles')
        else:
            # Validate roles
            invalid = [r for r in metadata['roles'] if r not in VALID_ROLES]
            if invalid:
                results['invalid_roles'].append((file_name, invalid))
                issues.append(f'invalid roles: {invalid}')
        
        if not has_functional:
            results['missing_functional'].append(file_name)
            issues.append('missing functional')
        else:
            # Validate functional
            invalid = [f for f in metadata['functional'] if f not in VALID_FUNCTIONAL]
            if invalid:
                results['invalid_functional'].append((file_name, invalid))
                issues.append(f'invalid functional: {invalid}')
        
        if has_industries and has_roles and has_functional:
            results['complete'] += 1
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name}: {', '.join(issues)}")
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"📈 AUDIT SUMMARY")
    print(f"{'='*60}")
    print(f"Total projects: {results['total']}")
    print(f"Complete (all 3 tags): {results['complete']} ({results['complete']/results['total']*100:.1f}%)")
    print(f"Missing industries: {len(results['missing_industries'])}")
    print(f"Missing roles: {len(results['missing_roles'])}")
    print(f"Missing functional: {len(results['missing_functional'])}")
    print(f"No frontmatter: {len(results['no_frontmatter'])}")
    
    if results['invalid_industries']:
        print(f"\n⚠️  Invalid industries found:")
        for file, invalid in results['invalid_industries']:
            print(f"   {file}: {invalid}")
    
    if results['invalid_roles']:
        print(f"\n⚠️  Invalid roles found:")
        for file, invalid in results['invalid_roles']:
            print(f"   {file}: {invalid}")
    
    if results['invalid_functional']:
        print(f"\n⚠️  Invalid functional domains found:")
        for file, invalid in results['invalid_functional']:
            print(f"   {file}: {invalid}")
    
    # Generate recommendations
    print(f"\n{'='*60}")
    print(f"💡 RECOMMENDATIONS")
    print(f"{'='*60}")
    
    if results['missing_roles']:
        print(f"\n🔧 Files missing 'roles' tag ({len(results['missing_roles'])}):")
        for file in results['missing_roles'][:10]:  # Show first 10
            print(f"   - {file}")
        if len(results['missing_roles']) > 10:
            print(f"   ... and {len(results['missing_roles']) - 10} more")
    
    return results

if __name__ == '__main__':
    # Find knowledge base directory
    script_dir = Path(__file__).parent
    kb_dir = script_dir / 'knowledge-base'
    
    if not kb_dir.exists():
        print(f"❌ Knowledge base not found at: {kb_dir}")
        print(f"   Looking in: {script_dir}")
        exit(1)
    
    results = audit_project_files(kb_dir)
    
    print(f"\n✨ Audit complete!")
    print(f"\nNext steps:")
    print(f"1. Review the files with missing tags")
    print(f"2. Run fix script to add missing tags")
    print(f"3. Verify changes")
