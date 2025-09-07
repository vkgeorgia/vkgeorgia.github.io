#!/usr/bin/env python3
"""
Script to add Jekyll front matter to markdown files
"""

import os
import re
from pathlib import Path

def get_title_from_content(content):
    """Extract title from first h1 heading"""
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    return "Untitled"

def add_front_matter(file_path, lang='en'):
    """Add Jekyll front matter to a markdown file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has front matter
    if content.startswith('---'):
        return
    
    # Extract title from content
    title = get_title_from_content(content)
    
    # Determine permalink based on file path
    rel_path = str(file_path).replace(str(Path.cwd()), '').lstrip('\\/')
    permalink = '/' + rel_path.replace('\\', '/').replace('.md', '/')
    
    # Create front matter
    front_matter = f"""---
layout: page
title: "{title}"
description: "{title}"
lang: {lang}
permalink: {permalink}
---

"""
    
    # Add front matter to content
    new_content = front_matter + content
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Added front matter to: {file_path}")

def process_directory(directory, lang='en'):
    """Process all markdown files in a directory"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md') and file != 'README.md':
                file_path = Path(root) / file
                add_front_matter(file_path, lang)

if __name__ == "__main__":
    # Process English files
    process_directory('en', 'en')
    
    # Process Russian files  
    process_directory('ru', 'ru')
    
    print("Front matter addition completed!")
