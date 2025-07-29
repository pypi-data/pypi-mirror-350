from gnor.src.signature import get_signed_gitignore
from gnor.src.utils import FINAL_SIGNATURE, INIT_SIGNATURE


def test_get_signed_gitignore_correct_formatted(get_fake_gitignore):
    gitigore = get_fake_gitignore

    signed_gitignore = get_signed_gitignore(gitignore=gitigore)

    assert INIT_SIGNATURE in signed_gitignore
    assert FINAL_SIGNATURE in signed_gitignore
