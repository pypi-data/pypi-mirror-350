===================
**aws_tgw_details**
===================

Overview
--------

Get AWS Transit Gateway details.

.. image:: https://gitlab.com/fer1035_python/modules/pypi-aws_tgw_details/-/raw/main/images/workflow.png
   :alt: Workflow diagram

This module helps to retrieve AWS Transit Gateway details, including the following:

- Transit Gateways
- Transit Gateway Route Tables
- Transit Gateway Routes
- Transit Gateway Attachments
- Customer Gateways
- VPN Connections

The *aws_authenticator* module is installed with this module, and is used to login to AWS using IAM access key credentials from the following environment variables:

- TGW_AWS_ACCESS_KEY_ID
- TGW_AWS_SECRET_ACCESS_KEY
- TGW_AWS_SESSION_TOKEN (Optional. Default: *None*.)

If the environment variables are not set, the module will try to use the default AWS credentials from the AWS CLI configuration file.

Usage
------

- Installation:

.. code-block:: BASH

   pip3 install aws_tgw_details
   # or
   python3 -m pip install aws_tgw_details

- Set environment variables:

.. code-block:: BASH

   export TGW_AWS_ACCESS_KEY_ID=your_access_key_id
   export TGW_AWS_SECRET_ACCESS_KEY=your_secret_access_key
   export TGW_AWS_SESSION_TOKEN=your_session_token

- Examples:

.. code-block:: BASH

   # Overview.
   aws_tgws

   # Help.
   aws_tgws -h

   # Get all Transit Gateways.
   aws_tgws -t ALL

   # Get a specific Transit Gateway.
   aws_tgws -t tgw-1234567890abcdef0

   # Get all Customer Gateways.
   aws_tgws -c ALL

You can also use the available functions independently to create your own workflow instead of using the installed *aws_tgws* command line tool.

Options
-------

.. code-block:: BASH

   -h, --help           show this help message and exit
   -V, --version        show program's version number and exit
   -t, --tgw_id [TGW_ID]
                        Transit Gateway ID. Use 'ALL' to get all TGWs. Default: None.
   -y, --tgw_only       Transit Gateway details only, no other components.
   -r, --tgw_rt_id [TGW_RT_ID]
                        Transit Gateway Route Table ID. Default: None.
   -a, --tgw_attachment_id [TGW_ATTACHMENT_ID]
                        Transit Gateway Attachment ID. Default: None.
   -v, --tgw_vpn_connection_id [TGW_VPN_CONNECTION_ID]
                        VPN Connection ID. Use 'ALL' to get all connections. Default: None.
   -c, --cgw_id [CGW_ID]
                        Customer Gateway ID. Use 'ALL' to get all CGWs. Default: None.
   -w, --region [REGION]
                        AWS Region. Default: us-east-1.
   -l, --log_path [LOG_PATH]
                        Log file path. Default: /tmp.
   -e, --log_level [{NONE,DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                        Log level. Default: INFO.
   -o, --output_file [OUTPUT_FILE]
                        Output file and path. Default: ./transit_gateway_details.json

Output
------

The output is in the JSON format. Additionally, the output for the full Transit Gateway details will also be written to file. You can customize the output path and file name using the *-o* option. More details in help.

Logging
-------

The module creates logs in the */tmp* directory with the *<application_name>.<utc_date_and_time>.log* file name format. This can be customized or disabled by setting the *-l* and *-e* options. More details in help.

Boto3 Functions
---------------

- Main Documentation
   - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html
   - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/export_transit_gateway_routes.html
- Transit Gateway
   - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTransitGateways.html
   - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTransitGatewayAttachments.html
   - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTransitGatewayVpcAttachments.html
   - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/GetTransitGatewayRouteTableAssociations.html
   - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/paginator/DescribeTransitGatewayRouteTables.html
   - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/search_transit_gateway_routes.html
- Customer Gateway
   - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_customer_gateways.html
- VPN
   - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_vpn_connections.html
   - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_vpn_gateways.html
