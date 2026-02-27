#!/usr/bin/env python3
"""
OCIP/CCIP Compliance Reporter
============================
Automated report generation for wrap-up program compliance tracking.

Features:
- Weekly compliance scorecards  
- Deadline monitoring and alerts
- Financial impact analysis
- Integration with wrap-up manager backend

Usage:
    python3 compliance-reporter.py --weekly-report
    python3 compliance-reporter.py --deadline-check
    python3 compliance-reporter.py --financial-summary
"""

import json
import sqlite3
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import sys
import os

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

class ComplianceReporter:
    
    def __init__(self, db_path: str = None):
        """Initialize compliance reporter."""
        if db_path is None:
            # Try to find wrap-up manager database
            possible_paths = [
                "/workspace/output/wrapup.db",
                "~/.openclaw/workspace/output/wrapup.db", 
                "../output/wrapup.db"
            ]
            self.db_path = None
            for path in possible_paths:
                full_path = Path(path).expanduser()
                if full_path.exists():
                    self.db_path = str(full_path)
                    break
            
            if self.db_path is None:
                self.db_path = "/tmp/wrapup_demo.db"
                self._create_demo_data()
        else:
            self.db_path = db_path
            
    def _create_demo_data(self):
        """Create demo data for testing."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        # Create tables
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS programs (
                id TEXT PRIMARY KEY,
                project_name TEXT NOT NULL,
                program_type TEXT DEFAULT 'OCIP',
                enrollment_status TEXT DEFAULT 'pending',
                bid_deduct_pct REAL DEFAULT 0,
                contract_value REAL DEFAULT 0,
                estimated_completion TEXT
            );
            
            CREATE TABLE IF NOT EXISTS payroll_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                program_id TEXT NOT NULL,
                due_date TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                payroll_amount REAL
            );
            
            CREATE TABLE IF NOT EXISTS enrollment_docs (
                program_id TEXT NOT NULL,
                document_type TEXT NOT NULL,
                status TEXT DEFAULT 'not_started'
            );
        """)
        
        # Insert demo data
        demo_programs = [
            ("WU-2026-001", "Riverside Development Phase II", "OCIP", "enrolled", 3.5, 2850000, "2026-08-15"),
            ("WU-2026-002", "Metro Office Complex", "CCIP", "pending", 4.2, 1650000, "2026-06-30"),
            ("WU-2026-003", "Industrial Park Expansion", "OCIP", "active", 3.8, 4200000, "2026-12-15")
        ]
        
        for program in demo_programs:
            conn.execute("""
                INSERT OR REPLACE INTO programs 
                (id, project_name, program_type, enrollment_status, bid_deduct_pct, contract_value, estimated_completion)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, program)
        
        # Demo payroll reports
        payroll_data = [
            ("WU-2026-001", "2026-03-15", "pending", 125000),
            ("WU-2026-001", "2026-04-15", "pending", 0),
            ("WU-2026-002", "2026-03-01", "overdue", 85000),
            ("WU-2026-003", "2026-03-10", "submitted", 180000)
        ]
        
        for payroll in payroll_data:
            conn.execute("""
                INSERT OR REPLACE INTO payroll_reports (program_id, due_date, status, payroll_amount)
                VALUES (?, ?, ?, ?)
            """, payroll)
        
        # Demo enrollment docs
        doc_data = [
            ("WU-2026-001", "enrollment_form", "completed"),
            ("WU-2026-001", "insurance_verification", "completed"), 
            ("WU-2026-001", "loss_history", "completed"),
            ("WU-2026-002", "enrollment_form", "pending"),
            ("WU-2026-002", "insurance_verification", "not_started"),
            ("WU-2026-003", "enrollment_form", "completed"),
            ("WU-2026-003", "waiver_request", "pending")
        ]
        
        for doc in doc_data:
            conn.execute("""
                INSERT OR REPLACE INTO enrollment_docs (program_id, document_type, status)
                VALUES (?, ?, ?)
            """, doc)
        
        conn.commit()
        conn.close()
        print(f"Demo database created at {self.db_path}")

    def get_programs(self) -> List[Dict]:
        """Get all programs with current status."""
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
            program_dict['next_deadline'] = self._get_next_deadline(program['id'])
            
            # Calculate estimated savings
            savings = (program['contract_value'] or 0) * (program['bid_deduct_pct'] or 0) / 100
            program_dict['estimated_savings'] = savings
            
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
        """, (program_id,)).fetchone()['total']
        
        completed_docs = conn.execute("""
            SELECT COUNT(*) as completed FROM enrollment_docs 
            WHERE program_id = ? AND status = 'completed'
        """, (program_id,)).fetchone()['completed']
        
        # Check payroll reports
        overdue_reports = conn.execute("""
            SELECT COUNT(*) as overdue FROM payroll_reports 
            WHERE program_id = ? AND status = 'overdue'
        """, (program_id,)).fetchone()['overdue']
        
        conn.close()
        
        # Calculate score
        if total_docs == 0:
            doc_score = 50  # No docs required yet
        else:
            doc_score = (completed_docs / total_docs) * 70
        
        penalty = overdue_reports * 15  # 15 points per overdue report
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

    def generate_weekly_report(self) -> Dict[str, Any]:
        """Generate weekly compliance report."""
        programs = self.get_programs()
        
        # Calculate summary metrics
        total_programs = len(programs)
        active_programs = len([p for p in programs if p['enrollment_status'] in ['enrolled', 'active']])
        avg_compliance = sum(p['compliance_score'] for p in programs) / total_programs if total_programs > 0 else 0
        total_savings = sum(p['estimated_savings'] for p in programs)
        
        # Find issues
        compliance_issues = [p for p in programs if p['compliance_score'] < 70]
        upcoming_deadlines = []
        
        for program in programs:
            if program['next_deadline']:
                deadline_date = datetime.strptime(program['next_deadline'], '%Y-%m-%d')
                days_until = (deadline_date - datetime.now()).days
                if days_until <= 7:
                    upcoming_deadlines.append({
                        'program': program['project_name'],
                        'deadline': program['next_deadline'],
                        'days_until': days_until
                    })
        
        return {
            'report_date': datetime.now().strftime('%Y-%m-%d'),
            'summary': {
                'total_programs': total_programs,
                'active_programs': active_programs,
                'avg_compliance_score': round(avg_compliance, 1),
                'total_estimated_savings': total_savings
            },
            'programs': programs,
            'compliance_issues': compliance_issues,
            'upcoming_deadlines': upcoming_deadlines,
            'recommendations': self._generate_recommendations(compliance_issues, upcoming_deadlines)
        }

    def _generate_recommendations(self, issues: List[Dict], deadlines: List[Dict]) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        if issues:
            recommendations.append(f"🔴 {len(issues)} programs have compliance scores below 70% - prioritize document completion")
        
        if deadlines:
            urgent = [d for d in deadlines if d['days_until'] <= 3]
            if urgent:
                recommendations.append(f"⏰ {len(urgent)} payroll reports due within 3 days - immediate action required")
        
        high_value_low_compliance = [
            p for p in issues if p.get('contract_value', 0) > 2000000
        ]
        if high_value_low_compliance:
            recommendations.append("💰 High-value contracts have compliance issues - potential savings at risk")
        
        if not recommendations:
            recommendations.append("✅ All programs are performing well - maintain current compliance levels")
        
        return recommendations

    def check_deadlines(self) -> Dict[str, Any]:
        """Check for upcoming deadlines and generate alerts."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        today = datetime.now().date()
        alerts = []
        
        # Check payroll deadlines
        upcoming = conn.execute("""
            SELECT pr.*, p.project_name, p.program_type 
            FROM payroll_reports pr
            JOIN programs p ON pr.program_id = p.id
            WHERE pr.status IN ('pending', 'overdue')
            AND date(pr.due_date) BETWEEN date('now') AND date('now', '+14 days')
            ORDER BY pr.due_date
        """).fetchall()
        
        for report in upcoming:
            due_date = datetime.strptime(report['due_date'], '%Y-%m-%d').date()
            days_until = (due_date - today).days
            
            if days_until < 0:
                priority = 'critical'
                message = f"OVERDUE: {report['project_name']} payroll report was due {abs(days_until)} days ago"
            elif days_until <= 2:
                priority = 'high'
                message = f"URGENT: {report['project_name']} payroll report due in {days_until} day(s)"
            elif days_until <= 7:
                priority = 'medium'
                message = f"Upcoming: {report['project_name']} payroll report due in {days_until} days"
            else:
                priority = 'low'
                message = f"Scheduled: {report['project_name']} payroll report due in {days_until} days"
            
            alerts.append({
                'type': 'deadline',
                'priority': priority,
                'message': message,
                'program_id': report['program_id'],
                'due_date': report['due_date'],
                'days_until': days_until
            })
        
        conn.close()
        
        return {
            'check_date': today.strftime('%Y-%m-%d'),
            'alerts': alerts,
            'summary': {
                'total_alerts': len(alerts),
                'critical': len([a for a in alerts if a['priority'] == 'critical']),
                'high': len([a for a in alerts if a['priority'] == 'high']),
                'medium': len([a for a in alerts if a['priority'] == 'medium'])
            }
        }

    def financial_summary(self) -> Dict[str, Any]:
        """Generate financial impact summary."""
        programs = self.get_programs()
        
        total_contract_value = sum(p.get('contract_value', 0) for p in programs)
        total_estimated_savings = sum(p['estimated_savings'] for p in programs)
        
        # Group by program type
        by_type = {}
        for program in programs:
            ptype = program.get('program_type', 'Unknown')
            if ptype not in by_type:
                by_type[ptype] = {
                    'count': 0,
                    'contract_value': 0,
                    'estimated_savings': 0,
                    'avg_bid_deduct': 0
                }
            
            by_type[ptype]['count'] += 1
            by_type[ptype]['contract_value'] += program.get('contract_value', 0)
            by_type[ptype]['estimated_savings'] += program['estimated_savings']
        
        # Calculate averages
        for ptype in by_type:
            if by_type[ptype]['count'] > 0:
                total_deduct = sum(p.get('bid_deduct_pct', 0) for p in programs if p.get('program_type') == ptype)
                by_type[ptype]['avg_bid_deduct'] = total_deduct / by_type[ptype]['count']
        
        return {
            'report_date': datetime.now().strftime('%Y-%m-%d'),
            'totals': {
                'total_programs': len(programs),
                'total_contract_value': total_contract_value,
                'total_estimated_savings': total_estimated_savings,
                'savings_percentage': (total_estimated_savings / total_contract_value * 100) if total_contract_value > 0 else 0
            },
            'by_program_type': by_type,
            'top_programs': sorted(
                programs, 
                key=lambda x: x['estimated_savings'], 
                reverse=True
            )[:5]
        }

def main():
    parser = argparse.ArgumentParser(description='OCIP/CCIP Compliance Reporter')
    parser.add_argument('--weekly-report', action='store_true', help='Generate weekly compliance report')
    parser.add_argument('--deadline-check', action='store_true', help='Check upcoming deadlines')
    parser.add_argument('--financial-summary', action='store_true', help='Generate financial summary')
    parser.add_argument('--output', default='console', choices=['console', 'json', 'html'], help='Output format')
    parser.add_argument('--db-path', help='Path to wrap-up manager database')
    
    args = parser.parse_args()
    
    if not any([args.weekly_report, args.deadline_check, args.financial_summary]):
        parser.print_help()
        return
    
    reporter = ComplianceReporter(args.db_path)
    
    if args.weekly_report:
        report = reporter.generate_weekly_report()
        print("\n📊 WEEKLY COMPLIANCE REPORT")
        print("=" * 50)
        print(f"Report Date: {report['report_date']}")
        print(f"Total Programs: {report['summary']['total_programs']}")
        print(f"Active Programs: {report['summary']['active_programs']}")
        print(f"Average Compliance: {report['summary']['avg_compliance_score']}%")
        print(f"Total Estimated Savings: ${report['summary']['total_estimated_savings']:,.0f}")
        
        if report['compliance_issues']:
            print(f"\n⚠️  COMPLIANCE ISSUES ({len(report['compliance_issues'])} programs)")
            for issue in report['compliance_issues']:
                print(f"  • {issue['project_name']}: {issue['compliance_score']}%")
        
        if report['upcoming_deadlines']:
            print(f"\n⏰ UPCOMING DEADLINES ({len(report['upcoming_deadlines'])} reports)")
            for deadline in report['upcoming_deadlines']:
                print(f"  • {deadline['program']} due in {deadline['days_until']} days ({deadline['deadline']})")
        
        print("\n💡 RECOMMENDATIONS:")
        for rec in report['recommendations']:
            print(f"  • {rec}")
    
    if args.deadline_check:
        alerts = reporter.check_deadlines()
        print(f"\n⏰ DEADLINE CHECK - {alerts['check_date']}")
        print("=" * 40)
        print(f"Total Alerts: {alerts['summary']['total_alerts']}")
        print(f"Critical: {alerts['summary']['critical']} | High: {alerts['summary']['high']} | Medium: {alerts['summary']['medium']}")
        
        if alerts['alerts']:
            print("\nALERT DETAILS:")
            for alert in alerts['alerts']:
                priority_icon = {'critical': '🔴', 'high': '🟡', 'medium': '🟠', 'low': '🟢'}
                print(f"  {priority_icon.get(alert['priority'], '•')} {alert['message']}")
        else:
            print("\n✅ No upcoming deadlines within the next 14 days")
    
    if args.financial_summary:
        summary = reporter.financial_summary()
        print(f"\n💰 FINANCIAL SUMMARY - {summary['report_date']}")
        print("=" * 45)
        totals = summary['totals']
        print(f"Total Contract Value: ${totals['total_contract_value']:,.0f}")
        print(f"Total Estimated Savings: ${totals['total_estimated_savings']:,.0f}")
        print(f"Overall Savings Rate: {totals['savings_percentage']:.1f}%")
        
        print("\nBY PROGRAM TYPE:")
        for ptype, data in summary['by_program_type'].items():
            print(f"  {ptype}: {data['count']} programs, ${data['estimated_savings']:,.0f} savings ({data['avg_bid_deduct']:.1f}% avg deduct)")
        
        print(f"\nTOP 5 PROGRAMS BY SAVINGS:")
        for i, program in enumerate(summary['top_programs'][:5], 1):
            print(f"  {i}. {program['project_name']}: ${program['estimated_savings']:,.0f}")

if __name__ == '__main__':
    main()