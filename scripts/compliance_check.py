# 3. Create compliance check script
compliance_check_py = '''#!/usr/bin/env python3
"""
Federal Compliance Checker
Automated verification of federal funding requirements
"""

import sys
import yaml
from datetime import datetime
from pathlib import Path

class ComplianceChecker:
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.passed = []
        
    def check_ntia_config(self):
        """Check NTIA configuration completeness."""
        print("\\n[1/5] Checking NTIA TBCP 2026 Configuration...")
        
        try:
            with open("config/ntia_config.yaml", 'r') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            self.issues.append("config/ntia_config.yaml not found")
            return
        
        # Check required fields
        checks = [
            ("Tribal Name", config.get("tribal_name")),
            ("UEI", config.get("uei")),
            ("SAM.gov Active", config.get("sam_gov", {}).get("active")),
            ("Tribal Council Resolution", config.get("tribal_council_resolution")),
            ("Consultation Meetings", config.get("consultation_meetings")),
            ("Technology Choice", config.get("technology_choice", {}).get("tribal_preference")),
            ("Climate Risks", config.get("climate_risks")),
            ("Workforce Budget", config.get("workforce_budget", 0) > 0),
        ]
        
        for name, value in checks:
            if value:
                self.passed.append(f"✓ {name}")
                print(f"  ✓ {name}")
            else:
                self.issues.append(f"Missing or incomplete: {name}")
                print(f"  ✗ {name} - REQUIRES ATTENTION")
    
    def check_bia_config(self):
        """Check BIA configuration."""
        print("\\n[2/5] Checking BIA Integration Configuration...")
        
        try:
            with open("config/bia_integration.yaml", 'r') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            self.warnings.append("config/bia_integration.yaml not found (optional for BIA funding)")
            print("  ⚠ Optional for BIA funding - skipped")
            return
        
        if config.get("tpa_base_funding", 0) > 0:
            self.passed.append("✓ BIA TPA configuration present")
            print("  ✓ TPA configuration found")
        else:
            self.warnings.append("TPA base funding not configured")
            print("  ⚠ TPA base funding not set")
    
    def check_isac_config(self):
        """Check Tribal-ISAC configuration."""
        print("\\n[3/5] Checking Tribal-ISAC Configuration...")
        
        try:
            with open("config/tribal_isac.yaml", 'r') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            self.warnings.append("config/tribal_isac.yaml not found (recommended)")
            print("  ⚠ Recommended but not required")
            return
        
        if config.get("membership_active"):
            self.passed.append("✓ Tribal-ISAC membership active")
            print("  ✓ Tribal-ISAC membership active")
        else:
            self.warnings.append("Tribal-ISAC membership not active - recommended for threat intel")
            print("  ⚠ Membership not active - recommended")
    
    def check_documentation(self):
        """Check required documentation."""
        print("\\n[4/5] Checking Documentation...")
        
        required_docs = [
            "docs/FUNDING.md",
            "docs/TRIBAL_DATA_SOVEREIGNTY.md",
            "docs/BROADBAND_SECURITY.md",
            "docs/TRIBAL_CONSULTATION_PROTOCOL.md",
            "docs/WORKFORCE_DEVELOPMENT.md",
            "docs/ECONOMIC_IMPACT.md",
            "docs/FEDERAL_COMPLIANCE.md",
        ]
        
        for doc in required_docs:
            if Path(doc).exists():
                self.passed.append(f"✓ {doc}")
                print(f"  ✓ {doc}")
            else:
                self.issues.append(f"Missing documentation: {doc}")
                print(f"  ✗ {doc} - MISSING")
    
    def check_templates(self):
        """Check grant templates."""
        print("\\n[5/5] Checking Grant Templates...")
        
        templates = [
            "templates/grant_proposal_template.md",
        ]
        
        for template in templates:
            if Path(template).exists():
                self.passed.append(f"✓ {template}")
                print(f"  ✓ {template}")
            else:
                self.warnings.append(f"Missing template: {template}")
                print(f"  ⚠ {template} - Recommended")
    
    def generate_report(self):
        """Generate compliance report."""
        print("\\n" + "="*50)
        print("COMPLIANCE CHECK REPORT")
        print("="*50)
        print(f"\\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"\\nPassed: {len(self.passed)}")
        print(f"Warnings: {len(self.warnings)}")
        print(f"Issues: {len(self.issues)}")
        
        if self.issues:
            print("\\n⚠ CRITICAL ISSUES (Must resolve before application):")
            for issue in self.issues:
                print(f"  • {issue}")
        
        if self.warnings:
            print("\\n⚠ WARNINGS (Recommended to address):")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if not self.issues and not self.warnings:
            print("\\n✓ ALL CHECKS PASSED - Ready for federal application!")
        elif not self.issues:
            print("\\n✓ NO CRITICAL ISSUES - Address warnings before application")
        else:
            print("\\n✗ ISSUES FOUND - Resolve before submitting application")
        
        print("\\n" + "="*50)
        print("Next Steps:")
        if self.issues:
            print("1. Resolve all critical issues listed above")
            print("2. Re-run this check: python scripts/compliance_check.py")
        print("3. Review docs/FUNDING.md for application timeline")
        print("4. Monitor NTIA.gov for Spring 2026 NOFO release")
        print("="*50)

if __name__ == "__main__":
    print("Tribal Cybersecurity Platform - Federal Compliance Check")
    print("="*50)
    
    checker = ComplianceChecker()
    checker.check_ntia_config()
    checker.check_bia_config()
    checker.check_isac_config()
    checker.check_documentation()
    checker.check_templates()
    checker.generate_report()
    
    # Exit with appropriate code
    sys.exit(1 if checker.issues else 0)
'''

with open(f"{base_dir}/scripts/compliance_check.py", "w") as f:
    f.write(compliance_check_py)

os.chmod(f"{base_dir}/scripts/compliance_check.py", 0o755)
