## What Is Subdomain Takeover?

Subdomain takeover happens when a company's DNS record (a **CNAME**)
points to an external service — like GitHub Pages, Heroku, or an AWS
S3 bucket — but that resource is no longer active or has been deleted.

Example:
- `blog.company.com` → CNAME → `company.github.io`
- The company deletes its GitHub Pages project but forgets to remove
  the CNAME record.
- `blog.company.com` still points to `company.github.io`, but nobody
  owns that name anymore.
- An attacker can create a new GitHub Pages site named `company` and
  claim it — now `blog.company.com` serves the attacker's content
  instead of the real company's.

This is dangerous because the subdomain still looks 100% legitimate
(same domain, same SSL setup in many cases) — making it a common tool
for phishing, cookie theft, and brand impersonation.


## Folder Structure

```
02-subdomain-takeover-scanner/
├── README.md              # This file — setup, usage, and documentation
├── report.md               # Scan methodology, results, and PoC evidence
├── domains.txt              # Input file — list of target domains to scan
├── scan_results.txt         # Output file — generated after running the scanner
└── src/
    ├── scanner.py            # Main scanner logic
    └── mock_vulnerable_server.py   # Local server used to test/prove detection works
```

## Example Output

```
Domain                              CNAME                          Service         Vulnerable
-----------------------------------------------------------------------------------------------
www.wikipedia.org                   dyna.wikimedia.org.            N/A             No
www.google.com                      None                           N/A             No
docs.python.org                     dualstack.python.map.fastly.net N/A            No

Results saved to scan_results.txt
```

## Future Improvements

- Add more service fingerprints (Azure, Fastly, Cloudfront, Bitbucket,
  Zendesk, Unbounce, etc.) — this tool currently only covers 4.
- Add HTTPS support alongside HTTP.
- Add multithreading to scan large domain lists faster.
- Add a simple Flask dashboard to visualize scan results instead of
  reading raw text output.
- Export results as JSON/CSV for integration with other tools.

## Troubleshooting

**`type nul` fails with "Cannot find path...nul"**
This happens because `type nul` is a `cmd.exe` trick, not valid in
PowerShell. Use `New-Item filename.ext` instead.

**`IndentationError: expected an indented block`**
Usually caused by a function accidentally indented under another
function instead of starting at column 0. Check that every top-level
`def` starts with zero leading spaces.

**`venv\Scripts\Activate.ps1` says "module could not be loaded"**
This means you're not inside the correct project folder — PowerShell
is trying to interpret `venv` as something else because the path
doesn't exist from your current location. Run `cd` into the correct
folder first, then activate.

**Script hangs or takes long on a domain**
Some domains may be slow or unreachable — `check_takeover()` uses a
5-second timeout per request, so a single bad domain won't hang the
whole scan indefinitely.
