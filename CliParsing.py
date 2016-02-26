import argparse


def default_arg_parser():
    """
    This function creates an ArgParser to parse command line arguments.
    """
    arg_parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog="OCRA",
        description="""
                O          .
             O            ' '
               o         '   .
             o         .'
          __________.-'       '...___
       .-'     .-. .-. .-. .-.  ###  '''...__
      /   a### | | |   |(  |-| ##            ''--.._ ______
      '.       `-' `-' ' ' ` '#     ########        '   .-'
        '-._          ..**********####  ___...---'''\   '
            '-._     __________...---'''             \   l
                \   |                                 '._|
                 \__;

OCRA is a specialised OCR Application that uses computer vision and various
open ocr engines to extract text from scans with a low readability.""")

    arg_parser.add_argument('-f',
                            nargs='+',
                            metavar='FILE',
                            help='PDF files to be read (supports unix globs)')

    arg_parser.add_argument('-o',
                            metavar='FILE',
                            help='CSV output file name')

    arg_parser.add_argument('-e',
                            nargs='+',
                            choices=('tesseract', 'cuneiform',
                                     'gocr', 'ocrad'),
                            metavar='ENGINE',
                            help='OCR engines to be used. Choices: '
                                 '(tesseract, cuneiform, gocr, ocrad)')

    arg_parser.add_argument('-v',
                            action='store_true',
                            help='give verbose output')

    return arg_parser


def cli_args():
    arg_parser = default_arg_parser()
    args = arg_parser.parse_args()
    return args
