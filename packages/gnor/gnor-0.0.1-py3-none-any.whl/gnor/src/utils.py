from http import HTTPStatus

import requests

from gnor.settings import settings

INIT_SIGNATURE = """# 🐈‍ Created by https://github.com/github/gitignore
# 📝 Edit at https://github.com/github/gitignore/pulls
"""

FINAL_SIGNATURE = """# 🔦 Generated using IGNOR - github.com/machadoah/ignor"""


def get_github_template(stack: str) -> str:
    """
    Request a template from GitHub.
    """
    url = settings.URL_GITHUB_TEMPLATE.format(stack=stack)

    print(f'Requesting template from {url}...')

    response = requests.get(url)

    if response.status_code == HTTPStatus.OK:
        return response.text
    else:
        return f"""Failed to fetch template {stack} from GitHub.
Status code: {response.status_code}"""
