#!/usr/bin/env python3
"""
Generate cases.md page from project markdown files.
Reads projects from knowledge-base/3. projects-eng/ and creates an accordion-based page.
Respects client_name_visibility tag to hide client names when needed.
"""

import os
import re
from pathlib import Path
from collections import defaultdict
import yaml
import markdown

# Client name replacement patterns for hidden clients
CLIENT_REPLACEMENTS = {
    'X5 Retail Group': 'a major European retail company',
    'X5': 'a major retail company',
    'Ahold Delhaize': 'a large European grocery chain',
    'Carrefour': 'a major retail company',
    'Namos': 'a retail company',
    'Zastava Group': 'a retail company',
    'BTC': 'a telecommunications company',
    'VTB Pension Fund': 'a financial services company',
    'VTB': 'a financial services company',
    'EPAM': 'an IT services company',
    'Transitrix': 'a consulting company',
    'DME': 'a manufacturing company',
    'Gamma': 'an IT services company',
}

# Industry-based generic descriptions
INDUSTRY_DESCRIPTIONS = {
    'retail': 'a retail company',
    'telecom': 'a telecommunications provider',
    'finance': 'a financial services company',
    'oil-gas': 'an oil and gas company',
    'healthcare': 'a healthcare organization',
    'consulting': 'a consulting company',
    'it-services': 'an IT services company',
}

def parse_project_file(filepath):
    """Parse a project markdown file and extract metadata and content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract YAML frontmatter
    yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if not yaml_match:
        return None
    
    frontmatter_text = yaml_match.group(1)
    markdown_content = yaml_match.group(2)
    
    # Parse YAML
    try:
        metadata = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return None
    
    # Extract project number from filename
    filename = filepath.name
    project_num_match = re.match(r'^(\d+)\.', filename)
    project_num = int(project_num_match.group(1)) if project_num_match else 0
    
    return {
        'number': project_num,
        'filename': filename,
        'metadata': metadata,
        'content': markdown_content,
        'filepath': filepath
    }

def replace_client_names(content, metadata):
    """Replace client names with generic descriptions if visibility is hidden."""
    if metadata.get('client_name_visibility', ['public'])[0] == 'public':
        return content
    
    # Replace known client names
    modified_content = content
    for client_name, replacement in CLIENT_REPLACEMENTS.items():
        # Case-insensitive replacement
        pattern = re.compile(re.escape(client_name), re.IGNORECASE)
        modified_content = pattern.sub(replacement, modified_content)
    
    return modified_content

def convert_markdown_to_html(markdown_text):
    """Convert markdown to HTML."""
    md = markdown.Markdown(extensions=['extra', 'nl2br'])
    return md.convert(markdown_text)

def get_tag_display_name(tag):
    """Convert tag to display name."""
    return tag.replace('-', ' ').replace('_', ' ').title()

def remove_project_code_from_title(title):
    """Remove project code in parentheses from title."""
    # Remove patterns like (SKY-BARS), (GAM-X5), (BTCL-ARCO (1)), etc.
    # Match: opening paren, any content with uppercase/numbers/hyphens/spaces/parens, closing paren at end
    cleaned_title = re.sub(r'\s*\([A-Z0-9\-\s()]+\)\s*$', '', title)
    return cleaned_title.strip()

def generate_accordion_html(project):
    """Generate HTML for a single project accordion."""
    metadata = project['metadata']
    
    # Replace client names in content if needed (do this FIRST)
    content = replace_client_names(project['content'], metadata)
    
    # Extract title from content (first # heading) - now from cleaned content
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else f"Project {project['number']}"
    
    # Remove project code from title
    title = remove_project_code_from_title(title)
    
    # Also remove project codes from H1 in content (including nested parens like BTCL-ARCO (1))
    content = re.sub(r'^(#\s+.+?)\s*\([A-Z0-9\-\s()]+\)\s*$', r'\1', content, flags=re.MULTILINE)
    
    # Get project code
    project_code = metadata.get('project_code', [''])[0]
    
    # Get tags for display
    industries = [get_tag_display_name(i) for i in metadata.get('client_side_industry', [])]
    roles = [get_tag_display_name(r) for r in metadata.get('roles', [])]
    functional = [get_tag_display_name(f) for f in metadata.get('functional', [])]
    
    # Build tag display
    tags_display = []
    if industries:
        tags_display.append(f"<em>Industry:</em> {', '.join(industries)}")
    if roles:
        tags_display.append(f"<em>Role:</em> {', '.join(roles)}")
    if functional:
        tags_display.append(f"<em>Domain:</em> {', '.join(functional[:2])}")  # Limit to 2 for brevity
    
    tags_html = ' | '.join(tags_display) if tags_display else ''
    
    # Convert to HTML
    content_html = convert_markdown_to_html(content)
    
    # Build accordion
    accordion = f"""
<details>
<summary><strong>{title}</strong></summary>
<div style="padding: 15px; border-left: 3px solid #0066cc; margin-top: 10px;">
{f'<p style="color: #666; font-size: 0.9em;">{tags_html}</p>' if tags_html else ''}
{content_html}
</div>
</details>
"""
    return accordion

def group_projects_by_tag(projects, tag_key):
    """Group projects by a specific tag."""
    groups = defaultdict(list)
    
    for project in projects:
        tags = project['metadata'].get(tag_key, [])
        if not tags:
            tags = ['other']
        
        for tag in tags:
            groups[tag].append(project)
    
    return groups

def generate_cases_page(projects):
    """Generate the complete cases.md page."""
    
    # Sort projects by number
    projects_sorted = sorted(projects, key=lambda p: p['number'])
    
    # Group projects
    by_industry = group_projects_by_tag(projects_sorted, 'client_side_industry')
    by_functional = group_projects_by_tag(projects_sorted, 'functional')
    by_roles = group_projects_by_tag(projects_sorted, 'roles')
    
    # Start building the page
    page_content = """---
layout: page
title: "Cases"
seo_title: "Project Portfolio & Case Studies - Enterprise Architecture Projects"
description: "Browse 44+ enterprise architecture projects across Retail, Finance, Healthcare, Telecom, and Oil & Gas industries. Explore detailed project descriptions, architecture approaches, and implementation outcomes."
keywords: "Enterprise Architecture projects, TOGAF projects, ArchiMate diagrams, Business Transformation case studies, IT Strategy projects, Digital Transformation portfolio"
lang: en
permalink: /cases/
---

Browse my project portfolio organized by industry, role, and functional domain. Each project includes detailed context, decision challenges, architectural perspectives, and measurable outcomes.

---

## Professional Profile

<a href="/downloads/resume.pdf" target="_blank"><strong>Resume (PDF)</strong></a> — My up-to-date CV in English

---

## Project Portfolio

Browse my **44 completed projects** organized by industry, role, or functional domain. Click on any project to expand and view details.

<h2 id="industry">By Industry</h2>

"""
    
    # Add industry sections
    industry_order = ['retail', 'telecom', 'oil-gas', 'finance', 'healthcare', 'consulting', 'it-services', 'other']
    for industry in industry_order:
        if industry not in by_industry:
            continue
        
        industry_projects = by_industry[industry]
        industry_name = get_tag_display_name(industry)
        
        page_content += f"""
<details>
<summary><strong>{industry_name} ({len(industry_projects)} projects)</strong></summary>
<div style="padding-left: 20px;">
"""
        
        for project in sorted(industry_projects, key=lambda p: p['number']):
            page_content += generate_accordion_html(project)
        
        page_content += """
</div>
</details>

"""
    
    page_content += """
---

<h2 id="role">By Role</h2>

"""
    
    # Add role sections
    role_order = ['enterprise-architect', 'solution-architect', 'business-analyst', 'product-manager', 'project-manager', 'other']
    for role in role_order:
        if role not in by_roles:
            continue
        
        role_projects = by_roles[role]
        role_name = get_tag_display_name(role)
        
        page_content += f"""
<details>
<summary><strong>{role_name} ({len(role_projects)} projects)</strong></summary>
<div style="padding-left: 20px;">
"""
        
        for project in sorted(role_projects, key=lambda p: p['number']):
            page_content += generate_accordion_html(project)
        
        page_content += """
</div>
</details>

"""
    
    page_content += """
---

<h2 id="domain">By Functional Domain</h2>

"""
    
    # Add functional domain sections (top 10 most common)
    functional_sorted = sorted(by_functional.items(), key=lambda x: len(x[1]), reverse=True)[:10]
    
    for functional, functional_projects in functional_sorted:
        functional_name = get_tag_display_name(functional)
        
        page_content += f"""
<details>
<summary><strong>{functional_name} ({len(functional_projects)} projects)</strong></summary>
<div style="padding-left: 20px;">
"""
        
        for project in sorted(functional_projects, key=lambda p: p['number']):
            page_content += generate_accordion_html(project)
        
        page_content += """
</div>
</details>

"""
    
    return page_content

def main():
    """Main function to generate cases page."""
    # Find project files
    projects_dir = Path(__file__).parent / 'knowledge-base' / '3. projects-eng'
    
    if not projects_dir.exists():
        print(f"Error: Projects directory not found: {projects_dir}")
        return
    
    # Parse all project files
    projects = []
    for filepath in sorted(projects_dir.glob('*.md')):
        project = parse_project_file(filepath)
        if project:
            projects.append(project)
            print(f"Parsed: {filepath.name}")
    
    print(f"\nTotal projects parsed: {len(projects)}")
    
    # Generate page
    page_content = generate_cases_page(projects)
    
    # Write to cases.md
    output_file = Path(__file__).parent / 'cases.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(page_content)
    
    print(f"\nGenerated: {output_file}")
    print("Done!")

if __name__ == '__main__':
    main()
