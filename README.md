
# SEEDLABS -MORRIS WORM

This script simulates a network worm attack. It creates and sends a malicious payload (`badfile2`) to a target host, which then executes a shell command and attempts to spread the worm further.

## Description

The script performs the following actions:
1. **Check for Existing Infection**: Determines if the host is already infected by checking for the presence of `badfile2`.
2. **Generate Malicious Payload**: Creates a payload with a shellcode that runs specified commands on the target host.
3. **Network Scanning**: Randomly generates IP addresses, pings them, and selects an active target for the attack.
4. **Send Malicious Payload**: Sends the payload to the target host.
5. **Spread the Worm**: If the target host is infected, the worm attempts to spread by sending itself to the newly infected host.

**Note**: This script is for educational purposes only. It should not be used for unauthorized or illegal activities. Ensure you have permission to test and deploy this script in controlled environments.

## Prerequisites

- Python 3
- `scapy` library (for network packet handling)
- `nc` (netcat) for network communication

## Usage

1. **Set Up**: Ensure that you have the required libraries and permissions.
2. **Run the Script**: Execute the script using Python 3. It will start scanning for targets and attempting to infect them.
   ```bash
   python3 worm.py
   ```

## Security Considerations

- **Testing Environment**: Run this script in a controlled, isolated environment to avoid unintended consequences.
- **Ethical Use**: Use responsibly and only with explicit authorization. Unauthorized use of this script is illegal and unethical.

## License

This project is licensed under SEEDLABS.

