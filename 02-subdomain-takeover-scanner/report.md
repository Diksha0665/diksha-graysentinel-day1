# Subdomain Takeover Scanner — Detailed Report

## 1. Objective

Build a tool that identifies subdomains vulnerable to **takeover** —
a class of vulnerability where a DNS CNAME record points to an
external service that has since been deleted/unclaimed, allowing an
attacker to register that exact resource and hijack the subdomain.

This report documents the full build process, methodology, real-world
test results, and a verified proof-of-concept demonstrating the
detection logic works correctly.

## 2. Background / Why This Matters

Subdomain takeover is a well-documented, real-world vulnerability
class tracked in bug bounty programs across the industry (HackerOne,
Bugcrowd). It's dangerous because:
- The hijacked subdomain still belongs to the legitimate company's
  domain (e.g. `blog.company.com`), so it inherits trust — users,
  browsers, and even some security scanners treat it as legitimate.
- It can be used for phishing, malware hosting, cookie/session theft,
  or brand damage — all while looking like official company content.
- It's caused by a simple, common mistake: deleting a cloud resource
  (like a GitHub Pages project or S3 bucket) without removing the
  DNS record that still points to it.

## 3. Methodology

### Step-by-step pipeline
1. **Input collection** — target domains are listed in `domains.txt`,
   one per line.
2. **DNS resolution** — for each domain, query its CNAME record using
   `dnspython`'s resolver.
3. **Service fingerprinting** — compare the CNAME against a known list
   of vulnerable service patterns (`SERVICE_FINGERPRINTS` in
   `scanner.py`), currently covering GitHub Pages, Heroku, AWS S3, and
   Shopify.
4. **Live verification** — if a CNAME matches a tracked service, send
   an HTTP GET request to the domain and search the response body for
   that service's specific "unclaimed resource" error text.
5. **Result classification** — mark as `Vulnerable: Yes` if the
   fingerprint text is found, `No` otherwise (including cases with no
   CNAME, or a CNAME that doesn't match any tracked service).
6. **Output** — results are printed as a formatted table and saved to
   `scan_results.txt` for record-keeping.

### Tools and libraries used
- **Python 3.13**
- **dnspython** — for CNAME record resolution
- **requests** — for HTTP fingerprint checks
- **http.server** (Python standard library) — used only to build the
  local mock server for PoC verification, not part of the scanner itself

## 4. Real-World Scan Results

Domains tested (chosen as safe, well-known, publicly reachable sites —
not scanned with any intent to exploit, purely to validate the tool's
DNS/HTTP logic against real infrastructure):

| Domain | CNAME Found | Matched Service | Takeover Possible |
|---|---|---|---|
| www.wikipedia.org | dyna.wikimedia.org | N/A (not a tracked service) | No |
| www.google.com | None (uses A record) | N/A | No |
| docs.python.org | dualstack.python.map.fastly.net | N/A (Fastly not yet tracked) | No |
| mail.google.com | None | N/A | No |
| help.github.com | None | N/A | No |
| nonexistent-domain-xyz123.com | None (NXDOMAIN) | N/A | No |

**Analysis:** All tested domains returned `No`, which is the correct
and expected outcome — these are large, actively maintained production
domains, not misconfigured ones. This result set demonstrates the
scanner correctly handles multiple real-world conditions without
false positives:
- A domain with a CNAME to an untracked service (Wikipedia, Python docs)
- A domain with no CNAME at all (Google)
- A domain that doesn't exist (NXDOMAIN case)

## 5. Proof-of-Concept: Positive Detection Case

Since none of the real-world test domains were actually vulnerable
(expected, as they're legitimate/maintained), a **local mock server**
was built to validate that the detection logic correctly identifies a
*truly* vulnerable condition when one exists — without scanning or
touching any real company's infrastructure without authorization.

### Setup
- A minimal Python HTTP server (`src/mock_vulnerable_server.py`) was
  run on `localhost:8000`.
- It was configured to respond with the exact fingerprint text GitHub
  Pages shows for an unclaimed site: *"There isn't a GitHub Pages site
  here."*

### Test
`check_takeover()` was called directly against `localhost:8000` with
a GitHub Pages service entry.

### Result

| Simulated Domain | Simulated Service | Fingerprint Checked | Result |
|---|---|---|---|
| localhost:8000 | GitHub Pages | "There isn't a GitHub Pages site here" | **Vulnerable: True** |

This confirms the detection function correctly returns `True` when the
fingerprint is genuinely present — proving the tool doesn't just
default to "No" for everything, and the positive-detection path works
as designed.

### PoC Steps — How a Real Takeover Would Work (if found)
1. Scanner flags a subdomain (e.g. `myproject.github.io` via CNAME)
   whose fingerprint indicates the resource is currently unclaimed.
2. An attacker registers that exact name on the service (e.g. creates
   a GitHub Pages project named `myproject`).
3. Since the DNS CNAME still points there, the original company
   subdomain now serves the attacker's content.
4. The attacker could use this for phishing pages, malicious downloads,
   or cookie/session harvesting — all under the trusted company domain.

### Responsible Disclosure Note
This tool is a **detector only** — it never attempts to actually claim
or register any resource. If a real vulnerable subdomain were found in
authorized testing, the correct action is to report it to the domain
owner (via their security contact or bug bounty program), not to
exploit it.

## 6. Limitations

- Only 4 services are currently fingerprinted (GitHub Pages, Heroku,
  AWS S3, Shopify) — many other vulnerable services exist (Fastly,
  Azure, Cloudfront, Zendesk, Unbounce, Bitbucket, etc.) and would
  need their fingerprints added to `SERVICE_FINGERPRINTS`.
- Only checks plain HTTP, not HTTPS.
- Single-threaded — scanning a large domain list would be slow; each
  domain is checked sequentially.
- Detection relies on exact fingerprint text matching — if a service
  changes its error message wording, the fingerprint would need
  updating.

## 7. Conclusion

The scanner successfully implements the full detection pipeline
(DNS → service match → live fingerprint check → report), was validated
against 6 real-world domains with no false positives, and was proven
to correctly detect a genuinely vulnerable condition via a controlled,
locally-hosted proof-of-concept — without scanning any real
infrastructure without authorization.
