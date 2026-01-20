# Update the config file
cat > config/google_sheets_config.py << 'EOF'
"""
Google Sheets Configuration for PC-MLRA
"""

# Google Sheets Configuration
GOOGLE_SHEETS_CONFIG = {
    # Your actual Sheet ID
    "SHEET_ID": "1qzzqiK1rrMqiUPX3JGSTSGFP3JKUCLDrp9i4XLAMPq0",
    
    # Sheet names
    "SHEET_NAMES": {
        "sessions": "user_sessions",
        "queries": "query_logs", 
        "clause_usage": "clause_usage",
        "system_metrics": "system_metrics",
        "errors": "error_logs"
    },
    
    # Column headers for each sheet
    "COLUMNS": {
        "user_sessions": [
            "session_id", "user_ip", "user_agent", "start_time",
            "end_time", "total_queries", "country", "device_type",
            "platform", "browser", "screen_resolution"
        ],
        
        "query_logs": [
            "log_id", "session_id", "timestamp", "user_query",
            "detected_intent", "matched_clause_ids", "category",
            "response_preview", "response_length", "processing_time_ms",
            "proof_requested", "system_mode", "http_status"
        ],
        
        "clause_usage": [
            "date", "clause_id", "clause_title", "usage_count",
            "document", "category", "last_used"
        ],
        
        "system_metrics": [
            "timestamp", "total_queries", "unique_sessions",
            "avg_response_time", "most_used_intent", "most_used_clause",
            "error_count", "uptime_percentage"
        ],
        
        "error_logs": [
            "error_id", "timestamp", "session_id", "error_type",
            "error_message", "stack_trace", "query_context",
            "user_agent", "resolved"
        ]
    },
    
    # Privacy settings
    "PRIVACY": {
        "anonymize_ip": True,
        "truncate_queries": 500,
        "remove_phi": True,
        "log_errors_only": False
    },
    
    # Performance settings
    "PERFORMANCE": {
        "batch_size": 10,
        "max_retries": 3,
        "timeout_seconds": 10,
        "async_logging": True
    }
}

# Use relative path (works both locally and on Render)
CREDENTIALS_FILE = "config/google_sheets_credentials.json"

# Logging level
LOG_LEVEL = "INFO"
EOF