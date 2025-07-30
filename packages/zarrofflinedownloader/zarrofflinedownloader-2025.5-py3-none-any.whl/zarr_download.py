#!/usr/bin/env python3
# By MB
# Download a zarr Array / Group from a URL


def download_chunk(url: str, output: str) -> bool:
    """Download a chunk from a URL

    Args:
        url (str): ZARR chunk/file URL
        output (str): output directory

    Returns:
        bool: True if download was successful, False otherwise
    """
    import requests

    try:
        # Stream the download
        response = requests.get(url, stream=True)
        with open(output, "wb") as f:
            # 1MB chunks (bytes, kb, mb)
            for chunk in response.iter_content(chunk_size=1024 * 1024 * 1024):
                f.write(chunk)
        return True
    except requests.exceptions.RequestException as e:
        print("Error: Could not download", url)
        return False


def generate_chunk_list(chunks: tuple, shapes: tuple, offset: tuple = (), size: tuple = ()) -> list:
    """Generate a list of chunk access patterns

    Args:
        chunks (tuple): Chunksizes, e.g. (5,)
        shapes (tuple): Shape of the array, e.g. (10,)
        offset (int, optional): Offset. Defaults to 0.
        size (int, optional): Size of the chunk access pattern. Defaults to 0.

    Returns:
        list: List of chunk access patterns, e.g. [(0,), (1,), (2,), (3,), (4,)]
    """
    from math import ceil
    import itertools

    numbers = []
    if len(offset) == 0:
        offset = (0,) * len(chunks)
    if len(size) == 0:
        size = (-1,) * len(chunks)
    # iterate over the chunks
    for pos, ichunk in enumerate(chunks):
        # 1. divide the shape by the chunk size to get the number of chunks
        # 2. round down
        # 3. generate a list of numbers from 0 to the number of chunks
        # e.g. 11/5 = 2.2 -> 2 -> [0,1]
        isize = ceil(shapes[pos] / ichunk)
        if size[pos] > 0:
            # if size is given, use it to limit the number of chunks
            isize = min(isize, size[pos])
        numbers.append(range(offset[pos], offset[pos] + isize))
    # Generate the product of the chunk numbers
    # 0.0 0.1 0.2 ... 1.0 1.1 1.2
    return list(itertools.product(*numbers))


def download_zarr(
    url: str,
    output: str,
    variable: list = [],
    offset: tuple = (),
    size: tuple = (),
    netcdf: bool = False,
    overwrite: bool = False,
    verbose: bool = False,
) -> None:
    """Download a ZARR Array / Group from a URL

    Args:
        url (str): URL to download from
        output (str): Output directory to save the zarr file
        variable (list, optional): Subset of variable to download. Defaults to ''.
        offset (tuple, optional): Offset for the chunk access pattern. Defaults to ().
        size (tuple, optional): Size of the chunk access pattern. Defaults to ().
        netcdf (bool, optional): Convert to netcdf. Defaults to False.
        overwrite (bool, optional): Overwrite existing files. Defaults to False.
        verbose (bool, optional): Verbosness. Defaults to False.

    Raises:
        ValueError: no zarr metadata from URL
        JSONDecodeError: no json resonse from URL

    """
    import os
    import json
    import requests
    from tqdm.contrib.concurrent import thread_map

    if netcdf:
        # import only when necessary
        import xarray as xr

    if verbose:
        # import only when necessary
        import time
        from datetime import timedelta

    # Get the metadata (consolidated metadata for a group)
    try:
        metadata = requests.get(url + "/.zmetadata").json()
    except json.decoder.JSONDecodeError:
        raise ValueError("Error: Could not get metadata from", url)

    # Create output directories
    os.makedirs(output, exist_ok=True)
    # Write metadata
    with open(os.path.join(output, ".zmetadata"), "w") as f:
        json.dump(metadata, f, indent=2)

    # only this is relevant information
    if verbose:
        start = time.time()

    # use only the subgroup (this is where zarr keeps that information)
    # not sure about zarr 3?
    metadata = metadata["metadata"]
    download_success = False

    for key, value in metadata.items():
        if len(variable) > 0:
            if not any([jvar in key for jvar in variable]):
                continue

        print("Downloading", key)

        if "/" in key:
            name = os.path.dirname(key)
            os.makedirs(os.path.join(output, name), exist_ok=True)

        with open(os.path.join(output, key), "w") as f:
            json.dump(value, f, indent=2)

        if "zarray" in key:
            name = os.path.dirname(key)
            # generate access pattern
            # TODO: There can be an offset, e.g. 1000000 or so. How does zarr know?
            # 0 or 0.0 or 0.0.0.0
            chunks = generate_chunk_list( value["chunks"], value["shape"], offset=offset, size=size)

            # parallel download ?
            if True:
                # create argument list
                arguments = []

                def wrapper_downloader(args):
                    return download_chunk(*args)

                for ichunk in chunks:
                    chunk_url = url + "/" + name + "/" + ".".join(map(str, ichunk))
                    chunk_path = (
                        os.path.join(output, name) + "/" + ".".join(map(str, ichunk))
                    )
                    arguments.append([chunk_url, chunk_path])
                reports = thread_map(wrapper_downloader, arguments, max_workers=3)
            else:
                reports = []
                for ichunk in chunks:
                    chunk_url = url + "/" + name + "/" + ".".join(map(str, ichunk))
                    chunk_path = (
                        os.path.join(output, name) + "/" + ".".join(map(str, ichunk))
                    )
                    if verbose:
                        istart = time.time()
                    status = download_chunk(chunk_url, chunk_path)
                    if verbose:
                        print(
                            "Downloaded",
                            chunk_url,
                            "to",
                            chunk_path,
                            "in",
                            timedelta(seconds=time.time() - istart),
                        )
                    reports.append(status)

            if all(reports):
                print("Downloaded", key)
                download_success = True
            else:
                print("Error: Could not download", key)
                download_success = False

    if download_success:
        if netcdf:
            # convert to netcdf
            ds = xr.open_zarr(output)
            # save to netcdf
            if overwrite:
                os.remove(os.path.join(output, "output.nc"))
                print("Removed existing netcdf file")
            ds.to_netcdf(os.path.join(output, "output.nc"), mode="w")
            print("Converted to netcdf:", os.path.join(output, "output.nc"))

    if verbose:
        print("Downloaded all chunks in", timedelta(seconds=time.time() - start))


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Download a zarr Array / Group from a URL"
    )
    parser.add_argument("url", type=str, help="URL to download from")
    parser.add_argument(
        "output", type=str, help="Output directory to save the zarr file"
    )
    parser.add_argument(
        "--variable",
        type=str,
        help="Subset of variables to download. e.g. t2m,lon,lat,... ",
    )
    parser.add_argument(
        "--offset", type=str, default="", help="Offset for the chunk access pattern"
    )
    parser.add_argument(
        "--size", type=str, default="", help="Size of the chunk access pattern")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument(
        "--to-netcdf", dest="netcdf", action="store_true", help="Convert to netcdf"
    )
    parser.add_argument(
        "--overwrite", "-o", action="store_true", help="Overwrite existing files"
    )
    args = parser.parse_args()

    if args.variable:
        # split by comma into list
        args.variable = args.variable.split(",")
        # print(args.variable)
    else:
        args.variable = []

    if args.offset:
        # split by comma into tuple
        args.offset = tuple(map(int, args.offset.split(",")))

    if args.size:
        # split by comma into tuple
        args.size = tuple(map(int, args.size.split(",")))

    download_zarr(**vars(args))


if __name__ == "__main__":
    main()
