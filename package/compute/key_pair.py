# -*- coding: utf-8 -*-

"""Module deleting all keypairs."""

import logging

import boto3

from botocore.exceptions import ClientError


def nuke_all_key_pair():
    """Keypair deleting function.

    Deleting all Keypair
    """
    # Define connection
    ec2 = boto3.client("ec2")

    # List all ec2 keypair
    ec2_keypair_list = ec2_list_keypair()

    # Nuke all ec2 keypairs
    for keypair in ec2_keypair_list:

        # Delete ec2 key pair
        try:
            ec2.delete_key_pair(KeyName=keypair)
            print("Nuke Key Pair {0}".format(keypair))
        except ClientError as e:
            logging.error("Unexpected error: %s", e)


def ec2_list_keypair():
    """Keypair list function.

    List the names of all Keypair

    :returns:
        List of Keypair names
    :rtype:
        [str]
    """
    # Define the connection
    ec2 = boto3.client("ec2")
    response = ec2.describe_key_pairs()

    # Initialize ec2 keypair list
    ec2_keypair_list = []

    # Retrieve all ec2 keypairs
    for keypair in response["KeyPairs"]:

        ec2_keypair = keypair["KeyName"]
        ec2_keypair_list.insert(0, ec2_keypair)

    return ec2_keypair_list
