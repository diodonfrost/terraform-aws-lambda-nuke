# -*- coding: utf-8 -*-

"""Exception function for aws nuke."""

import logging


def nuke_exceptions(resource_name, resource_id, exception):
    """Exception raised during execution of compute nuke.

    Log aws nuke compute exception on the specific aws resources.

    :param str resource_name:
        Aws resource name
    :param str resource_id:
        Aws resource id
    :param str exception:
        Human readable string describing the exception
    """
    info_error_codes = [
        "CannotDelete",
        "DependencyViolation",
        "InvalidVolume",
        "InvalidCacheClusterState",
        "InvalidSnapshotState",
        "InvalidCacheSubnetState",
        "InvalidParameterValue",
        "InvalidCacheParameterGroupState",
        "ServiceLinkedRoleNotFoundFault",
        "RequestLimitExceeded",
        "InvalidPermission.NotFound",
        "VolumeInUse",
    ]
    warning_error_codes = [
        "OperationNotPermitted",
        "ResourceInUse",
        "InvalidDBInstanceState",
        "InvalidDBClusterStateFault",
        "InvalidClusterStateFault",
        "InvalidClusterSnapshotStateFault",
        "InvalidClusterSubnetGroupStateFault",
        "InvalidClusterParameterGroupStateFault",
        "AccessDenied",
    ]

    if exception.response["Error"]["Code"] in info_error_codes:
        logging.info(
            "%s %s: %s", resource_name, resource_id, exception,
        )
    elif exception.response["Error"]["Code"] in warning_error_codes:
        logging.warning(
            "%s %s: %s", resource_name, resource_id, exception,
        )
    else:
        logging.error(
            "Unexpected error on %s %s: %s",
            resource_name,
            resource_id,
            exception,
        )
