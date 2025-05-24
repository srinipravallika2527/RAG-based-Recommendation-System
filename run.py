#!/usr/bin/env python
"""
Run script for the Renewable Energy Forecasting Web Application

This script launches the Flask web application for the Renewable Energy
Forecasting system. It sets up the necessary environment variables,
configures logging, and starts the application server.

Usage:
    python run.py [--debug] [--port PORT] [--host HOST]

Options:
    --debug     Run in debug mode
    --port      Specify the port to run on (default: 5000)
    --host      Specify the host to run on (default: 0.0.0.0)
"""

import os
import sys
import argparse
import logging
from logging.handlers import RotatingFileHandler

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask application
from web_app.app import app

def setup_logging(debug=False):
    """Configure logging for the application"""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    # Set up logging
    log_level = logging.DEBUG if debug else logging.INFO
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Set up file handler for application logs
    file_handler = RotatingFileHandler(
        'logs/app.log', 
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=10
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    
    # Add file handler to app logger
    app_logger = logging.getLogger('web_app')
    app_logger.addHandler(file_handler)
    
    # Log startup information
    app_logger.info('Starting Renewable Energy Forecasting application')
    if debug:
        app_logger.info('Running in DEBUG mode')

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Run the Renewable Energy Forecasting web application')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the application on')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to run the application on')
    return parser.parse_args()

def main():
    """Main function to run the application"""
    # Parse command line arguments
    args = parse_arguments()
    
    # Set up logging
    setup_logging(args.debug)
    
    # Create required directories
    for directory in ['uploads', 'models', 'results']:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    # Set Flask environment variables
    os.environ['FLASK_ENV'] = 'development' if args.debug else 'production'
    
    # Run the application
    app.run(
        debug=args.debug,
        host=args.host,
        port=args.port
    )

if __name__ == '__main__':
    main()