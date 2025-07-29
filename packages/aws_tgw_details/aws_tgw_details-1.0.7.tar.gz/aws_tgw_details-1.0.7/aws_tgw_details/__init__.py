#!/usr/bin/env python3
# -*- coding: latin-1 -*-
"""Get AWS Transit Gateway details."""

import os
import sys
import argparse
import logging
from pprint import pprint as pp
from typing import Optional
from aws_authenticator import AWSAuthenticator


__version__ = "1.0.7"
__author__ = "Ahmad Ferdaus Abd Razak"
__application__ = "aws_tgws"


logger = logging.getLogger(__name__)


def get_name_from_tags(
    tags: list
) -> str:
    """Get Name tag value from a list of tags."""
    name = ""
    for tag in tags:
        if tag["Key"] == "Name":
            name = tag["Value"]
            break
    return name


def get_tgws(
    client,
    tgw_id: str
) -> list:
    """Get Transit Gateway details."""
    logger.info(f"Getting Transit Gateway details for {tgw_id}...")
    tgws = []
    paginator = client.get_paginator("describe_transit_gateways")
    if tgw_id != "ALL":
        response_iterator = paginator.paginate(
            TransitGatewayIds=[tgw_id]
        )
    else:
        response_iterator = paginator.paginate()
    for page in response_iterator:
        for tgw in page["TransitGateways"]:
            tgw_id = tgw["TransitGatewayId"]
            tgw_name = get_name_from_tags(tgw["Tags"])
            tgw_owner_id = tgw.get("OwnerId", "")
            tgw_amazon_asn = tgw.get(
                "Options",
                {}
            ).get(
                "AmazonSideAsn",
                ""
            )
            tgw_dns_support = tgw.get(
                "Options",
                {}
            ).get(
                "DnsSupport",
                ""
            )
            tgw_vpn_ecmp_support = tgw.get(
                "Options",
                {}
            ).get(
                "VpnEcmpSupport",
                ""
            )
            tgws.append(
                {
                    "tgw_id": tgw_id,
                    "tgw_name": tgw_name,
                    "tgw_owner_id": tgw_owner_id,
                    "tgw_amazon_asn": tgw_amazon_asn,
                    "tgw_dns_support": tgw_dns_support,
                    "tgw_vpn_ecmp_support": tgw_vpn_ecmp_support
                }
            )
    return tgws


def get_tgw_rts(
    client,
    tgw_id: Optional[str] = None,
    tgw_rt_id: Optional[str] = None
) -> list:
    """Get Transit Gateway route table details."""
    tgw_rts = []
    paginator = client.get_paginator("describe_transit_gateway_route_tables")
    if tgw_rt_id:
        logger.info(f"Getting Route Table details for {tgw_rt_id}...")
        response_iterator = paginator.paginate(
            TransitGatewayRouteTableIds=[tgw_rt_id]
        )
    else:
        logger.info(f"Getting Route Table details for TGW {tgw_id}...")
        response_iterator = paginator.paginate(
            Filters=[
                {
                    "Name": "transit-gateway-id",
                    "Values": [tgw_id]
                }
            ]
        )
    for page in response_iterator:
        for tgw_rt in page["TransitGatewayRouteTables"]:
            tgw_rt_id = tgw_rt["TransitGatewayRouteTableId"]
            tgw_rt_name = get_name_from_tags(tgw_rt["Tags"])
            tgw_rts.append(
                {
                    "tgw_rt_id": tgw_rt_id,
                    "tgw_rt_name": tgw_rt_name
                }
            )
    return tgw_rts


def get_tgw_routes(
    client,
    tgw_rt_id: str
) -> list:
    """Get Transit Gateway route details."""
    logger.info(f"Getting routes for {tgw_rt_id}...")
    response = client.search_transit_gateway_routes(
        TransitGatewayRouteTableId=tgw_rt_id,
        Filters=[
            {
                "Name": "attachment.resource-type",
                "Values": [
                    "vpc",
                    "vpn",
                    "peering",
                    "direct-connect-gateway",
                    "connect"
                ]
            },
        ],
        MaxResults=1000
    )
    return response["Routes"]


def get_tgw_attachments(
    client,
    tgw_id: Optional[str] = None,
    tgw_attachment_id: Optional[str] = None
) -> list:
    """Get Transit Gateway attachment details."""
    tgw_attachments = []
    paginator = client.get_paginator('describe_transit_gateway_attachments')
    if tgw_attachment_id:
        logger.info(f"Getting attachment details for {tgw_attachment_id}...")
        response_iterator = paginator.paginate(
            TransitGatewayAttachmentIds=[tgw_attachment_id]
        )
    else:
        logger.info(f"Getting attachment details for TGW {tgw_id}...")
        response_iterator = paginator.paginate(
            Filters=[
                {
                    "Name": "transit-gateway-id",
                    "Values": [tgw_id]
                },
            ]
        )
    for page in response_iterator:
        for attachment in page["TransitGatewayAttachments"]:
            tgw_attachment_id = attachment["TransitGatewayAttachmentId"]
            tgw_attachment_name = get_name_from_tags(attachment["Tags"])
            tgw_attachment_resource_type = attachment.get("ResourceType", "")
            tgw_attachment_resource_id = attachment.get("ResourceId", "")
            tgw_attachment_assoc_rt_id = attachment.get(
                "Association",
                {}
            ).get(
                "TransitGatewayRouteTableId",
                ""
            )
            tgw_attachment_assoc_rt_name = get_tgw_rts(
                client,
                tgw_id,
                tgw_attachment_assoc_rt_id
            )[0]["tgw_rt_name"]
            tgw_attachments.append(
                {
                    "tgw_attachment_id": tgw_attachment_id,
                    "tgw_attachment_name": tgw_attachment_name,
                    "tgw_attachment_resource_type": tgw_attachment_resource_type,
                    "tgw_attachment_resource_id": tgw_attachment_resource_id,
                    "tgw_attachment_assoc_rt_id": tgw_attachment_assoc_rt_id,
                    "tgw_attachment_assoc_rt_name": tgw_attachment_assoc_rt_name
                }
            )
    return tgw_attachments


def get_tgw_vpn_connections(
    client,
    tgw_id: Optional[str] = None,
    tgw_vpn_connection_id: Optional[str] = None
) -> list:
    """Get Transit Gateway VPN connection details."""
    tgw_vpn_connections = []
    if tgw_vpn_connection_id:
        logger.info(f"Getting VPN details for {tgw_vpn_connection_id}...")
        response = client.describe_vpn_connections(
            VpnConnectionIds=[tgw_vpn_connection_id]
        )
    else:
        logger.info(f"Getting VPN details for TGW {tgw_id}...")
        response = client.describe_vpn_connections(
            Filters=[
                {
                    "Name": "transit-gateway-id",
                    "Values": [tgw_id]
                }
            ]
        )
    for connection in response["VpnConnections"]:
        tgw_vpn_connection_id = connection["VpnConnectionId"]
        tgw_vpn_connection_name = get_name_from_tags(connection["Tags"])
        tgw_vpn_connection_cgw_id = connection.get("CustomerGatewayId", "")
        tgw_vpn_connection_cgw_name = get_cgws(
            client,
            tgw_vpn_connection_cgw_id
        )[0]["cgw_name"]
        tgw_vpn_connection_accel = connection.get(
            "Options",
            {}
        ).get(
            "EnableAcceleration",
            ""
        )
        tgw_vpn_connection_routing = "static" if connection.get(
            "Options",
            {}
        ).get(
            "StaticRoutesOnly",
            ""
        ) else "dynamic"
        tgw_vpn_connection_cgw_ip = get_cgws(
            client,
            tgw_vpn_connection_cgw_id
        )[0]["cgw_ip_address"]
        try:
            tgw_vpn_connection_inside_cidr_0 = connection.get(
                "Options",
                {}
            ).get(
                "TunnelOptions",
                [{}]
            )[0].get(
                "TunnelInsideCidr",
                ""
            )
            tgw_vpn_connection_outside_ip_0 = connection.get(
                "Options",
                {}
            ).get(
                "TunnelOptions",
                [{}]
            )[0].get(
                "OutsideIpAddress",
                ""
            )
        except IndexError:
            tgw_vpn_connection_inside_cidr_0 = ""
            tgw_vpn_connection_outside_ip_0 = ""
        try:
            tgw_vpn_connection_inside_cidr_1 = connection.get(
                "Options",
                {}
            ).get(
                "TunnelOptions",
                [{}]
            )[1].get(
                "TunnelInsideCidr",
                ""
            )
            tgw_vpn_connection_outside_ip_1 = connection.get(
                "Options",
                {}
            ).get(
                "TunnelOptions",
                [{}]
            )[1].get(
                "OutsideIpAddress",
                ""
            )
        except IndexError:
            tgw_vpn_connection_inside_cidr_1 = ""
            tgw_vpn_connection_outside_ip_1 = ""
        tgw_vpn_connections.append(
            {
                "tgw_vpn_connection_id": tgw_vpn_connection_id,
                "tgw_vpn_connection_name": tgw_vpn_connection_name,
                "tgw_vpn_connection_cgw_id": tgw_vpn_connection_cgw_id,
                "tgw_vpn_connection_cgw_name": tgw_vpn_connection_cgw_name,
                "tgw_vpn_connection_accel": tgw_vpn_connection_accel,
                "tgw_vpn_connection_routing": tgw_vpn_connection_routing,
                "tgw_vpn_connection_cgw_ip": tgw_vpn_connection_cgw_ip,
                "tgw_vpn_connection_inside_cidr_0": tgw_vpn_connection_inside_cidr_0,
                "tgw_vpn_connection_outside_ip_0": tgw_vpn_connection_outside_ip_0,
                "tgw_vpn_connection_inside_cidr_1": tgw_vpn_connection_inside_cidr_1,
                "tgw_vpn_connection_outside_ip_1": tgw_vpn_connection_outside_ip_1
            }
        )
    return tgw_vpn_connections


def get_cgws(
    client,
    cgw_id: str
) -> list:
    """Get Customer Gateway details."""
    logger.info(f"Getting Customer Gateway details for {cgw_id}...")
    cgws = []
    if cgw_id != "ALL":
        response = client.describe_customer_gateways(
            CustomerGatewayIds=[cgw_id]
        )
    else:
        response = client.describe_customer_gateways()
    for cgw in response["CustomerGateways"]:
        cgw_id = cgw["CustomerGatewayId"]
        cgw_name = get_name_from_tags(cgw["Tags"])
        cgw_device_name = cgw.get("DeviceName", "")
        cgw_ip_address = cgw.get("IpAddress", "")
        cgw_bgp_asn = cgw.get("BgpAsn", "")
        cgw_type = cgw.get("Type", "")
        cgws.append(
            {
                "cgw_id": cgw_id,
                "cgw_name": cgw_name,
                "cgw_device_name": cgw_device_name,
                "cgw_ip_address": cgw_ip_address,
                "cgw_bgp_asn": cgw_bgp_asn,
                "cgw_type": cgw_type
            }
        )
    return cgws


def login_to_aws(
    service: str,
    region: str
):
    """Login to AWS iwth IAM access key credentials in environment variables."""
    logger.info("Signing-in to AWS...")
    aws_session_token = os.environ.get("TGW_AWS_SESSION_TOKEN", None)
    if aws_session_token:
        auth = AWSAuthenticator(
            access_key_id=os.environ.get("TGW_AWS_ACCESS_KEY_ID"),
            secret_access_key=os.environ.get("TGW_AWS_SECRET_ACCESS_KEY"),
            session_token=aws_session_token
        )
    else:
        auth = AWSAuthenticator(
            access_key_id=os.environ.get("TGW_AWS_ACCESS_KEY_ID"),
            secret_access_key=os.environ.get("TGW_AWS_SECRET_ACCESS_KEY")
        )
    session = auth.iam()
    client = session.client(
        service,
        region
    )
    return client


def get_params():
    """Get parameters from script inputs."""
    myparser = argparse.ArgumentParser(
        add_help=True,
        allow_abbrev=False,
        description="Get AWS Transit Gateway details.",
        usage=f"{__application__} [options]"
    )
    myparser.add_argument(
        "-V", "--version", action="version", version=f"{__application__} {__version__}"
    )
    myparser.add_argument(
        "-t",
        "--tgw_id",
        action="store",
        help="Transit Gateway ID. Use 'ALL' to get all TGWs. Default: None.",
        nargs="?",
        default=None,
        required=False,
        type=str
    )
    myparser.add_argument(
        "-r",
        "--tgw_rt_id",
        action="store",
        help="Transit Gateway Route Table ID. Default: None.",
        nargs="?",
        default=None,
        required=False,
        type=str
    )
    myparser.add_argument(
        "-a",
        "--tgw_attachment_id",
        action="store",
        help="Transit Gateway Attachment ID. Default: None.",
        nargs="?",
        default=None,
        required=False,
        type=str
    )
    myparser.add_argument(
        "-v",
        "--tgw_vpn_connection_id",
        action="store",
        help="Transit Gateway VPN Connection ID. Default: None.",
        nargs="?",
        default=None,
        required=False,
        type=str
    )
    myparser.add_argument(
        "-c",
        "--cgw_id",
        action="store",
        help="Customer Gateway ID. Use 'ALL' to get all CGWs. Default: None.",
        nargs="?",
        default=None,
        required=False,
        type=str
    )
    myparser.add_argument(
        "-w",
        "--region",
        action="store",
        help="AWS Region. Default: us-east-1.",
        nargs="?",
        default="us-east-1",
        required=False,
        type=str
    )
    myparser.add_argument(
        "-l",
        "--log_path",
        action="store",
        help="Log file path. Default: /tmp.",
        nargs="?",
        default="/tmp",
        required=False,
        type=str
    )
    return myparser.parse_args()


def main():
    """Execute main function."""
    if len(sys.argv) == 1:
        print(f"\n{__application__} {__version__} - Get AWS Transit Gateway details.")
        print(
            "\n"
            "Environment variables:\n"
            "  TGW_AWS_ACCESS_KEY_ID [Required]\n"
            "  TGW_AWS_SECRET_ACCESS_KEY [Required]\n"
            "  TGW_AWS_SESSION_TOKEN [Optional. Default: None]"
            "\n"
        )
        print(
            "Additional modules:\n"
            "  aws_authenticator"
            "\n"
        )
        print(f"usage: {__application__} [options]")
        print("Use -h or --help for more information.\n")

    # Get parameters from script inputs.
    args = get_params()
    tgw_id = args.tgw_id
    tgw_rt_id = args.tgw_rt_id
    tgw_attachment_id = args.tgw_attachment_id
    tgw_vpn_connection_id = args.tgw_vpn_connection_id
    cgw_id = args.cgw_id
    region = args.region
    log_path = args.log_path

    logging.basicConfig(
        filename=f"{log_path}/{__application__}.log",
        level=logging.INFO
    )
    logger.info("Started.")

    # Login to AWS.
    client = login_to_aws(
        "ec2",
        region
    )

    # Get specific Transit Gateway Route Table details,
    # filtered by Transit Gateway Route Table ID.
    if tgw_rt_id:
        tgw_rts = get_tgw_rts(
            client,
            tgw_id,
            tgw_rt_id
        )
        pp(tgw_rts, indent=2)

    # Get specific Transit Gateway Attachment details,
    # filtered by Transit Gateway Attachment ID.
    if tgw_attachment_id:
        tgw_attachments = get_tgw_attachments(
            client,
            tgw_id,
            tgw_attachment_id
        )
        pp(tgw_attachments, indent=2)

    # Get specific Transit Gateway VPN Connection details,
    # filtered by Transit Gateway VPN Connection ID.
    if tgw_vpn_connection_id:
        tgw_vpn_connections = get_tgw_vpn_connections(
            client,
            tgw_id,
            tgw_vpn_connection_id
        )
        pp(tgw_vpn_connections, indent=2)

    # Get Customer Gateway details,
    # optionally filterable by Customer Gateway ID.
    if cgw_id:
        cgws = get_cgws(
            client,
            cgw_id
        )
        pp(cgws, indent=2)

    # Get Transit Gateway details,
    # optionally filterable by Transit Gateway ID.
    if (
        not cgw_id
        and not tgw_rt_id
        and not tgw_attachment_id
        and not tgw_vpn_connection_id
    ):
        tgws = get_tgws(
            client,
            tgw_id
        )
        pp(tgws, indent=2)

        for tgw in tgws:
            tgw_id = tgw["tgw_id"]
            tgw_rts = get_tgw_rts(
                client,
                tgw_id,
                tgw_rt_id
            )
            pp(tgw_rts, indent=2)

            tgw_attachments = get_tgw_attachments(
                client,
                tgw_id,
                tgw_attachment_id
            )
            pp(tgw_attachments, indent=2)

            tgw_vpn_connections = get_tgw_vpn_connections(
                client,
                tgw_id,
                tgw_vpn_connection_id
            )
            pp(tgw_vpn_connections, indent=2)

            for tgw_rt in tgw_rts:
                tgw_rt_id = tgw_rt["tgw_rt_id"]
                routes = get_tgw_routes(client, tgw_rt_id)
                pp(routes, indent=2)

    logger.info("Finished.")
