# 1. FUNDING.md - Federal Funding Alignment Guide
funding_md = """# Federal Funding Alignment Guide

## Overview
This document maps Tribal Cyber Platform capabilities to active federal funding opportunities for 2026.

## Active Federal Opportunities (2026)

### 1. NTIA Tribal Broadband Connectivity Program (TBCP) - SPRING 2026
**Status**: New NOFO expected Spring 2026 | **Amount**: $500M+ available

**Alignment Points**:
- Cybersecurity as broadband infrastructure component
- Rural/remote deployment capabilities
- Digital equity enablement

**Required Documentation**:
- Broadband Security Architecture (see `docs/BROADBAND_SECURITY.md`)
- Tribal Consultation Protocol (see `docs/TRIBAL_CONSULTATION.md`)
- Economic Impact Assessment (see `templates/impact_assessment/`)

**Platform Features**:
- `src/security/broadband_protection.py` - DNS security, edge protection
- `src/compliance/ntia_tbcp.py` - Compliance validation

---

### 2. Bureau of Indian Affairs (BIA) - FY 2026
**Status**: Active via TPA reallocation | **Amount**: $461.2M TPA pool

**Alignment Points**:
- FASS-CMS Cloud security integration
- Public safety facility cybersecurity
- Self-determination contract support

**Required Documentation**:
- BIA Systems Integration Plan (see `src/compliance/bia_integration.py`)
- Tribal Priority Allocation justification

---

### 3. State Cybersecurity Grant Programs
**Example**: California SLCGP includes tribes ($9.6M available)

**Alignment Points**:
- Multi-entity collaboration tools
- State-tribal coordination protocols

---

## Expired Programs (Reference Only)
- ~~Tribal Cybersecurity Grant Program (TCGP)~~ - Ended Sept 2025

## Quick Start for Grant Writers

```bash
# Generate compliance report for specific funding source
python -m src.compliance.ntia_tbcp --generate-report

# Calculate economic impact metrics
python -m src.metrics.federal_reporting --impact-assessment
```

## Contact Information
- NTIA TBCP: [Check NTIA.gov for Spring 2026 NOFO]
- BIA Grants: https://www.bia.gov/bia/ots/grants
- Tribal-ISAC: https://www.tribalisac.org/
