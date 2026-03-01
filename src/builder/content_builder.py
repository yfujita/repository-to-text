from typing import List, Dict, Any

# コード区切り線の定数
CODE_SEPARATOR_LINE = '-' * 40 + '\n'

class ContentBuilder:
    """Build text representations of repository structure and code content.

    This class processes a repository structure (as returned by RepositoryReader)
    and generates formatted text output for both the file tree and code listings.
    """

    def __init__(self, whole_structure: List[Dict[str, Any]]) -> None:
        """Initialize ContentBuilder with repository structure.

        Args:
            whole_structure: List of dictionaries representing the repository structure.
                Each dict has 'name', 'type', and optionally 'children' or 'content'.
        """
        self.whole_structure: List[Dict[str, Any]] = whole_structure

    def build_project_tree_text(self) -> str:
        """Build a text representation of the project file tree.

        Returns:
            String containing all file paths in the repository, one per line.
        """
        return self._build_project_tree_text_recursive(self.whole_structure, '')

    def _build_project_tree_text_recursive(self, structure: List[Dict[str, Any]], parent_path: str) -> str:
        """Recursively build file tree text."""
        parts: List[str] = []
        for item in structure:
            if item['type'] == 'directory':
                parts.append(self._build_project_tree_text_recursive(item['children'], f'{parent_path}/{item["name"]}'))
            else:
                parts.append(f'{parent_path}/{item["name"]}\n')
        return ''.join(parts)

    def build_code_list(self) -> str:
        """Build a text listing of all code files with their contents.

        Returns:
            String containing formatted code listings with file paths and contents.
        """
        return self._build_code_list_recursive(self.whole_structure, '')

    def _build_code_list_recursive(self, structure: List[Dict[str, Any]], parent_path: str) -> str:
        """Recursively build code listing text."""
        parts: List[str] = []
        for item in structure:
            if item['type'] == 'directory':
                parts.append(self._build_code_list_recursive(item['children'], f'{parent_path}/{item["name"]}'))
            else:
                parts.append(CODE_SEPARATOR_LINE)
                parts.append(f'FilePath: {parent_path}/{item["name"]}\n')
                parts.append('\n')
                parts.append(item['content'] + '\n')
                parts.append('\n')
        return ''.join(parts)