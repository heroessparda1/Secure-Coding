import subprocess
import os
import json
from datetime import datetime
from html import escape

APP_PATH = "/var/www/html/sinerghi"
REPORT_DIR = "/var/reports/security"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

html_file = f"{REPORT_DIR}/security_report_{timestamp}.html"
json_file = f"/tmp/security_report_{timestamp}.json"

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip() or result.stderr.strip()
    except Exception as e:
        return str(e)

# Jalankan audit
print("🔹 Menjalankan audit keamanan...")

phpcs_result = run_command(f"phpcs --standard=PSR12 {APP_PATH}/app || true")
symfony_result = run_command(f"symfony check:security --dir={APP_PATH} || true")
trivy_result = run_command(f"trivy fs --quiet {APP_PATH} || true")

# Simpan versi JSON mentah
report_data = {
    "timestamp": timestamp,
    "phpcs": phpcs_result,
    "symfony_security": symfony_result,
    "trivy": trivy_result
}
with open(json_file, "w") as f:
    json.dump(report_data, f, indent=2)

# Template HTML
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Security Audit Report - {timestamp}</title>
<style>
  body {{ font-family: Arial, sans-serif; background-color: #f9f9f9; color: #333; }}
  h1 {{ background-color: #005f99; color: white; padding: 10px; }}
  pre {{ background: #272822; color: #f8f8f2; padding: 10px; border-radius: 8px; overflow-x: auto; }}
  section {{ margin: 20px 0; }}
  .ok {{ color: #28a745; }}
  .warn {{ color: #ffc107; }}
  .fail {{ color: #dc3545; }}
</style>
</head>
<body>
<h1>Security Audit Report</h1>
<p><strong>Generated at:</strong> {timestamp}</p>
<p><strong>Project Path:</strong> {APP_PATH}</p>

<section>
<h2>1️⃣ PHP_CodeSniffer (Secure Coding)</h2>
<pre>{escape(phpcs_result)}</pre>
</section>

<section>
<h2>2️⃣ Symfony Security Checker (Dependencies)</h2>
<pre>{escape(symfony_result)}</pre>
</section>

<section>
<h2>3️⃣ Trivy (Vulnerability Scan)</h2>
<pre>{escape(trivy_result)}</pre>
</section>

<p><em>Report saved automatically at {html_file}</em></p>
</body>
</html>
"""

# Simpan HTML
with open(html_file, "w") as f:
    f.write(html_content)

print(f"✅ Laporan keamanan dalam format HTML disimpan di: {html_file}")
