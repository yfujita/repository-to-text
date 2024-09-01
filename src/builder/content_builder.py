
class ContentBuilder:
    def __init__(self, whole_structure: list):
        self.whole_structure = whole_structure

    def build_project_tree_text(self) -> str:
        return self._build_project_tree_text_recursive(self.whole_structure, '')
    
    def _build_project_tree_text_recursive(self, structure: list, parent_path: str) -> str:
        result = ''
        for item in structure:
            if item['type'] == 'directory':
                result += self._build_project_tree_text_recursive(item['children'], f'{parent_path}/{item["name"]}')
            else:
                result += f'{parent_path}/{item["name"]}\n'
        return result

    def build_code_list(self) -> str:
        return self._build_code_list_recursive(self.whole_structure, '')
    
    def _build_code_list_recursive(self, structure: list, parent_path: str) -> str:
        result = ''
        for item in structure:
            if item['type'] == 'directory':
                result += self._build_code_list_recursive(item['children'], f'{parent_path}/{item["name"]}')
            else:
                result += '----------------------------------------\n'
                result += f'FilePath: {parent_path}/{item["name"]}\n'
                result += '\n'
                result += item['content'] + '\n'
                result += '\n'
        return result