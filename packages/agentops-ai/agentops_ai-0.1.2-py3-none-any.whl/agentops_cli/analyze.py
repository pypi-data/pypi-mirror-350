import click
import json
from agentops_core.analyzer import CodeAnalyzer, _add_parents
import ast

@click.command()
@click.argument('file', type=click.Path(exists=True))
def analyze(file):
    """Analyze a Python file and print structured info."""
    analyzer = CodeAnalyzer()
    with open(file, 'r') as f:
        code = f.read()
    tree = ast.parse(code)
    _add_parents(tree)
    result = analyzer.analyze_code(code)
    click.echo(json.dumps(result, indent=2, default=str)) 