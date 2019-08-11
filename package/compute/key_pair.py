# -*- coding: utf-8 -*-

"""Module deleting all keypairs."""

import logging

import boto3

from botocore.exceptions import ClientError


def nuke_all_key_pair():
    """Keypair deleting function.

    Deleting all Keypair
    """
    ec2 = boto3.client("ec2")

    for keypair in ec2_list_keypair():
        try:
            ec2.delete_key_pair(KeyName=keypair)
            print("Nuke Key Pair {0}".format(keypair))
        except ClientError as e:
            logging.error("Unexpected error: %s", e)


def ec2_list_keypair():
    """Keypair list function."""
    ec2_keypair_list = []
    ec2 = boto3.client("ec2")
    response = ec2.describe_key_pairs()

    for keypair in response["KeyPairs"]:
        ec2_keypair_list.append(keypair["KeyName"])
    return ec2_keypair_list
