import os
import shutil
import click
import importlib.resources

TEMPLATE_DIR = importlib.resources.files('flaskbuilder').joinpath('templates')

@click.command()
@click.argument('project_name')
def main(project_name):
    click.echo(f'🚧 Generating Flask project: {project_name}...')
    
    project_path = os.path.abspath(project_name)
    
    if os.path.exists(project_path):
        click.echo('❌ Folder already exists!')
        return

    shutil.copytree(TEMPLATE_DIR, project_path)

    click.echo('✅ Project created successfully!')
    click.echo(f'📂 Location: {project_path}')
    click.echo('👉 Next steps:')
    click.echo(f'    cd {project_name}')
    click.echo('    python -m venv venv')
    click.echo('    source venv/bin/activate  (or venv\\Scripts\\activate on Windows)')
    click.echo('    pip install -r requirements.txt')
    click.echo('    python main.py')

if __name__ == '__main__':
    main()
