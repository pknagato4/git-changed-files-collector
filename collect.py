#!/usr/bin/env python3

import sys
import pygit2
import tarfile
from datetime import date

repo = None
try:
    repo = pygit2.Repository('.')
    print("Found repo at {}".format(repo.path))
except:
    print("No repository in current dir")
    exit(1)

files=[]

master_oid = pygit2.Oid(hex = repo.head.peel().hex)
today = date.today()
with tarfile.open("taxbreak{}-{}.tar.gz".format(today.year, today.month), "w:gz") as tar:
    for commit_hash in sys.argv[1:]:
        commit = repo.revparse_single(commit_hash)
        repo.checkout_tree(commit)

        diff = repo.diff(commit_hash + '~1', commit_hash)

        for delta in diff.deltas:
            path = delta.old_file.path
            tar.add(path, arcname=path + '.' + commit_hash[:9])
            files.append(path)
        repo.reset(master_oid, pygit2.GIT_RESET_HARD)
files = set(files)
print("Found {} files".format(len(files)))
