import click
from rich.console import Console
from rich.panel import Panel
from agentops_ai.agentops_core.services.test_generator import TestGenerator
from agentops_ai.agentops_core.analyzer import CodeAnalyzer, _add_parents, analyze_tree_with_parents
import subprocess
import sys
import ast
import os
import yaml

console = Console()

@click.group()
@click.version_option()
def cli():
    """AgentOps - AI-powered testing for everyone."""
    pass

def load_config(directory):
    config_path = os.path.join(directory, '.agentops.yml')
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = yaml.safe_load(f)
        return config
    return {}

@cli.command()
@click.argument('directory', default='.')
def init(directory):
    """Initialize a new AgentOps project."""
    project_dir = os.path.abspath(directory)
    os.makedirs(project_dir, exist_ok=True)
    # Create tests directory
    tests_dir = os.path.join(project_dir, 'tests')
    if not os.path.exists(tests_dir):
        os.makedirs(tests_dir)
        console.print(Panel(f"Created tests directory at {tests_dir}", title="AgentOps Init", style="green"))
    else:
        console.print(Panel(f"Tests directory already exists at {tests_dir}", title="AgentOps Init", style="yellow"))
    # Create sample .agentops.yml config
    config_path = os.path.join(project_dir, '.agentops.yml')
    if not os.path.exists(config_path):
        sample_config = {
            'test_framework': 'pytest',
            'openai_model': 'gpt-4',
            'test_output_dir': 'tests',
            'coverage': True
        }
        with open(config_path, 'w') as f:
            yaml.dump(sample_config, f)
        console.print(Panel(f"Created sample config at {config_path}", title="AgentOps Init", style="green"))
    else:
        console.print(Panel(f"Config already exists at {config_path}", title="AgentOps Init", style="yellow"))
    console.print(Panel(f"AgentOps project initialized at {project_dir}", title="AgentOps Init", style="cyan"))

@cli.command(name="generate")
@click.argument('target', default='.')
@click.option('--type', '-t', default=None, help='What to generate (tests, docs, etc.)')
@click.option('--framework', '-f', default=None, help='Testing framework to use (pytest, unittest)')
@click.option('--api-key', default=None, help='OpenAI API key (or set OPENAI_API_KEY env var)')
def generate(target, type, framework, api_key):
    """Generate tests or other artifacts."""
    project_dir = os.path.dirname(target) if os.path.isfile(target) else target
    config = load_config(project_dir)
    if config:
        console.print(Panel(f"Loaded config from .agentops.yml:\n{config}", title="AgentOps Config", style="cyan"))
    type = type or config.get('type', 'tests')
    framework = framework or config.get('test_framework', 'pytest')
    api_key = api_key or config.get('openai_api_key')
    output_dir = config.get('test_output_dir', 'tests')
    if type != 'tests':
        console.print(Panel(f"Only test generation is supported right now.", title="AgentOps Generate", style="red"))
        return
    if not target.endswith('.py'):
        console.print(Panel(f"Currently, only single Python files are supported.", title="AgentOps Generate", style="red"))
        return
    try:
        with open(target) as f:
            code = f.read()
    except Exception as e:
        console.print(Panel(f"Failed to read file: {e}", title="AgentOps Generate", style="red"))
        return
    console.print(Panel(f"Generating {framework} tests for {target}...", title="AgentOps Generate", style="cyan"))
    tg = TestGenerator(api_key=api_key)
    result = tg.generate_tests(code, framework=framework)
    if not result["success"]:
        console.print(Panel(f"Test generation failed: {result['error']}", title="AgentOps Generate", style="red"))
        return
    test_code = result["tests"]
    out_file = tg.write_tests_to_file(test_code, output_dir=output_dir, base_name=f"test_{os.path.basename(target)}")
    console.print(Panel(f"[green]Test generation complete![/green]\nSaved to: {out_file}\nConfidence: {result['confidence']}", title="AgentOps Generate", style="green"))

@cli.command(name="run")
@click.argument('target', default='tests')
@click.option('--show-coverage', is_flag=True, help='Show coverage information')
def run(target, show_coverage):
    """Run tests and show results."""
    config = load_config(target) if os.path.isdir(target) else load_config(os.path.dirname(target))
    if config:
        console.print(Panel(f"Loaded config from .agentops.yml:\n{config}", title="AgentOps Config", style="cyan"))
    show_coverage = show_coverage or config.get('coverage', False)
    console.print(Panel(f"Running {target}...", title="AgentOps Run", style="cyan"))
    try:
        if show_coverage:
            result = subprocess.run([sys.executable, '-m', 'coverage', 'run', '-m', 'pytest', target], capture_output=True, text=True)
            cov_result = subprocess.run([sys.executable, '-m', 'coverage', 'report'], capture_output=True, text=True)
            output = result.stdout + '\n' + cov_result.stdout
        else:
            result = subprocess.run([sys.executable, '-m', 'pytest', target], capture_output=True, text=True)
            output = result.stdout
        if result.returncode == 0:
            console.print(Panel(f"[green]All tests passed![/green]\n\n{output}", title="AgentOps Run", style="green"))
        else:
            console.print(Panel(f"[red]Some tests failed.[/red]\n\n{output}", title="AgentOps Run", style="red"))
    except Exception as e:
        console.print(Panel(f"Failed to run tests: {e}", title="AgentOps Run", style="red"))

@cli.command(name="analyze")
@click.argument('target', default='.')
def analyze(target):
    """Analyze code quality and provide suggestions."""
    config = load_config(os.path.dirname(target))
    if config:
        console.print(Panel(f"Loaded config from .agentops.yml:\n{config}", title="AgentOps Config", style="cyan"))
    if not target.endswith('.py'):
        console.print(Panel(f"Currently, only single Python files are supported.", title="AgentOps Analyze", style="red"))
        return
    try:
        with open(target) as f:
            code = f.read()
    except Exception as e:
        console.print(Panel(f"Failed to read file: {e}", title="AgentOps Analyze", style="red"))
        return
    tree = ast.parse(code)
    _add_parents(tree)
    result = analyze_tree_with_parents(tree)
    summary = []
    summary.append(f"[bold]Imports:[/bold] {', '.join(result['imports']) if result['imports'] else 'None'}")
    summary.append(f"[bold]Functions:[/bold] {', '.join(f.name for f in result['functions']) if result['functions'] else 'None'}")
    summary.append(f"[bold]Classes:[/bold] {', '.join(c.name for c in result['classes']) if result['classes'] else 'None'}")
    suggestions = []
    if not result['functions']:
        suggestions.append("No functions found. Consider adding reusable functions.")
    if not result['classes']:
        suggestions.append("No classes found. Consider using classes for better organization.")
    if not result['imports']:
        suggestions.append("No imports found. Is this file self-contained?")
    console.print(Panel("\n".join(summary), title="Code Summary", style="cyan"))
    if suggestions:
        console.print(Panel("\n".join(suggestions), title="Suggestions", style="yellow"))
    else:
        console.print(Panel("Code looks well-structured!", title="Suggestions", style="green"))

if __name__ == '__main__':
    cli() 