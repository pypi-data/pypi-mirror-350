===================
**aws_tgw_details**
===================

Overview
--------

Get AWS Transit Gateway details.

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

Usage
------

Installation:

.. code-block:: BASH

   pip3 install aws_tgw_details
   # or
   python3 -m pip install aws_tgw_details

- Set environment variables.

.. code-block:: BASH

   export TGW_AWS_ACCESS_KEY_ID=your_access_key_id
   export TGW_AWS_SECRET_ACCESS_KEY=your_secret_access_key
   export TGW_AWS_SESSION_TOKEN=your_session_token

- Examples.

.. code-block:: BASH

   # Overview.
   aws_tgw_details

   # Help.
   aws_tgw_details -h

   # Get all Transit Gateways.
   aws_tgw_details -t ALL

   # Get a specific Transit Gateway.
   aws_tgw_details -t tgw-1234567890abcdef0

   # Get all Customer Gateways.
   aws_tgw_details -c ALL

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
