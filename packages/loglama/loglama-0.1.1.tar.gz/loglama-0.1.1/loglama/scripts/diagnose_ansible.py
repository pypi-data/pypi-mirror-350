#!/usr/bin/env python3

"""Ansible diagnostic tool for LogLama.

This script can be used to diagnose issues in Ansible playbooks and environments.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from loglama.core.logger import setup_logging
from loglama.decorators.diagnostics import with_diagnostics

# Add LogLama to path if not installed
loglama_path = Path(__file__).resolve().parent.parent.parent
if loglama_path.exists():
    sys.path.insert(0, str(loglama_path))


# Setup logging
logger = setup_logging(name="loglama.ansible", level="INFO", console=True)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="LogLama Ansible Diagnostic Tool"
    )

    parser.add_argument(
        "playbook_path",
        help="Path to the Ansible playbook or directory containing playbooks",
    )

    parser.add_argument(
        "--inventory", "-i", help="Path to the Ansible inventory file"
    )

    parser.add_argument(
        "--check",
        "-c",
        action="store_true",
        help="Run Ansible in check mode (dry run)",
    )

    parser.add_argument(
        "--fix",
        "-",
        action="store_true",
        help="Attempt to fix detected issues",
    )

    parser.add_argument(
        "--report",
        "-r",
        help="Path to save the diagnostic report (JSON format)",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
        help="Increase verbosity (can be used multiple times)",
    )

    return parser.parse_args()


@with_diagnostics(run_before=True, run_after=True, fix_issues=True)
def check_ansible_installation() -> Dict[str, Any]:
    """Check if Ansible is installed and get version information.

    Returns:
        Dict[str, Any]: Ansible installation details
    """
    result = {  # type: ignore[var-annotated]
        "installed": False,
        "version": None,
        "path": None,
        "python_version": sys.version,
        "issues": [],
    }

    try:
        # Check if ansible command is available
        process = subprocess.run(
            ["which", "ansible"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

        if process.returncode == 0:
            result["installed"] = True
            result["path"] = process.stdout.strip()

            # Get Ansible version
            version_process = subprocess.run(
                ["ansible", "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )

            if version_process.returncode == 0:
                version_output = version_process.stdout.strip()
                first_line = version_output.split("\n")[0]
                if "ansible" in first_line.lower() and "[" in first_line:
                    result["version"] = first_line.split("[")[1].split("]")[0]
        else:
            result["issues"].append(  # type: ignore[Any,union-attr]
                {
                    "type": "ansible_not_installed",
                    "message": "Ansible command not found in PATH",
                    "params": {},
                }
            )
    except Exception as e:
        result["issues"].append(  # type: ignore[Any,union-attr]
            {
                "type": "ansible_check_error",
                "message": f"Error checking Ansible installation: {str(e)}",
                "params": {},
            }
        )

    return result


@with_diagnostics(run_before=True, run_after=False)
def validate_playbook(playbook_path: str) -> Dict[str, Any]:
    """Validate an Ansible playbook syntax.

    Args:
        playbook_path: Path to the Ansible playbook

    Returns:
        Dict[str, Any]: Validation results
    """
    result = {"valid": False, "playbook_path": playbook_path, "issues": []}

    # Check if file exists
    if not os.path.exists(playbook_path):
        result["issues"].append(  # type: ignore[attr-defined]
            {
                "type": "playbook_not_found",
                "message": f"Playbook not found: {playbook_path}",
                "params": {"playbook_path": playbook_path},
            }
        )
        return result

    # Check if it's a YAML file
    if not playbook_path.endswith((".yml", ".yaml")):
        result["issues"].append(  # type: ignore[attr-defined]
            {
                "type": "invalid_playbook_extension",
                "message": f"Playbook file does not have .yml or .yaml extension: {playbook_path}",
                "params": {"playbook_path": playbook_path},
            }
        )

    try:
        # Run ansible-playbook with --syntax-check
        process = subprocess.run(
            ["ansible-playbook", "--syntax-check", playbook_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

        if process.returncode == 0:
            result["valid"] = True
        else:
            result["issues"].append(  # type: ignore[attr-defined]
                {
                    "type": "playbook_syntax_error",
                    "message": f"Playbook syntax check failed: {process.stderr.strip()}",
                    "params": {
                        "playbook_path": playbook_path,
                        "error": process.stderr.strip(),
                    },
                }
            )
    except Exception as e:
        result["issues"].append(  # type: ignore[attr-defined]
            {
                "type": "playbook_validation_error",
                "message": f"Error validating playbook: {str(e)}",
                "params": {"playbook_path": playbook_path},
            }
        )

    return result


@with_diagnostics(run_before=True, run_after=False)
def check_inventory(inventory_path: str) -> Dict[str, Any]:
    """Check an Ansible inventory file.

    Args:
        inventory_path: Path to the Ansible inventory file

    Returns:
        Dict[str, Any]: Inventory check results
    """
    result = {
        "valid": False,
        "inventory_path": inventory_path,
        "hosts": [],
        "groups": [],
        "issues": [],
    }

    # Check if file exists
    if not os.path.exists(inventory_path):
        result["issues"].append(  # type: ignore[attr-defined]
            {
                "type": "inventory_not_found",
                "message": f"Inventory file not found: {inventory_path}",
                "params": {"inventory_path": inventory_path},
            }
        )
        return result

    try:
        # Run ansible-inventory to list hosts
        process = subprocess.run(
            ["ansible-inventory", "-i", inventory_path, "--list"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

        if process.returncode == 0:
            result["valid"] = True
            try:
                inventory_data = json.loads(process.stdout)

                # Extract groups and hosts
                for key, value in inventory_data.items():
                    if key != "_meta" and key != "all":
                        result["groups"].append(key)  # type: ignore[attr-defined]
                        if "hosts" in value and isinstance(
                            value["hosts"], list
                        ):
                            for host in value["hosts"]:
                                if host not in result["hosts"]:  # type: ignore[operator]
                                    result["hosts"].append(host)  # type: ignore[attr-defined]
            except json.JSONDecodeError:
                result["issues"].append(  # type: ignore[attr-defined]
                    {
                        "type": "inventory_parse_error",
                        "message": "Failed to parse inventory JSON output",
                        "params": {"inventory_path": inventory_path},
                    }
                )
        else:
            result["issues"].append(  # type: ignore[attr-defined]
                {
                    "type": "inventory_validation_error",
                    "message": f"Inventory validation failed: {process.stderr.strip()}",
                    "params": {
                        "inventory_path": inventory_path,
                        "error": process.stderr.strip(),
                    },
                }
            )
    except Exception as e:
        result["issues"].append(  # type: ignore[attr-defined]
            {
                "type": "inventory_check_error",
                "message": f"Error checking inventory: {str(e)}",
                "params": {"inventory_path": inventory_path},
            }
        )

    return result


@with_diagnostics(run_before=True, run_after=True)
def run_ansible_playbook(
    playbook_path: str,
    inventory_path: Optional[str] = None,
    check_mode: bool = True,
    verbose: int = 0,
) -> Dict[str, Any]:
    """Run an Ansible playbook in check mode.

    Args:
        playbook_path: Path to the Ansible playbook
        inventory_path: Path to the Ansible inventory file
        check_mode: Whether to run in check mode (dry run)
        verbose: Verbosity level

    Returns:
        Dict[str, Any]: Playbook run results
    """
    result = {
        "success": False,
        "playbook_path": playbook_path,
        "inventory_path": inventory_path,
        "check_mode": check_mode,
        "output": "",
        "issues": [],
    }

    # Build command
    command = ["ansible-playbook"]

    # Add verbosity flags
    if verbose > 0:
        command.append("-" + "v" * verbose)

    # Add check mode flag
    if check_mode:
        command.append("--check")

    # Add inventory if provided
    if inventory_path:
        command.extend(["-i", inventory_path])

    # Add playbook path
    command.append(playbook_path)

    try:
        # Run ansible-playbook
        logger.info(f"Running Ansible command: {' '.join(command)}")
        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

        # Store output
        result["output"] = process.stdout.strip()

        if process.returncode == 0:
            result["success"] = True
        else:
            result["issues"].append(  # type: ignore[attr-defined]
                {
                    "type": "playbook_execution_error",
                    "message": f"Playbook execution failed: {process.stderr.strip()}",
                    "params": {
                        "playbook_path": playbook_path,
                        "error": process.stderr.strip(),
                        "command": " ".join(command),
                    },
                }
            )
    except Exception as e:
        result["issues"].append(  # type: ignore[attr-defined]
            {
                "type": "playbook_run_error",
                "message": f"Error running playbook: {str(e)}",
                "params": {"playbook_path": playbook_path},
            }
        )

    return result


def diagnose_ansible_environment() -> Dict[str, Any]:
    """Diagnose the Ansible environment.

    Returns:
        Dict[str, Any]: Diagnostic report
    """
    report = {  # type: ignore[var-annotated]
        "timestamp": datetime.now().isoformat(),
        "ansible": None,
        "environment": {},
        "issues": [],
        "status": "healthy",
    }

    # Check Ansible installation
    ansible_check = check_ansible_installation()
    report["ansible"] = ansible_check

    if ansible_check["issues"]:
        report["issues"].extend(ansible_check["issues"])  # type: ignore[Any, Any,union-attr]
        report["status"] = "issues_found"
        return report  # Stop if Ansible is not installed

    # Check environment variables
    ansible_env_vars = [
        "ANSIBLE_CONFIG",
        "ANSIBLE_INVENTORY",
        "ANSIBLE_ROLES_PATH",
        "ANSIBLE_LIBRARY",
        "ANSIBLE_COLLECTIONS_PATH",
        "ANSIBLE_HOST_KEY_CHECKING",
        "ANSIBLE_STDOUT_CALLBACK",
    ]

    for var in ansible_env_vars:
        if var in os.environ:
            report["environment"][var] = os.environ[var]  # type: ignore[Any,call-overload,index]

    # Check for common Ansible directories
    ansible_dirs = [
        "~/.ansible",
        "~/.ansible/roles",
        "~/.ansible/collections",
        "/etc/ansible",
    ]

    for dir_path in ansible_dirs:
        expanded_path = os.path.expanduser(dir_path)
        if os.path.exists(expanded_path):
            report["environment"][f"dir_{dir_path}"] = True  # type: ignore[Any,call-overload,index]
        else:
            report["environment"][f"dir_{dir_path}"] = False  # type: ignore[Any,call-overload,index]

    # Check for Ansible config file
    config_paths = [
        os.path.expanduser("~/.ansible.cfg"),
        os.path.expanduser("~/ansible.cfg"),
        "/etc/ansible/ansible.cfg",
    ]

    config_found = False
    for config_path in config_paths:
        if os.path.exists(config_path):
            report["environment"]["config_path"] = config_path  # type: ignore[Any,call-overload,index]
            config_found = True
            break

    if not config_found:
        report["issues"].append(  # type: ignore[Any, Any,union-attr]
            {
                "type": "ansible_config_not_found",
                "message": "Ansible configuration file not found",
                "params": {"searched_paths": config_paths},
            }
        )

    # Update status if issues were found
    if report["issues"]:
        report["status"] = "issues_found"

    return report


def fix_ansible_issues(report: Dict[str, Any]) -> Dict[str, Any]:
    """Fix detected Ansible issues.

    Args:
        report: Diagnostic report

    Returns:
        Dict[str, Any]: Fix results
    """
    results = {"fixed_issues": [], "failed_fixes": [], "created_files": []}  # type: ignore[var-annotated]

    # Skip if no issues found
    if not report["issues"]:
        logger.info("No issues to fix")
        return results

    # Fix Ansible config issues
    if any(
        issue["type"] == "ansible_config_not_found"
        for issue in report["issues"]
    ):
        try:
            # Create a basic Ansible config file
            config_path = os.path.expanduser("~/.ansible.cfg")
            config_content = """[defaults]
inventory = ~/inventory
host_key_checking = False
roles_path = ~/.ansible/roles
collections_paths = ~/.ansible/collections
log_path = ~/.ansible/ansible.log

[privilege_escalation]
become = True
become_method = sudo
become_user = root
become_ask_pass = False
"""

            # Create directory if it doesn't exist
            os.makedirs(os.path.expanduser("~/.ansible"), exist_ok=True)

            # Write config file
            with open(config_path, "w") as f:
                f.write(config_content)

            results["fixed_issues"].append(
                {
                    "type": "ansible_config_not_found",
                    "message": f"Created Ansible configuration file: {config_path}",
                    "details": {"path": config_path},
                }
            )

            results["created_files"].append(config_path)
        except Exception as e:
            results["failed_fixes"].append(
                {
                    "type": "ansible_config_not_found",
                    "message": f"Failed to create Ansible configuration file: {str(e)}",
                    "details": {"error": str(e)},
                }
            )

    # Create missing directories
    for dir_path in ["~/.ansible/roles", "~/.ansible/collections"]:
        expanded_path = os.path.expanduser(dir_path)
        if not os.path.exists(expanded_path):
            try:
                os.makedirs(expanded_path, exist_ok=True)
                results["fixed_issues"].append(
                    {
                        "type": "missing_ansible_directory",
                        "message": f"Created Ansible directory: {dir_path}",
                        "details": {"path": expanded_path},
                    }
                )
            except Exception as e:
                results["failed_fixes"].append(
                    {
                        "type": "missing_ansible_directory",
                        "message": f"Failed to create Ansible directory {dir_path}: {str(e)}",
                        "details": {"path": expanded_path, "error": str(e)},
                    }
                )

    return results


def main() -> int:
    """Main entry point for the script."""
    args = parse_args()

    # Diagnose Ansible environment
    logger.info("Diagnosing Ansible environment...")
    env_report = diagnose_ansible_environment()

    # Display environment results
    if env_report["ansible"] and env_report["ansible"]["installed"]:
        logger.info(f"Ansible version: {env_report['ansible']['version']}")
    else:
        logger.error("Ansible is not installed or not found in PATH")
        return 1

    if env_report["issues"]:
        logger.warning(
            f"Found {len(env_report['issues'])} issues in Ansible environment"
        )
        for i, issue in enumerate(env_report["issues"], 1):
            logger.warning(f"{i}. {issue['type']}: {issue['message']}")
    else:
        logger.info("Ansible environment looks good")

    # Fix environment issues if requested
    if args.fix and env_report["issues"]:
        logger.info("Fixing Ansible environment issues...")
        fix_results = fix_ansible_issues(env_report)

        if fix_results["fixed_issues"]:
            logger.info(f"Fixed {len(fix_results['fixed_issues'])} issues")
            for fix in fix_results["fixed_issues"]:
                logger.info(f"- {fix['message']}")

        if fix_results["failed_fixes"]:
            logger.warning(
                f"Failed to fix {len(fix_results['failed_fixes'])} issues"
            )
            for fail in fix_results["failed_fixes"]:
                logger.warning(f"- {fail['message']}")

    # Check if playbook path is a directory or file
    playbook_path = args.playbook_path
    if os.path.isdir(playbook_path):
        # Find all playbook files in directory
        playbooks = []
        for root, _, files in os.walk(playbook_path):
            for file in files:
                if file.endswith((".yml", ".yaml")):
                    playbooks.append(os.path.join(root, file))

        if not playbooks:
            logger.error(
                f"No playbook files found in directory: {playbook_path}"
            )
            return 1

        logger.info(f"Found {len(playbooks)} playbook files")

        # Validate each playbook
        valid_playbooks = []
        for pb in playbooks:
            logger.info(f"Validating playbook: {pb}")
            validation = validate_playbook(pb)

            if validation["valid"]:
                logger.info(f"Playbook is valid: {pb}")
                valid_playbooks.append(pb)
            else:
                logger.warning(f"Playbook validation failed: {pb}")
                for issue in validation["issues"]:
                    logger.warning(f"- {issue['message']}")

        # Run check on valid playbooks if requested
        if args.check and valid_playbooks:
            for pb in valid_playbooks:
                logger.info(f"Running playbook in check mode: {pb}")
                run_result = run_ansible_playbook(
                    pb,
                    inventory_path=args.inventory,
                    check_mode=True,
                    verbose=args.verbose,
                )

                if run_result["success"]:
                    logger.info(f"Playbook check successful: {pb}")
                else:
                    logger.warning(f"Playbook check failed: {pb}")
                    for issue in run_result["issues"]:
                        logger.warning(f"- {issue['message']}")
    else:
        # Single playbook file
        logger.info(f"Validating playbook: {playbook_path}")
        validation = validate_playbook(playbook_path)

        if validation["valid"]:
            logger.info("Playbook is valid")

            # Check inventory if provided
            if args.inventory:
                logger.info(f"Checking inventory: {args.inventory}")
                inventory_check = check_inventory(args.inventory)

                if inventory_check["valid"]:
                    logger.info(
                        f"Inventory is valid, found {len(inventory_check['hosts'])} hosts in {len(inventory_check['groups'])} groups"  # noqa: E501
                    )
                else:
                    logger.warning("Inventory check failed")
                    for issue in inventory_check["issues"]:
                        logger.warning(f"- {issue['message']}")

            # Run playbook in check mode if requested
            if args.check:
                logger.info("Running playbook in check mode")
                run_result = run_ansible_playbook(
                    playbook_path,
                    inventory_path=args.inventory,
                    check_mode=True,
                    verbose=args.verbose,
                )

                if run_result["success"]:
                    logger.info("Playbook check successful")
                else:
                    logger.warning("Playbook check failed")
                    for issue in run_result["issues"]:
                        logger.warning(f"- {issue['message']}")
        else:
            logger.error("Playbook validation failed")
            for issue in validation["issues"]:
                logger.error(f"- {issue['message']}")
            return 1

    # Save report if requested
    if args.report:
        try:
            # Create report
            report = {
                "timestamp": datetime.now().isoformat(),
                "environment": env_report,
                "playbook_path": args.playbook_path,
                "inventory_path": args.inventory,
                "check_mode": args.check,
            }

            # Create directory if it doesn't exist
            report_dir = os.path.dirname(args.report)
            if report_dir and not os.path.exists(report_dir):
                os.makedirs(report_dir, exist_ok=True)

            # Save report
            with open(args.report, "w") as f:
                json.dump(report, f, indent=2)

            logger.info(f"Diagnostic report saved to: {args.report}")
        except Exception as e:
            logger.error(f"Failed to save report: {str(e)}")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
