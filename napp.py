import os
import sys
import glob
import shutil

import click


def get_files(folder, pattern='*'):
    """
    Return generator of files matching pattern
    """
    return glob.iglob(os.path.join(folder, '**', '*'), recursive=True)


@click.group()
@click.version_option('1.0')
@click.pass_context
def cli(ctx):
    pass


@cli.command(short_help='Copies files.')
@click.argument('src', nargs=1, type=click.Path())
@click.argument('dst', nargs=1, type=click.Path())
@click.option('--overwrite/--no-overwrite', default=True,
              help='Overwrite existing files')
@click.option('--match', '-m', type=str, default='*',
              help='Files matching pattern.')
@click.option('--verbose', '-v', is_flag=True,
              help='Print operation info.')
def cp(src, dst, overwrite=True, match='*', verbose=False):
    """Copies one or multiple files to a new location.  This copies all
    files from SRC to DST.
    """

    if dst[-1] in ['/', '\\']:
        pass

    if os.path.isfile(src):
        src, dst = get_file_paths(src, dst)
        shutil.copy2(src, dst)
        return None

    filenames = get_files(src)
    for fn in filenames:
        click.echo('Copy from %s -> %s' % (fn, dst))


def get_file_paths(src, dst):
    cwd = os.getcwd()
    src_abs = os.path.abspath(src)
    dst_abs = os.path.abspath(dst)

    if dst[-1] in ['/', '\\']:
        os.makedirs(dst, exist_ok=True)
        dst = os.path.join(dst_abs, os.path.basename(src))
    else:
        if os.path.isdir(dst_abs):
            print(dst_abs)
            print(os.path.exists(dst_abs))
            raise FileExistsError("Destination file is a folder.")
        dst = dst_abs

    src = src_abs

    return src, dst
