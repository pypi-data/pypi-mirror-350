#!/bin/bash

# LogLama Bash Helper Script
# This script provides simple functions for logging from bash scripts

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Path to the LogLama installation
LOGLAMA_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Default logger name
DEFAULT_LOGGER_NAME="bash_script"

# Default database path
DEFAULT_DB_PATH="$LOGLAMA_ROOT/logs/loglama.db"

# Function to log a message using LogLama
log_message() {
    local level="$1"
    local message="$2"
    local logger_name="${3:-$DEFAULT_LOGGER_NAME}"
    
    # Collect additional context
    local script_name="$(basename "${BASH_SOURCE[1]}")"
    local line_number="${BASH_LINENO[0]}"
    local hostname="$(hostname)"
    local timestamp="$(date +"%Y-%m-%d %H:%M:%S")"
    
    # Use Python to call LogLama's simple logger
    python3 -c "
# Add paths to Python path
import sys, os
from pathlib import Path

# Add LogLama root directory
sys.path.append('$LOGLAMA_ROOT')

# Import simple logger
from loglama.core.simple_logger import log

# Log message with context
log('$level', '$message', '$logger_name', 
    script='$script_name', 
    line='$line_number', 
    hostname='$hostname', 
    timestamp='$timestamp',
    bash_pid=$$)
"
}

# Helper functions for different log levels
log_debug() {
    log_message "debug" "$1" "${2:-$DEFAULT_LOGGER_NAME}"
}

log_info() {
    log_message "info" "$1" "${2:-$DEFAULT_LOGGER_NAME}"
}

log_warning() {
    log_message "warning" "$1" "${2:-$DEFAULT_LOGGER_NAME}"
}

log_error() {
    log_message "error" "$1" "${2:-$DEFAULT_LOGGER_NAME}"
}

log_critical() {
    log_message "critical" "$1" "${2:-$DEFAULT_LOGGER_NAME}"
}

# Function to set up database logging
setup_db_logging() {
    local db_path="${1:-$DEFAULT_DB_PATH}"
    
    # Create directory for database if it doesn't exist
    mkdir -p "$(dirname "$db_path")"
    
    # Use Python to configure database logging
    python3 -c "
# Add paths to Python path
import sys, os
from pathlib import Path

# Add LogLama root directory
sys.path.append('$LOGLAMA_ROOT')

# Import and configure database logging
from loglama.core.simple_logger import configure_db_logging
configure_db_logging('$db_path')

print('LogLama database logging configured to use: $db_path')
"
}

# Function to start the web interface
start_web_interface() {
    local host="${1:-127.0.0.1}"
    local port="${2:-8081}"
    local db_path="${3:-$DEFAULT_DB_PATH}"
    
    echo "Starting LogLama web interface on $host:$port..."
    
    # Start the web interface in the background
    nohup python3 -c "
# Add paths to Python path
import sys, os
from pathlib import Path

# Add LogLama root directory
sys.path.append('$LOGLAMA_ROOT')

# Import and run web interface
import subprocess
subprocess.Popen(['python', '-m', 'loglama.cli.main', 'web', 
                  '--host', '$host', '--port', '$port', '--db', '$db_path'])

print('LogLama web interface started at http://$host:$port')
" > /dev/null 2>&1 &
    
    echo "LogLama web interface started at http://$host:$port"
    echo "Access it in your browser to view logs"
}

# Function to time a command execution
time_command() {
    local command="$1"
    local description="${2:-Command execution}"
    local logger_name="${3:-$DEFAULT_LOGGER_NAME}"
    
    log_info "Starting: $description" "$logger_name"
    
    # Record start time
    local start_time=$(date +%s.%N)
    
    # Execute the command
    eval "$command"
    local status=$?
    
    # Record end time and calculate duration
    local end_time=$(date +%s.%N)
    local duration=$(echo "$end_time - $start_time" | bc)
    
    if [ $status -eq 0 ]; then
        log_info "Completed: $description (took ${duration}s)" "$logger_name"
    else
        log_error "Failed: $description (took ${duration}s, exit code: $status)" "$logger_name"
    fi
    
    return $status
}

# Print usage information if this script is run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "LogLama Bash Helper Script"
    echo "This script provides functions for logging from bash scripts"
    echo ""
    echo "Usage:"
    echo "  source $(basename "${BASH_SOURCE[0]}") # Include in your bash script"
    echo ""
    echo "Available functions:"
    echo "  log_debug "message" [logger_name]"
    echo "  log_info "message" [logger_name]"
    echo "  log_warning "message" [logger_name]"
    echo "  log_error "message" [logger_name]"
    echo "  log_critical "message" [logger_name]"
    echo "  setup_db_logging [db_path]"
    echo "  start_web_interface [host] [port] [db_path]"
    echo "  time_command "command" [description] [logger_name]"
    echo ""
    echo "Example:"
    echo "  source $(basename "${BASH_SOURCE[0]}")"
    echo "  setup_db_logging"
    echo "  log_info "Starting my script""
    echo "  time_command "sleep 2" "Sleeping for 2 seconds""
    echo "  start_web_interface"
    exit 0
fi
