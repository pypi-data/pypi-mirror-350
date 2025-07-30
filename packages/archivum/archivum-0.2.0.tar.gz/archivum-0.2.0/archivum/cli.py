"""Implement command line interface for archivum."""

from functools import partial
import os
from pathlib import Path
import shlex
import socket
import subprocess
import yaml

import click
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import FuzzyCompleter, WordCompleter, NestedCompleter, PathCompleter
from prompt_toolkit.formatted_text import HTML

from greater_tables import GT

from . reference import Reference
from . library import Library
from . import DEFAULT_CONFIG_FILE, BASE_DIR, APP_SUFFIX, APP_NAME
from . utilities import df_to_str


def clear_screen():
    os.system('cls')


@click.group()
def entry():
    """CLI for managing bibliographic entries."""
    pass


@entry.command()
@click.option('-d', '--directory', default='~/Downloads', type=click.Path(exists=True), help='Directory to scan for PDFs')
def new(directory):
    """List PDFs and show basic metadata."""
    pdfs = find_pdfs(directory)
    for i, pdf in enumerate(pdfs):
        meta = extract_metadata(pdf)
        click.echo(f"{i}: {pdf.name}")
        if meta:
            click.echo(f"    Title: {meta.get('title', 'Unknown')}")
            click.echo(f"    Author: {meta.get('author', 'Unknown')}")


@entry.command()
@click.option('-p', '--partial', required=True, help='Comma-separated list of PDF numbers to upload')
def upload(partial):
    """Interactively create reference object."""
    indices = [int(i.strip()) for i in partial.split(',')]
    pdfs = find_pdfs()  # reuse previous list or cache it
    for i in indices:
        pdf_path = pdfs[i]
        ref = Reference.from_pdf(pdf_path)
        prompt_for_fields(ref)  # interactively fill in fields
        click.echo(ref.to_dict())  # or save it, display BibTeX, etc.


@entry.command()
@click.argument('libname', type=str)
def create_library(libname):
    """Interactively create a YAML config file for a new library called libname."""

    # sort the file out
    lib_path = BASE_DIR / f'{libname}{APP_SUFFIX}'
    click.secho("=== Library Config Creator ===", fg='cyan')
    click.secho(f'Creating Library {libname} at {lib_path}')

    config = {
        "library": libname,
        "description": click.prompt('Description'),
        "database": str(lib_path.with_suffix(f'.{APP_NAME}-feather')),
        "columns": ['type', 'tag', 'author', 'doi', 'file', 'journal', 'pages', 'title',
                    'volume', 'year', 'publisher', 'url', 'institution', 'number',
                    'mendeley-tags', 'booktitle', 'edition', 'month', 'address', 'editor',
                    'arc-citations'],
        "bibtex_file": click.prompt('BibTeX File', default=f'{libname}-test.bib'),
        "pdf_dir": click.prompt('PDF Directory', default='NOT USED YET'),
        "file_formats": ["*.pdf"],
        "hash_files": click.confirm("Hash files?", default=True),
        "hash_workers": click.prompt("Number of hash workers", default=6, type=int),
        "last_indexed": 0,
        "timezone": click.prompt("Timezone", default="Europe/London"),
        "tablefmt": click.prompt("Table format", default="mixed_grid"),
    }

    with lib_path.open("w", encoding="utf-8") as f:
        yaml.dump(config, f, sort_keys=False)

    click.secho(f"\nConfig written to {lib_path}", fg="green")


# todo add a default config
@ entry.command()
@ click.option('-c', '--config', type=DEFAULT_CONFIG_FILE, help='Library config path')
@ click.option('-t', '--tablefmt', default='', show_default=True, help='Markdown table format (see tabulate docs); default uses config file value.')
def query_repl(config: Path, tablefmt: str):
    """Interactive REPL to run multiple queries on the file index with fuzzy completion."""
    lib = Library(config)
    print(lib)
    if tablefmt == '':
        tablefmt = lib.tablefmt
    click.echo(f"Loaded {len(lib.database):,} rows from {lib.name}")
    click.echo(
        "Enter pandas query expressions (type 'exit', 'x', 'quit' or 'q' to stop and ? for help).\n")

    keywords = ['cls', 'and', 'or'] + list(lib.database.columns)
    word_completer = FuzzyCompleter(WordCompleter(keywords, sentence=True))
    session = PromptSession(completer=word_completer)
    result = None

    while True:
        try:
            expr = session.prompt(HTML('<ansiyellow>>> </ansiyellow>')).strip()
            pipe = False
            if expr.lower() in {"exit", "x", "quit", "q"}:
                break
            elif expr == "?":
                click.echo(lib.query_help())
                click.echo(repl_help())
                continue
            elif expr == 'cls':
                # clear screen
                os.system('cls')
                continue
            elif expr.find(">") >= 0:
                # contains a pipe
                expr, pipe = expr.split('>')
                pipe = pipe.strip()
            elif expr.startswith('o'):
                # open files
                if result is None:
                    print('No existing query! Run query first')
                    continue
                # open file mode, start with o n
                try:
                    expr = int(expr[1:].strip())
                except ValueError:
                    print('Wrong syntax for open, expect o index number')
                try:
                    fname = result.loc[expr, 'file']
                    print('TODO...open ', file)
                    # os.startfile(fname)
                except KeyError:
                    print(f'Key {expr} not found.')
                except FileNotFoundError:
                    print("File does not exist.")
                except OSError as e:
                    print(f"No association or error launching: {e}")
                continue

            # if here, run query work
            result = lib.querex(expr)
            click.echo(df_to_str(result, tablefmt=tablefmt))
            click.echo(
                f'{lib._last_unrestricted:,d} unrestricted results, {len(result)} shown.')
            if pipe:
                click.echo(
                    f'Found pipe clause {pipe = } TODO: deal with this!')
        except Exception as e:
            click.echo(f"[Error] {e}")


def repl_help():
    """Help string for repl loop."""
    return """
Repl Help
=========

[select top regex order etc] > output file

* > pipe output NYI.

cls     clear screen
?       show help
x       exit

"""


@entry.command()
@click.pass_context
@click.argument("start", type=str, default='')
@click.option('-d', '--debug', is_flag=True, help='Debug mode.')
def uber(ctx, start, debug):
    """
    uber: access to all archivum functions, viz:

        upload
        new
        create-library
        query-repl

    Pass start argument to begin in that command:

        uber q[uery-repl]
    """

    # List of commands for completion
    commands = [
        # special commands
        'upload',
        'new',
        'query-repl',
        'create-library',
        "list",
        'deets',
        'cls',
        "dir", "cd", "pwd",
        # all commands
        "exit"
    ]
    dcommands = {c: None for c in commands}
    # Add a special case for `cd` to use a PathCompleter
    dcommands["cd"] = PathCompleter(only_directories=True, expanduser=True)

    # word_completer = WordCompleter(commands)
    word_completer = NestedCompleter(dcommands)
    fuzzy_completer = FuzzyCompleter(word_completer)
    session = PromptSession(completer=fuzzy_completer)

    while True:
        try:
            if start == '':
                q = session.prompt(HTML(f'{os.getcwd()} <ansired>archivum uber > </ansired>')).strip()
            else:
                q = start
                start = ''
            # process
            if q in [';', 'x', '..']:
                break
            elif q in ['?', 'h']:
                uber_help()
            elif q in ['cls']:
                clear_screen()
            elif q.startswith('cd '):
                path = q[3:].strip()
                if path:
                    try:
                        os.chdir(path)
                        # print(f"Changed directory to: {os.getcwd()}")
                    except FileNotFoundError:
                        print("Error: Directory not found.")
                continue  # Skip further processing
            else:
                # delegate
                try:
                    # per the help, prog_name is not used for much
                    sq = shlex.split(q)
                    if len(sq) == 0:
                        continue
                    if sq[0] == 'dir':
                        result = subprocess.run(
                            sq, shell=True, text=True, capture_output=True)
                        print(result.stdout)
                    elif sq[0] == 'cd':
                        try:
                            os.chdir(sq[1])
                            print(os.getcwd())
                        except FileNotFoundError:
                            print(f'{sq[1]} directory does not exist')
                    elif sq[0] in ['cwd', 'pwd']:
                        print(os.getcwd())
                    else:
                        if debug:
                            print(f'Executing {sq}')
                        entry.main(args=sq,
                            standalone_mode=False,
                            prog_name='archivum uber',
                            obj=ctx.obj)
                except SystemExit:
                    # Handle the exit signal from click without exiting the REPL
                    pass
        except KeyboardInterrupt:
            continue
        except EOFError:
            break


def uber_help():
    h = '''
Meta
====
.. ; x               quit
? h                  help
--help               Built in help (always available)

Help for Archivum Scripts
==========================
query-repl          enter query REPL loop
new                 display new PDFs in watched folders
upload              upload new pdf(s)
list                list all archivum libraries
deets               details on all archivum libraries
uber                Uber search, access to all archivum functions

General Functions
==================
cd                  change directory
cls                 clear screen
dir                 DOS dir
pwd                 print current working directory

'''
    print(h)
