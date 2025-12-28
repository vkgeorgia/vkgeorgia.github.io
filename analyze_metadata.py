#!/usr/bin/env python3
"""
Analyze and validate metadata in all project files.
"""

import os
import re
from pathlib import Path
from collections import defaultdict

KB_DIR = Path("digital-avatar/backend/knowledge_base/3. projects-eng")

def parse_frontmatter(content):
    """Extract YAML frontmatter from markdown file."""
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None
    
    frontmatter = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            if value.startswith('[') and value.endswith(']'):
                value = [v.strip() for v in value[1:-1].split(',')]
            frontmatter[key] = value
    
    return frontmatter

def extract_industry_from_content(content):
    """Try to extract industry from content."""
    # Look for Industry field
    match = re.search(r'\*\*Industry:\*\*\s*(.+?)(?:\n|$)', content)
    if match:
        industry = match.group(1).strip()
        # Map to our industry tags
        industry_map = {
            'Telecom': 'telecom',
            'Telecommunications': 'telecom',
            'Transport': 'transport',
            'Aviation': 'aviation',
            'Oil & Gas': 'oil-gas',
            'Healthcare': 'healthcare',
            'Retail': 'retail',
            'IT Services': 'consulting',
            'Finance': 'finance',
            'Banking': 'finance'
        }
        for key, value in industry_map.items():
            if key.lower() in industry.lower():
                return value
    return None

def extract_role_from_content(content):
    """Try to extract role from content."""
    match = re.search(r'\*\*Role\(s\):\*\*\s*(.+?)(?:\n|$)', content)
    if match:
        roles_text = match.group(1).strip()
        roles = []
        
        role_map = {
            'Enterprise Architect': 'enterprise-architect',
            'Chief Architect': 'enterprise-architect',
            'Domain Architect': 'domain-architect',
            'Solution Architect': 'solution-architect',
            'Business Analyst': 'business-analyst',
            'Lead Business Analyst': 'business-analyst',
            'Project Manager': 'project-manager',
            'Product Manager': 'product-manager',
            'IT Strategy Consultant': 'consultant'
        }
        
        for key, value in role_map.items():
            if key.lower() in roles_text.lower():
                if value not in roles:
                    roles.append(value)
        
        return roles if roles else None
    return None

def extract_functional_from_content(content):
    """Try to extract functional domain from content."""
    domains = []
    
    # Domain field
    match = re.search(r'\*\*Domain:\*\*\s*(.+?)(?:\n|$)', content)
    if match:
        domain_text = match.group(1).strip().lower()
        
        domain_map = {
            'finance': 'finance',
            'payment': 'payment-systems',
            'erp': 'erp',
            'hr': 'hr',
            'human resource': 'hr',
            'data': 'data-analytics',
            'analytics': 'data-analytics',
            'architecture': 'architecture',
            'ai': 'ai',
            'artificial intelligence': 'ai',
            'automation': 'workflow-automation',
            'workflow': 'workflow-automation',
            'scm': 'scm',
            'supply chain': 'scm',
            'product management': 'product-management',
            'loyalty': 'loyalty-programs',
            'crm': 'crm'
        }
        
        for key, value in domain_map.items():
            if key in domain_text:
                if value not in domains:
                    domains.append(value)
    
    return domains if domains else None

def analyze_project(filepath):
    """Analyze a single project file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = os.path.basename(filepath)
    project_num = re.match(r'(\d+)\.', filename).group(1) if re.match(r'(\d+)\.', filename) else '??'
    
    # Get current frontmatter
    current_fm = parse_frontmatter(content)
    
    # Extract from content
    suggested_industry = extract_industry_from_content(content)
    suggested_roles = extract_role_from_content(content)
    suggested_functional = extract_functional_from_content(content)
    
    # Get title
    title_match = re.search(r'##\s*Project:\s*(.+?)(?:\n|$)', content)
    title = title_match.group(1).strip() if title_match else "Unknown"
    
    result = {
        'num': project_num,
        'filename': filename,
        'title': title,
        'current': current_fm,
        'suggested': {
            'industries': suggested_industry,
            'roles': suggested_roles,
            'functional': suggested_functional
        }
    }
    
    return result

def main():
    """Main analysis function."""
    print("Analyzing all project files...\n")
    print("=" * 100)
    
    issues = []
    complete = []
    
    for filepath in sorted(KB_DIR.glob("*.md")):
        result = analyze_project(filepath)
        
        has_issues = False
        issue_details = []
        
        # Check if frontmatter exists
        if result['current'] is None:
            has_issues = True
            issue_details.append("❌ NO FRONTMATTER")
        else:
            # Check industries
            if 'industries' not in result['current'] or not result['current']['industries']:
                has_issues = True
                issue_details.append(f"⚠️  Missing industries (suggest: {result['suggested']['industries']})")
            
            # Check roles
            if 'roles' not in result['current'] or not result['current']['roles']:
                if result['suggested']['roles']:
                    has_issues = True
                    issue_details.append(f"⚠️  Missing roles (suggest: {result['suggested']['roles']})")
            
            # Check functional
            if 'functional' not in result['current'] or not result['current']['functional']:
                if result['suggested']['functional']:
                    has_issues = True
                    issue_details.append(f"⚠️  Missing functional (suggest: {result['suggested']['functional']})")
        
        if has_issues:
            issues.append((result, issue_details))
            print(f"\n📄 Project {result['num']}: {result['title'][:60]}")
            print(f"   File: {result['filename']}")
            for issue in issue_details:
                print(f"   {issue}")
            if result['current']:
                print(f"   Current: {result['current']}")
        else:
            complete.append(result)
    
    print("\n" + "=" * 100)
    print(f"\n✅ Complete: {len(complete)}/44 projects")
    print(f"⚠️  Issues: {len(issues)}/44 projects")
    
    if issues:
        print("\n\nProjects needing metadata updates:")
        for result, _ in issues:
            print(f"  - Project {result['num']}: {result['filename']}")

if __name__ == "__main__":
    main()
