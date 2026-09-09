# repository-to-text

リポジトリのファイル構成とコードを1つのテキストにまとめて、LLMに投げやすくするツール。

- `.gitignore` に従ってファイルを除外
- バイナリファイルは中身を空にして安全に処理
- LLM向けの見やすい形式で出力

---

## 使い方

### Docker（推奨）

```bash
bash run.sh /path/to/repository > out.txt
```

`.gitignore` に加えて除外したいディレクトリ・ファイルがある場合は、第2引数以降に指定する（gitignore と同じパターン形式）。

```bash
bash run.sh /path/to/repository node_modules dist "*.log" > out.txt
```

### ローカル実行

```bash
pip install -r requirements.txt
export REPO_PATH=/path/to/repository
export IGNORE_DIRS="node_modules,dist"  # 任意
python src/main.py > out.txt
```

## 出力形式

こんな感じで出力される：

```
The following shows the file structure and code text of the project.

# Project Tree
/README.md
/src/main.py
/src/reader/repository_reader.py

# Code List
----------------------------------------
FilePath: /src/main.py

import os
from reader.repository_reader import RepositoryReader
...
```

## 仕組み

- すべての `.gitignore` ファイルを読み込んで除外判定
- `.git` フォルダは常に除外
- バイナリファイルは中身を空文字列にする
- ファイル一覧とコード内容の2セクション構成

## LLM Service での使い方例

出力ファイルを添付した上でレビューなどを依頼する。

