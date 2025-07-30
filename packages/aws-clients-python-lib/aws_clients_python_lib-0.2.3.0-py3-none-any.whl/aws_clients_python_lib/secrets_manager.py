from typing import Tuple, Dict
import boto3
from botocore.exceptions import ClientError
import json


__copyright__  = "Copyright (c) 2025 Jeffrey Jonathan Jennings"
__credits__    = ["Jeffrey Jonathan Jennings"]
__license__    = "MIT"
__maintainer__ = "Jeffrey Jonathan Jennings"
__email__      = "j3@thej3.com"
__status__     = "dev"


def get_secrets(aws_region_name: str, secrets_name: str) -> Tuple[Dict[str, str], str]:
    """This method retrieve secrets from the AWS Secrets Manager.
   
    Arg(s):
        aws_region_name (str):  The AWS region.
        secrets_name (str):     Thehe name of the secrets you want the secrets for.
       
    Returns:
        Dict:  If successful, the secrets in a dict.  Otherwise, returns an empty dict.
        str:   If method fails, the error message is returned.  Otherwise, empty string
               is returned.
    """    
    try:
        aws_secrets_manager = boto3.session.Session().client(service_name='secretsmanager', region_name=aws_region_name)    
        get_secret_value_response = aws_secrets_manager.get_secret_value(SecretId=secrets_name)
        return json.loads(get_secret_value_response['SecretString']), ""
    except KeyError as e:
        return {}, f"KeyError with ({secrets_name}) from the AWS Secrets Manager because of {e}."    
    except ClientError as e:
        return {}, f"ClientError with ({secrets_name}) from the AWS Secrets Manager because of {e}."