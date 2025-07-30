from typing import Dict
import json
from cc_clients_python_lib.http_status import HttpStatus


__copyright__  = "Copyright (c) 2025 Jeffrey Jonathan Jennings"
__license__    = "MIT"
__credits__    = ["Jeffrey Jonathan Jennings (J3)"]
__maintainer__ = "Jeffrey Jonathan Jennings (J3)"
__email__      = "j3@thej3.com"
__status__     = "dev"


def aws_lambda_function_return_json_object(logger, status_code: int, body: str) -> Dict[int, str]:
    """This method logs the body message and constructs AWS Lambda Function the JSON object.
 
    Arg(s):
        status_code (int):  The HTTP Status Code.
        body (str)       :  The body message.
 
    Returns:
        str:  The AWS Lambda Function JSON object.
    """
    if status_code == HttpStatus.OK:
        logger.info(body)
        key = "message"
    else:
        logger.error(body)
        key = "error"
   
    return {
        'statusCode': status_code,
        'body': json.dumps({key: body})
    }