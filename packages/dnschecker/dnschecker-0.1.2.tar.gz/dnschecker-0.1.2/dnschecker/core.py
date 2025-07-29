#!/usr/bin/env python3
import dns.resolver
import argparse
import sys
import socket

def get_dns_records(domain, record_type, dns_servers):
    """
    Query DNS records for a domain using specified DNS servers
    """
    resolver = dns.resolver.Resolver()
    resolver.nameservers = dns_servers
    resolver.timeout = 10
    resolver.lifetime = 10
    
    try:
        # Handle SPF records specially - they are stored as TXT records
        if record_type.upper() == 'SPF':
            record_type = 'TXT'
        
        answers = resolver.resolve(domain, record_type)
        records = [str(answer) for answer in answers]
        
        # Filter SPF records from TXT records
        if record_type == 'TXT':
            original_type = record_type
            # Check if we were originally looking for SPF
            import inspect
            frame = inspect.currentframe()
            if frame and frame.f_back and frame.f_back.f_locals.get('record_type', '').upper() == 'SPF':
                spf_records = [record for record in records if 'v=spf1' in record.lower()]
                return spf_records if spf_records else [f"No SPF records found in TXT records for {domain}"]
        
        return records
    except dns.resolver.NXDOMAIN:
        return [f"NXDOMAIN: {domain} does not exist"]
    except dns.resolver.NoAnswer:
        return [f"No {record_type} records found for {domain}"]
    except dns.resolver.Timeout:
        return [f"Timeout querying {domain} for {record_type} records"]
    except Exception as e:
        return [f"Error: {str(e)}"]

def get_domain_ip(domain):
    """
    Get the IP address of a domain using system resolver
    """
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def check_records(domains, record_type, dns_servers, find_value=None, find_ipv4=None, find_ipv6=None):
    """
    Check DNS records for multiple domains
    """
    # ANSI color codes
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    
    print(f"Using DNS servers: {', '.join(dns_servers)}")
    print(f"Record type: {record_type}")
    if find_value:
        print(f"Searching for: {find_value}")
    if find_ipv4:
        print(f"Searching for IPv4: {find_ipv4}")
    if find_ipv6:
        print(f"Searching for IPv6: {find_ipv6}")
    print("-" * 60)
    
    for domain in domains:
        print(f"\nDomain: {domain}")
        records = get_dns_records(domain, record_type, dns_servers)
        
        # Initialize found flags
        found_value = False
        found_ipv4 = False
        found_ipv6 = False
        highlighted_record = None
        
        # Check all records and apply highlighting
        for record in records:
            record = record.replace("\" \"", "")
            temp_highlighted_record = record
            record_has_match = False
            
            # Check for find_value (general search)
            if find_value and find_value.lower() in record.lower():
                temp_highlighted_record = temp_highlighted_record.replace(find_value, f"{GREEN}{find_value}{RESET}")
                found_value = True
                record_has_match = True
            
            # Check for IPv4 addresses
            if find_ipv4:
                import re
                ipv4_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
                
                # Direct IP match
                if find_ipv4 in record:
                    temp_highlighted_record = temp_highlighted_record.replace(find_ipv4, f"{GREEN}{find_ipv4}{RESET}")
                    found_ipv4 = True
                    record_has_match = True
                # Check for IP in SPF includes/redirects
                elif record_type.upper() == 'SPF' or 'v=spf1' in record.lower():
                    ips_in_record = re.findall(ipv4_pattern, record)
                    if find_ipv4 in ips_in_record:
                        temp_highlighted_record = temp_highlighted_record.replace(find_ipv4, f"{GREEN}{find_ipv4}{RESET}")
                        found_ipv4 = True
                        record_has_match = True
            
            # Check for IPv6 addresses
            if find_ipv6:
                import re
                ipv6_pattern = r'\b(?:[0-9a-fA-F]{1,4}:){2,7}[0-9a-fA-F]{1,4}\b'
                
                # Direct IPv6 match
                if find_ipv6.lower() in record.lower():
                    temp_highlighted_record = re.sub(re.escape(find_ipv6), f"{GREEN}{find_ipv6}{RESET}", temp_highlighted_record, flags=re.IGNORECASE)
                    found_ipv6 = True
                    record_has_match = True
                # Check for IPv6 in SPF includes/redirects
                elif record_type.upper() == 'SPF' or 'v=spf1' in record.lower():
                    ipv6s_in_record = re.findall(ipv6_pattern, record, re.IGNORECASE)
                    if any(find_ipv6.lower() == ip.lower() for ip in ipv6s_in_record):
                        temp_highlighted_record = re.sub(re.escape(find_ipv6), f"{GREEN}{find_ipv6}{RESET}", temp_highlighted_record, flags=re.IGNORECASE)
                        found_ipv6 = True
                        record_has_match = True
            
            # Store the highlighted record if any match was found
            if record_has_match:
                highlighted_record = temp_highlighted_record
                break  # We found a record with matches, use this one
        
        # Build combined status message for multiple searches
        if (find_value or find_ipv4 or find_ipv6) and highlighted_record:
            status_parts = []
            
            if find_value:
                if found_value:
                    status_parts.append(f"✅ {find_value}")
                else:
                    status_parts.append(f"❌ {find_value}")
            
            if find_ipv4:
                if found_ipv4:
                    status_parts.append(f"✅ IPv4 {find_ipv4}")
                else:
                    status_parts.append(f"❌ IPv4 {find_ipv4}")
            
            if find_ipv6:
                if found_ipv6:
                    status_parts.append(f"✅ IPv6 {find_ipv6}")
                else:
                    status_parts.append(f"❌ IPv6 {find_ipv6}")
            
            if status_parts:
                status_message = ", ".join(status_parts)
                print(f"{status_message} in: {highlighted_record}")
        
        # Handle case where nothing was found at all
        elif find_value or find_ipv4 or find_ipv6:
            status_parts = []
            
            if find_value and not found_value:
                status_parts.append(f"❌ {find_value}")
            
            if find_ipv4 and not found_ipv4:
                status_parts.append(f"❌ IPv4 {find_ipv4}")
            
            if find_ipv6 and not found_ipv6:
                status_parts.append(f"❌ IPv6 {find_ipv6}")
            
            if status_parts:
                status_message = ", ".join(status_parts)
                print(f"{status_message} - NOT found")
                for record in records:
                    print(f"  → {record}")
        
        # If no specific search parameters, handle default behavior
        else:
            # If no find value is specified and it's A record, show the IP
            if record_type.upper() == 'A':
                domain_ip = get_domain_ip(domain)
                if domain_ip and domain_ip in records:
                    print(f"✅ IP {domain_ip} found")
                elif domain_ip:
                    print(f"❌ Expected IP {domain_ip} NOT found in DNS records")
                    print(f"DNS records: {', '.join(records)}")
                else:
                    print(f"Could not resolve domain IP")
            
            # Always show the actual records when not searching
            for record in records:
                print(f"  → {record}")

def main():
    parser = argparse.ArgumentParser(description='DNS Record Checker')
    
    parser.add_argument('--dns-servers', 
                       nargs='+', 
                       default=['1.1.1.1', '1.0.0.1'],
                       help='DNS servers to query (default: 1.1.1.1 1.0.0.1)')
    
    parser.add_argument('--type', 
                       default='A',
                       help='DNS record type (A, MX, TXT, SPF, CNAME, etc.) (default: A)')
    
    parser.add_argument('--find',
                       help='Value to search for in the records')
    
    parser.add_argument('--find-ipv4',
                       help='IPv4 address to search for in the records')
    
    parser.add_argument('--find-ipv6',
                       help='IPv6 address to search for in the records')
    
    parser.add_argument('--domains',
                       nargs='+',
                       required=True,
                       help='Domains to check')
    
    args = parser.parse_args()
    
    # Validate DNS servers
    valid_dns_servers = []
    for server in args.dns_servers:
        try:
            socket.inet_aton(server)  # Validate IP format
            valid_dns_servers.append(server)
        except socket.error:
            print(f"Warning: Invalid DNS server IP: {server}")
    
    if not valid_dns_servers:
        print("Error: No valid DNS servers provided")
        sys.exit(1)
    
    check_records(args.domains, args.type, valid_dns_servers, args.find, args.find_ipv4, args.find_ipv6)

if __name__ == "__main__":
    main()