# Subdomain Takeover Scanner — Report

## Methodology
1. Collected a list of target domains in `domains.txt`.
2. For each domain, resolved its CNAME record via `dnspython`.
3. Matched the CNAME against known vulnerable service patterns
   (GitHub Pages, Heroku, AWS S3, Shopify).
4. Where a match was found, sent an HTTP request and checked the
   response for each service's known "unclaimed resource" fingerprint.
5. Logged results to `scan_results.txt`.

## Real-World Scan Results

| Domain | CNAME | Service | Takeover Possible |
|---|---|---|---|
| www.wikipedia.org | dyna.wikimedia.org | N/A | No |
| www.google.com | None | N/A | No |
| docs.python.org | dualstack.python.map.fastly.net | N/A | No |
| mail.google.com | None | N/A | No |
| help.github.com | None | N/A | No |

**Conclusion:** None of the tested domains are vulnerable — all are
either using A records directly or are actively/correctly configured.
This is expected, since these are large, well-maintained production
domains.

## Proof-of-Concept: Positive Detection Case

To verify the tool correctly detects a *real* vulnerable condition
(not just correctly reporting "safe" domains as safe), a local mock
server was used to simulate an unclaimed GitHub Pages response:

- **Simulated domain:** localhost:8000
- **Simulated CNAME/service:** GitHub Pages
- **Fingerprint returned:** "There isn't a GitHub Pages site here"
- **Scanner result:** `Vulnerable: True`

### PoC Steps (how a real takeover would work, if found)
1. Scanner identifies a subdomain with a CNAME pointing to a service
   (e.g. `myproject.github.io`) where the fingerprint indicates the
   resource is unclaimed.
2. An attacker registers that exact resource name on the service
   (e.g. creates a GitHub Pages site named `myproject`).
3. The attacker's content is now served whenever anyone visits the
   original company subdomain — since DNS still points there.
4. **Responsible disclosure:** rather than exploiting this, the
   correct action is to report the finding to the domain owner
   (e.g. via their security.txt contact or bug bounty program) so
   they can remove the dangling CNAME record.

## Limitations
- Only detects 4 services (GitHub Pages, Heroku, AWS S3, Shopify) —
  extendable by adding entries to `SERVICE_FINGERPRINTS`.
- Requires the domain to be live and reachable via HTTP.
- Does not attempt actual takeover — detection only, by design.