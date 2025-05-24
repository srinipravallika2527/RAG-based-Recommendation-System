#!/usr/bin/env python
"""
Setup script for the Renewable Energy Forecasting project.

This script performs the initial setup for the project:
1. Creates the necessary directory structure
2. Downloads sample data files
3. Sets up the virtual environment
4. Installs required dependencies

Usage:
    python setup.py [--no-download] [--no-venv]

Options:
    --no-download  Skip downloading sample data
    --no-venv      Skip virtual environment setup
"""

import os
import sys
import argparse
import subprocess
import logging
import platform
import shutil
from pathlib import Path
import urllib.request
import zipfile
import tempfile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent

# Data URLs
SAMPLE_DATA_URLS = {
    'opsd': 'https://data.open-power-system-data.org/time_series/2020-10-06/time_series_60min_singleindex.csv',
    'era5': 'https://example.com/sample_era5_data.zip'  # Example URL, would need to be updated
}

def create_directory_structure():
    """Create the necessary directory structure for the project"""
    logger.info("Creating directory structure...")
    
    # Create main directories
    directories = [
        'data/raw/opsd',
        'data/raw/era5',
        'data/processed',
        'data/models',
        'logs',
        'models',
        'results',
        'uploads',
        'web_app/static/css',
        'web_app/static/js',
        'web_app/static/img',
        'web_app/templates',
        'notebooks',
        'docs/images'
    ]
    
    for directory in directories:
        dir_path = ROOT_DIR / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")
    
    logger.info("Directory structure created successfully.")

def download_sample_data():
    """Download sample data files"""
    logger.info("Downloading sample data...")
    
    # Download OPSD data
    opsd_url = SAMPLE_DATA_URLS['opsd']
    opsd_path = ROOT_DIR / 'data/raw/opsd/time_series_60min_singleindex.csv'
    
    try:
        logger.info(f"Downloading OPSD data from {opsd_url}")
        urllib.request.urlretrieve(opsd_url, opsd_path)
        logger.info(f"Downloaded OPSD data to {opsd_path}")
    except Exception as e:
        logger.error(f"Failed to download OPSD data: {e}")
    
    # Download ERA5 data (mock - in a real setup, this would use the CDS API)
    # For this example, we'll just create a placeholder file
    era5_path = ROOT_DIR / 'data/raw/era5/sample_era5_data.nc'
    with open(era5_path, 'w') as f:
        f.write("# This is a placeholder for ERA5 data\n")
        f.write("# In a real setup, you would use the CDS API to download actual data\n")
    logger.info(f"Created ERA5 data placeholder at {era5_path}")
        
    logger.info("Sample data setup completed.")

def setup_virtual_environment():
    """Set up a virtual environment and install dependencies"""
    logger.info("Setting up virtual environment...")
    
    # Determine the python executable to use
    python_exec = sys.executable
    
    # Check if venv module is available
    try:
        import venv
        venv_available = True
    except ImportError:
        venv_available = False
        logger.warning("Python venv module not available. Will try virtualenv instead.")
    
    # Determine virtual environment path and activation script
    venv_path = ROOT_DIR / 'venv'
    if platform.system() == 'Windows':
        activate_script = venv_path / 'Scripts' / 'activate'
        python_path = venv_path / 'Scripts' / 'python.exe'
    else:
        activate_script = venv_path / 'bin' / 'activate'
        python_path = venv_path / 'bin' / 'python'
    
    # Create virtual environment
    if venv_path.exists():
        logger.info(f"Virtual environment already exists at {venv_path}")
    else:
        try:
            if venv_available:
                logger.info(f"Creating virtual environment using venv at {venv_path}")
                subprocess.run([python_exec, '-m', 'venv', str(venv_path)], check=True)
            else:
                # Try using virtualenv if venv is not available
                logger.info(f"Creating virtual environment using virtualenv at {venv_path}")
                subprocess.run([python_exec, '-m', 'pip', 'install', 'virtualenv'], check=True)
                subprocess.run([python_exec, '-m', 'virtualenv', str(venv_path)], check=True)
                
            logger.info("Virtual environment created successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create virtual environment: {e}")
            return
    
    # Install dependencies
    try:
        if platform.system() == 'Windows':
            # On Windows, we need to run a batch file to activate the environment
            command = f'"{python_path}" -m pip install -r requirements.ini'
            logger.info(f"Installing dependencies: {command}")
            subprocess.run(command, shell=True, check=True)
        else:
            # On Unix-like systems, we can use the source command
            command = f'"{python_path}" -m pip install -r requirements.ini'
            logger.info(f"Installing dependencies: {command}")
            subprocess.run(command, shell=True, check=True)
            
        logger.info("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {e}")
        
    # Print activation instructions
    if platform.system() == 'Windows':
        logger.info(f"\nTo activate the virtual environment, run:\n  {activate_script}")
    else:
        logger.info(f"\nTo activate the virtual environment, run:\n  source {activate_script}")

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Setup the Renewable Energy Forecasting project')
    parser.add_argument('--no-download', action='store_true', help='Skip downloading sample data')
    parser.add_argument('--no-venv', action='store_true', help='Skip virtual environment setup')
    return parser.parse_args()

def main():
    """Main function to run the setup"""
    logger.info("Starting Renewable Energy Forecasting project setup...")
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Create directory structure
    create_directory_structure()
    
    # Download sample data
    if not args.no_download:
        download_sample_data()
    else:
        logger.info("Skipping sample data download.")
    
    # Setup virtual environment
    if not args.no_venv:
        setup_virtual_environment()
    else:
        logger.info("Skipping virtual environment setup.")
    
    logger.info("Setup completed successfully!")
    logger.info("\nTo run the web application:")
    logger.info("1. Activate the virtual environment")
    logger.info("2. Run 'python run.py'")
    logger.info("3. Open your browser and navigate to http://localhost:5000")

if __name__ == '__main__':
    main()