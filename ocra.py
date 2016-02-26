#!/usr/bin/env python2
import shutil
import tempfile

if __name__ == "__main__":
    temp_dir = tempfile.mkdtemp(prefix="ocra_tmp")
    try:
        pass

    finally:
        shutil.rmtree(temp_dir)
