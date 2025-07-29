import subprocess
from typing import List, Optional

def run_adb_command(cmd: List[str], timeout=10):
    """
    Runs an adb command and returns its output.
    
    Parameters:
        cmd (list): List of adb command arguments, e.g., ["devices"].
        timeout (int): Timeout in seconds.
        
    Returns:
        str: The standard output from the command. If an error occurs, returns None.
    """
    full_cmd = ["adb"] + cmd
    try:
        result = subprocess.run(full_cmd, capture_output=True, text=True, timeout=timeout)
        if result.returncode != 0:
            print(f"Command failed: {' '.join(full_cmd)}\nError: {result.stderr}", flush=True)
        return "\n".join([
            result.stdout.strip(),
            result.stderr.strip()
        ])
    except subprocess.TimeoutExpired:
        print(f"Command timed out: {' '.join(full_cmd)}", flush=True)
        return None

def get_devices():
    """
    Retrieves the list of connected Android devices.
    
    Returns:
        list: A list of device serial numbers.
    """
    output = run_adb_command(["devices"])
    devices = []
    if output:
        lines = output.splitlines()
        # The first line is usually "List of devices attached". The following lines list individual devices.
        for line in lines[1:]:
            if line.strip():
                parts = line.split()
                if len(parts) >= 2 and parts[1] == "device":
                    devices.append(parts[0])
    return devices

def ensure_device(func):
    """
    A decorator that resolves the device parameter automatically if it's not provided.
    
    If 'device' is None or not present in the keyword arguments and only one device is connected,
    that device will be automatically used. If no devices are connected or multiple devices are
    connected, it raises a RuntimeError.
    """
    def wrapper(*args, **kwargs):
        devices = get_devices()
        if kwargs.get("device") is None:
            if not devices:
                raise RuntimeError("No connected devices.")
            if len(devices) > 1:
                raise RuntimeError("Multiple connected devices detected. Please specify a device.")
            kwargs["device"] = devices[0]
        if kwargs["device"] not in devices:
            output = run_adb_command(["-s", kwargs["device"], "get-state"])
            if output.strip() != "device":
                raise RuntimeError(f"[ERROR] {kwargs['device']} not connected. Please check.\n{output}")
        return func(*args, **kwargs)
    return wrapper

@ensure_device
def adb_shell(cmd: List[str], device:Optional[str]=None):
    """
    run adb shell commands

    Parameters:
        cmd (List[str])
        device (str, optional): The device serial number. If None, it's resolved automatically when only one device is connected.
    """
    return run_adb_command(["-s", device, "shell"] + cmd)


@ensure_device
def install_app(apk_path: str, device: Optional[str]=None):
    """
    Installs an APK application on the specified device.
    
    Parameters:
        apk_path (str): The local path to the APK file.
        device (str, optional): The device serial number. If None, it's resolved automatically when only one device is connected.
        
    Returns:
        str: The output from the install command.
    """
    return run_adb_command(["-s", device, "install", apk_path])


@ensure_device
def uninstall_app(package_name: str, device: Optional[str] = None):
    """
    Uninstalls an app from the specified device.
    
    Parameters:
        package_name (str): The package name of the app.
        device (str, optional): The device serial number. If None, it's resolved automatically when only one device is connected.
        
    Returns:
        str: The output from the uninstall command.
    """
    return run_adb_command(["-s", device, "uninstall", package_name])


@ensure_device
def push_file(local_path: str, remote_path: str, device: Optional[str] = None):
    """
    Pushes a file to the specified device.
    
    Parameters:
        local_path (str): The local file path.
        remote_path (str): The destination path on the device.
        device (str, optional): The device serial number. If None, it's resolved automatically when only one device is connected.
        
    Returns:
        str: The output from the push command.
    """
    local_path = str(local_path)
    remote_path = str(remote_path)
    return run_adb_command(["-s", device, "push", local_path, remote_path])


@ensure_device
def pull_file(remote_path: str, local_path: str, device: Optional[str] = None):
    """
    Pulls a file from the device to a local path.
    
    Parameters:
        remote_path (str): The file path on the device.
        local_path (str): The local destination path.
        device (str, optional): The device serial number. If None, it's resolved automatically when only one device is connected.
        
    Returns:
        str: The output from the pull command.
    """
    return run_adb_command(["-s", device, "pull", remote_path, local_path])


# Forward-related functions


@ensure_device
def list_forwards(device: Optional[str] = None):
    """
    Lists current port forwarding rules on the specified device.
    
    Parameters:
        device (str, optional): The device serial number. If None, it is resolved automatically.
        
    Returns:
        list: A list of forwarding rules. Each rule is a dictionary with keys: device, local, remote.
    """
    output = run_adb_command(["-s", device, "forward", "--list"])
    forwards = []
    if output:
        lines = output.splitlines()
        for line in lines:
            parts = line.split()
            if len(parts) == 3:
                # Each line is expected to be: <device> <local> <remote>
                rule = {"device": parts[0], "local": parts[1], "remote": parts[2]}
                if rule["device"] == device:
                    forwards.append(rule)
            else:
                forwards.append(line)
    return forwards


@ensure_device
def create_forward(local_spec: str, remote_spec: str, device: Optional[str] = None):
    """
    Creates a port forwarding rule on the specified device.
    
    Parameters:
        local_spec (str): The local forward specification (e.g., "tcp:8000").
        remote_spec (str): The remote target specification (e.g., "tcp:9000").
        device (str, optional): The device serial number. If None, it is resolved automatically.
        
    Returns:
        str: The output from the forward creation command.
    """
    return run_adb_command(["-s", device, "forward", local_spec, remote_spec])


@ensure_device
def remove_forward(local_spec, device: Optional[str] = None):
    """
    Removes a specific port forwarding rule on the specified device.
    
    Parameters:
        local_spec (str): The local forward specification to remove (e.g., "tcp:8000").
        device (str, optional): The device serial number. If None, it is resolved automatically.
        
    Returns:
        str: The output from the forward removal command.
    """
    return run_adb_command(["-s", device, "forward", "--remove", local_spec])


@ensure_device
def remove_all_forwards(device: Optional[str] = None):
    """
    Removes all port forwarding rules on the specified device.
    
    Parameters:
        device (str, optional): The device serial number. If None, it is resolved automatically.
        
    Returns:
        str: The output from the command to remove all forwards.
    """
    return run_adb_command(["-s", device, "forward", "--remove-all"])


if __name__ == '__main__':
    # For testing: print the list of currently connected devices.
    devices = get_devices()
    if devices:
        print("Connected devices:", flush=True)
        for dev in devices:
            print(f" - {dev}", flush=True)
    else:
        print("No devices connected.", flush=True)

    # Example usage of forward-related functionalities:
    try:
        # List current forwards
        forwards = list_forwards()
        print("Current forward rules:", flush=True)
        for rule in forwards:
            print(rule, flush=True)
            
        # Create a forward rule (example: forward local tcp 8000 to remote tcp 9000)
        output = create_forward("tcp:8000", "tcp:9000")
        print("Create forward output:", output, flush=True)
        
        # List forwards again
        forwards = list_forwards()
        print("Forward rules after creation:", flush=True)
        for rule in forwards:
            print(rule, flush=True)
        
        # Remove the forward rule
        output = remove_forward("tcp:8000")
        print("Remove forward output:", output, flush=True)
        
        # Remove all forwards (if needed)
        # output = remove_all_forwards()
        # print("Remove all forwards output:", output)
        
    except RuntimeError as e:
        print("Error:", e, flush=True)
