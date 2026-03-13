#!/usr/bin/env python3
"""
Generate missing navigation pages from knowledge base metadata.
Parses all project files and creates industry, role, and domain pages.
"""

import os
import re
from pathlib import Path
from collections import defaultdict

# Paths
KB_DIR = Path("digital-avatar/backend/knowledge_base/3. projects-eng")
SITE_ROOT = Path(".")

# Category mappings
INDUSTRY_MAP = {
    "aviation": "Aviation",
    "transport": "Transport",
    "telecom": "Telecommunications",
    "oil-gas": "Oil & Gas",
    "retail": "Retail",
    "healthcare": "Healthcare",
    "consulting": "IT Consulting",
    "finance": "Finance"
}

ROLE_MAP = {
    "enterprise-architect": "Enterprise Architect",
    "domain-architect": "Domain Architect",
    "business-analyst": "Business Analyst",
    "project-manager": "Project Manager",
    "product-manager": "Product Manager"
}

DOMAIN_MAP = {
    "finance": "Finance & Payments",
    "payment-systems": "Payment Systems",
    "erp": "ERP Systems",
    "scm": "Supply Chain Management",
    "product-management": "Product Management",
    "data-analytics": "Data Analytics",
    "architecture": "Enterprise Architecture",
    "hr": "Human Resources",
    "ai": "Artificial Intelligence",
    "workflow-automation": "Workflow Automation"
}

def parse_frontmatter(content):
    """Extract YAML frontmatter from markdown file."""
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    
    frontmatter = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            # Parse arrays like [telecom, consulting]
            if value.startswith('[') and value.endswith(']'):
                value = [v.strip() for v in value[1:-1].split(',')]
            frontmatter[key] = value
    
    return frontmatter

def extract_project_info(filepath):
    """Extract project number, title, and summary from markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get project number from filename
    filename = os.path.basename(filepath)
    match = re.match(r'(\d+)\.', filename)
    project_num = match.group(1) if match else None
    
    # Parse frontmatter
    metadata = parse_frontmatter(content)
    
    # Extract title (## Project: ...)
    title_match = re.search(r'##\s*Project:\s*(.+?)(?:\n|$)', content)
    title = title_match.group(1).strip() if title_match else "Unknown Project"
    
    # Remove project code from title (e.g., "DME-25 – " or "SKY-BARS – ")
    title = re.sub(r'^[A-Z]+-[A-Z0-9]+\s*[–-]\s*', '', title)
    title = re.sub(r'^[A-Z]+-[A-Z0-9]+\s*', '', title)
    
    # Extract Key Result
    key_result_match = re.search(r'\*\*Key Result:\*\*\s*(.+?)(?:\n|$)', content)
    summary = key_result_match.group(1).strip() if key_result_match else ""
    
    # Truncate summary to 500 chars
    if len(summary) > 500:
        summary = summary[:497] + "..."
    
    return {
        'number': project_num,
        'title': title,
        'summary': summary,
        'industries': metadata.get('industries', []),
        'functional': metadata.get('functional', []),
        'roles': metadata.get('roles', [])
    }

def collect_all_projects():
    """Collect all project information."""
    projects = []
    for filepath in sorted(KB_DIR.glob("*.md")):
        try:
            project = extract_project_info(filepath)
            projects.append(project)
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
    
    return projects

def group_by_category(projects, category_key):
    """Group projects by a specific category (industries, functional, roles)."""
    grouped = defaultdict(list)
    for project in projects:
        categories = project.get(category_key, [])
        if isinstance(categories, str):
            categories = [categories]
        for cat in categories:
            grouped[cat].append(project)
    return grouped

def create_page(filepath, title, description, projects, permalink):
    """Create a category page with project listings."""
    content = f"""---
layout: page
title: "{title}"
description: "{description}"
permalink: {permalink}
---

## {title}

{description}

### Projects

"""
    
    for project in sorted(projects, key=lambda p: int(p['number'])):
        content += f"""
**[Project {project['number']}](/downloads/{project['number'].zfill(2)}.pdf):** {project['title']}

{project['summary']}

---
"""
    
    content += """

<p align="center" style="font-size: 14px;">
  📧 <a href="mailto:vkgeorgia@icloud.com">vkgeorgia@icloud.com</a> | 
  💼 <a href="https://www.linkedin.com/in/valeriikorobeinikov/" target="_blank">LinkedIn</a> | 
  📅 <a href="https://calendar.app.google/YwmXZytfSQ2qWX4Z7" target="_blank">Schedule a Meeting</a>
</p>
"""
    
    # Create directory if needed
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    # Write file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Created: {filepath}")

def main():
    """Main function to generate all pages."""
    print("Collecting project information...")
    projects = collect_all_projects()
    print(f"Found {len(projects)} projects")
    
    # Group by industries
    print("\nGenerating industry pages...")
    industries = group_by_category(projects, 'industries')
    for industry_key, industry_projects in industries.items():
        if industry_key in INDUSTRY_MAP:
            title = INDUSTRY_MAP[industry_key]
            filepath = SITE_ROOT / "industries" / f"{industry_key}.md"
            create_page(
                filepath,
                title,
                f"Projects in {title} industry",
                industry_projects,
                f"/industries/{industry_key}/"
            )
    
    # Also create project category pages (same as industries but different URL)
    print("\nGenerating project category pages...")
    for industry_key, industry_projects in industries.items():
        if industry_key in INDUSTRY_MAP:
            title = INDUSTRY_MAP[industry_key]
            filepath = SITE_ROOT / "projects" / f"{industry_key}.md"
            create_page(
                filepath,
                title,
                f"Projects in {title}",
                industry_projects,
                f"/projects/{industry_key}/"
            )
    
    # Group by roles
    print("\nGenerating role pages...")
    roles = group_by_category(projects, 'roles')
    for role_key, role_projects in roles.items():
        if role_key in ROLE_MAP:
            title = ROLE_MAP[role_key]
            filepath = SITE_ROOT / "roles" / f"{role_key}.md"
            create_page(
                filepath,
                title,
                f"Projects where I worked as {title}",
                role_projects,
                f"/roles/{role_key}/"
            )
    
    # Group by functional domains
    print("\nGenerating domain pages...")
    domains = group_by_category(projects, 'functional')
    for domain_key, domain_projects in domains.items():
        if domain_key in DOMAIN_MAP:
            title = DOMAIN_MAP[domain_key]
            filepath = SITE_ROOT / "domains" / f"{domain_key}.md"
            create_page(
                filepath,
                title,
                f"Projects in {title}",
                domain_projects,
                f"/domains/{domain_key}/"
            )
    
    print("\n✅ All pages generated successfully!")

if __name__ == "__main__":
    main()
