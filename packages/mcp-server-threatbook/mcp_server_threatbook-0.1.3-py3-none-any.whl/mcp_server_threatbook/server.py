# server.py
import os
import requests
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("MCPThreatBook")

apikey = os.getenv("THREATBOOK_APIKEY")
base_url = "https://api.threatbook.cn/v3"


@mcp.tool()
def query_domain_subdomain(domain: str) -> object:
    """Search for subdomains associated with a domain
    
    Args:
    domain (str): The domain to search for.
    Returns:
    object: The subdomains associated with the domain.
    """
    # Simulate a domain search
    interface = f"{base_url}/domain/sub_domains"
    data = {
        "apikey": apikey,
        "resource": domain,
        "lang": "en",
    }
    resp = requests.get(interface, params=data)
    if resp.status_code != 200:
        return f"Error fetching subdomains for {domain}: {resp.text}"
    return resp.json()


@mcp.tool()
def query_domain_detail_information(domain: str) -> object:
    """Search for detailed information associated with a domain
    
    Args:
    domain (str): The domain to search for.
    Returns:
    object: The detailed information associated with the domain, such as resolving IP, whois, etc..
    """
    # Simulate a domain search
    interface = f"{base_url}/domain/adv_query"
    data = {
        "apikey": apikey,
        "resource": domain,
        "lang": "en",
    }
    resp = requests.get(interface, params=data)
    if resp.status_code != 200:
        return f"Error fetching details for {domain}: {resp.text}"
    return resp.json()


@mcp.tool()
def query_domain_threat_information(domain: str) -> object:
    """Search for threat information associated with a domain
    
    Args:
    domain (str): The domain to search for.
    Returns:
    object: The threat information or history information associated with the domain.
    """
    # Simulate a domain search
    interface = f"{base_url}/domain/query"
    data = {
        "apikey": apikey,
        "resource": domain,
        "lang": "en",
    }
    resp = requests.get(interface, params=data)
    if resp.status_code != 200:
        return f"Error fetching threat information for {domain}: {resp.text}"
    return resp.json()


@mcp.tool()
def query_ip_for_domain_information(ip: str) -> object:
    """Search for domain information associated with an IP address
    
    Args:
    ip (str): The IP address to search for.
    Returns:
    object: The domain information or history information associated with the IP address.
    """
    # Simulate a domain search
    interface = f"{base_url}/ip/adv_query"
    data = {
        "apikey": apikey,
        "resource": ip,
        "lang": "en",
    }
    resp = requests.get(interface, params=data)
    if resp.status_code != 200:
        return f"Error fetching domain information for {ip}: {resp.text}"
    return resp.json()


@mcp.tool()
def query_ip_basic_information(ip: str) -> object:
    """Analyze an IP address
    
    Args:
    ip (str): The IP address to analyze.
    Returns:
    object: The analysis results for the IP address.
    """
    # Simulate an IP analysis
    interface = f"{base_url}/ip/query"
    data = {
        "apikey": apikey,
        "resource": ip,
        "lang": "en",
    }
    resp = requests.get(interface, params=data)
    if resp.status_code != 200:
        return f"Error fetching analysis for {ip}: {resp.text}"
    return resp.json()


@mcp.tool()
def query_ioc(ioc: str) -> object:
    """Search for an IOC (Indicator of Compromise)
    
    Args:
    ioc (str): The IOC to search for, such as an IP address or domain.
    Returns:
    object: The search results for the IOC.
    """
    # Simulate an IOC search
    interface = f"{base_url}/scene/ioc"
    data = {
        "apikey": apikey,
        "resource": ioc,
        "lang": "en",
    }
    resp = requests.get(interface, params=data)
    if resp.status_code != 200:
        return f"Error fetching IOC {ioc}: {resp.text}"
    return resp.json()


@mcp.tool()
def query_ip_reputation(ip: str) -> object:
    """Get IP reputation
    
    Args:
    ip (str): The IP address to check reputation for.
    Returns:
    object: The reputation data for the IP address.
    """
    # Simulate an IP reputation lookup
    interface = f"{base_url}/scene/ip_reputation"
    data = {
        "apikey": apikey,
        "resource": ip,
        "lang": "en",
    }
    resp = requests.get(interface, params=data)
    if resp.status_code != 200:
        return f"Error fetching reputation for {ip}: {resp.text}"
    return resp.json()


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


def run_mcp():
    """Run the MCP server"""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    run_mcp()
