from gnor.src.github_stacks import STACKS
from gnor.src.utils import get_github_template


def get_template_list() -> list[str]:
    return STACKS['root']


def get_template_stack(
    stack: str, stacks: list[str] = get_template_list()
) -> str:
    for s in stacks:
        if s.split('.')[0].lower() == stack.lower():
            return get_github_template(s.split('.')[0])


def search_stack(
    stack: str, stacks: list[str] = get_template_list()
) -> list[str]:
    return [s for s in stacks if stack.lower() in s.lower()]
