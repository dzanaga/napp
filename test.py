import os
import shutil

import pytest
from napp import get_file_paths, cp
import click
from click.testing import CliRunner

TESTDATA = '/tmp/napptests/'


@pytest.fixture
def testdata():
    testdata = TESTDATA
    yield testdata
    if os.path.isdir(testdata):
        shutil.rmtree(testdata)


def test_get_file_paths1(testdata):
    src = '/src/im.jpg'
    dst = testdata + "dst/"

    s, d = get_file_paths(src, dst)
    shutil.rmtree(dst)

    assert s == '/src/im.jpg'
    assert d == testdata + "dst/im.jpg"


def test_get_file_paths2(testdata):
    src = '/src/im.jpg'
    dst = testdata + 'dst'

    s, d = get_file_paths(src, dst)

    assert s == '/src/im.jpg'
    assert d == testdata + "dst"


def test_get_file_paths3(testdata):
    src = '/src/im.jpg'
    dst = 'dst/'
    cwd = os.getcwd()

    s, d = get_file_paths(src, dst)
    shutil.rmtree(dst)

    assert s == '/src/im.jpg'
    assert d == os.path.join(cwd, 'dst', 'im.jpg')


def test_get_file_paths4(testdata):
    src = '/src/im.jpg'
    dst = 'dst'
    cwd = os.getcwd()

    s, d = get_file_paths(src, dst)

    assert s == '/src/im.jpg'
    assert d == os.path.join(cwd, 'dst')


def test_get_file_paths5(testdata):
    src = '/src/im.jpg'
    dst = testdata + 'dst'
    os.makedirs(dst)

    with pytest.raises(FileExistsError):
        s, d = get_file_paths(src, dst)


def test_cp_file1(testdata):

    src = os.path.join(testdata, 'im.jpg')
    dst = os.path.join(testdata, 'dst/')

    os.makedirs(testdata)
    with open(src, 'w') as f:
        f.write('testing')

    runner = CliRunner()
    result = runner.invoke(cp, [src, dst])

    assert result.exit_code == 0
    assert os.path.isfile(src)
    assert os.path.isfile(os.path.join(dst, 'im.jpg'))
