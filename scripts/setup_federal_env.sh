# 2. Create setup script
setup_script = '''#!/bin/bash
# Setup script for Tribal Cybersecurity Platform
# Configures environment for federal compliance

echo "======================================"
echo "Tribal Cybersecurity Platform Setup"
echo "Federal Compliance Edition"
echo "======================================"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install pyyaml requests

# Create necessary directories
echo "Creating directory structure..."
mkdir -p logs
mkdir -p reports
mkdir -p data/tribal_records

# Check configuration files
echo "Checking configuration files..."
if [ ! -f "config/ntia_config.yaml" ]; then
    echo "⚠ config/ntia_config.yaml not found - copying from template"
    cp config/ntia_config.yaml.template config/ntia_config.yaml
fi

if [ ! -f "config/bia_integration.yaml" ]; then
    echo "⚠ config/bia_integration.yaml not found - copying from template"
    cp config/bia_integration.yaml.template config/bia_integration.yaml
fi

if [ ! -f "config/tribal_isac.yaml" ]; then
    echo "⚠ config/tribal_isac.yaml not found - copying from template"
    cp config/tribal_isac.yaml.template config/tribal_isac.yaml
fi

echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "Next Steps:"
echo "1. Edit config/ntia_config.yaml with your Tribal information"
echo "2. Edit config/bia_integration.yaml with BIA details"
echo "3. Edit config/tribal_isac.yaml with Tribal-ISAC info"
echo "4. Run compliance check: python scripts/compliance_check.py"
echo "5. Review docs/FUNDING.md for application guidance"
echo ""
echo "Federal Compliance Checklist:"
echo "[ ] SAM.gov registration active"
echo "[ ] UEI obtained"
echo "[ ] Tribal Council resolution drafted"
echo "[ ] Consultation meetings scheduled"
echo "[ ] Cybersecurity plan completed"
echo ""
echo "For NTIA TBCP 2026:"
echo "Monitor NTIA.gov for Spring 2026 NOFO release"
echo ""
'''

with open(f"{base_dir}/scripts/setup_federal_env.sh", "w") as f:
    f.write(setup_script)

# Make executable
import os
os.chmod(f"{base_dir}/scripts/setup_federal_env.sh", 0o755)
