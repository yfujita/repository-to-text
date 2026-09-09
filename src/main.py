"""Main entry point for repository-to-text tool.

This module reads a repository path from REPO_PATH environment variable,
processes the repository structure and content, and outputs a formatted
text representation suitable for AI prompts.
"""
import os
import sys
from reader.repository_reader import RepositoryReader
from builder.content_builder import ContentBuilder

def main() -> None:
    """Main entry point for the repository-to-text tool."""
    repo_path = os.getenv('REPO_PATH', '')
    if repo_path == '':
        print('REPO_PATH is not set.', file=sys.stderr)
        exit(1)
    ignore_dirs = [d for d in os.getenv('IGNORE_DIRS', '').split(',') if d]
    reader = RepositoryReader(repo_path, ignore_dirs=ignore_dirs)
    whole_structure: list = reader.get_whole_structure()

    builder = ContentBuilder(whole_structure)
    prompt = build_repository_prompt(builder)
    print(prompt)

def build_repository_prompt(content_builder: ContentBuilder) -> str:
    """Build a complete prompt text from repository content.

    Args:
        content_builder: ContentBuilder instance with repository structure.

    Returns:
        Formatted prompt string containing project tree and code listings.
    """
    parts = [
        'The following shows the file structure and code text of the project.\n\n',
        '# Project Tree\n',
        content_builder.build_project_tree_text(),
        '\n',
        '# Code List\n',
        content_builder.build_code_list()
    ]
    return ''.join(parts)

if __name__ == '__main__':
    main()