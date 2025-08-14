#!/usr/bin/env python3
"""
Production server runner for log classification API
"""
import os
from app import app

if __name__ == '__main__':
    # Production settings
    port = int(os.environ.get('PORT', 5000))
    
    # For production, use 0.0.0.0 to accept external connections
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )
