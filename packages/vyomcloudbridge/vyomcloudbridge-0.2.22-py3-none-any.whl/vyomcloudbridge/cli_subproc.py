# vyomcloudbridge/cli.py
import os
import subprocess
import sys



def format_duration(seconds):
    """Format duration in seconds to a human-readable string."""
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"


def display_system_health(library_health):
    try:
        # Check 1: Certificates
        print("\nCheck 1: Certificates and Security:\n------------------------------")
        cert_components = ["certificates_dir", "cert_file", "private_key", "root_ca"]
        for component in cert_components:
            if component in library_health:
                status_symbol = "✓" if library_health[component]["status"] else "✗"
                print(
                    f"{status_symbol} {component}: {library_health[component]['message']}"
                )

        # Check 2: Log directory
        print("\nCheck 2: Logging Configuration:\n---------------------------")
        if "log_directory" in library_health:
            status_symbol = "✓" if library_health["log_directory"]["status"] else "✗"
            print(f"{status_symbol} {library_health['log_directory']['message']}")

        # Check 3: Home directory and configs
        print(
            "\nCheck 3: Home Directory and Configuration:\n------------------------------------"
        )
        home_components = ["root_directory", "machine_config", "start_script"]
        for component in home_components:
            if component in library_health:
                status_symbol = "✓" if library_health[component]["status"] else "✗"
                print(
                    f"{status_symbol} {component}: {library_health[component]['message']}"
                )

        # Check 4: System service
        print(
            "\nCheck 4: System Service Configuration:\n---------------------------------"
        )
        service_components = ["service_dir", "service_file_path"]
        for component in service_components:
            if component in library_health:
                status_symbol = "✓" if library_health[component]["status"] else "✗"
                print(
                    f"{status_symbol} {component}: {library_health[component]['message']}"
                )

        # Check 5: RabbitMQ
        print("\nCheck 5: RabbitMQ and Dependencies:\n------------------------------")
        rabbitmq_components = ["rabbitmq", "pika_library"]
        for component in rabbitmq_components:
            if component in library_health:
                status_symbol = "✓" if library_health[component]["status"] else "✗"
                print(
                    f"{status_symbol} {component}: {library_health[component]['message']}"
                )

        # Overall status
        print("\nOverall Status:\n--------------")
        all_complete = all(status["status"] for status in library_health.values())
        if all_complete:
            print("✓ All system requirements are met. The system is ready to use.")
        else:
            incomplete_steps = []
            if not all(
                library_health[comp]["status"]
                for comp in cert_components
                if comp in library_health
            ):
                incomplete_steps.append("Check 1: Certificates")
            if (
                "log_directory" in library_health
                and not library_health["log_directory"]["status"]
            ):
                incomplete_steps.append("Check 2: Logging")
            if not all(
                library_health[comp]["status"]
                for comp in home_components
                if comp in library_health
            ):
                incomplete_steps.append("Check 3: Configuration")
            if not all(
                library_health[comp]["status"]
                for comp in service_components
                if comp in library_health
            ):
                incomplete_steps.append("Check 4: System Service")
            if not all(
                library_health[comp]["status"]
                for comp in rabbitmq_components
                if comp in library_health
            ):
                incomplete_steps.append("Check 5: RabbitMQ not installed/running")

            print("✗ The setup is incomplete. The following steps need attention:")
            for step in incomplete_steps:
                print(f"  - {step}")
            print("\nTo complete setup, run:")
            print("  vyomcloudbridge setup")
    except Exception as e:
        print("Error occurred in displaying system health")


def main():
    if not os.environ.get("VYOM_ENV_READY"):
        vyom_env_file = "/home/shitiz/.bashrc"
        if not os.path.exists(vyom_env_file):
            # if we have not stored check the AMENT_PREFIX_PATH path
            ament_prefix_path = os.environ.get("AMENT_PREFIX_PATH", "")
            if not ament_prefix_path:
                print(
                    "===> Your ROS2 workspaces have not been found. Please ensure you manually source them before running `vyomcloudbridge setup`. <==="
                )
                sys.exit(0)
            # else case - user has already sourced the ros workspaces
        else:
            # Compose the command to re-run the CLI inside a shell with ROS sourced
            command = f"source {vyom_env_file} && VYOM_ENV_READY=1 vyomcloudbridge {' '.join(sys.argv[1:])}"
            subprocess.run(["bash", "-c", command])
            # Exit the original process after spawning the ROS-enabled process
            sys.exit(0)

    # Only the ROS-enabled process continues from here
    import argparse
    import time
    from typing import Dict, Type
    from vyomcloudbridge.types import AVAILABLE_SERVICES
    from .service_manager import ServiceManager
    from .setup import setup

    parser = argparse.ArgumentParser(description="Service Manager CLI")
    manager = ServiceManager()

    subparsers = parser.add_subparsers(dest="action", required=True)

    # General Commands
    subparsers.add_parser("setup", help="Setup the service environment")
    subparsers.add_parser("restart", help="Restart all instances started by users")

    # list of running/all services
    list_parser = subparsers.add_parser("list", help="List running services")
    list_parser.add_argument(
        "--all", "-a", action="store_true", help="Show all services (including stopped)"
    )

    # library status, health
    subparsers.add_parser(
        "status",
        help="Check library installation/setup status, configurations, and requirements",
    )
    subparsers.add_parser(
        "health",
        help="Check library installation/setup health, configurations, and requirements",
    )

    subparsers.add_parser(
        "cleanup",
        help="Remove all files, directories, and services created by the library installation",
    )

    # Stop Command
    stop_parser = subparsers.add_parser("stop", help="Stop a running service")
    stop_parser.add_argument(
        "service",
        help="Service name (identifier of service)",
    )

    # Start Command (with service-specific arguments)
    start_parser = subparsers.add_parser("start", help="Start a service")
    start_parser.add_argument(
        "service", choices=AVAILABLE_SERVICES.keys(), help="Service name to start"
    )
    start_parser.add_argument(
        "--name", help="Custom instance name for the service instance"
    )
    start_parser.add_argument(
        "--system-default",
        action="store_true",
        help="Mark if the service is started by the system",
    )

    # Service-specific arguments
    service_parsers = {
        "queueworker": start_parser.add_argument_group("Queue Worker"),
        "dirwatcher": start_parser.add_argument_group("Directory Watcher"),
        "missionstats": start_parser.add_argument_group("Mission Stats Monitor"),
        "machinestats": start_parser.add_argument_group("Machine Stats Service"),
        "vyomlistener": start_parser.add_argument_group("Vyom Listener"),
        "rospublisher": start_parser.add_argument_group("Ros Publisher"),
    }

    # Arguments for queueworker
    service_parsers["queueworker"].add_argument(
        "--multi-thread",
        action="store_true",
        help="Enable multi-threading for queueworker",
    )

    # Arguments for dirwatcher
    service_parsers["dirwatcher"].add_argument(
        "--mission-dir",
        action="store_true",
        help="If included, the <dir> provided will be considered a mission data directory.",
    )

    service_parsers["dirwatcher"].add_argument(
        "--merge-chunks",
        action="store_true",
        help="If included, combines S3 chunks after all have been uploaded.",
    )

    service_parsers["dirwatcher"].add_argument(
        "--preserve-file",
        action="store_true",
        help="If included, files will be moved to <dir>_preserve instead of being deleted after uploading to S3.",
    )

    service_parsers["dirwatcher"].add_argument(
        "--dir",
        required=False,
        help="Directory to watch.",
    )

    service_parsers["dirwatcher"].add_argument(
        "--dir-properties",
        required=False,
        help="Path to a directory properties JSON file or an inline JSON object.",
    )

    service_parsers["dirwatcher"].add_argument(
        "--priority",
        required=False,
        help="Priority order of files in this directory to be pushed.",
    )

    args = parser.parse_args()

    if args.action == "setup":
        success = setup()
        sys.exit(0 if success else 1)

    if args.action == "restart":
        success = manager.restart_user_started_services()
        sys.exit(0 if success else 1)

    # Handle stopping a service
    if args.action == "stop":
        success = manager.stop_service(args.service)
        if success:
            print(f"Successfully stopped service: {args.service}")
        else:
            print(f"Failed to stop service: {args.service}")
        sys.exit(0 if success else 1)

    # Handle listing services
    if args.action == "list":
        services = manager.list_services()

        if not services:
            print("No services running OR started.")
            sys.exit(0)

        # Filter stopped services unless --all/-a is specified
        if not args.all:
            services = {
                key: val
                for key, val in services.items()
                if val.get("status") == "running"
            }
            if not services:
                print("No running services found. Use --all or -a to see all services.")
                sys.exit(0)

        print(
            "\nINSTANCE ID       SERVICE NAME     INSTANCE NAME    CREATED      STATUS       PID        COMMAND"
        )
        print("-" * 100)
        now = time.time()
        for instance_id, info in services.items():
            service_name = info.get("service_name", "unknown")
            command = f"\"{info.get('command', '')}\""
            pid = info.get("pid", "")
            name = info.get("name", "")

            # Format created time
            created_ago = format_duration(now - info.get("created", now))

            # Format status
            status = info.get("status", "unknown")
            if status == "running":
                status = f"Up {format_duration(info.get('uptime', 0))}"
            elif status == "exited":
                exit_code = info.get("exit_code", 0)
                exit_time = format_duration(now - info.get("exit_time", now))
                status = f"Exited ({exit_code}) {exit_time} ago"
            print(
                f"{instance_id:<17} {service_name:<16} {name:<16} {created_ago:<12} {status:<12} {pid:<10} {command}"
            )
        sys.exit(0)

    if args.action == "status":
        # Check overall system status
        library_health = manager.check_library_status()
        display_system_health(library_health)
        sys.exit(0)

    if args.action == "health":
        # Check overall system health
        library_health = manager.check_library_status()
        display_system_health(library_health)
        sys.exit(0)

    if args.action == "cleanup":
        confirm = (
            input(
                "WARNING: This will remove all vyomcloudbridge files and directories. Continue? [Y/n]: "
            )
            .strip()
            .lower()
        )

        if confirm not in ["y", "yes"]:
            print("Cleanup aborted.")
            sys.exit(0)
        print("Stopping all system background services...")
        stop_success = manager.stop_all_services()
        if stop_success:
            print(f"All background services of library have been stopped completely!")
        else:
            print(f"All background services stopping failed!")

        cleanup_results = manager.cleanup_system()
        manager.display_cleanup_results(cleanup_results)
        sys.exit(0)

    # Handle starting a service with proper argument validation
    if args.action == "start":
        service_args = {}

        if args.service == "queueworker":
            service_args["multi_thread"] = args.multi_thread

        if args.service == "dirwatcher":
            if not args.dir:
                print("Error: --dir is required for dirwatcher service")
                sys.exit(1)
            service_args["mission_dir"] = args.mission_dir
            service_args["merge_chunks"] = args.merge_chunks
            service_args["preserve_file"] = args.preserve_file
            service_args["dir"] = args.dir
            if args.dir_properties:
                service_args["dir_properties"] = args.dir_properties
            if args.priority:
                service_args["priority"] = args.priority

        if args.service == "missionstats":
            pass

        if args.service == "machinestats":
            pass

        if args.service == "rospublisher":
            pass

        service_class = AVAILABLE_SERVICES[args.service]
        success, instance_id, instance_name = manager.start_service(
            args.service,
            service_class,
            name=args.name,
            system_default=args.system_default,
            **service_args,
        )

        if success:
            print(f"Successfully started {args.service} service")
            print(f"Instance ID: {instance_id}")
            print(f"Instance Name: {instance_name}")
        else:
            print(f"Failed to start {args.service} service")

        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()