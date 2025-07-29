# Akamai Swiss Army Knife

A simple utility library to perform basic network diagnostics and IP intelligence checks for Akamai.

## Installation
```bash
pip install akamai-swissarmyknife
```

## Usage
```python
from akamai_swissarmyknife import check_ip

print(check_ip("23.67.253.113"))
```

## Upcoming Features (Next Release Preview)

Aiming to support the Akamai Open APIs to ease automation for security researchers and defenders.

### 🔐 Akamai WAF & AppSec

1. **get_waf_ruleset_config(policy_id)**
   - Description: Retrieve the ruleset configuration for a specific policy.
   - Example: `get_waf_ruleset_config("pol-12345")`

2. **list_waf_policies()**
   - Description: List all WAF security policies associated with an account.
   - Example: `list_waf_policies()`

3. **get_waf_attack_groups(policy_id)**
   - Description: Fetch attack group settings for a given policy.
   - Example: `get_waf_attack_groups("pol-67890")`

4. **update_waf_rule_threshold(rule_id, threshold)**
   - Description: Update anomaly detection thresholds for a rule.
   - Example: `update_waf_rule_threshold("rule-001", 10)`

5. **toggle_waf_rule(rule_id, enable=True)**
   - Description: Enable or disable a specific rule.
   - Example: `toggle_waf_rule("rule-001", enable=False)`

### ⚙️ Akamai Control Center Utilities

6. **get_alert_definitions()**
   - Description: Get all alert types available in Akamai Control Center.
   - Example: `get_alert_definitions()`

7. **list_active_alerts()**
   - Description: Show currently active alerts in the environment.
   - Example: `list_active_alerts()`

8. **acknowledge_alert(alert_id)**
   - Description: Acknowledge a triggered alert.
   - Example: `acknowledge_alert("alert-789")`

9. **get_account_info()**
   - Description: Fetch account details from the identity management endpoint.
   - Example: `get_account_info()`

10. **get_contracts()**
    - Description: List all contracts available for the account.
    - Example: `get_contracts()`

### 🛡️ Network & Edge Intelligence

11. **check_edge_server_status(ip)**
    - Description: Lookup if an IP belongs to Akamai's edge network.
    - Example: `check_edge_server_status("23.67.253.113")`

12. **get_cpcode_usage(cpcode)**
    - Description: Monitor usage stats for a specific cpCode.
    - Example: `get_cpcode_usage("123456")`

13. **list_property_hostnames(property_id)**
    - Description: Retrieve all hostnames linked to a specific property.
    - Example: `list_property_hostnames("prp_123")`

14. **purge_cache_by_url(urls)**
    - Description: Programmatically purge edge cache for a list of URLs.
    - Example: `purge_cache_by_url(["https://example.com/index.html"])`

15. **get_edge_dns_records(zone)**
    - Description: Fetch DNS records from Akamai Edge DNS.
    - Example: `get_edge_dns_records("example.com")`

These APIs will require API client credentials and integration with Akamai's EdgeGrid authentication. Coming soon.