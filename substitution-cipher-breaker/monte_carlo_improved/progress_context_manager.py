from contextlib import contextmanager
import time


@contextmanager
def progress(s: str):
    print(f'{s}... ', end='')
    start = time.time()

    try:
        yield
    except:
        print_result('❌', start, time.time())

        raise

    print_result('✅', start, time.time())


def print_result(icon: str, start, end):
    print(f'{icon} ({end - start:.2f}s)')
