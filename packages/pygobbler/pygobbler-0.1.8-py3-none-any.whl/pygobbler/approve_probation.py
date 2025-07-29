from . import _utils as ut


def approve_probation(project: str, asset: str, version: str, staging: str, url: str):
    """
    Approve a probational upload of a version of a project's asset.

    Args:
        project:
            The name of the project.

        asset:
            The name of the asset of the ``project``.

        version:
            The name of the version of the ``asset`` to approve.

        staging:
            Path to the staging directory.

        url:
            URL to the Gobbler REST API.
    """
    ut.dump_request(staging, url, "approve_probation", { "project": project, "asset": asset, "version": version })
