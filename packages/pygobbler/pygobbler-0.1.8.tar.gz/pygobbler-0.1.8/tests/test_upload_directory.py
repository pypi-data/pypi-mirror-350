import pygobbler as pyg
import tempfile
import os
import pytest


@pytest.fixture(scope="module")
def setup():
    _, staging, registry, url = pyg.start_gobbler()

    pyg.remove_project("test-upload", staging=staging, url=url)
    pyg.remove_project("test-more-upload", staging=staging, url=url)
    pyg.remove_project("test-upload-perms", staging=staging, url=url)
    pyg.create_project("test-upload", staging=staging, url=url)
    pyg.create_project("test-more-upload", staging=staging, url=url)
    pyg.create_project("test-upload-perms", staging=staging, url=url)

    tmp = tempfile.mkdtemp()
    with open(os.path.join(tmp, "blah.txt"), "w") as f:
        f.write("BAR")
    os.mkdir(os.path.join(tmp, "foo"))
    with open(os.path.join(tmp, "foo", "bar.txt"), "w") as f:
        f.write("1 2 3 4 5 6 7 8 9 10")

    pyg.upload_directory(
        project="test-upload", 
        asset="jennifer", 
        version="1", 
        directory=tmp,
        staging=staging, 
        url=url
    )

    return tmp


def test_upload_directory_simple(setup):
    _, staging, registry, url = pyg.start_gobbler()

    # Checking that the files were, in fact, correctly uploaded.
    man = pyg.fetch_manifest("test-upload", "jennifer", "1", registry=registry, url=url)
    assert sorted(man.keys()) == ["blah.txt", "foo/bar.txt"]
    for k, v in man.items():
        assert "link" not in v

    # Deduplication happens naturally.
    pyg.upload_directory(
        project="test-upload", 
        asset="jennifer", 
        version="2", 
        directory=setup, # i.e., the 'tmp' returned by the setup.
        staging=staging,
        url=url
    )

    man = pyg.fetch_manifest("test-upload", "jennifer", "2", registry=registry, url=url)
    assert sorted(man.keys()) == ["blah.txt", "foo/bar.txt"]
    for k, v in man.items():
        assert "link" in v


def test_upload_directory_links(setup):
    _, staging, registry, url = pyg.start_gobbler()

    dest = tempfile.mkdtemp()
    pyg.clone_version("test-upload", "jennifer", "2", dest, registry=registry)
    with open(os.path.join(dest, "whee"), "w") as f:
        f.write("BLAH")

    pyg.upload_directory(
        project="test-more-upload", 
        asset="natalie", 
        version="1", 
        directory=dest,
        staging=staging,
        url=url
    )

    man = pyg.fetch_manifest("test-more-upload", "natalie", "1", registry=registry, url=url)
    assert sorted(man.keys()) == ["blah.txt", "foo/bar.txt", "whee"]
    assert "link" in man["blah.txt"]
    assert "link" in man["foo/bar.txt"]
    assert "link" not in man["whee"]


def test_upload_directory_relative_links(setup):
    _, staging, registry, url = pyg.start_gobbler()

    dest = tempfile.mkdtemp()
    with open(os.path.join(dest, "blah.txt"), "w") as handle:
        handle.write("motto motto")
    os.symlink("blah.txt", os.path.join(dest, "whee.txt")) # relative links inside the directory are retained.
    os.mkdir(os.path.join(dest, "foo"))
    os.symlink("../whee.txt", os.path.join(dest, "foo/bar.txt")) 

    fid, outside = tempfile.mkstemp(dir=os.path.dirname(dest))
    with open(outside, "w") as handle:
        handle.write("toki wa kizuna uta")
    os.symlink(os.path.join("../../", os.path.basename(outside)), os.path.join(dest, "foo/outer.txt")) # relative links outside the directory are lost.

    pyg.upload_directory(
        project="test-more-upload", 
        asset="nicole", 
        version="1", 
        directory=dest,
        staging=staging,
        url=url
    )

    man = pyg.fetch_manifest("test-more-upload", "nicole", "1", registry=registry, url=url)
    assert sorted(man.keys()) == [ "blah.txt", "foo/bar.txt", "foo/outer.txt", "whee.txt" ]
    assert "link" in man["whee.txt"]
    assert "link" not in man["foo/outer.txt"]
    assert "link" in man["foo/bar.txt"]
    assert "link" not in man["blah.txt"]
    assert man["foo/outer.txt"]["size"] == 18
    assert man["whee.txt"]["size"] == man["foo/bar.txt"]["size"]
    assert man["whee.txt"]["size"] == man["blah.txt"]["size"]


def test_upload_directory_staging(setup):
    _, staging, registry, url = pyg.start_gobbler()

    dir = pyg.allocate_upload_directory(staging)
    with open(os.path.join(dir, "blah.txt"), "w") as f:
        f.write("A B C D E")
    os.mkdir(os.path.join(dir, "foo"))
    with open(os.path.join(dir, "foo", "bar.txt"), "w") as f:
        f.write("1 2 3 4 5 6 7 8 9 10")

    pyg.upload_directory(
        project="test-upload", 
        asset="jennifer", 
        version="3", 
        directory=dir,
        staging=staging,
        url=url
    )

    man  = pyg.fetch_manifest("test-upload", "jennifer", "3", registry=registry, url=url)
    assert sorted(man.keys()) == ["blah.txt", "foo/bar.txt"]
    assert "link" not in man["blah.txt"]
    assert "link" in man["foo/bar.txt"]


def test_upload_directory_consume(setup):
    _, staging, registry, url = pyg.start_gobbler()

    dir = pyg.allocate_upload_directory(staging)
    with open(os.path.join(dir, "blah.txt"), "w") as f:
        f.write("A B C D E")
    os.mkdir(os.path.join(dir, "foo"))
    with open(os.path.join(dir, "foo", "bar.txt"), "w") as f:
        f.write("1 2 3 4 5 6 7 8 9 10")

    pyg.upload_directory(
        project="test-upload", 
        asset="anastasia", 
        version="1", 
        directory=dir,
        staging=staging,
        url=url,
        consume=False
    )
    assert os.path.exists(os.path.join(dir, "blah.txt"))
    assert os.path.exists(os.path.join(dir, "foo/bar.txt"))

    pyg.upload_directory(
        project="test-upload", 
        asset="victoria", 
        version="1", 
        directory=dir,
        staging=staging,
        url=url,
        consume=True
    )
    assert not os.path.exists(os.path.join(dir, "blah.txt"))
    assert not os.path.exists(os.path.join(dir, "foo/bar.txt"))


def test_upload_directory_ignore_dot(setup):
    _, staging, registry, url = pyg.start_gobbler()

    dir = pyg.allocate_upload_directory(staging)
    with open(os.path.join(dir, ".blah.txt"), "w") as f:
        f.write("A B C D E")
    os.mkdir(os.path.join(dir, ".foo"))
    with open(os.path.join(dir, ".foo", "bar.txt"), "w") as f:
        f.write("1 2 3 4 5 6 7 8 9 10")

    pyg.upload_directory(
        project="test-upload", 
        asset="annabelle", 
        version="0", 
        directory=dir,
        staging=staging,
        url=url
    )
    man = pyg.fetch_manifest("test-upload", "annabelle", "0", registry=registry, url=url)
    assert len(man) == 0

    pyg.upload_directory(
        project="test-upload", 
        asset="annabelle", 
        version="1", 
        directory=dir,
        staging=staging,
        url=url,
        ignore_dot=False
    )
    man = pyg.fetch_manifest("test-upload", "annabelle", "1", registry=registry, url=url)
    assert ".blah.txt" in man
    assert ".foo/bar.txt" in man


def test_allocate_upload_directory():
    _, staging, registry, url = pyg.start_gobbler()
    assert os.path.exists(pyg.allocate_upload_directory(staging))
    assert not os.path.exists(pyg.allocate_upload_directory(staging, create=False))
