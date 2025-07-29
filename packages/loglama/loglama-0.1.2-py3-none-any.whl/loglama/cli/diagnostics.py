#!/usr/bin/env python3

"""Command-line interface for LogLama diagnostics."""

import argparse
import json
import sys

from loglama.diagnostics import (
    check_database_connection,
    check_file_permissions,
    check_system_health,
    diagnose_context_issues,
    generate_diagnostic_report,
    troubleshoot_context,
    troubleshoot_database,
    troubleshoot_logging,
    verify_logging_setup,
)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="LogLama Diagnostics Tool")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Health check command
    health_parser = subparsers.add_parser("health", help="Check system health")
    health_parser.add_argument(
        "--output", "-o", help="Output file for health report (JSON format)"
    )

    # Verify logging command
    verify_parser = subparsers.add_parser(
        "verify", help="Verify logging setup"
    )
    verify_parser.add_argument(
        "--log-dir", "-d", help="Directory for test log files"
    )

    # Context diagnostics command
    context_parser = subparsers.add_parser(
        "context", help="Diagnose context issues"
    )
    context_parser.add_argument(
        "--log-dir", "-d", help="Directory for test log files"
    )

    # Database check command
    db_parser = subparsers.add_parser(
        "database", help="Check database connection"
    )
    db_parser.add_argument("--db-path", "-p", help="Path to database file")

    # File permissions check command
    file_parser = subparsers.add_parser("files", help="Check file permissions")
    file_parser.add_argument(
        "--log-dir", "-d", help="Directory to check permissions"
    )

    # Troubleshoot logging command
    troubleshoot_logging_parser = subparsers.add_parser(
        "troubleshoot-logging", help="Troubleshoot logging issues"
    )
    troubleshoot_logging_parser.add_argument(
        "--log-dir", "-d", help="Directory for test log files"
    )
    troubleshoot_logging_parser.add_argument(
        "--log-level", "-l", default="INFO", help="Log level to use for tests"
    )

    # Troubleshoot context command
    troubleshoot_context_parser = subparsers.add_parser(
        "troubleshoot-context", help="Troubleshoot context issues"
    )
    troubleshoot_context_parser.add_argument(
        "--log-dir", "-d", help="Directory for test log files"
    )

    # Troubleshoot database command
    troubleshoot_db_parser = subparsers.add_parser(
        "troubleshoot-database", help="Troubleshoot database issues"
    )
    troubleshoot_db_parser.add_argument(
        "--db-path", "-p", help="Path to database file"
    )

    # Full diagnostic report command
    report_parser = subparsers.add_parser(
        "report", help="Generate full diagnostic report"
    )
    report_parser.add_argument(
        "--output",
        "-o",
        default="loglama_diagnostic_report.json",
        help="Output file for diagnostic report (JSON format)",
    )

    return parser.parse_args()


def format_result(result, title):
    """Format a diagnostic result for display."""
    output = [f"\n=== {title} ==="]

    if "status" in result:
        if isinstance(result["status"], bool):
            status_str = "OK" if result["status"] else "Failed"
        else:
            status_str = result["status"]
        output.append(f"Status: {status_str}")

    if "issues" in result and result["issues"]:
        output.append(f"\nIssues found: {len(result['issues'])}")
        for i, issue in enumerate(result["issues"], 1):
            output.append(f"  {i}. {issue}")

    if "recommendations" in result and result["recommendations"]:
        output.append("\nRecommendations:")
        for i, rec in enumerate(result["recommendations"], 1):
            output.append(f"  {i}. {rec}")

    if "tests" in result and result["tests"]:
        output.append("\nTests:")
        for i, test in enumerate(result["tests"], 1):
            status = test.get("status", "unknown")
            name = test.get("name", f"Test {i}")
            reason = test.get("reason", "")
            output.append(
                f"  {i}. {name}: {status}" + (f" - {reason}" if reason else "")
            )

    if "fixes_applied" in result and result["fixes_applied"]:
        output.append("\nFixes applied:")
        for i, fix in enumerate(result["fixes_applied"], 1):
            output.append(f"  {i}. {fix}")

    return "\n".join(output)


def save_json(data, filename):
    """Save data as JSON to a file."""
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"\nReport saved to {filename}")
        return True
    except Exception as e:
        print(f"\nError saving report: {str(e)}")
        return False


def main():
    """Main entry point for the diagnostics CLI."""
    args = parse_args()

    if not args.command:
        print("No command specified. Use --help for available commands.")
        return 1

    try:
        if args.command == "health":
            result = check_system_health()
            print(format_result(result, "System Health Check"))
            if args.output:
                save_json(result, args.output)

        elif args.command == "verify":
            result = verify_logging_setup()
            print(format_result(result, "Logging Setup Verification"))

        elif args.command == "context":
            result = diagnose_context_issues()
            print(format_result(result, "Context Handling Diagnostics"))

        elif args.command == "database":
            result = check_database_connection(args.db_path)
            print(format_result(result, "Database Connection Check"))

        elif args.command == "files":
            result = check_file_permissions(args.log_dir)
            print(format_result(result, "File Permissions Check"))

        elif args.command == "troubleshoot-logging":
            result = troubleshoot_logging(args.log_dir, args.log_level)
            print(format_result(result, "Logging Troubleshooting"))

        elif args.command == "troubleshoot-context":
            result = troubleshoot_context(args.log_dir)
            print(format_result(result, "Context Troubleshooting"))

        elif args.command == "troubleshoot-database":
            result = troubleshoot_database(args.db_path)
            print(format_result(result, "Database Troubleshooting"))

        elif args.command == "report":
            print("Generating comprehensive diagnostic report...")
            result = generate_diagnostic_report()
            print(format_result(result, "Diagnostic Report Summary"))
            save_json(result, args.output)
            print(f"\nFull diagnostic report saved to {args.output}")

        return 0

    except Exception as e:
        print(f"\nError running diagnostics: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
