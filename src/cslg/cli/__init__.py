import argparse
import os

PROGRAM = """
namespace {name}
{{
    public class Program
    {{
        public static void Main()
        {{
        }}
    }}
}}
"""

GITIGNORE = """
#Class Diagram
*.cd.md
"""


def process(
    name: str,
    output: str = None,
    projects: list[str] = None,
    git: bool = False,
):
    if not name.lower().startswith("lab"):
        name = f"Lab{name}"

    if output is None:
        output = os.getcwd()

    if not output.strip("/").strip("\\").endswith(name):
        output = os.path.join(output, name)

    if projects is None:
        projects = []

    tests = f"{name}Tests"

    os.makedirs(output)
    os.chdir(output)
    os.system(f'dotnet new sln -n "{name}"')

    sln = os.path.join(output, name) + ".sln"

    if git:
        os.system("git init")
        os.system("dotnet new gitignore")
        with open(".gitignore", "a", encoding="utf-8") as gitignore:
            gitignore.write(GITIGNORE)

    for project in projects:
        os.system(f'dotnet sln "{sln}" add "{project}"')

    os.system(f'dotnet new "console" -lang "C#" -n "{name}" -o "{name}"')

    lab_proj = f"{os.path.join(output, name, name)}.csproj"

    os.system(f'dotnet sln "{sln}" add "{lab_proj}"')
    os.chdir(os.path.join(output, name))

    for project in projects:
        os.system(f'dotnet add "{lab_proj}" reference "{project}"')

    with open("Program.cs", "w", encoding="utf-8") as program:
        program.write(PROGRAM.format(name=name))

    os.chdir(output)

    os.system(f'dotnet new "xunit" -lang "C#" -n "{tests}" -o "{tests}"')

    tests_proj = f"{os.path.join(output, tests, tests)}.csproj"

    os.system(f'dotnet sln "{sln}" add "{tests_proj}"')
    os.chdir(os.path.join(output, tests))

    os.system(f'dotnet add "{tests_proj}" reference "{lab_proj}"')
    for project in projects:
        os.system(f'dotnet add "{tests_proj}" reference "{project}"')

    os.system(f'dotnet add "{tests_proj}" package "coverlet.msbuild" -v "6.0.0"')


def main():
    parser = argparse.ArgumentParser(description="C# Lab Generator")
    parser.add_argument(
        "-n",
        "--name",
        help="lab name (example: Lab1)",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="path to output dir (default: current dir)",
        type=str,
    )
    parser.add_argument(
        "-p",
        "--projects",
        help="add existing projects to sln (absolute path to .csproj)",
        nargs="+",
    )
    parser.add_argument(
        "-g",
        "--git",
        help="init git repo in output dir",
        action="store_true",
    )
    args = parser.parse_args()

    process(args.name, args.output, args.projects, args.git)
