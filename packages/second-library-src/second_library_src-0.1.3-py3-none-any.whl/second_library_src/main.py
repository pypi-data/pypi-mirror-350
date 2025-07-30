import boto3
from typing import List, Dict
import os
from mcp.server.fastmcp import FastMCP

eb_client = boto3.client(
    "elasticbeanstalk",
    region_name=os.getenv('AWS_REGION', 'us-east-1'),
)

mcp = FastMCP("Amazon Web Services Elastic Beanstalk Utility")

@mcp.tool()
def aws_elasticBeanstalk_applications() -> List[Dict]:
    """
    Get the Elastic Beanstalk Applications and List them
    
    Returns:
        List[Dict]: List of Elastic Beanstalk Applications
    """
    response = eb_client.describe_applications()
    return response["Applications"]