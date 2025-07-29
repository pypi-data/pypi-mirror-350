# vyomcloudbridge/setup.py
import os
import subprocess
import sys
import json
import configparser
import getpass
import requests
import time
from urllib.parse import urlencode

from vyomcloudbridge.constants.constants import (
    log_dir,
    log_file,
    pid_file,
    vyom_root_dir,
    machine_config_file,
    machine_topics_file,
    start_script_file,
    service_file_path,
    cert_dir,
    cert_file_path,
    pri_key_file_path,
    pub_key_file_path,
    root_ca_file_path,
    MACHINE_REGISTER_API_URL,
    MACHINE_MODELS_API_URL,
    MACHINE_TOPICS_API_URL,
)
from vyomcloudbridge.utils.ros_topics import ROSTopic


# def setup_ros2_workspaces(): # Not in use
#     """
#     Writes AMENT_PREFIX_PATH and PYTHONPATH to a shell-compatible .env file for later sourcing.

#     Returns:
#         bool: True if environment file was written successfully, False otherwise
#     """
#     print("\n--- STEP 0: Fetching ROS2 workspace environment variables ---")

#     python_path = os.environ.get("PYTHONPATH", "")
#     ament_prefix_path = os.environ.get("AMENT_PREFIX_PATH", "")
#     ld_library_path = os.environ.get("LD_LIBRARY_PATH", "")
#     rmw_implementation = os.environ.get("RMW_IMPLEMENTATION", "")
#     # print("After reading in setup, PYTHONPATH-", python_path)
#     # print("After reading in setup, AMENT_PREFIX_PATH-", ament_prefix_path)
#     # print("After reading in setup, LD_LIBRARY_PATH-", ld_library_path)
#     # print("After reading in setup, RMW_IMPLEMENTATION-", rmw_implementation)

#     if (
#         not ament_prefix_path
#         or not python_path
#         or not ld_library_path
#         or not rmw_implementation
#     ) and not os.path.exists(vyom_services_env_file):
#         missing_vars = []
#         if not python_path:
#             missing_vars.append("PYTHONPATH env variable")
#         if not ament_prefix_path:
#             missing_vars.append("Your ROS2 workspaces (AMENT_PREFIX_PATH env variable)")
#         if not ld_library_path:
#             missing_vars.append("LD_LIBRARY_PATH env variable")
#         if not rmw_implementation:
#             missing_vars.append("RMW_IMPLEMENTATION env variable")

#         error_message = "Missing environment variables:\n - " + "\n - ".join(
#             missing_vars
#         )
#         print(
#             "===> "
#             + error_message
#             + "\nPlease ensure you manually source them, before running `vyomcloudbridge setup`. <==="
#         )
#         return False
#     # else here either we have all three varibale or the file saved already
#     needs_sudo = os.geteuid() != 0
#     if needs_sudo:
#         print("Error - Root permission required.")
#         return False

#     try:
#         if (
#             ament_prefix_path and python_path and ld_library_path
#         ):  # we have all three varibale
#             os.makedirs(vyom_root_dir, exist_ok=True)

#             with open(vyom_services_env_file, "w") as f:
#                 f.write("#!/bin/bash\n")
#                 if python_path:
#                     f.write(f'export PYTHONPATH="{python_path.strip()}"\n')
#                 if ament_prefix_path:
#                     f.write(f'export AMENT_PREFIX_PATH="{ament_prefix_path.strip()}"\n')
#                 if ld_library_path:
#                     f.write(f'export LD_LIBRARY_PATH="{ld_library_path.strip()}"\n')
#                 if rmw_implementation:
#                     f.write(
#                         f'export RMW_IMPLEMENTATION="{rmw_implementation.strip()}"\n'
#                     )
#                 # f.write(f'export RMW_IMPLEMENTATION="rmw_cyclonedds_cpp"\n')

#             subprocess.run(["chmod", "+x", vyom_services_env_file], check=True)

#             print(f"✅ ROS2 environment variables saved to: {vyom_services_env_file}")
#         else:  # the file saved already before
#             print(f"✅ Using Exiting ROS2 env variables saved at: {vyom_services_env_file}")
#         return True

#     except Exception as e:
#         print(f"❌ Error saving ROS2 environment file: {e}")
#         return False


def install_rabbitmq():
    """
    Install and configure RabbitMQ server

    Returns:
        bool: True if installation was successful, False otherwise
    """
    print("\n--- STEP 1: Installing and configuring RabbitMQ server ---")

    try:
        # Update package lists
        # print("Updating package lists...")
        # subprocess.run(["apt", "update", "-y"], check=True)

        # Install RabbitMQ server
        print("Installing RabbitMQ server...")
        subprocess.run(["apt", "install", "rabbitmq-server", "-y"], check=True)

        # Start the RabbitMQ service
        print("Starting RabbitMQ service...")
        subprocess.run(["systemctl", "start", "rabbitmq-server"], check=True)

        # Enable RabbitMQ to start on boot
        print("Enabling RabbitMQ to start on boot...")
        subprocess.run(["systemctl", "enable", "rabbitmq-server"], check=True)

        # Enable the RabbitMQ management plugin
        print("Enabling RabbitMQ management plugin...")
        subprocess.run(
            ["rabbitmq-plugins", "enable", "rabbitmq_management"], check=True
        )

        print("RabbitMQ installation and configuration completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during RabbitMQ installation: {e}")
        return False


def _get_machine_data_topic_list():
    # return machine_topics_list
    try:
        topics_discoverer = ROSTopic(discovery_timeout=5.0)
        topic_list = topics_discoverer.serialize_topic_list()

        # cleanup before exit
        try:
            topics_discoverer.cleanup()
        except:
            pass
        if len(topic_list):
            return topic_list, None
        else:
            return [], "Error - No ROS topics detected"
    except Exception as e:

        # cleanup before exit
        try:
            topics_discoverer.cleanup()
        except:
            pass

        error = f"Error - Failed to fetch ROS topics: {str(e)}"
        return [], error


def _fetch_organization_models(organization_id, otp):
    """
    Fetch machine models for an organization using API call
    Args:
        organization_id (str): The organization ID
        otp (str): One-time password for authentication

    Returns:
        dict: Response containing models and possibly new OTP
    """
    try:
        headers = {
            "Content-Type": "application/json",
        }
        payload = {"otp": otp, "organization_id": organization_id}

        response = requests.post(MACHINE_MODELS_API_URL, headers=headers, json=payload)
        data = response.json()
        if data.get("status") == 200:
            otp = str(data["data"].get("otp", ""))
            session_id = str(data["data"].get("session_id", ""))
            machine_models = data["data"].get("machine_models", [])
            return otp, session_id, machine_models
        else:
            error_message = data.get("error", {}).get(
                "message",
                "API failed due to an unknown error - please contact the support team.",
            )
            raise Exception(error_message)

    except Exception as e:
        raise


def register_machine(interactive=True):
    """
    Register the machine with VyomOS API or display existing configuration
    if already registered.

    Args:
        interactive (bool): Whether to run in interactive mode and prompt for input

    Returns:
        bool: True if registration was successful or config already exists,
              False otherwise
        dict: Response data from the API call if successful, or config data if
              already registered, empty dict otherwise
    """
    print("\n--- STEP 2: Machine Registration Check ---")

    # Check if config file already exists
    if os.path.exists(machine_config_file):
        print(f"Configuration file already exists at: {machine_config_file}")
        try:
            # Read existing configuration
            config = configparser.ConfigParser()
            config.read(machine_config_file)

            if "MACHINE" in config:
                machine_id = config["MACHINE"].get("machine_id", "Unknown")
                machine_uid = config["MACHINE"].get("machine_uid", "Unknown")
                organization_id = config["MACHINE"].get("organization_id", "Unknown")
                organization_name = config["MACHINE"].get(
                    "organization_name", "Unknown"
                )
                machine_name = config["MACHINE"].get("machine_name", "Unknown")

                print("\n--- Basic Machine Details ---")
                print(f"Machine ID: {machine_id}")
                print(f"Machine UID: {machine_uid}")
                print(f"Machine Name: {machine_name}")
                print(f"Organization ID: {organization_id}")
                print(f"Organization Name: {organization_name}")

                return True, {}
            else:
                print(
                    "Warning: Configuration file exists but appears to be invalid. Re-registering..."
                )
        except Exception as e:
            print(f"Error reading configuration file: {e}")

    print("\n--- STEP 2: Registering machine with VyomIQ ---")

    # Check if we're running with sufficient privileges
    needs_sudo = os.geteuid() != 0

    if not interactive:
        print("Running in non-interactive mode. Machine registration skipped.")
        return False, {}

    # Get machine registration information
    organization_id = input("Organization ID: ").strip()
    print("Fetching organization-related details...")
    otp = input("Enter the OTP: ").strip()

    # Fetch machine models from API
    try:
        # API call to fetch machine models
        try:
            new_otp, session_id, machine_models = _fetch_organization_models(
                organization_id, otp
            )
            otp = new_otp
        except Exception as e:
            print(f"Error fetching machine models: {e}")
            return False, {}
    except Exception as e:
        print(f"Error fetching machine models: {e}")
        return False, {}

    # Prompt for machine details

    # Display machine models in a table format
    print("\n--- Available Machine Models ---")

    print("| {:<10} | {:<20} | {:<30} |".format("Model ID", "Model UID", "Model Name"))
    print("|" + "-" * 12 + "|" + "-" * 22 + "|" + "-" * 32 + "|")

    for model in machine_models:
        print(
            "| {:<10} | {:<20} | {:<30} |".format(
                model.get("id", "N/A"),
                model.get("model_uid", "N/A"),
                model.get("name", "N/A"),
            )
        )
    print(
        "Choose a Machine Model ID from the list, or enter 'N' to create a new one..."
    )
    machine_model_id = input("Machine Model ID: ").strip().lower()
    if machine_model_id == "n" or machine_model_id == "'n'":
        machine_model_id = None
        machine_model_uid = input("Machine Model UID: ").strip()
        machine_model_name = input("Machine Model Name: ").strip()
        type = "drone"
        # TODO: If invalid, prompt the user multiple times to choose from the list.
    else:
        machine_model_id = int(machine_model_id)
        machine_model_uid = None
        machine_model_name = None
        type = None

    machine_uid = input("Machine UID: ").strip()
    machine_name = input("Machine Name: ").strip()

    # Validate input
    is_valid_model = machine_model_id or (
        machine_model_uid and machine_model_name and type
    )
    if not organization_id or not machine_uid or not is_valid_model:
        print("Missing required registration information. Registration failed.")
        return False, {}
    machine_model_topics, error = _get_machine_data_topic_list()
    if error:
        print(error)
        return False, {}
    # Create payload JSON
    payload = {
        "organization_id": int(organization_id),
        "otp": otp,  # string
        "session_id": session_id,
        # model detail
        "machine_model_id": machine_model_id,  # TODO just check int of None will work here or not
        "machine_model_uid": machine_model_uid,
        "machine_model_name": machine_model_name,
        "type": type,
        # machine detail
        "machine_uid": machine_uid,
        "name": machine_name,
        # machine topic detail
        "machine_model_topics": machine_model_topics,
    }

    # Make API call to register machine
    print("Registering machine with VyomIQ...")
    try:

        response = requests.post(
            MACHINE_REGISTER_API_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
        )

        # Check response
        data = response.json()
        if data.get("status") == 200:
            print("Machine registration successful!")

            if needs_sudo:
                print(f"Creating config directory requires root privileges.")
                print(f"Please run: sudo mkdir -p {vyom_root_dir}")
                print(f"Response data: {json.dumps(data)}")
                print("")
                print(
                    "======>    PLEASE MANUALLY CREATE THE CONFIGURATION FILE.  <======="
                )
                return True, data
            else:
                os.makedirs(vyom_root_dir, exist_ok=True)

                # Save configuration
                print("Saving machine configuration...")

                # Extract data from response and save in INI format
                config = configparser.ConfigParser()
                config["MACHINE"] = {
                    "machine_id": str(data["data"].get("id", "")),
                    "machine_uid": data["data"].get("machine_uid", ""),
                    "machine_name": data["data"].get("name", ""),
                    "machine_model": str(data["data"].get("machine_model", "")),
                    "machine_model_name": data["data"].get("machine_model_name", ""),
                    "machine_model_type": data["data"].get("machine_model_type", ""),
                    "mfg_date": data["data"].get("mfg_date", ""),
                    "activation_date": str(data["data"].get("activation_date", "")),
                    "end_of_service_date": str(
                        data["data"].get("end_of_service_date", "")
                    ),
                    "organization_id": str(data["data"].get("current_owner", "")),
                    "organization_name": data["data"].get("current_owner_name", ""),
                    "usage_status": data["data"].get("usage_status", ""),
                    "camera_feed": data["data"].get("camera_feed", ""),
                    "created_at": data["data"].get("created_at", ""),
                    "updated_at": data["data"].get("updated_at", ""),
                    "session_id": data["data"].get("session_id", ""),
                }
                print(
                    "=====>  Your new Machine Model ID is -",
                    str(data["data"].get("machine_model", "")),
                    " <======",
                )

                try:
                    with open(machine_config_file, "w") as f:
                        config.write(f)
                    print(f"Configuration saved to {machine_config_file}")

                    # Check if IoT data is present in the response
                    if "iot_data" in data["data"]:
                        iot_data = data["data"]["iot_data"]
                        machine_id = data["data"].get("id", "")

                        print("Saving IoT certificates...")
                        os.makedirs(cert_dir, exist_ok=True)
                        try:
                            # Save the certificate
                            with open(cert_file_path, "w") as f:
                                f.write(iot_data["certificate"]["certificatePem"])

                            # Save the private key
                            with open(pri_key_file_path, "w") as f:
                                f.write(
                                    iot_data["certificate"]["keyPair"]["PrivateKey"]
                                )

                            # Save the public key
                            with open(pub_key_file_path, "w") as f:
                                f.write(iot_data["certificate"]["keyPair"]["PublicKey"])

                            # Save the root CA
                            with open(root_ca_file_path, "w") as f:
                                f.write(iot_data["root_ca"])

                            print(f"IoT certificates saved to {cert_dir}")

                            # Update config with certificate paths
                            config["IOT"] = {
                                "thing_name": iot_data["thing_name"],
                                "thing_arn": iot_data["thing_arn"],
                                "policy_name": iot_data["policy_name"],
                                "certificate_path": cert_file_path,
                                "private_key_path": pri_key_file_path,
                                "public_key_path": pub_key_file_path,
                                "root_ca_path": root_ca_file_path,
                            }

                            # Update the config file with IoT information
                            with open(machine_config_file, "w") as f:
                                config.write(f)
                            print(f"Configuration updated with IoT information")

                        except Exception as e:
                            print(f"Error saving IoT certificates: {e}")
                    else:
                        print("No IoT credentials found in response")

                    return True, data
                except Exception as e:
                    print(f"Error saving configuration: {e}")
                    return False, {}
        else:
            print(f"Machine registration failed with status: {data.get('status')}")
            print(f"Response: {data}")
            return False, {}

    except Exception as e:
        print(f"Error during machine registration: {e}")
        return False, {}


def fetch_topics(interactive=True):
    """
    Fetch and save machine subscribed topics from the API

    Args:
        interactive (bool): Whether to run in interactive mode and prompt for input

    Returns:
        tuple: (success (bool), data (dict))
    """
    print("\n--- Fetching machine subscribed topic ---")

    # Prompt user for confirmation if already configured
    # if interactive:
    #     user_input = (
    #         input(
    #             "Have you already configured the subscribed topics for this machine model? [Y/n]: "
    #         )
    #         .strip()
    #         .lower()
    #     )
    #     if user_input not in ["y", "yes"]:
    #         print(
    #             "Skipping topic fetch as per user input. please run setup again once you are done"
    #         )
    #         return False, {}

    # Check if config file already exists
    if os.path.exists(machine_config_file):
        print(f"Configuration file reading from: {machine_config_file}")
        try:
            # Read existing configuration
            config = configparser.ConfigParser()
            config.read(machine_config_file)
            if "MACHINE" in config:
                machine_model_id = config["MACHINE"].get("machine_model", "")
                if not machine_model_id:
                    print("Error: Machine model ID not found in configuration file.")
                    print(f"Please delete {machine_config_file} and set up again.")
                    return False, {}

                try:
                    url = MACHINE_TOPICS_API_URL
                    params = {"machine_model_id": machine_model_id}
                    full_url = f"{url}?{urlencode(params)}"
                    headers = {
                        "Content-Type": "application/json",
                    }
                    payload = {"machine_model_id": machine_model_id}
                    response = requests.get(full_url, headers=headers)

                    if response.status_code != 200:
                        print(f"Error: API returned status code {response.status_code}")
                        return False, {}

                    data = response.json()

                    # Save fetched topics to machine_topics_file
                    os.makedirs(os.path.dirname(machine_topics_file), exist_ok=True)
                    with open(machine_topics_file, "w") as f:
                        json.dump(data, f, indent=4)
                    print(f"Topics successfully saved to {machine_topics_file}")
                    return True, data

                except requests.RequestException as e:
                    print(f"Error: Failed to connect to API: {e}")
                    print(f"Please re-run setup again after some time")
                    return False, {}
                except json.JSONDecodeError:
                    print("Error: Received invalid JSON response from API")
                    return False, {}
                except Exception as e:
                    print(
                        f"Error: in fetching machine topics from API or saving to {machine_topics_file}: {e}"
                    )
                    print("Please try setting up again.")
                    return False, {}
            else:
                print(f"Error: Configuration file exists but appears to be invalid.")
                print(f"Please delete {machine_config_file} and set up again.")
                return False, {}
        except Exception as e:
            print(f"Error: Failed to read configuration file: {e}")
            print(f"Please delete {machine_config_file} and set up again.")
            return False, {}
    else:
        print(
            f"Error: Machine configuration file ({machine_config_file}) does not exist."
        )
        print("Please run the setup process first.")
        return False, {}


def poll_for_topics(session_id, machine_model_id, timeout=900, interval=5):
    """
    Poll the machine-model/topic/list/ endpoint until topics are available or timeout.
    Args:
        session_id (str): Session ID for the request
        machine_model_id (str|int): Machine model ID
        timeout (int): Max seconds to poll
        interval (int): Seconds between polls
    Returns:
        bool: True if topics were fetched and saved, False otherwise
    """
    print(
        "\nPlease complete the setup on the Fleet manager to complete the setup of your new device."
    )
    print("Waiting for topics to be configured in the Fleet manager UI...")
    start_time = time.time()
    url = MACHINE_TOPICS_API_URL
    params = {"session_id": session_id, "machine_model_id": machine_model_id}
    full_url = f"{url}?{urlencode(params)}"
    headers = {"Content-Type": "application/json"}
    while time.time() - start_time < timeout:
        try:
            response = requests.get(full_url, headers=headers)
            if response.status_code == 200:
                topics = response.json()
                if topics and isinstance(topics, (list, dict)) and len(topics) > 0:
                    # Save topics to machine_topics_file
                    os.makedirs(os.path.dirname(machine_topics_file), exist_ok=True)
                    with open(machine_topics_file, "w") as f:
                        json.dump(topics, f, indent=4)
                    print(
                        f"\nTopics successfully fetched and saved to {machine_topics_file}"
                    )
                    return True
            else:
                print(f"Polling... (status: {response.status_code})")
        except Exception as e:
            print(f"Polling error: {e}")
        time.sleep(interval)
    print(
        "\nTimeout: Topics were not configured in the Fleet manager within the expected time."
    )
    return False


def setup_shell_script():
    """
    Create the shell script for vyomcloudbridge and make it executable

    Returns:
        bool: True if shell script setup was successful, False otherwise
    """
    print("\n--- STEP 3: Setting up vyomcloudbridge shell script ---")

    import os
    import subprocess
    import getpass

    # Check if we're running with sufficient privileges
    needs_sudo = os.geteuid() != 0

    # Shell script content
    shell_script_content = """#!/bin/bash
# Wait for system to fully boot
sleep 15

export PYTHONUNBUFFERED=1

# Start all the services
echo "Starting vyomcloudbridge services..."
source /vyomos/.bash_sources
source /opt/ros/humble/setup.bash
source /vyomos/os/robotics/install/setup.bash
source /root/ros2_ws/install/setup.bash
source /home/shitiz/workspaces/orville/install/setup.bash
source ~/Fast-DDS/install/setup.bash
vyomcloudbridge restart
vyomcloudbridge start queueworker --multi-thread --system-default
vyomcloudbridge start missionstats --system-default
vyomcloudbridge start machinestats --system-default
vyomcloudbridge start rospublisher --system-default
# vyomcloudbridge start vyomlistener --system-default

echo "All system default's services started successfully"

# This keeps the systemd service active/ running indefinitely with minimal resource usage
echo "Services are running, monitoring process active"
tail -f /dev/null

# The script will only reach this point if explicitly terminated
echo "vyomcloudbridge monitor shutting down"
"""

    if needs_sudo:
        # Create template for manual installation
        temp_script_dir = os.path.expanduser("~/vyomcloudbridge_scripts")
        temp_script_file = os.path.join(temp_script_dir, "vyomcloudbridge.sh")

        try:
            os.makedirs(temp_script_dir, exist_ok=True)

            with open(temp_script_file, "w") as f:
                f.write(shell_script_content)

            # Try to make the script executable
            os.chmod(temp_script_file, 0o755)

            print(f"Shell script created at: {temp_script_file}")
            print("Run the following commands to install the script:")
            print(f"sudo mkdir -p {vyom_root_dir}")
            print(f"sudo cp {temp_script_file} {start_script_file}")
            print(f"sudo chmod +x {start_script_file}")
            return True
        except Exception as e:
            print(f"Error creating shell script template: {e}")
            return False
    else:
        # We have sudo privileges, create the file directly
        try:
            os.makedirs(vyom_root_dir, exist_ok=True)

            with open(start_script_file, "w") as f:
                f.write(shell_script_content)

            # Make the script executable
            print("Setting execute permissions on shell script...")
            subprocess.run(["chmod", "+x", start_script_file], check=True)

            print(
                f"Shell script has been created at {start_script_file} and made executable."
            )
            return True
        except Exception as e:
            print(f"Error creating or setting permissions on shell script: {e}")
            return False


def setup_service():
    """
    Create and start the systemd service for vyomcloudbridge

    Returns:
        bool: True if service setup was successful, False otherwise
    """
    print("\n--- STEP 4: Setting up vyomcloudbridge service ---")

    # Check if we're running with sufficient privileges
    needs_sudo = os.geteuid() != 0

    if needs_sudo:
        # Create template for manual installation
        username = getpass.getuser()
        temp_service_file = os.path.expanduser("~/vyomcloudbridge.service")

        try:
            # TODO later we willl replace User=root with User={username}
            with open(temp_service_file, "w") as f:
                f.write(
                    f"""[Unit]
Description=VyomCloudBridge Service
After=network.target rabbitmq-server.service
Wants=rabbitmq-server.service

[Service]
Type=simple
User=root
Group=root
WorkingDirectory={vyom_root_dir}
ExecStart=/bin/bash -c 'source /home/shitiz/.bashrc && {start_script_file}'
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal
LogRateLimitIntervalSec=0
LogRateLimitBurst=0
KillMode=process
KillSignal=SIGTERM
TimeoutStartSec=60
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target
"""
                )

            print(f"Service file template created at: {temp_service_file}")
            print("Run the following commands to install and enable the service:")
            print(f"sudo cp {temp_service_file} {service_file_path}")
            print("sudo systemctl daemon-reload")
            print("sudo systemctl enable vyomcloudbridge.service")
            print("sudo systemctl start vyomcloudbridge.service")
            return True
        except Exception as e:
            print(f"Error creating service template: {e}")
            return False
    else:
        # We have sudo privileges, create the file directly
        # Try to get the actual username even when running with sudo
        try:
            username = subprocess.check_output(["logname"], text=True).strip()
        except subprocess.CalledProcessError:
            username = getpass.getuser()

        try:
            # TODO later we willl replace User=root with User={username}
            with open(service_file_path, "w") as f:
                f.write(
                    f"""[Unit]
Description=VyomCloudBridge Service
After=network.target rabbitmq-server.service
Wants=rabbitmq-server.service

[Service]
Type=simple
User=root
Group=root
WorkingDirectory={vyom_root_dir}
ExecStart=/bin/bash -c 'source ~/.bashrc && {start_script_file}'
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal
LogRateLimitIntervalSec=0
LogRateLimitBurst=0
KillMode=process
KillSignal=SIGTERM
TimeoutStartSec=60
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target
"""
                )
            print(f"Vyomcloudbridge Service has been created at {start_script_file}")

            print("Reloading systemd daemon...")
            subprocess.run(["systemctl", "daemon-reload"], check=True)

            # Enable and start the service
            print("Enabling and starting vyomcloudbridge service...")
            subprocess.run(
                ["systemctl", "enable", "vyomcloudbridge.service"], check=True
            )
            subprocess.run(
                ["systemctl", "start", "vyomcloudbridge.service"], check=True
            )
            print("Service has been installed and started.")
            return True
        except Exception as e:
            print(f"Error creating or starting service: {e}")
            return False


def setup_log_directories():
    """
    Create necessary log directories and files with 777 permissions

    Returns:
        bool: True if setup was successful, False otherwise
    """
    print("\n--- STEP 5: Setting up log directories and files ---")

    # Check if we're running with sufficient privileges
    needs_sudo = os.geteuid() != 0

    try:
        if needs_sudo:
            print("Creating log directories requires administrative privileges.")
            print("Please run the following commands:")
            print(f"sudo mkdir -p {log_dir}")
            print(f"sudo touch {log_file}")
            print(f"sudo touch {pid_file}")
            print(f"sudo chmod 777 {log_dir}")  # Updated to 777
            print(f"sudo chmod 777 {log_file}")  # Updated to 777
            print(f"sudo chmod 777 {pid_file}")  # Updated to 777

            # For a non-admin user to write to these files
            username = getpass.getuser()
            print(f"sudo chown {username} {log_dir}")
            print(f"sudo chown {username} {log_file}")
            print(f"sudo chown {username} {pid_file}")

            return True
        else:
            print(f"Creating log directory: {log_dir}")
            os.makedirs(log_dir, exist_ok=True)

            print(f"Setting up log file: {log_file}")
            if not os.path.exists(log_file):
                with open(log_file, "w") as f:
                    pass  # Just create an empty file

            print(f"Setting up PID file: {pid_file}")
            if not os.path.exists(pid_file):
                with open(pid_file, "w") as f:
                    f.write("{}")  # Initialize with empty JSON object

            print("Setting full permissions (777/666)...")
            # Set 777 permissions for directory (rwxrwxrwx)
            os.chmod(log_dir, 0o777)
            # Set 777 permissions for files (rwxrwxrwx)
            os.chmod(log_file, 0o777)
            os.chmod(pid_file, 0o777)

            try:
                username = subprocess.check_output(["logname"], text=True).strip()
            except subprocess.CalledProcessError:
                username = getpass.getuser()

            # Only change owner (not group) to avoid issues with mismatched group names
            try:
                subprocess.run(["chown", username, log_dir], check=True)
                subprocess.run(["chown", username, log_file], check=True)
                subprocess.run(["chown", username, pid_file], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Warning: Could not change ownership: {e}")
                # Already set to 777, so no need for fallback permissions

            print(
                f"Log directories and files setup completed successfully with full permissions (777)."
            )
            return True

    except Exception as e:
        print(f"Error setting up log directories and files: {e}")
        return False


def setup(interactive=True):
    """
    Perform the VyomCloudBridge setup process.
    This is a Python implementation of the install_script.sh functionality.

    Args:
        interactive (bool): Whether to run in interactive mode and prompt for input

    Returns:
        bool: True if setup completed successfully, False otherwise
    """
    print("\n=== Starting VyomCloudBridge Setup ===\n")

    # Print welcome message
    print("Running post-installation setup for vyomcloudbridge...")
    success = True

    # Check if we're running with sufficient privileges
    needs_sudo = os.geteuid() != 0
    if needs_sudo:
        print("Note: Some operations may require administrative privileges.")

    rosenv_success = True
    if not needs_sudo:
        rosenv_success = setup_ros2_workspaces()
        if not rosenv_success:
            print("Ros environment fetch unsuccessful!, Exiting...")
            success = False
            return False

    # STEP 1: Install RabbitMQ (only if we have root privileges)
    rabbitmq_success = True
    if not needs_sudo:
        rabbitmq_success = install_rabbitmq()
        if not rabbitmq_success:
            print("RabbitMQ installation failed!, Exiting...")
            success = False
            # return False
    else:
        print("\nSkipping RabbitMQ installation (requires root privileges)")
        print("You can install RabbitMQ manually with the following commands:")
        print("sudo apt update -y")
        print("sudo apt install rabbitmq-server -y")
        print("sudo systemctl start rabbitmq-server")
        print("sudo systemctl enable rabbitmq-server")
        print("sudo rabbitmq-plugins enable rabbitmq_management")

    # STEP 2: Register machine
    registration_success, _ = register_machine(interactive=interactive)
    if not registration_success and interactive:
        print("Machine registration failed!, Exiting...")
        success = False
        return False

    # STEP 2.1: fetch machine subscribe topic
    session_id = None
    machine_model_id = None
    if registration_success:
        max_retries = 3
        retry_count = 0
        topic_fetch_success = False
        # Try to get session_id and machine_model_id from config or registration
        try:
            if os.path.exists(machine_config_file):
                config = configparser.ConfigParser()
                config.read(machine_config_file)
                if "MACHINE" in config:
                    machine_model_id = config["MACHINE"].get("machine_model", None)
                    session_id = config["MACHINE"].get("session_id", None)
        except Exception:
            pass
        while retry_count < max_retries and not topic_fetch_success:
            try:
                topic_fetch_success, _ = fetch_topics(interactive=interactive)
                if not topic_fetch_success and interactive:
                    retry_count += 1
                    if retry_count < max_retries:
                        print(
                            f"Machine topics fetch failed! Retrying... (Attempt {retry_count + 1}/{max_retries})"
                        )
                    else:
                        print(
                            "Machine topics fetch failed after maximum retries! Exiting..."
                        )
                        success = False
                        return False
            except Exception as e:
                retry_count += 1
                if retry_count < max_retries:
                    print(
                        f"Error fetching topics: {str(e)}. Retrying... (Attempt {retry_count + 1}/{max_retries})"
                    )
                else:
                    print(
                        f"Failed to fetch topics after {max_retries} attempts. Error: {str(e)}"
                    )
                    success = False
                    return False
    # STEP 3: Setup shell script
    script_success = setup_shell_script()
    if not script_success:
        print("Shell script setup failed!, Exiting...")
        success = False
        return False

    # STEP 4: Setup service
    service_success = setup_service()
    if not service_success:
        print("Service setup failed!, Exiting...")
        success = False
        return False

    # STEP 5: logs file and permission
    files_setup_success = setup_log_directories()
    if not files_setup_success:
        print("Script log directories failed!, Exiting...")
        success = False
        return False

    # Print message for Fleet manager step
    print(
        "\nPlease complete setup on your fleet manager to finish the device registration."
    )

    # STEP 6: Poll for topics after Fleet manager setup
    if session_id and machine_model_id:
        poll_success = poll_for_topics(session_id, machine_model_id)
        if not poll_success:
            print(
                "Setup could not complete because topics were not configured in time."
            )
            return False
    else:
        print(
            "Missing session_id or machine_model_id for polling topics. Skipping STEP 6."
        )
        return False

    # Final status
    if success:
        print(
            "\n=== VyomIQ setup finished, please continue further setup on your browser. ==="
        )
    else:
        print("\n=== VyomCloudBridge setup encountered errors ===")
        print("Please resolve the issues and try again.")

    return success


if __name__ == "__main__":
    # Check if script is run with --non-interactive flag
    is_interactive = "--non-interactive" not in sys.argv
    success = setup(interactive=is_interactive)

    # Exit with appropriate status code
    if not success:
        sys.exit(1)
