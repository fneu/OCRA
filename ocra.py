#!/usr/bin/env python2
import CliParsing
import Converting
import shutil
import tempfile

if __name__ == "__main__":
    temp_dir = tempfile.mkdtemp(prefix="ocra_tmp")
    try:
        args = CliParsing.cli_args()
        file_list = Converting.pdf_to_tiff(args['f'], temp_dir)

    finally:
        shutil.rmtree(temp_dir)
