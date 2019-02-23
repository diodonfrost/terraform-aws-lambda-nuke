
"""This script nuke all elasticbeanstalk resources"""

import time
import boto3

ELASTICBEANSTALK = boto3.client('elasticbeanstalk')

def nuke_all_elasticbeanstalk(older_than_seconds, logger):
    """
         elasticbeanstalk function for nuke all
         elasticbeanstalk stack
    """

    #### Nuke all elasticbeanstalk application ####
    response = ELASTICBEANSTALK.describe_applications()
    time_delete = time.time() - older_than_seconds

    for application in response['Applications']:

        if application['DateCreated'].timestamp() < time_delete:

            # Nuke all elasticbeanstalk application
            ELASTICBEANSTALK.delete_application(ApplicationName=\
            application['ApplicationName'], TerminateEnvByForce=True)
            logger.info("Nuke elasticbeanstalk application %s", application['ApplicationName'])
