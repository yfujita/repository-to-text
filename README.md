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

### ローカル実行

```bash
pip install -r requirements.txt
export REPO_PATH=/path/to/repository
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

## ChatGPT での使い方例

出力ファイルをChatGPTに添付して：

```
このプロジェクトの内容を理解して、以下について教えて：
- 何をするツールか
- 改善点があるか
- バグがありそうな箇所
```


