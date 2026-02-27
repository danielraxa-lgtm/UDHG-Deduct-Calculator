#!/usr/bin/env python3
"""
Data Sync for OCIP/CCIP Web Portal
==================================
Syncs data between wrap-up manager database and web portal JSON files.

Features:
- Real-time dashboard data updates
- Automatic alert generation
- Status synchronization
- Compliance score calculation

Usage:
    python3 data-sync.py --sync-dashboard
    python3 data-sync.py --generate-alerts
    python3 data-sync.py --full-sync
"""

import json
import sqlite3
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import sys

class DataSync:
    
    def __init__(self, web_root: str = None, db_path: str = None):
        """Initialize data sync."""
        self.web_root = Path(web_root) if web_root else Path(__file__).parent.parent
        self.api_dir = self.web_root / "api"
        self.api_dir.mkdir(exist_ok=True)
        
        # Find wrap-up manager database
        if db_path and Path(db_path).exists():
            self.db_path = db_path
        else:
            possible_paths = [
                "/workspace/output/wrapup.db",
                "~/.openclaw/workspace/output/wrapup.db",
                "/tmp/wrapup_demo.db"
            ]
            self.db_path = None
            for path in possible_paths:
                full_path = Path(path).expanduser()
                if full_path.exists():
                    self.db_path = str(full_path)
                    break
            
            if self.db_path is None:
                print("⚠️  Wrap-up manager database not found. Using demo data.")
                self._create_demo_db()

    def _create_demo_db(self):
        """Create demo database for testing."""
        self.db_path = "/tmp/wrapup_sync_demo.db"
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        # Create tables
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS programs (
                id TEXT PRIMARY KEY,
                project_name TEXT NOT NULL,
                project_address TEXT,
                program_type TEXT DEFAULT 'OCIP',
                enrollment_status TEXT DEFAULT 'pending',
                bid_deduct_pct REAL DEFAULT 0,
                contract_value REAL DEFAULT 0,
                estimated_completion TEXT,
                contact_name TEXT,
                contact_email TEXT
            );
            
            CREATE TABLE IF NOT EXISTS payroll_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                program_id TEXT NOT NULL,
                due_date TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                payroll_amount REAL,
                submitted_date TEXT
            );
            
            CREATE TABLE IF NOT EXISTS enrollment_docs (
                program_id TEXT NOT NULL,
                document_type TEXT NOT NULL,
                status TEXT DEFAULT 'not_started',
                submitted_date TEXT
            );
        """)
        
        # Insert realistic demo data
        demo_programs = [
            ("WU-2026-001", "Riverside Development Phase II", "1245 Riverside Dr, Dallas TX", "OCIP", "enrolled", 3.5, 2850000, "2026-08-15", "Sarah Chen", "s.chen@riverside.com"),
            ("WU-2026-002", "Metro Office Complex", "890 Metro Blvd, Phoenix AZ", "CCIP", "pending", 4.2, 1650000, "2026-06-30", "Mike Rodriguez", "mrodriguez@metroffice.com"),
            ("WU-2026-003", "Industrial Park Expansion", "3400 Industrial Way, Seattle WA", "OCIP", "active", 3.8, 4200000, "2026-12-15", "Jennifer Walsh", "j.walsh@indpark.com"),
            ("WU-2026-004", "Healthcare Campus", "720 Medical Center Dr, Denver CO", "OCIP", "enrolled", 4.0, 3100000, "2026-10-30", "David Kumar", "d.kumar@healthcampus.org")
        ]
        
        for program in demo_programs:
            conn.execute("""
                INSERT OR REPLACE INTO programs 
                (id, project_name, project_address, program_type, enrollment_status, bid_deduct_pct, contract_value, estimated_completion, contact_name, contact_email)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, program)
        
        # Demo payroll reports with realistic dates
        payroll_data = [
            ("WU-2026-001", "2026-03-15", "pending", 125000, None),
            ("WU-2026-001", "2026-04-15", "pending", 0, None),
            ("WU-2026-002", "2026-03-01", "overdue", 85000, None),
            ("WU-2026-003", "2026-03-10", "submitted", 180000, "2026-03-08"),
            ("WU-2026-003", "2026-04-10", "pending", 0, None),
            ("WU-2026-004", "2026-03-20", "pending", 95000, None),
            ("WU-2026-004", "2026-04-20", "pending", 0, None)
        ]
        
        for payroll in payroll_data:
            conn.execute("""
                INSERT OR REPLACE INTO payroll_reports (program_id, due_date, status, payroll_amount, submitted_date)
                VALUES (?, ?, ?, ?, ?)
            """, payroll)
        
        # Demo enrollment docs
        doc_data = [
            ("WU-2026-001", "enrollment_form", "completed", "2026-01-15"),
            ("WU-2026-001", "insurance_verification", "completed", "2026-01-18"),
            ("WU-2026-001", "loss_history", "completed", "2026-01-20"),
            ("WU-2026-002", "enrollment_form", "pending", None),
            ("WU-2026-002", "insurance_verification", "not_started", None),
            ("WU-2026-003", "enrollment_form", "completed", "2026-02-01"),
            ("WU-2026-003", "waiver_request", "pending", None),
            ("WU-2026-004", "enrollment_form", "completed", "2026-02-10"),
            ("WU-2026-004", "insurance_verification", "completed", "2026-02-12"),
            ("WU-2026-004", "loss_history", "pending", None)
        ]
        
        for doc in doc_data:
            conn.execute("""
                INSERT OR REPLACE INTO enrollment_docs (program_id, document_type, status, submitted_date)
                VALUES (?, ?, ?, ?)
            """, doc)
        
        conn.commit()
        conn.close()
        print(f"✅ Demo database created at {self.db_path}")

    def get_programs_data(self):
        """Get programs data from database."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        programs = conn.execute("""
            SELECT * FROM programs ORDER BY project_name
        """).fetchall()
        
        result = []
        for program in programs:
            program_dict = dict(program)
            
            # Calculate compliance score
            program_dict['compliance_score'] = self._calculate_compliance_score(program['id'])
            
            # Get next deadline
            program_dict['payroll_due'] = self._get_next_deadline(program['id'])
            
            # Calculate estimated savings
            savings = (program['contract_value'] or 0) * (program['bid_deduct_pct'] or 0) / 100
            program_dict['estimated_savings'] = int(savings)
            
            # Set status based on enrollment
            if program['enrollment_status'] == 'enrolled':
                program_dict['status'] = 'active'
            elif program['enrollment_status'] == 'pending':
                program_dict['status'] = 'pending'
            else:
                program_dict['status'] = program['enrollment_status']
            
            # Add timestamp
            program_dict['last_updated'] = datetime.utcnow().isoformat() + 'Z'
            
            result.append(program_dict)
        
        conn.close()
        return result

    def _calculate_compliance_score(self, program_id: str) -> int:
        """Calculate compliance score for a program."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        # Check enrollment docs
        total_docs = conn.execute("""
            SELECT COUNT(*) as total FROM enrollment_docs WHERE program_id = ?
        """, (program_id,)).fetchone()
        total_docs = total_docs['total'] if total_docs else 0
        
        completed_docs = conn.execute("""
            SELECT COUNT(*) as completed FROM enrollment_docs 
            WHERE program_id = ? AND status = 'completed'
        """, (program_id,)).fetchone()
        completed_docs = completed_docs['completed'] if completed_docs else 0
        
        # Check payroll reports
        overdue_reports = conn.execute("""
            SELECT COUNT(*) as overdue FROM payroll_reports 
            WHERE program_id = ? AND status = 'overdue'
        """, (program_id,)).fetchone()
        overdue_reports = overdue_reports['overdue'] if overdue_reports else 0
        
        # Check if any pending reports are actually overdue
        today = datetime.now().date()
        actually_overdue = conn.execute("""
            SELECT COUNT(*) as overdue FROM payroll_reports 
            WHERE program_id = ? AND status = 'pending' AND date(due_date) < date('now')
        """, (program_id,)).fetchone()
        actually_overdue = actually_overdue['overdue'] if actually_overdue else 0
        
        conn.close()
        
        # Calculate score
        if total_docs == 0:
            doc_score = 50  # No docs required yet
        else:
            doc_score = (completed_docs / total_docs) * 70
        
        penalty = (overdue_reports + actually_overdue) * 15  # 15 points per overdue report
        score = max(0, min(100, doc_score + 30 - penalty))
        
        return int(score)

    def _get_next_deadline(self, program_id: str) -> str:
        """Get next upcoming deadline for a program."""
        conn = sqlite3.connect(self.db_path)
        
        deadline = conn.execute("""
            SELECT due_date FROM payroll_reports 
            WHERE program_id = ? AND status IN ('pending', 'overdue') 
            ORDER BY due_date LIMIT 1
        """, (program_id,)).fetchone()
        
        conn.close()
        
        if deadline:
            return deadline[0]
        return ""

    def generate_alerts(self, programs_data):
        """Generate alerts based on current program status."""
        alerts = []
        today = datetime.now().date()
        
        for program in programs_data:
            # Deadline alerts
            if program.get('payroll_due'):
                try:
                    due_date = datetime.strptime(program['payroll_due'], '%Y-%m-%d').date()
                    days_until = (due_date - today).days
                    
                    if days_until < 0:
                        alerts.append({
                            "type": "deadline",
                            "priority": "high",
                            "message": f"{program['project_name']} payroll report is {abs(days_until)} days overdue",
                            "program_id": program['id']
                        })
                    elif days_until <= 3:
                        alerts.append({
                            "type": "deadline", 
                            "priority": "high",
                            "message": f"{program['project_name']} payroll report due in {days_until} day(s) ({due_date.strftime('%B %d')})",
                            "program_id": program['id']
                        })
                    elif days_until <= 7:
                        alerts.append({
                            "type": "deadline",
                            "priority": "medium", 
                            "message": f"{program['project_name']} payroll report due in {days_until} days ({due_date.strftime('%B %d')})",
                            "program_id": program['id']
                        })
                except ValueError:
                    pass  # Invalid date format
            
            # Compliance alerts
            if program['compliance_score'] < 60:
                alerts.append({
                    "type": "compliance",
                    "priority": "high" if program['compliance_score'] < 40 else "medium",
                    "message": f"{program['project_name']} compliance score below {'40%' if program['compliance_score'] < 40 else '60%'} - missing enrollment docs",
                    "program_id": program['id']
                })
            
            # High-value program alerts
            if program.get('contract_value', 0) > 3000000 and program['compliance_score'] < 80:
                alerts.append({
                    "type": "financial",
                    "priority": "medium",
                    "message": f"{program['project_name']} is high-value (${program['contract_value']:,.0f}) with suboptimal compliance ({program['compliance_score']}%)",
                    "program_id": program['id']
                })
        
        return alerts

    def calculate_summary(self, programs_data):
        """Calculate summary metrics."""
        total_programs = len(programs_data)
        active_programs = len([p for p in programs_data if p['status'] == 'active'])
        pending_enrollment = len([p for p in programs_data if p['enrollment_status'] == 'pending'])
        
        total_contract_value = sum(p.get('contract_value', 0) for p in programs_data)
        estimated_total_savings = sum(p.get('estimated_savings', 0) for p in programs_data)
        
        compliance_scores = [p['compliance_score'] for p in programs_data if p['compliance_score'] > 0]
        avg_compliance_score = sum(compliance_scores) / len(compliance_scores) if compliance_scores else 0
        
        # Count upcoming deadlines
        today = datetime.now().date()
        upcoming_deadlines = 0
        for program in programs_data:
            if program.get('payroll_due'):
                try:
                    due_date = datetime.strptime(program['payroll_due'], '%Y-%m-%d').date()
                    if (due_date - today).days <= 14:
                        upcoming_deadlines += 1
                except ValueError:
                    pass
        
        return {
            "total_programs": total_programs,
            "active_programs": active_programs,
            "pending_enrollment": pending_enrollment,
            "upcoming_deadlines": upcoming_deadlines,
            "total_contract_value": int(total_contract_value),
            "estimated_total_savings": int(estimated_total_savings),
            "avg_compliance_score": int(avg_compliance_score)
        }

    def sync_dashboard_data(self):
        """Sync dashboard data from database to JSON files."""
        print("🔄 Syncing dashboard data...")
        
        # Get programs data
        programs_data = self.get_programs_data()
        print(f"   Found {len(programs_data)} programs")
        
        # Generate alerts
        alerts = self.generate_alerts(programs_data)
        print(f"   Generated {len(alerts)} alerts")
        
        # Calculate summary
        summary = self.calculate_summary(programs_data)
        
        # Create dashboard JSON
        dashboard_data = {
            "programs": programs_data,
            "summary": summary,
            "alerts": alerts,
            "last_sync": datetime.utcnow().isoformat() + 'Z'
        }
        
        # Write to API directory
        api_file = self.api_dir / "wrapup-status.json"
        with open(api_file, 'w') as f:
            json.dump(dashboard_data, f, indent=2)
        
        print(f"✅ Dashboard data synced to {api_file}")
        return dashboard_data

    def generate_program_detail(self, program_id: str):
        """Generate detailed data for a specific program."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        # Get program details
        program = conn.execute("""
            SELECT * FROM programs WHERE id = ?
        """, (program_id,)).fetchone()
        
        if not program:
            return None
        
        # Get payroll reports
        payroll_reports = conn.execute("""
            SELECT * FROM payroll_reports 
            WHERE program_id = ? 
            ORDER BY due_date DESC
        """, (program_id,)).fetchall()
        
        # Get enrollment docs
        enrollment_docs = conn.execute("""
            SELECT * FROM enrollment_docs 
            WHERE program_id = ?
            ORDER BY document_type
        """, (program_id,)).fetchall()
        
        conn.close()
        
        # Format data
        program_dict = dict(program)
        program_dict['compliance_score'] = self._calculate_compliance_score(program_id)
        program_dict['payroll_reports'] = [dict(row) for row in payroll_reports]
        program_dict['enrollment_docs'] = [dict(row) for row in enrollment_docs]
        
        return program_dict

    def full_sync(self):
        """Perform full synchronization."""
        print("🚀 Starting full sync...")
        
        # Sync dashboard
        dashboard_data = self.sync_dashboard_data()
        
        # Generate individual program details
        program_details_dir = self.api_dir / "programs"
        program_details_dir.mkdir(exist_ok=True)
        
        for program in dashboard_data['programs']:
            program_id = program['id']
            detail_data = self.generate_program_detail(program_id)
            
            if detail_data:
                detail_file = program_details_dir / f"{program_id}.json"
                with open(detail_file, 'w') as f:
                    json.dump(detail_data, f, indent=2)
        
        print(f"✅ Full sync completed. {len(dashboard_data['programs'])} programs synced.")
        
        # Print summary
        summary = dashboard_data['summary']
        print(f"\n📊 SUMMARY:")
        print(f"   Active Programs: {summary['active_programs']}")
        print(f"   Total Contract Value: ${summary['total_contract_value']:,}")
        print(f"   Estimated Savings: ${summary['estimated_total_savings']:,}")
        print(f"   Average Compliance: {summary['avg_compliance_score']}%")
        print(f"   Active Alerts: {len(dashboard_data['alerts'])}")

def main():
    parser = argparse.ArgumentParser(description='OCIP/CCIP Data Sync')
    parser.add_argument('--sync-dashboard', action='store_true', help='Sync dashboard data only')
    parser.add_argument('--generate-alerts', action='store_true', help='Generate alerts only')
    parser.add_argument('--full-sync', action='store_true', help='Perform full synchronization')
    parser.add_argument('--web-root', help='Web portal root directory')
    parser.add_argument('--db-path', help='Path to wrap-up manager database')
    
    args = parser.parse_args()
    
    if not any([args.sync_dashboard, args.generate_alerts, args.full_sync]):
        parser.print_help()
        return
    
    sync = DataSync(args.web_root, args.db_path)
    
    if args.sync_dashboard:
        sync.sync_dashboard_data()
    
    if args.generate_alerts:
        programs_data = sync.get_programs_data()
        alerts = sync.generate_alerts(programs_data)
        print(f"Generated {len(alerts)} alerts:")
        for alert in alerts:
            priority_icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
            print(f"  {priority_icon.get(alert['priority'], '•')} {alert['message']}")
    
    if args.full_sync:
        sync.full_sync()

if __name__ == '__main__':
    main()