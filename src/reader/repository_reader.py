from pathlib import Path

class RepositoryReader:
    def __init__(self, repo_path: str) -> None:
        self.repo_path = repo_path

    def get_whole_structire(self) -> list:
        root_path = Path(self.repo_path)
        return self.get_dir_structure(root_path)

    def get_dir_structure(self, dir_path: Path) -> list:
        result: list = []

        items = list(dir_path.iterdir())

        for item in items:
            if item.is_dir():
                if item.name == '.git':
                    # Skip .git directory
                    continue
                
                result.append({
                    'name': item.name,
                    'type': 'directory',
                    'children': self.get_dir_structure(item)
                })
            else:
                result.append({
                    'name': item.name,
                    'type': 'file',
                    'content': item.read_text()
                })
        return result
