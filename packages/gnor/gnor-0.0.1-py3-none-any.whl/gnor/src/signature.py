from gnor.src.utils import FINAL_SIGNATURE, INIT_SIGNATURE


def get_signed_gitignore(gitignore: str) -> str:
    return f"""
{INIT_SIGNATURE}
{gitignore}
{FINAL_SIGNATURE}
"""
