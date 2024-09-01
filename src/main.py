import os
from reader.repository_reader import RepositoryReader
from builder.content_builder import ContentBuilder

def main():
    repo_path = os.getenv('REPO_PATH', '')
    if repo_path == '':
        print('REPO_PATH is not set.', flush=True)
        exit(1)
    reader = RepositoryReader(repo_path)
    whole_structure: list = reader.get_whole_structire()

    builder = ContentBuilder(whole_structure)
    prompt = get_prompt_text(builder)
    print(prompt)

def get_prompt_text(content_builder: ContentBuilder) -> str:
    prompt = 'The following shows the file structure and code text of the project.\n\n'
    prompt += '# Project Tree\n'
    project_tree_text = content_builder.build_project_tree_text()
    prompt += project_tree_text
    prompt += '\n'
    prompt += '# Code List\n'
    code_list = content_builder.build_code_list()
    prompt += code_list
    return prompt

if __name__ == '__main__':
    main()