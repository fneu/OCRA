import os
import subprocess


def pdf_to_tiff(source_pdf_list, destination, dpi=300):
    """
    Most libraries cannot work on PDFs, we therefore need these.
    Tiff files will keep the file basename but receive a'.tif' extension.

    :param source_pdf_list: List of PDFs to convert
    :param destination:     Destination dir for tiff files
    :param dpi:             dpi of the scanned PDFs
    :return:                list of converted files
    """
    new_file_names = []

    for file_name in source_pdf_list:
        file_basename = os.path.basename(os.path.splitext(file_name)[0])
        new_file_name = os.path.join(destination, file_basename)

        ret_val = subprocess.call(["pdftoppm", "-f", "1", "-singlefile",
                                   "-tiff", "-r", str(dpi),
                                   file_name, new_file_name])

        if ret_val == 0:  # conversion completed successfully
            new_file_names.append(new_file_name + ".tif")

    return new_file_names
