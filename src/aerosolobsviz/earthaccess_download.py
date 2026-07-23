"""This script was developed from a download script used exclusively for VIIRS, which has been generalized for other products"""

import argparse
import earthaccess
from aerosolobsviz.download_utils import validate_date


def parse_arguments():
    """
    Parse command line arguments for target file(s).

    Returns:
    argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Parse earth access input data")

    parser.add_argument(
        "-p",
        "--product",
        type=str,
        required=True,
        help="Product short name",
    )
    parser.add_argument(
        "-v", "--version", type=str, required=True, help="Product version"
    )

    parser.add_argument(
        "-gs",
        "--granule-string",
        type=str,
        required=False,
        help="Granule string (fix for VIIRS 16-day running average products)",
    )

    parser.add_argument(
        "-s",
        "--start-date",
        type=validate_date,
        required=True,
        help="Start date in YYYY-MM-DD format",
    )

    parser.add_argument(
        "-e",
        "--end-date",
        type=validate_date,
        required=True,
        help="End date in YYYY-MM-DD format",
    )

    return parser.parse_args()


def setup_earthdata_auth():
    """
    Authenticate with NASA Earthdata using standard .netrc file with the host urs.earthdata.nasa.gov.
    Returns: authentication
    """
    try:
        # earthaccess will automatically use .netrc if available
        auth = earthaccess.login(strategy="netrc")
        print("Successfully authenticated Earthdata login")
        return auth
    except Exception:
        print("Check .netrc login credentials for urs.earthdata.nasa.gov")
        return None


def query_files():
    # Parse input args
    args = parse_arguments()

    # Authenticate with earthaccess
    setup_earthdata_auth()

    # Query results
    print("Querying results...")
    # Include granule_string only if optional param is set
    if args.granule_string is not None:
        results = earthaccess.search_data(
            short_name=args.product,
            version=args.version,
            granule_name=args.granule_string,
            cloud_hosted=True,
            temporal=(args.start_date, args.end_date),
        )
    else:
        results = earthaccess.search_data(
            short_name=args.product,
            version=args.version,
            cloud_hosted=True,
            temporal=(args.start_date, args.end_date),
        )

    # print(len(results))
    # print(results[0])
    if len(results) < 1:
        print("No matching results found. Check input arguments")
        return None, None

    folder_name = f"{args.product}_V{args.version}_{args.start_date}_{args.end_date}"
    return results, folder_name


def download_results(results, folder_name):
    # Make sure to not overwrite existing
    try:
        import os

        os.makedirs(folder_name, exist_ok=False)
    except FileExistsError as e:
        print(e)
        return

    # print(download_folder)
    files = earthaccess.download(results, folder_name)
    print(f"{len(files)} files downloaded to {folder_name}")


def download_earthaccess():
    results, foldername = query_files()
    if (results, foldername) != (None, None):
        download_results(results, foldername)


if __name__ == "__main__":
    download_earthaccess
