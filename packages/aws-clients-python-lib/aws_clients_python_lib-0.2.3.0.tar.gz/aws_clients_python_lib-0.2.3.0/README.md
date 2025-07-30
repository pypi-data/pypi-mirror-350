# AWS Clients Python Library
This library is a collection of client helper functions that I have found useful when working with AWS services. The library is written in Python and is intended to be used in Python projects. The library is not intended to be a comprehensive library for all AWS services, but rather a collection of helper functions that I have found useful when working with AWS services.

The library includes support for:
+ **Lambda**
+ **Secrets Manager**
+ **Systems Manager Parameter Store**

> **Note:** _This library is in active development and is subject to change.  It covers only the methods I have needed so far.  If you need a method that is not covered, please feel free to open an issue or submit a pull request._

**Table of Contents**

<!-- toc -->
- [**1.0 Library Client Helpers**](#10-library-client-helpers)
    * [**1.1 Lambda**](#11-lambda)
    * [**1.2 Secrets Manager**](#12-secrets-manager)
    * [**1.3 Systems Manager Parameter Store**](#13-systems-manager-parameter-store)
- [**2.0 Installation**](#20-installation)
+ [**3.0 Resources**](#30-resources)
    * [**3.1 AWS Service Documentation**](#31-aws-service-documentation)
<!-- tocstop -->

## **1.0 Library Client Helpers**

### **1.1 Lambda**
The following method is provided:
- `aws_lambda_function_return_json_object`

### **1.2 Secrets Manager**
The following method is provided:
- `get_secrets`

### **1.3 Systems Manager Parameter Store**
The following method is provided:
- `get_parameters`

## **2.0 Installation**
Install the AWS Clients Python Library using **`pip`**:
```bash
pip install aws-clients-python-lib
```

Or, using [**`uv`**](https://docs.astral.sh/uv/):
```bash
uv add aws-clients-python-lib
```

## **3.0 Resources**

### **3.1 AWS Service Documentation**
* [AWS Lambda](https://docs.aws.amazon.com/lambda/)
* [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/)
* [AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)