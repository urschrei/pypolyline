#!/usr/bin/env python
"""
release.py
Retrieve latest compressed wheels from GitHub


Created by Stephan Hügel on 2016-06-19
"""

import io
import tarfile
import zipfile
import requests
from subprocess import check_output
from multiprocessing import Pool

path = "dist/"
url = "https://github.com/urschrei/pypolyline/releases/download/{tag}/pypolyline-{tag}-{target}.{extension}"
# url = "https://github.com/urschrei/pypolyline/releases/download/{tag}/pypolyline-{tag}-{target}.{extension}"
# get latest tag
tag = check_output(["git", "describe", "--abbrev=0"]).strip().decode("utf-8")

releases = [
    {"tag": tag, "target": "x86_64-apple-darwin-cp36", "extension": "tar.gz"},
    {"tag": tag, "target": "x86_64-apple-darwin-cp37", "extension": "tar.gz"},
    {"tag": tag, "target": "x86_64-apple-darwin-cp38", "extension": "tar.gz"},
    {"tag": tag, "target": "x86_64-apple-darwin-cp39", "extension": "tar.gz"},
    {"tag": tag, "target": "x86_64-unknown-linux-gnu", "extension": "tar.gz"},
    {"tag": tag, "target": "x86_64-pc-windows-msvc-cp27", "extension": "zip"},
    {"tag": tag, "target": "x86_64-pc-windows-msvc-cp36", "extension": "zip"},
    {"tag": tag, "target": "i686-pc-windows-msvc-cp27", "extension": "zip"},
    {"tag": tag, "target": "i686-pc-windows-msvc-cp36", "extension": "zip"},
]


def retrieve(url):
    sess = requests.Session()
    retrieved = sess.get(url, stream=True)
    # don't continue if something's wrong
    retrieved.raise_for_status()
    try:
        raw_zip = zipfile.ZipFile(io.BytesIO(retrieved.content))
        raw_zip.extractall(path)
    except zipfile.BadZipfile:
        # it's a tar
        tar = tarfile.open(mode="r:gz", fileobj=io.BytesIO(retrieved.content))
        tar.extractall(path)

if __name__ == "__main__":
    # main()
    urls = (url.format(**release) for release in releases)

    # let's do this in parallel
    pool = Pool()
    # we could use map, but it consumes the entire iterable (doesn't matter for small n)
    res = pool.map_async(retrieve, urls)
    # need these if we use _async
    pool.close()
    pool.join()
