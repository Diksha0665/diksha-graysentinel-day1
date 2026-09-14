import dns.resolver
import requests

# Each entry: which CNAME pattern to match, and what text on the page
# proves the resource is unclaimed (vulnerable to takeover)
SERVICE_FINGERPRINTS = [
    {
        "service": "GitHub Pages",
        "cname_match": "github.io",
        "fingerprint": "There isn't a GitHub Pages site here"
    },
    {
        "service": "Heroku",
        "cname_match": "herokuapp.com",
        "fingerprint": "No such app"
    },
    {
        "service": "AWS S3",
        "cname_match": "s3.amazonaws.com",
        "fingerprint": "NoSuchBucket"
    },
    {
        "service": "Shopify",
        "cname_match": "myshopify.com",
        "fingerprint": "Sorry, this shop is currently unavailable"
    },
]


def match_service(cname):
    """
    Given a CNAME string, check which known service it belongs to.
    Returns the matching service dict, or None if no known service matches.
    """
    if cname is None:
        return None
    for entry in SERVICE_FINGERPRINTS:
        if entry["cname_match"] in cname:
            return entry
    return None


def check_takeover(domain, service_entry):
    """
    Visits the domain over HTTP(S) and checks if the service's
    'unclaimed' fingerprint text appears in the response.
    Returns True if vulnerable, False if not, None if the site couldn't be reached.
    """
    url = f"http://{domain}"
    try:
        response = requests.get(url, timeout=5)
        if service_entry["fingerprint"] in response.text:
            return True
        return False
    except requests.exceptions.RequestException as e:
        print(f"Could not reach {domain}: {e}")
        return None

def scan_domain(domain):
    """
    Runs the full takeover-check pipeline on a single domain.
    Returns a dictionary summarizing the result.
    """
    cname = get_cname(domain)
    service_entry = match_service(cname)

    if service_entry is None:
        # No CNAME, or CNAME doesn't match any known vulnerable service pattern
        return {
            "domain": domain,
            "cname": cname,
            "service": "N/A",
            "vulnerable": "No"
        }

    is_vulnerable = check_takeover(domain, service_entry)

    return {
        "domain": domain,
        "cname": cname,
        "service": service_entry["service"],
        "vulnerable": "Yes" if is_vulnerable else "No"
    }


def scan_domains(domain_list):
    """
    Runs scan_domain() on a list of domains and returns all results.
    """
    results = []
    for domain in domain_list:
        print(f"Scanning {domain}...")
        result = scan_domain(domain)
        results.append(result)
    return results

def load_domains_from_file(filepath):
    """
    Reads a list of domains from a text file, one per line.
    Skips empty lines.
    """
    with open(filepath, "r") as f:
        domains = [line.strip() for line in f if line.strip()]
    return domains


def print_report(results):
    """
    Prints scan results in a clean, readable table format.
    """
    print("\n{:<35} {:<30} {:<15} {:<10}".format("Domain", "CNAME", "Service", "Vulnerable"))
    print("-" * 95)
    for r in results:
        print("{:<35} {:<30} {:<15} {:<10}".format(
            r["domain"], str(r["cname"]), r["service"], r["vulnerable"]
        ))


def save_report(results, filepath="scan_results.txt"):
    """
    Saves scan results to a text file in the same table format.
    """
    with open(filepath, "w") as f:
        f.write("{:<35} {:<30} {:<15} {:<10}\n".format("Domain", "CNAME", "Service", "Vulnerable"))
        f.write("-" * 95 + "\n")
        for r in results:
            f.write("{:<35} {:<30} {:<15} {:<10}\n".format(
                r["domain"], str(r["cname"]), r["service"], r["vulnerable"]
            ))
    print(f"\nResults saved to {filepath}")

def get_cname(domain):
    """
    Attempts to fetch the CNAME record for a given domain.
    Returns the CNAME as a string if found, otherwise None.
    """
    try:
        answers = dns.resolver.resolve(domain, 'CNAME')
        cname = str(answers[0].target)
        return cname
    except dns.resolver.NoAnswer:
        # Domain exists but has no CNAME record (might use an A record instead)
        return None
    except dns.resolver.NXDOMAIN:
        # Domain doesn't exist at all
        return None
    except Exception as e:
        # Catch-all for other DNS errors (timeouts, etc.)
        print(f"Error resolving {domain}: {e}")
        return None

if __name__ == "__main__":
    domains = load_domains_from_file("domains.txt")
    results = scan_domains(domains)
    print_report(results)
    save_report(results)


 