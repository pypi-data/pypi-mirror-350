#!/usr/bin/env python3

import os
import sys
import signal
import argparse
from pathlib import Path
import logging
import daemon
import lockfile
from sugcommand.integrations.auto_suggest import AutoSuggestionServer

def setup_logging():
    """Setup logging configuration"""
    log_dir = Path.home() / ".config" / "sugcommand"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "auto_suggest.log"),
            logging.StreamHandler()
        ]
    )

def create_pid_file():
    """Create PID file"""
    pid_file = Path.home() / ".config" / "sugcommand" / "auto_suggest.pid"
    with open(pid_file, "w") as f:
        f.write(str(os.getpid()))
    return pid_file

def remove_pid_file():
    """Remove PID file"""
    pid_file = Path.home() / ".config" / "sugcommand" / "auto_suggest.pid"
    if pid_file.exists():
        pid_file.unlink()

def main():
    parser = argparse.ArgumentParser(description="SugCommand Auto-Suggestion Daemon")
    parser.add_argument("--background", action="store_true", help="Run in background")
    parser.add_argument("--foreground", action="store_true", help="Run in foreground")
    args = parser.parse_args()
    
    setup_logging()
    logger = logging.getLogger("auto_suggest")
    
    server = AutoSuggestionServer()
    
    def signal_handler(signum, frame):
        logger.info("Received signal %d, shutting down...", signum)
        server.stop()
        remove_pid_file()
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        if args.background:
            # Run as daemon
            pid_file = create_pid_file()
            logger.info("Starting auto-suggestion server in background...")
            
            with daemon.DaemonContext(
                pidfile=lockfile.FileLock(str(pid_file)),
                signal_map={
                    signal.SIGTERM: signal_handler,
                    signal.SIGINT: signal_handler,
                }
            ):
                server.start()
        else:
            # Run in foreground
            logger.info("Starting auto-suggestion server...")
            create_pid_file()
            server.start()
                
    except Exception as e:
        logger.error("Error running server: %s", e)
        remove_pid_file()
        sys.exit(1)

if __name__ == "__main__":
    main() 