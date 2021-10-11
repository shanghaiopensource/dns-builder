#!/usr/bin/env python

"""
This script reads the apt cache and writes in-toto material provenance
to stdout in JSON format or argv[1] when provided.
"""

from __future__ import print_function
import apt.cache
import json
import sys

cache = apt.cache.Cache()
in_toto_data = list()

for pkg_name in cache.keys():
    pkg = cache[pkg_name]
    if not pkg.is_installed:
        continue

    in_toto_data.append(
        {
            "uri": "pkg:deb/{origin}/{name}@{version}?arch={arch}".format(
                origin=pkg.installed.origins[0].origin,
                name=pkg.shortname,
                version=pkg.installed.version,
                arch=pkg.installed.architecture
            ),
            "digest": {
                "sha256": pkg.installed.sha256
            }
        }
    )

if len(sys.argv) > 1:
    with open(sys.argv[1], 'w') as f:
        json.dump(in_toto_data, f)
else:
    print(json.dumps(in_toto_data))
