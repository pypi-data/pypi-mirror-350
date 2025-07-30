# Toolit
MCP Server and Typer CLI in one, provides an easy way to configure your own DevTools in a project.

## Installation
To get started with Toolit, install the package via pip:

```bash
pip install toolit
```

## Usage
Add a folder called `devtools` to your project root. Create python modules, you decide the name, in this folder. Add the tool decorator to functions you want to expose as commands.

```python
from toolit import tool
@tool
def my_command(to_print: str = "Hello, World!") -> None:
    """This is a command that can be run from the CLI."""
    print(to_print)
```

Toolit will automatically discover these modules and make them available as commands.

Now you can run your command from the command line:

```bash
toolit --help  # To see available commands
toolit my-command --to_print "Hello, Toolit!"  # To run your command
```

## Create the VS code tasks.json file
You can automatically create a `tasks.json` file for Visual Studio Code to run your ToolIt commands directly from the editor. This is useful for integrating your development tools into your workflow.

To create the `.vscode/tasks.json` file, run the following command in your terminal:
```bash
python -m toolit.create_tasks_json
```
NOTE: THIS WILL OVERWRITE YOUR EXISTING `.vscode/tasks.json` FILE IF IT EXISTS!

## Contributing
We welcome contributions to ToolIt! If you have ideas for new features, improvements, or bug fixes, please open an issue or submit a pull request on our GitHub repository. We appreciate your feedback and support in making ToolIt even better for the community.
