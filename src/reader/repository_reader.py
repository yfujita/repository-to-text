import sys
from pathlib import Path
from typing import List, Optional
from pathspec import PathSpec

# バイナリ判定の定数
BINARY_CHECK_BLOCK_SIZE = 1024  # バイトサイズ
BINARY_CHECK_MAX_BLOCKS = 8     # 最大チェックブロック数

class RepositoryReader:
    """
    - ルート直下から再帰的に走査
    - .git は常に除外
    - すべての .gitignore と .git/info/exclude を取り込み、gitwildmatch で判定
      * ネガティブ(!)パターン / ** / 末尾スラッシュなどにも対応
      * サブディレクトリの .gitignore は、その配置ディレクトリ基準として前置
    """
    def __init__(self, repo_path: str, ignore_dirs: Optional[List[str]] = None) -> None:
        self.root = Path(repo_path).resolve()
        if not self.root.exists():
            raise FileNotFoundError(f"repo_path not found: {self.root}")
        self.ignore_dirs = ignore_dirs or []
        self._spec: PathSpec = self._build_gitignore_spec()

    """
    ルート直下から再帰的に走査し、辞書のリストで返す
    """
    def get_whole_structure(self) -> List[dict]:
        return self._walk(self.root)

    def _walk(self, dir_path: Path) -> List[dict]:
        result: List[dict] = []

        try:
            items = sorted(dir_path.iterdir())
        except PermissionError:
            return result

        for item in items:
            # 常に .git を除外
            if item.name == ".git":
                continue
            # .gitignore 判定で除外
            if self._is_ignored(item):
                # ディレクトリが無視対象なら中にも潜らない
                continue

            if item.is_dir():
                result.append({
                    "name": item.name,
                    "type": "directory",
                    "children": self._walk(item)
                })
            elif self.is_binary(item):
                result.append({
                    "name": item.name,
                    "type": "file",
                    "content": ""
                })
            else:
                try:
                    content = item.read_text(encoding="utf-8", errors="ignore")
                except (IOError, OSError, UnicodeDecodeError) as e:
                    print(f"Warning: Could not read {item}: {e}", file=sys.stderr)
                    content = ""
                result.append({
                    "name": item.name,
                    "type": "file",
                    "content": content
                })
        return result

    def _is_ignored(self, path: Path) -> bool:
        rel = path.relative_to(self.root).as_posix()
        # ディレクトリは末尾スラッシュも試す
        if path.is_dir() and self._spec.match_file(rel + "/"):
            return True
        return self._spec.match_file(rel)

    def _build_gitignore_spec(self) -> PathSpec:
        patterns: List[str] = []

        # すべての .gitignore を集めて、その配置ディレクトリを前置
        for gi in self.root.rglob(".gitignore"):
            base = gi.parent.relative_to(self.root).as_posix()
            try:
                lines = gi.read_text(encoding="utf-8", errors="ignore").splitlines()
            except (IOError, OSError) as e:
                print(f"Warning: Could not read .gitignore at {gi}: {e}", file=sys.stderr)
                lines = []

            for raw in lines:
                s = raw.strip()
                if not s or s.startswith("#"):
                    continue
                neg = s.startswith("!")
                if neg:
                    s = s[1:]

                # 先頭の "/" はその .gitignore の置き場を基準にするので取り除く
                s = s.lstrip("/")

                # ルートからの相対に正規化
                if base != ".":
                    s = f"{base}/{s}"

                if neg:
                    s = "!" + s

                patterns.append(s)

        # .git/info/exclude も取り込む
        info_exclude = self.root / ".git" / "info" / "exclude"
        if info_exclude.exists():
            try:
                for raw in info_exclude.read_text(encoding="utf-8", errors="ignore").splitlines():
                    s = raw.strip()
                    if not s or s.startswith("#"):
                        continue
                    patterns.append(s)
            except (IOError, OSError) as e:
                print(f"Warning: Could not read .git/info/exclude: {e}", file=sys.stderr)

        # 実行時に追加指定された除外ディレクトリを取り込む
        patterns.extend(self.ignore_dirs)

        # パターンが空でも空の spec を返す
        return PathSpec.from_lines("gitwildmatch", patterns)

    def is_binary(self, file_path: Path) -> bool:
        """Check if a file is binary by reading limited blocks.

        Args:
            file_path: Path to the file to check

        Returns:
            True if file appears to be binary, False otherwise
        """
        try:
            with file_path.open("rb") as f:  # Pathlibの一貫性を保つ
                for _ in range(BINARY_CHECK_MAX_BLOCKS):
                    block = f.read(BINARY_CHECK_BLOCK_SIZE)
                    if not block:
                        break
                    if b"\0" in block:
                        return True
        except (IOError, OSError) as e:
            print(f"Error checking file {file_path}: {e}", file=sys.stderr, flush=True)
            return False
        return False
