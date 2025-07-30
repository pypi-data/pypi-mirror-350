=====================
**aws-authenticator**
=====================

Overview
--------

Login to AWS using CLI named profiles, IAM access key credentials, or SSO.

Prerequisites
-------------

- *Python >= 3.10*
- *aws-ssooidc (https://pypi.org/project/aws-ssooidc/) >= 2021.1.1.1*
- *boto3 (https://pypi.org/project/boto3/) >= 1.17.78*

Conditional Arguments
---------------------

If authenticating with named profiles:

- AWSCLI profile name

If authenticating with IAM acccess key credentials:

- AWS access key id
- AWS secret access key
- AWS session token (optional, if using temporary credentials)

If authenticating with SSO:

- AWS account ID
- AWS SSO Permission Set (role) name
- AWS SSO login URL

Additional argument:

- AWS region (optional)

Usage
-----

Installation:

.. code-block:: BASH

   pip3 install aws-authenticator
   # or
   python3 -m pip install aws-authenticator

In Python3 authenticating with default profile:

.. code-block:: PYTHON

   import aws_authenticator

   auth = aws_authenticator.AWSAuthenticator()
   session = auth.profile()
   client = session.client("<service-name>")

In Python3 authenticating with named profiles:

.. code-block:: PYTHON

   import aws_authenticator

   auth = aws_authenticator.AWSAuthenticator(
      profile_name="<profile-name>"
   )
   session = auth.profile()
   client = session.client("<service-name>")

In Python3 authenticating with IAM access key credentials:

.. code-block:: PYTHON

   import aws_authenticator

   auth = aws_authenticator.AWSAuthenticator(
      access_key_id="<access-key-id>",
      secret_access_key="<secret-access-key>",
      session_token="<session-token>"
   )
   session = auth.iam()
   client = session.client("<service-name>")

In Python3 authenticating with SSO:

.. code-block:: PYTHON

   import aws_authenticator

   auth = aws_authenticator.AWSAuthenticator(
      sso_url="<sso-url>",
      sso_role_name="<sso-role-name>",
      sso_account_id="<sso-account-id>",
      region_name="<region-name>"
   )
   session = auth.sso()
   client = session.client("<service-name>")

Testing Examples
----------------

Testing SSO-based login in Python3:

.. code-block:: PYTHON

   import aws_authenticator

   auth = aws_authenticator.AWSAuthenticator(
      sso_url="<sso-url>",
      sso_role_name="<sso-role-name>",
      sso_account_id="<sso-account-id>"
   )
   session = auth.sso()
   client = session.client("sts")

   response = client.get_caller_identity()
   print(response)

Testing profile-based login as a script in BASH:

.. code-block:: BASH

   python [/path/to/]aws_authenticator \
   -m profile \
   -p <profile-name>
