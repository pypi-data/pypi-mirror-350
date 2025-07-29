import typer

from gnor.src.gitignore import (
    get_template_list,
    search_stack,
)

app = typer.Typer()


@app.command()
def list():
    """
    List all available .gitignore templates.
    """
    # Placeholder for the actual implementation
    print('Listing all available .gitignore templates...')

    for template in get_template_list():
        print(f'- {template}')


@app.command()
def search(term: str):
    """
    Search for a term in the list of available templates.
    """
    # Placeholder for the actual implementation
    print(f'Searching for "{term}" in the list of available templates...\n')

    for template in search_stack(term):
        print(f'- {template}')


if __name__ == '__main__':
    app()
