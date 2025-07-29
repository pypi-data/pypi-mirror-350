from typing import Optional
import os
from . import allocate_upload_directory
from . import _utils as ut


def upload_directory(project: str, asset: str, version: str, directory: str, staging: str, url: str, probation: bool = False, consume: Optional[bool] = None, ignore_dot: bool = True):
    """
    Upload a directory as a new versioned asset of a project in the registry.

    Args:
        project:
            The name of an existing project.

        asset:
            The name of a new or existing asset in ``project``.

        version:
            The name of a new version of ``asset``.

        directory:
            Path to a directory to be uploaded. For best performace, this
            should be a subdirectory of ``staging``, e.g., as created by
            :py:func:`~.allocate_upload_directory`.

        staging:
            Path to the staging directory.

        url:
            URL for the Gobbler REST API.

        probation:
            Whether to upload a probational version.
    
        consume:
            Whether the contents of ``directory`` can be consumed by the upload process.
            If true, the Gobbler will attempt to move files from ``directory`` into the registry.
            Otherwise, the contents of ``directory`` will not be modified by the upload.
            Defaults to true if the contents of ``directory`` need to be copied to ``staging``.

        ignore_dot:
            Whether to skip dotfiles in ``directory`` during upload.
    """
    # Normalizing them so that they're comparable, in order to figure out whether 'directory' lies inside 'staging'.
    directory = os.path.normpath(directory)
    staging = os.path.normpath(staging)

    in_staging = False
    tmpd = directory
    while len(tmpd) > len(staging):
        tmpd = os.path.dirname(tmpd)
        if tmpd == staging:
            in_staging = True
            break

    purge_newdir = False 
    try:
        if not in_staging:
            newdir = allocate_upload_directory(staging) 

            # If we're copying everything to our own staging directory, we can
            # delete it afterwards without affecting the user. We do this
            # clean-up to free up storage in the staging space.
            purge_newdir = True 

            for root, dirs, files in os.walk(directory):
                for f in files:
                    src = os.path.join(root, f)
                    rel = os.path.relpath(src, directory)
                    dest = os.path.join(newdir, rel)
                    os.makedirs(os.path.dirname(dest), exist_ok=True)

                    slink = ""
                    if os.path.islink(src):
                        slink = os.readlink(src)

                    if slink == "":
                        _link_or_copy(src, dest)
                    elif _is_absolute_or_local_link(slink, rel):
                        os.symlink(slink, dest)
                    else:
                        full_src = os.path.normpath(os.path.join(os.path.dirname(src), slink))
                        _link_or_copy(full_src, dest)

            directory = newdir

        if consume is None:
            # If we copied everything over to our own staging directory, we're entitled to consume its contents.
            consume = not in_staging

        req = {
            "source": os.path.basename(directory),
            "project": project,
            "asset": asset,
            "version": version,
            "on_probation": probation,
            "consume": consume,
            "ignore_dot": ignore_dot
        }
        ut.dump_request(staging, url, "upload", req)
        return

    finally:
        if purge_newdir:
            import shutil
            shutil.rmtree(newdir)


def _is_absolute_or_local_link(target: str, link_path: str) -> bool:
    if os.path.isabs(target):
        return True

    # Both 'target' and 'link_path' should be relative at this point, so the
    # idea is to check whether 'os.path.join(os.path.dirname(link_path),
    # target)' is still a child of 'os.path.dirname(link_path)'.
    pre_length = len(link_path.split("/")) - 1
    post_fragments = target.split("/")[:-1]

    for x in post_fragments:
        if x == ".":
            continue
        elif x == "..":
            pre_length -= 1
            if pre_length < 0:
                return False
        else:
            pre_length += 1

    return True


def _link_or_copy(src: str, dest: str):
    try:
        os.link(src, dest)
    except:
        import shutil
        shutil.copy(src, dest)
