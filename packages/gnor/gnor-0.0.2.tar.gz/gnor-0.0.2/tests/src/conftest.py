import pytest


@pytest.fixture
def get_fake_gitignore() -> str:
    return """
.venv
.env
.machadoah
.sao_paulo_futebol_clube
"""
