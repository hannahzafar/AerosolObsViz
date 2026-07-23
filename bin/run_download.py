#!/usr/bin/env python3

import argparse
from aerosolobsviz.eodag_download import download_eodag
from aerosolobsviz.earthaccess_download import download_earthaccess

# apis = ["eodag", "earthaccess"]
# def parse_args():
#     parser = argparse.ArgumentParser("Parse download api and input args")
#     parser.add_argument("--api",
#                         type=str,
#                         required=True,
#                         choices=apis,
#                         help="API specific to data")

# download_eodag()
download_earthaccess()
