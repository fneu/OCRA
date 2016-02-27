#!/usr/bin/env python2
import CliParsing
import Converting
import Cutting
import shutil
import tempfile

if __name__ == "__main__":
    temp_dir = tempfile.mkdtemp(prefix="ocra_tmp")
    try:
        args = CliParsing.cli_args()
        file_list = Converting.pdf_to_tiff(args['f'], temp_dir)

        for file_name in file_list:
            crops = Cutting.crop_lines(file_name)
    finally:
        shutil.rmtree(temp_dir)
