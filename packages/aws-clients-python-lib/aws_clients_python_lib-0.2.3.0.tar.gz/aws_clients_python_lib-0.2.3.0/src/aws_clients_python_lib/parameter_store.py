from typing import Tuple, Dict
import boto3
from botocore.exceptions import ClientError


__copyright__  = "Copyright (c) 2025 Jeffrey Jonathan Jennings"
__license__    = "MIT"
__credits__    = ["Jeffrey Jonathan Jennings (J3)"]
__maintainer__ = "Jeffrey Jonathan Jennings (J3)"
__email__      = "j3@thej3.com"
__status__     = "dev"


def get_parameters(aws_region_name: str, parameter_path: str) -> Tuple[Dict[str, str], str]:
    """This method retrieves the parameteres from the System Manager Parameter Store.
    
    Arg(s):
        aws_region_name (str):  The AWS region.
        parameter_path (str):   The hierarchy for the parameter.  Hierarchies start with a 
                                forward slash (/). The hierarchy is the parameter name except the 
                                last part of the parameter.  For the API call to succeed, the last
                                part of the parameter name can't be in the path. A parameter name
                                hierarchy can have a maximum of 15 levels.
        
    Return(s):
        parameters (dict): Goes throught recursively and returns all the parameters within a hierarchy.
    """
    try:
        client = boto3.session.Session().client(service_name='ssm', region_name=aws_region_name)    
        response = client.get_parameters_by_path(Path=parameter_path, Recursive=False, WithDecryption=True)
        parameters = { param['Name'].split('/')[-1]: param['Value'] for param in response.get('Parameters', []) }
        return parameters, ""
    except ClientError as e:
        return {}, f"ClientError with ({parameter_path}) from the AWS Systems Manager Parameter Store because of {e}."