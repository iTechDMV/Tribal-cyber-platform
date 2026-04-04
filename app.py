#!/usr/bin/env python3
"""
Tribal Cybersecurity Compliance Platform (TCCP)
Sovereign Systems — Native-owned cybersecurity for tribal nations.

A NIST 800-171 mapped, TCGP grant-ready compliance platform
designed for the 574 federally recognized tribal nations.
"""

import os
import json
import secrets
import hashlib
import sqlite3
from datetime import datetime
from functools import wraps
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, jsonify, g, make_response
)

# ═══════════════════════════════════════════════════════════════════════════════
# APP CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['DATABASE'] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'instance', 'tribal_cyber.db'
)

# ═══════════════════════════════════════════════════════════════════════════════
# NIST 800-171 Rev 2 — CONTROL FAMILIES (Representative Controls)
# 14 families, ~60 key controls covering the full framework
# ═══════════════════════════════════════════════════════════════════════════════

NIST_FAMILIES = [
    {
        'id': 'AC', 'name': 'Access Control', 'icon': 'shield-lock',
        'controls': [
            {'id': '3.1.1', 'desc': 'Limit system access to authorized users, processes acting on behalf of authorized users, or devices.', 'weight': 5},
            {'id': '3.1.2', 'desc': 'Limit system access to the types of transactions and functions that authorized users are permitted to execute.', 'weight': 5},
            {'id': '3.1.3', 'desc': 'Control the flow of CUI in accordance with approved authorizations.', 'weight': 3},
            {'id': '3.1.5', 'desc': 'Employ the principle of least privilege, including for specific security functions and privileged accounts.', 'weight': 5},
            {'id': '3.1.8', 'desc': 'Limit unsuccessful logon attempts.', 'weight': 3},
            {'id': '3.1.12', 'desc': 'Monitor and control remote access sessions.', 'weight': 5},
            {'id': '3.1.13', 'desc': 'Employ cryptographic mechanisms to protect the confidentiality of remote access sessions.', 'weight': 5},
            {'id': '3.1.16', 'desc': 'Authorize wireless access prior to allowing such connections.', 'weight': 3},
            {'id': '3.1.20', 'desc': 'Verify and control/limit connections to and use of external information systems.', 'weight': 3},
        ]
    },
    {
        'id': 'AT', 'name': 'Awareness & Training', 'icon': 'mortarboard',
        'controls': [
            {'id': '3.2.1', 'desc': 'Ensure that managers, systems administrators, and users of organizational systems are made aware of the security risks.', 'weight': 3},
            {'id': '3.2.2', 'desc': 'Ensure that personnel are trained to carry out their assigned information security-related duties and responsibilities.', 'weight': 3},
            {'id': '3.2.3', 'desc': 'Provide security awareness training on recognizing and reporting potential indicators of insider threat.', 'weight': 1},
        ]
    },
    {
        'id': 'AU', 'name': 'Audit & Accountability', 'icon': 'journal-check',
        'controls': [
            {'id': '3.3.1', 'desc': 'Create and retain system audit logs and records to the extent needed to enable monitoring, analysis, investigation, and reporting.', 'weight': 5},
            {'id': '3.3.2', 'desc': 'Ensure that the actions of individual system users can be uniquely traced to those users.', 'weight': 5},
            {'id': '3.3.5', 'desc': 'Correlate audit record review, analysis, and reporting processes for investigation and response.', 'weight': 3},
            {'id': '3.3.8', 'desc': 'Protect audit information and audit logging tools from unauthorized access, modification, and deletion.', 'weight': 5},
            {'id': '3.3.9', 'desc': 'Limit management of audit logging functionality to a subset of privileged users.', 'weight': 3},
        ]
    },
    {
        'id': 'CM', 'name': 'Configuration Management', 'icon': 'gear',
        'controls': [
            {'id': '3.4.1', 'desc': 'Establish and maintain baseline configurations and inventories of organizational systems.', 'weight': 5},
            {'id': '3.4.2', 'desc': 'Establish and enforce security configuration settings for IT products employed in organizational systems.', 'weight': 5},
            {'id': '3.4.3', 'desc': 'Track, review, approve or disapprove, and log changes to organizational systems.', 'weight': 3},
            {'id': '3.4.5', 'desc': 'Define, document, approve, and enforce physical and logical access restrictions associated with changes.', 'weight': 3},
            {'id': '3.4.6', 'desc': 'Employ the principle of least functionality by configuring systems to provide only essential capabilities.', 'weight': 3},
        ]
    },
    {
        'id': 'IA', 'name': 'Identification & Authentication', 'icon': 'fingerprint',
        'controls': [
            {'id': '3.5.1', 'desc': 'Identify information system users, processes acting on behalf of users, or devices.', 'weight': 5},
            {'id': '3.5.2', 'desc': 'Authenticate (or verify) the identities of those users, processes, or devices as a prerequisite to allowing access.', 'weight': 5},
            {'id': '3.5.3', 'desc': 'Use multifactor authentication for local and network access to privileged accounts and for network access to non-privileged accounts.', 'weight': 5},
            {'id': '3.5.7', 'desc': 'Enforce a minimum password complexity and change of characters when new passwords are created.', 'weight': 3},
            {'id': '3.5.10', 'desc': 'Store and transmit only cryptographically-protected passwords.', 'weight': 5},
        ]
    },
    {
        'id': 'IR', 'name': 'Incident Response', 'icon': 'exclamation-triangle',
        'controls': [
            {'id': '3.6.1', 'desc': 'Establish an operational incident-handling capability for organizational systems that includes preparation, detection, analysis, containment, recovery, and user response activities.', 'weight': 5},
            {'id': '3.6.2', 'desc': 'Track, document, and report incidents to designated officials and/or authorities both internal and external to the organization.', 'weight': 5},
            {'id': '3.6.3', 'desc': 'Test the organizational incident response capability.', 'weight': 3},
        ]
    },
    {
        'id': 'MA', 'name': 'Maintenance', 'icon': 'wrench-adjustable',
        'controls': [
            {'id': '3.7.1', 'desc': 'Perform maintenance on organizational systems.', 'weight': 1},
            {'id': '3.7.2', 'desc': 'Provide controls on the tools, techniques, mechanisms, and personnel used to conduct system maintenance.', 'weight': 3},
            {'id': '3.7.5', 'desc': 'Require multifactor authentication to establish nonlocal maintenance sessions and terminate such sessions when nonlocal maintenance is complete.', 'weight': 3},
        ]
    },
    {
        'id': 'MP', 'name': 'Media Protection', 'icon': 'device-hdd',
        'controls': [
            {'id': '3.8.1', 'desc': 'Protect (i.e., physically control and securely store) system media containing CUI, both paper and digital.', 'weight': 3},
            {'id': '3.8.3', 'desc': 'Sanitize or destroy system media containing CUI before disposal or release for reuse.', 'weight': 5},
            {'id': '3.8.5', 'desc': 'Control access to media containing CUI and maintain accountability for media during transport outside of controlled areas.', 'weight': 3},
            {'id': '3.8.9', 'desc': 'Protect the confidentiality of backup CUI at storage locations.', 'weight': 3},
        ]
    },
    {
        'id': 'PS', 'name': 'Personnel Security', 'icon': 'person-badge',
        'controls': [
            {'id': '3.9.1', 'desc': 'Screen individuals prior to authorizing access to organizational systems containing CUI.', 'weight': 3},
            {'id': '3.9.2', 'desc': 'Ensure that organizational systems containing CUI are protected during and after personnel actions such as terminations and transfers.', 'weight': 5},
        ]
    },
    {
        'id': 'PE', 'name': 'Physical Protection', 'icon': 'building-lock',
        'controls': [
            {'id': '3.10.1', 'desc': 'Limit physical access to organizational systems, equipment, and the respective operating environments to authorized individuals.', 'weight': 5},
            {'id': '3.10.2', 'desc': 'Protect and monitor the physical facility and support infrastructure for organizational systems.', 'weight': 3},
            {'id': '3.10.3', 'desc': 'Escort visitors and monitor visitor activity.', 'weight': 1},
            {'id': '3.10.6', 'desc': 'Enforce safeguarding measures for CUI at alternate work sites.', 'weight': 3},
        ]
    },
    {
        'id': 'RA', 'name': 'Risk Assessment', 'icon': 'clipboard-data',
        'controls': [
            {'id': '3.11.1', 'desc': 'Periodically assess the risk to organizational operations, organizational assets, and individuals.', 'weight': 5},
            {'id': '3.11.2', 'desc': 'Scan for vulnerabilities in organizational systems and applications periodically and when new vulnerabilities are identified.', 'weight': 5},
            {'id': '3.11.3', 'desc': 'Remediate vulnerabilities in accordance with risk assessments.', 'weight': 5},
        ]
    },
    {
        'id': 'CA', 'name': 'Security Assessment', 'icon': 'search',
        'controls': [
            {'id': '3.12.1', 'desc': 'Periodically assess the security controls in organizational systems to determine if the controls are effective.', 'weight': 5},
            {'id': '3.12.2', 'desc': 'Develop and implement plans of action designed to correct deficiencies and reduce or eliminate vulnerabilities.', 'weight': 5},
            {'id': '3.12.3', 'desc': 'Monitor security controls on an ongoing basis to ensure the continued effectiveness of the controls.', 'weight': 3},
            {'id': '3.12.4', 'desc': 'Develop, document, and periodically update system security plans.', 'weight': 5},
        ]
    },
    {
        'id': 'SC', 'name': 'System & Communications Protection', 'icon': 'hdd-network',
        'controls': [
            {'id': '3.13.1', 'desc': 'Monitor, control, and protect communications at the external boundaries and key internal boundaries of organizational systems.', 'weight': 5},
            {'id': '3.13.2', 'desc': 'Employ architectural designs, software development techniques, and systems engineering principles that promote effective information security.', 'weight': 3},
            {'id': '3.13.5', 'desc': 'Implement subnetworks for publicly accessible system components that are physically or logically separated from internal networks.', 'weight': 5},
            {'id': '3.13.8', 'desc': 'Implement cryptographic mechanisms to prevent unauthorized disclosure of CUI during transmission.', 'weight': 5},
            {'id': '3.13.11', 'desc': 'Employ FIPS-validated cryptography when used to protect the confidentiality of CUI.', 'weight': 5},
            {'id': '3.13.16', 'desc': 'Protect the confidentiality of CUI at rest.', 'weight': 5},
        ]
    },
    {
        'id': 'SI', 'name': 'System & Information Integrity', 'icon': 'shield-check',
        'controls': [
            {'id': '3.14.1', 'desc': 'Identify, report, and correct information and information system flaws in a timely manner.', 'weight': 5},
            {'id': '3.14.2', 'desc': 'Provide protection from malicious code at appropriate locations within organizational systems.', 'weight': 5},
            {'id': '3.14.3', 'desc': 'Monitor system security alerts and advisories and take action in response.', 'weight': 3},
            {'id': '3.14.6', 'desc': 'Monitor organizational systems, including inbound and outbound communications traffic, to detect attacks and indicators of potential attacks.', 'weight': 5},
            {'id': '3.14.7', 'desc': 'Identify unauthorized use of organizational systems.', 'weight': 3},
        ]
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# TCGP — FOUR OBJECTIVES (Tribal Cybersecurity Grant Program)
# ═══════════════════════════════════════════════════════════════════════════════

TCGP_OBJECTIVES = [
    {
        'id': 1,
        'title': 'Cyber Governance Planning',
        'icon': 'clipboard2-check',
        'color': '#0d9488',
        'description': 'Develop and establish cybersecurity governance plans that document strategic objectives, priorities, and resource planning.',
        'tasks': [
            'Designate a cybersecurity lead or coordinator',
            'Develop a written cybersecurity governance plan',
            'Establish formal cybersecurity policies and procedures',
            'Define roles and responsibilities for cybersecurity',
            'Create an incident response plan',
            'Establish a cybersecurity budget',
            'Document and maintain IT asset inventory',
        ]
    },
    {
        'id': 2,
        'title': 'Assess & Evaluate Infrastructure',
        'icon': 'pc-display-horizontal',
        'color': '#2563eb',
        'description': 'Conduct comprehensive assessments of existing cybersecurity infrastructure to identify vulnerabilities and gaps.',
        'tasks': [
            'Conduct a comprehensive network assessment',
            'Perform vulnerability scanning of all systems',
            'Inventory all hardware, software, and data assets',
            'Assess current security control effectiveness',
            'Identify gaps against NIST 800-171 framework',
            'Document findings in a formal risk assessment report',
        ]
    },
    {
        'id': 3,
        'title': 'Implement Security Protections',
        'icon': 'lock',
        'color': '#7c3aed',
        'description': 'Deploy technical and procedural security protections to address identified vulnerabilities and strengthen overall posture.',
        'tasks': [
            'Deploy multi-factor authentication (MFA)',
            'Implement endpoint detection and response (EDR)',
            'Configure network segmentation and firewalls',
            'Deploy encrypted communications (VPN, TLS)',
            'Establish backup and disaster recovery procedures',
            'Implement access control and least privilege policies',
            'Deploy security information and event management (SIEM)',
        ]
    },
    {
        'id': 4,
        'title': 'Ensure Cyber Workforce Readiness',
        'icon': 'people',
        'color': '#ea580c',
        'description': 'Build and maintain a cybersecurity-aware workforce through training, exercises, and continuing education.',
        'tasks': [
            'Conduct cybersecurity awareness training for all staff',
            'Provide specialized training for IT personnel',
            'Implement phishing simulation exercises',
            'Establish continuing education requirements',
            'Cross-train backup personnel for critical IT roles',
            'Document training completion and certifications',
        ]
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# DATABASE LAYER
# ═══════════════════════════════════════════════════════════════════════════════

def get_db():
    if 'db' not in g:
        os.makedirs(os.path.dirname(app.config['DATABASE']), exist_ok=True)
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            tribe_name TEXT NOT NULL,
            contact_name TEXT DEFAULT '',
            contact_email TEXT DEFAULT '',
            role TEXT DEFAULT 'admin',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS controls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            family TEXT NOT NULL,
            control_id TEXT NOT NULL,
            description TEXT NOT NULL,
            weight INTEGER DEFAULT 3,
            status TEXT DEFAULT 'not_started',
            notes TEXT DEFAULT '',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS tcgp_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            objective_id INTEGER NOT NULL,
            task_text TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            notes TEXT DEFAULT '',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS training_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            member_name TEXT NOT NULL,
            member_role TEXT DEFAULT '',
            training_name TEXT NOT NULL,
            status TEXT DEFAULT 'not_started',
            due_date TEXT DEFAULT '',
            completion_date TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS governance_sections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            section_key TEXT NOT NULL,
            section_title TEXT NOT NULL,
            content TEXT DEFAULT '',
            sort_order INTEGER DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    ''')
    db.commit()

def seed_user_data(user_id):
    """Seed NIST controls and TCGP tasks for a new user."""
    db = get_db()
    for family in NIST_FAMILIES:
        for ctrl in family['controls']:
            db.execute(
                'INSERT INTO controls (user_id, family, control_id, description, weight) VALUES (?, ?, ?, ?, ?)',
                (user_id, family['id'], ctrl['id'], ctrl['desc'], ctrl['weight'])
            )
    for obj in TCGP_OBJECTIVES:
        for task in obj['tasks']:
            db.execute(
                'INSERT INTO tcgp_tasks (user_id, objective_id, task_text) VALUES (?, ?, ?)',
                (user_id, obj['id'], task)
            )
    # Seed governance plan sections
    gov_sections = [
        ('executive_summary', 'Executive Summary', 0),
        ('scope', 'Scope & Objectives', 1),
        ('governance_structure', 'Governance Structure', 2),
        ('roles', 'Roles & Responsibilities', 3),
        ('risk_assessment', 'Risk Assessment Summary', 4),
        ('current_posture', 'Current Security Posture', 5),
        ('implementation_roadmap', 'Implementation Roadmap', 6),
        ('training_plan', 'Training & Workforce Plan', 7),
        ('incident_response', 'Incident Response Plan', 8),
        ('budget', 'Budget & Resource Planning', 9),
        ('timeline', 'Timeline & Milestones', 10),
    ]
    for key, title, order in gov_sections:
        db.execute(
            'INSERT INTO governance_sections (user_id, section_key, section_title, sort_order) VALUES (?, ?, ?, ?)',
            (user_id, key, title, order)
        )
    db.commit()

# ═══════════════════════════════════════════════════════════════════════════════
# AUTHENTICATION
# ═══════════════════════════════════════════════════════════════════════════════

def hash_password(password):
    salt = 'sovereign_systems_tccp'
    return hashlib.sha256(f'{salt}{password}'.encode()).hexdigest()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access the platform.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ═══════════════════════════════════════════════════════════════════════════════
# HELPER — METRICS CALCULATION
# ═══════════════════════════════════════════════════════════════════════════════

def get_dashboard_metrics(user_id):
    db = get_db()
    
    # NIST compliance
    total_controls = db.execute(
        'SELECT COUNT(*) FROM controls WHERE user_id = ?', (user_id,)
    ).fetchone()[0]
    implemented = db.execute(
        "SELECT COUNT(*) FROM controls WHERE user_id = ? AND status = 'implemented'", (user_id,)
    ).fetchone()[0]
    in_progress = db.execute(
        "SELECT COUNT(*) FROM controls WHERE user_id = ? AND status = 'in_progress'", (user_id,)
    ).fetchone()[0]
    not_applicable = db.execute(
        "SELECT COUNT(*) FROM controls WHERE user_id = ? AND status = 'not_applicable'", (user_id,)
    ).fetchone()[0]
    
    applicable = total_controls - not_applicable
    compliance_pct = round(implemented / applicable * 100) if applicable > 0 else 0
    
    # SPRS Score calculation
    total_weight = db.execute(
        "SELECT COALESCE(SUM(weight), 0) FROM controls WHERE user_id = ? AND status != 'not_applicable'", (user_id,)
    ).fetchone()[0]
    implemented_weight = db.execute(
        "SELECT COALESCE(SUM(weight), 0) FROM controls WHERE user_id = ? AND status = 'implemented'", (user_id,)
    ).fetchone()[0]
    penalty = total_weight - implemented_weight
    sprs_score = 110 - penalty
    
    # Risk score (inverse of compliance)
    risk_score = 100 - compliance_pct
    if risk_score >= 80:
        risk_level = 'Critical'
        risk_color = '#dc2626'
    elif risk_score >= 60:
        risk_level = 'High'
        risk_color = '#ea580c'
    elif risk_score >= 40:
        risk_level = 'Medium'
        risk_color = '#ca8a04'
    elif risk_score >= 20:
        risk_level = 'Low'
        risk_color = '#2563eb'
    else:
        risk_level = 'Minimal'
        risk_color = '#16a34a'
    
    # TCGP progress
    total_tasks = db.execute(
        'SELECT COUNT(*) FROM tcgp_tasks WHERE user_id = ?', (user_id,)
    ).fetchone()[0]
    completed_tasks = db.execute(
        'SELECT COUNT(*) FROM tcgp_tasks WHERE user_id = ? AND completed = 1', (user_id,)
    ).fetchone()[0]
    tcgp_pct = round(completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # Per-family stats
    family_stats = []
    for fam in NIST_FAMILIES:
        f_total = db.execute(
            "SELECT COUNT(*) FROM controls WHERE user_id = ? AND family = ? AND status != 'not_applicable'",
            (user_id, fam['id'])
        ).fetchone()[0]
        f_done = db.execute(
            "SELECT COUNT(*) FROM controls WHERE user_id = ? AND family = ? AND status = 'implemented'",
            (user_id, fam['id'])
        ).fetchone()[0]
        f_prog = db.execute(
            "SELECT COUNT(*) FROM controls WHERE user_id = ? AND family = ? AND status = 'in_progress'",
            (user_id, fam['id'])
        ).fetchone()[0]
        family_stats.append({
            'id': fam['id'], 'name': fam['name'], 'icon': fam['icon'],
            'total': f_total, 'done': f_done, 'in_progress': f_prog,
            'pct': round(f_done / f_total * 100) if f_total > 0 else 0
        })
    
    # Per-objective stats
    obj_stats = []
    for obj in TCGP_OBJECTIVES:
        o_total = db.execute(
            'SELECT COUNT(*) FROM tcgp_tasks WHERE user_id = ? AND objective_id = ?',
            (user_id, obj['id'])
        ).fetchone()[0]
        o_done = db.execute(
            'SELECT COUNT(*) FROM tcgp_tasks WHERE user_id = ? AND objective_id = ? AND completed = 1',
            (user_id, obj['id'])
        ).fetchone()[0]
        obj_stats.append({
            'id': obj['id'], 'title': obj['title'], 'icon': obj['icon'],
            'color': obj['color'], 'total': o_total, 'done': o_done,
            'pct': round(o_done / o_total * 100) if o_total > 0 else 0
        })
    
    # Training stats
    training_total = db.execute(
        'SELECT COUNT(*) FROM training_records WHERE user_id = ?', (user_id,)
    ).fetchone()[0]
    training_done = db.execute(
        "SELECT COUNT(*) FROM training_records WHERE user_id = ? AND status = 'completed'", (user_id,)
    ).fetchone()[0]
    
    return {
        'total_controls': total_controls,
        'implemented': implemented,
        'in_progress': in_progress,
        'not_applicable': not_applicable,
        'applicable': applicable,
        'compliance_pct': compliance_pct,
        'sprs_score': sprs_score,
        'risk_score': risk_score,
        'risk_level': risk_level,
        'risk_color': risk_color,
        'tcgp_pct': tcgp_pct,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'family_stats': family_stats,
        'obj_stats': obj_stats,
        'training_total': training_total,
        'training_done': training_done,
    }

# ═══════════════════════════════════════════════════════════════════════════════
# ROUTES — AUTH
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Please enter both username and password.', 'danger')
            return render_template('login.html')
        
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()
        
        if user and user['password_hash'] == hash_password(password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['tribe_name'] = user['tribe_name']
            session['role'] = user['role']
            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        tribe_name = request.form.get('tribe_name', '').strip()
        contact_name = request.form.get('contact_name', '').strip()
        contact_email = request.form.get('contact_email', '').strip()
        
        if not all([username, password, tribe_name]):
            flash('Username, password, and tribe name are required.', 'danger')
            return render_template('login.html', register=True)
        
        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return render_template('login.html', register=True)
        
        if len(password) < 8:
            flash('Password must be at least 8 characters.', 'danger')
            return render_template('login.html', register=True)
        
        db = get_db()
        existing = db.execute(
            'SELECT id FROM users WHERE username = ?', (username,)
        ).fetchone()
        
        if existing:
            flash('Username already exists.', 'danger')
            return render_template('login.html', register=True)
        
        cursor = db.execute(
            'INSERT INTO users (username, password_hash, tribe_name, contact_name, contact_email) VALUES (?, ?, ?, ?, ?)',
            (username, hash_password(password), tribe_name, contact_name, contact_email)
        )
        db.commit()
        user_id = cursor.lastrowid
        
        # Seed NIST controls and TCGP tasks
        seed_user_data(user_id)
        
        session['user_id'] = user_id
        session['username'] = username
        session['tribe_name'] = tribe_name
        session['role'] = 'admin'
        
        flash(f'Welcome to TCCP, {username}! Your compliance workspace has been initialized.', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('login.html', register=True)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# ═══════════════════════════════════════════════════════════════════════════════
# ROUTES — MAIN PAGES
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/dashboard')
@login_required
def dashboard():
    metrics = get_dashboard_metrics(session['user_id'])
    return render_template('dashboard.html', **metrics)

@app.route('/assessment')
@login_required
def assessment():
    db = get_db()
    user_id = session['user_id']
    
    families_data = []
    for fam in NIST_FAMILIES:
        controls = db.execute(
            'SELECT * FROM controls WHERE user_id = ? AND family = ? ORDER BY control_id',
            (user_id, fam['id'])
        ).fetchall()
        
        total = len(controls)
        done = sum(1 for c in controls if c['status'] == 'implemented')
        prog = sum(1 for c in controls if c['status'] == 'in_progress')
        na = sum(1 for c in controls if c['status'] == 'not_applicable')
        applicable = total - na
        pct = round(done / applicable * 100) if applicable > 0 else 0
        
        families_data.append({
            'id': fam['id'],
            'name': fam['name'],
            'icon': fam['icon'],
            'controls': [dict(c) for c in controls],
            'total': total,
            'done': done,
            'in_progress': prog,
            'pct': pct,
        })
    
    # Overall stats
    total_all = db.execute('SELECT COUNT(*) FROM controls WHERE user_id = ?', (user_id,)).fetchone()[0]
    done_all = db.execute("SELECT COUNT(*) FROM controls WHERE user_id = ? AND status = 'implemented'", (user_id,)).fetchone()[0]
    na_all = db.execute("SELECT COUNT(*) FROM controls WHERE user_id = ? AND status = 'not_applicable'", (user_id,)).fetchone()[0]
    applicable_all = total_all - na_all
    overall_pct = round(done_all / applicable_all * 100) if applicable_all > 0 else 0
    
    return render_template('assessment.html',
        families=families_data,
        overall_pct=overall_pct,
        total_controls=total_all,
        implemented=done_all,
    )

@app.route('/governance')
@login_required
def governance():
    db = get_db()
    user_id = session['user_id']
    
    sections = db.execute(
        'SELECT * FROM governance_sections WHERE user_id = ? ORDER BY sort_order',
        (user_id,)
    ).fetchall()
    
    metrics = get_dashboard_metrics(user_id)
    
    return render_template('governance.html',
        sections=[dict(s) for s in sections],
        metrics=metrics,
    )

@app.route('/training')
@login_required
def training():
    db = get_db()
    user_id = session['user_id']
    
    records = db.execute(
        'SELECT * FROM training_records WHERE user_id = ? ORDER BY created_at DESC',
        (user_id,)
    ).fetchall()
    
    # TCGP Objective 4 tasks
    obj4_tasks = db.execute(
        'SELECT * FROM tcgp_tasks WHERE user_id = ? AND objective_id = 4 ORDER BY id',
        (user_id,)
    ).fetchall()
    
    total = len(records)
    completed = sum(1 for r in records if r['status'] == 'completed')
    in_progress = sum(1 for r in records if r['status'] == 'in_progress')
    
    return render_template('training.html',
        records=[dict(r) for r in records],
        obj4_tasks=[dict(t) for t in obj4_tasks],
        total=total,
        completed=completed,
        in_progress=in_progress,
    )

@app.route('/reports')
@login_required
def reports():
    metrics = get_dashboard_metrics(session['user_id'])
    return render_template('reports.html', metrics=metrics)

# ═══════════════════════════════════════════════════════════════════════════════
# API ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/api/control/<int:control_id>', methods=['POST'])
@login_required
def update_control(control_id):
    db = get_db()
    data = request.get_json()
    status = data.get('status', 'not_started')
    notes = data.get('notes', '')
    
    db.execute(
        'UPDATE controls SET status = ?, notes = ?, updated_at = ? WHERE id = ? AND user_id = ?',
        (status, notes, datetime.now().isoformat(), control_id, session['user_id'])
    )
    db.commit()
    
    # Return updated metrics
    metrics = get_dashboard_metrics(session['user_id'])
    return jsonify({'success': True, 'metrics': {
        'compliance_pct': metrics['compliance_pct'],
        'sprs_score': metrics['sprs_score'],
        'risk_score': metrics['risk_score'],
        'risk_level': metrics['risk_level'],
    }})

@app.route('/api/tcgp/<int:task_id>', methods=['POST'])
@login_required
def update_tcgp_task(task_id):
    db = get_db()
    data = request.get_json()
    completed = 1 if data.get('completed') else 0
    notes = data.get('notes', '')
    
    db.execute(
        'UPDATE tcgp_tasks SET completed = ?, notes = ?, updated_at = ? WHERE id = ? AND user_id = ?',
        (completed, notes, datetime.now().isoformat(), task_id, session['user_id'])
    )
    db.commit()
    return jsonify({'success': True})

@app.route('/api/training/add', methods=['POST'])
@login_required
def add_training():
    db = get_db()
    data = request.get_json()
    
    db.execute(
        'INSERT INTO training_records (user_id, member_name, member_role, training_name, status, due_date, notes) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (session['user_id'], data.get('member_name', ''), data.get('member_role', ''),
         data.get('training_name', ''), data.get('status', 'not_started'),
         data.get('due_date', ''), data.get('notes', ''))
    )
    db.commit()
    return jsonify({'success': True})

@app.route('/api/training/<int:record_id>', methods=['POST'])
@login_required
def update_training(record_id):
    db = get_db()
    data = request.get_json()
    
    db.execute(
        'UPDATE training_records SET status = ?, completion_date = ?, notes = ? WHERE id = ? AND user_id = ?',
        (data.get('status', 'not_started'), data.get('completion_date', ''),
         data.get('notes', ''), record_id, session['user_id'])
    )
    db.commit()
    return jsonify({'success': True})

@app.route('/api/training/<int:record_id>/delete', methods=['POST'])
@login_required
def delete_training(record_id):
    db = get_db()
    db.execute('DELETE FROM training_records WHERE id = ? AND user_id = ?', (record_id, session['user_id']))
    db.commit()
    return jsonify({'success': True})

@app.route('/api/governance/save', methods=['POST'])
@login_required
def save_governance():
    db = get_db()
    data = request.get_json()
    section_id = data.get('section_id')
    content = data.get('content', '')
    
    db.execute(
        'UPDATE governance_sections SET content = ?, updated_at = ? WHERE id = ? AND user_id = ?',
        (content, datetime.now().isoformat(), section_id, session['user_id'])
    )
    db.commit()
    return jsonify({'success': True})

@app.route('/api/governance/generate', methods=['POST'])
@login_required
def generate_governance():
    """Auto-generate governance plan content based on assessment data."""
    db = get_db()
    user_id = session['user_id']
    tribe_name = session.get('tribe_name', 'Tribal Nation')
    metrics = get_dashboard_metrics(user_id)
    now = datetime.now().strftime('%B %d, %Y')
    
    # Generate content for each section
    generated = {
        'executive_summary': f'This Cybersecurity Governance Plan establishes the strategic framework for {tribe_name} to protect its information systems, digital assets, and the personal data of tribal members. As of {now}, the tribe has achieved {metrics["compliance_pct"]}% compliance with NIST 800-171 controls ({metrics["implemented"]} of {metrics["applicable"]} applicable controls implemented). This plan outlines the governance structure, risk posture, implementation roadmap, and workforce development strategy to achieve full compliance and strengthen the tribe\'s cybersecurity posture.',
        
        'scope': f'This plan applies to all information systems, networks, and digital assets owned, operated, or managed by {tribe_name}. It covers:\n\n- All tribal government IT infrastructure\n- Data systems containing member information\n- Financial and administrative systems\n- Communication networks\n- Third-party systems with tribal data access\n\nThe objectives of this plan are to:\n1. Establish a cybersecurity governance framework aligned with NIST 800-171\n2. Protect Controlled Unclassified Information (CUI) and tribal member data\n3. Meet TCGP grant compliance requirements\n4. Reduce cybersecurity risk from {metrics["risk_level"]} ({metrics["risk_score"]}%) to Low (<20%)',
        
        'governance_structure': f'{tribe_name} Cybersecurity Governance Structure:\n\n- Tribal Council: Ultimate authority for cybersecurity policy and budget approval\n- Cybersecurity Lead/Coordinator: Day-to-day oversight of security operations\n- IT Staff: Implementation and maintenance of security controls\n- Department Heads: Compliance within their respective departments\n- All Staff: Adherence to security policies and reporting of incidents',
        
        'roles': f'Key Cybersecurity Roles for {tribe_name}:\n\n1. Chief Information Security Officer (CISO) / Cybersecurity Lead\n   - Develop and maintain security policies\n   - Oversee risk assessments and compliance\n   - Report to Tribal Council on security posture\n   - Manage incident response\n\n2. IT Administrator(s)\n   - Implement technical security controls\n   - Monitor systems and networks\n   - Perform vulnerability assessments\n   - Maintain backup and recovery systems\n\n3. Department Managers\n   - Ensure staff compliance with security policies\n   - Report security incidents\n   - Manage access requests for their teams\n\n4. All Personnel\n   - Complete required security awareness training\n   - Follow password and access policies\n   - Report suspicious activity immediately',
    }
    
    # Build risk assessment based on family stats
    risk_lines = []
    for fs in metrics['family_stats']:
        status = 'Complete' if fs['pct'] == 100 else f'{fs["pct"]}% implemented'
        risk_lines.append(f'- {fs["name"]} ({fs["id"]}): {status} ({fs["done"]}/{fs["total"]} controls)')
    
    generated['risk_assessment'] = f'Current Risk Level: {metrics["risk_level"]} ({metrics["risk_score"]}%)\nSPRS Score: {metrics["sprs_score"]} (Range: -203 to +110)\nDate Assessed: {now}\n\nControl Family Status:\n' + '\n'.join(risk_lines)
    
    generated['current_posture'] = f'As of {now}, {tribe_name} has:\n\n- Implemented {metrics["implemented"]} of {metrics["applicable"]} applicable NIST 800-171 controls\n- {metrics["in_progress"]} controls currently in progress\n- Overall compliance rate: {metrics["compliance_pct"]}%\n- TCGP objective completion: {metrics["tcgp_pct"]}%\n- Training records tracked: {metrics["training_total"]} ({metrics["training_done"]} completed)\n\nThe current SPRS score is {metrics["sprs_score"]}, with a target of 110 (full compliance).'
    
    # Gap analysis for roadmap
    gap_families = [fs for fs in metrics['family_stats'] if fs['pct'] < 100]
    gap_families.sort(key=lambda x: x['pct'])
    roadmap_lines = []
    for i, gf in enumerate(gap_families[:5], 1):
        remaining = gf['total'] - gf['done']
        roadmap_lines.append(f'{i}. {gf["name"]}: {remaining} controls remaining ({gf["pct"]}% complete)')
    
    generated['implementation_roadmap'] = f'Priority Implementation Areas (by gap severity):\n\n' + '\n'.join(roadmap_lines) + f'\n\nTarget: Achieve 100% NIST 800-171 compliance within 12-18 months.\n\nPhase 1 (Months 1-3): Address critical access control and authentication gaps\nPhase 2 (Months 4-6): Implement audit, monitoring, and incident response capabilities\nPhase 3 (Months 7-9): Complete configuration management and media protection\nPhase 4 (Months 10-12): Full assessment, documentation, and continuous monitoring\nPhase 5 (Months 13-18): Optimization, testing, and third-party validation'
    
    generated['training_plan'] = f'Workforce Development Plan:\n\n- Total training records: {metrics["training_total"]}\n- Completed: {metrics["training_done"]}\n\nRequired Training Programs:\n1. Cybersecurity Awareness Training — All staff, annual requirement\n2. Phishing Recognition & Reporting — All staff, quarterly simulations\n3. NIST 800-171 Compliance — IT staff, upon hire and annually\n4. Incident Response Procedures — IT staff and management, semi-annually\n5. Insider Threat Awareness — All staff, annual requirement\n6. Data Handling & CUI Protection — Staff handling sensitive data, upon hire\n\nAll training completion must be documented and certificates retained.'
    
    generated['incident_response'] = f'{tribe_name} Incident Response Plan Framework:\n\n1. PREPARATION\n   - Maintain incident response team contact list\n   - Ensure incident detection tools are operational\n   - Conduct tabletop exercises quarterly\n\n2. DETECTION & ANALYSIS\n   - Monitor system logs and security alerts\n   - Classify incident severity (Low/Medium/High/Critical)\n   - Document initial findings\n\n3. CONTAINMENT\n   - Isolate affected systems immediately\n   - Preserve forensic evidence\n   - Notify cybersecurity lead within 1 hour\n\n4. ERADICATION & RECOVERY\n   - Remove threat from all systems\n   - Restore from clean backups\n   - Verify system integrity before reconnection\n\n5. POST-INCIDENT\n   - Conduct lessons learned review within 5 business days\n   - Update security controls as needed\n   - Report to CISA if CUI is involved (within 72 hours)\n   - Document for compliance records'
    
    generated['budget'] = f'Cybersecurity Budget Framework for {tribe_name}:\n\nCategory 1: Personnel\n- Cybersecurity Lead/CISO (FTE or contracted)\n- IT Administrator(s)\n- Training and certification costs\n\nCategory 2: Technology\n- Endpoint Detection & Response (EDR)\n- Firewall and network security appliances\n- Multi-factor authentication (MFA) solution\n- SIEM or log management platform\n- Backup and disaster recovery\n- Vulnerability scanning tools\n\nCategory 3: Services\n- Managed Security Service Provider (MSSP) if needed\n- Penetration testing (annual)\n- Third-party security assessment\n- Cybersecurity insurance\n\nCategory 4: Training\n- Security awareness platform\n- Phishing simulation service\n- Staff certification (CompTIA Security+, CISSP, etc.)\n\nNote: Many of these costs are eligible for reimbursement under TCGP grants.'
    
    generated['timeline'] = f'Implementation Timeline:\n\nMonth 1-2: Governance & Planning\n- Appoint cybersecurity lead\n- Complete asset inventory\n- Conduct initial risk assessment\n- Finalize this governance plan\n\nMonth 3-4: Critical Controls\n- Deploy MFA across all systems\n- Implement access control policies\n- Configure audit logging\n- Establish backup procedures\n\nMonth 5-6: Network & Infrastructure\n- Deploy firewalls and segmentation\n- Implement encryption (at rest and in transit)\n- Configure endpoint protection\n- Begin vulnerability scanning\n\nMonth 7-9: Operations & Monitoring\n- Deploy SIEM/monitoring\n- Establish incident response capability\n- Conduct first tabletop exercise\n- Implement change management\n\nMonth 10-12: Workforce & Validation\n- Complete all staff training\n- Conduct security assessment\n- Update SPRS score\n- Prepare TCGP grant reporting\n\nMonth 13-18: Continuous Improvement\n- Ongoing monitoring and optimization\n- Third-party assessment\n- Annual plan review and update'
    
    # Save all generated content
    for key, content in generated.items():
        db.execute(
            'UPDATE governance_sections SET content = ?, updated_at = ? WHERE user_id = ? AND section_key = ?',
            (content, datetime.now().isoformat(), user_id, key)
        )
    db.commit()
    
    return jsonify({'success': True, 'message': 'Governance plan generated successfully.'})

@app.route('/governance/export')
@login_required
def governance_export():
    """Generate a printable governance plan document."""
    db = get_db()
    user_id = session['user_id']
    tribe_name = session.get('tribe_name', 'Tribal Nation')
    
    sections = db.execute(
        'SELECT * FROM governance_sections WHERE user_id = ? ORDER BY sort_order',
        (user_id,)
    ).fetchall()
    
    metrics = get_dashboard_metrics(user_id)
    
    return render_template('report_print.html',
        report_type='Governance Plan Document',
        tribe_name=tribe_name,
        metrics=metrics,
        generated_date=datetime.now().strftime('%B %d, %Y'),
        sections=[dict(s) for s in sections],
    )

@app.route('/api/reports/compliance')
@login_required
def report_compliance():
    """Generate a printable compliance summary report."""
    metrics = get_dashboard_metrics(session['user_id'])
    tribe_name = session.get('tribe_name', 'Tribal Nation')
    return render_template('report_print.html',
        report_type='Compliance Summary Report',
        tribe_name=tribe_name,
        metrics=metrics,
        generated_date=datetime.now().strftime('%B %d, %Y'),
    )

@app.route('/api/reports/gap-analysis')
@login_required
def report_gap_analysis():
    """Generate a gap analysis report."""
    db = get_db()
    user_id = session['user_id']
    metrics = get_dashboard_metrics(user_id)
    
    # Get all non-implemented controls
    gaps = db.execute(
        "SELECT * FROM controls WHERE user_id = ? AND status NOT IN ('implemented', 'not_applicable') ORDER BY weight DESC, family, control_id",
        (user_id,)
    ).fetchall()
    
    tribe_name = session.get('tribe_name', 'Tribal Nation')
    return render_template('report_print.html',
        report_type='Gap Analysis Report',
        tribe_name=tribe_name,
        metrics=metrics,
        gaps=[dict(g) for g in gaps],
        generated_date=datetime.now().strftime('%B %d, %Y'),
        nist_families={f['id']: f['name'] for f in NIST_FAMILIES},
    )

@app.route('/api/reports/tcgp-export')
@login_required
def report_tcgp():
    """Generate TCGP grant application data export."""
    db = get_db()
    user_id = session['user_id']
    metrics = get_dashboard_metrics(user_id)
    
    tasks = db.execute(
        'SELECT * FROM tcgp_tasks WHERE user_id = ? ORDER BY objective_id, id',
        (user_id,)
    ).fetchall()
    
    tribe_name = session.get('tribe_name', 'Tribal Nation')
    return render_template('report_print.html',
        report_type='TCGP Grant Application Data',
        tribe_name=tribe_name,
        metrics=metrics,
        tcgp_tasks=[dict(t) for t in tasks],
        tcgp_objectives=TCGP_OBJECTIVES,
        generated_date=datetime.now().strftime('%B %d, %Y'),
    )

# ═══════════════════════════════════════════════════════════════════════════════
# APP INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
