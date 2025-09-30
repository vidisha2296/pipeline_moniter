import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any

class PipelineDatabase:
    def __init__(self, db_path: str = "pipeline_events.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pipeline_events (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                status TEXT NOT NULL,
                failure_type TEXT,
                component TEXT,
                details TEXT NOT NULL
            )
        ''')
        
        # Create recovery attempts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recovery_attempts (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                failure_type TEXT NOT NULL,
                success BOOLEAN NOT NULL,
                message TEXT NOT NULL,
                action_taken TEXT NOT NULL,
                related_event_id TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_event(self, event: Dict[str, Any]):
        """Store a pipeline event in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO pipeline_events 
            (id, timestamp, event_type, status, failure_type, component, details)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            event.get('id', ''),
            event.get('timestamp', '').isoformat() if hasattr(event.get('timestamp'), 'isoformat') else str(event.get('timestamp', '')),
            event.get('event_type', ''),
            event.get('status', ''),
            event.get('failure_type', ''),
            event.get('component', ''),
            json.dumps(event.get('details', {}))
        ))
        
        conn.commit()
        conn.close()
    
    def store_recovery_attempt(self, recovery: Dict[str, Any]):
        """Store a recovery attempt in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO recovery_attempts 
            (id, timestamp, failure_type, success, message, action_taken, related_event_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            recovery.get('id', ''),
            recovery.get('timestamp', '').isoformat() if hasattr(recovery.get('timestamp'), 'isoformat') else str(recovery.get('timestamp', '')),
            recovery.get('failure_type', ''),
            recovery.get('success', False),
            recovery.get('message', ''),
            recovery.get('action_taken', ''),
            recovery.get('related_event_id', '')
        ))
        
        conn.commit()
        conn.close()
    
    def get_recent_events(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent pipeline events"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM pipeline_events 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        events = []
        for row in cursor.fetchall():
            events.append({
                'id': row[0],
                'timestamp': row[1],
                'event_type': row[2],
                'status': row[3],
                'failure_type': row[4],
                'component': row[5],
                'details': json.loads(row[6])
            })
        
        conn.close()
        return events
    
    def get_recovery_attempts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent recovery attempts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM recovery_attempts 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        recoveries = []
        for row in cursor.fetchall():
            recoveries.append({
                'id': row[0],
                'timestamp': row[1],
                'failure_type': row[2],
                'success': bool(row[3]),
                'message': row[4],
                'action_taken': row[5],
                'related_event_id': row[6]
            })
        
        conn.close()
        return recoveries