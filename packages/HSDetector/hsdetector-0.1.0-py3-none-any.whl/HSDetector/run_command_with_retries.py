import subprocess
import time
import sys

def run_command_with_retries(command, max_retries=10, delay=2):
    """
    Run a terminal command with retries on failure.

    Args:
        command (str or list): The command to run
        max_retries (int): Maximum number of retries (default 10)
        delay (float): Delay between retries in seconds (default 1)
    """
    retries = 0

    while retries < max_retries:
        try:
            # Run the command - shell=True if command is a string, False if list
            result = subprocess.run(
                command,
                shell=isinstance(command, str),
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print("[INFO] Martinize2 success, proceeding with next step")
            print("Output:", result.stdout)
            return True

        except subprocess.CalledProcessError as e:
            retries += 1
            print(f"[INFO] Martinize2 failed (attempt {retries}/{max_retries}): {e}")
            print("Error output:", e.stderr)

            if retries < max_retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)

    # At this point, all attempts failed, so crash the program
    print(f"[FATAL ERROR] Martinize2 failed after {max_retries} attempts. Check your input structure for issues.")
    sys.exit(1)