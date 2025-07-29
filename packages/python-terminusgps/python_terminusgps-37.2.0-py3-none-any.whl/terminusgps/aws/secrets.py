import json

import boto3


def get_secret(name: str, region: str = "us-east-1") -> dict[str, str]:
    """
    Logs into the default AWS CLI session and returns a secret value.

    :param name: An AWS `secretsmanager <https://docs.aws.amazon.com/secretsmanager/>`_ name.
    :type name: :py:obj:`str`
    :param region: An AWS region name. Default is :py:obj:`"us-east-1"`.
    :type region: :py:obj:`str`
    :returns: A secret value dictionary.
    :rtype: :py:obj:`dict`

    """
    client = boto3.Session().client(service_name="secretsmanager", region_name=region)
    secret = client.get_secret_value(SecretId=name)["SecretString"]
    return json.loads(secret)
