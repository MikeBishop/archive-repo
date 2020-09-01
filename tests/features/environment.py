from behave import *
from contextlib import contextmanager
import tempfile


@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


def before_all(context):
    context.tempdir = tempfile.TemporaryDirectory()
