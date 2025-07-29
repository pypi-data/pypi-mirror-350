"""A module for controlling the Android emulator and interacting with it via ADB."""

import os
import sys
import time
import argparse
import platform
import subprocess
from pathlib import Path

from whatxtract.utils import generate_vcf_batches, timestamped_output_path
from whatxtract.constants import VCF_DIR
from whatxtract.db_parser import extract_valid_contacts

_adb_path: str | None = None


def get_adb_path() -> str:
    """Return the effective ADB path, considering any overrides."""
    global _adb_path
    if _adb_path is not None:
        return _adb_path
    else:
        """Detect platform and set OS-aware ADB binary location."""
        system = platform.system()
        path_map = {
            'Windows': Path(__file__).resolve().parents[1] / 'platform-tools/windows/adb.exe',
            'Darwin': Path(__file__).resolve().parents[1] / 'platform-tools/mac/adb',
            'Linux': Path(__file__).resolve().parents[1] / 'platform-tools/linux/adb',
        }

        return str(path_map.get(system, 'adb'))  # last fallback: assume adb in PATH


def set_adb_path(custom_path: str):
    """Override the ADB binary path."""
    global _adb_path
    resolved_path = Path(custom_path).resolve()
    if not resolved_path.exists():
        raise FileNotFoundError(f'Provided ADB path does not exist: {resolved_path}')
    if not resolved_path.is_file() or not os.access(resolved_path, os.X_OK):
        raise PermissionError(f'ADB path exists but is not executable: {resolved_path}')

    _adb_path = str(resolved_path)


def run_adb_command(cmd, check=True):
    """Run an ADB command and return the output."""
    full_cmd = [get_adb_path(), *cmd]
    result = subprocess.run(full_cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise RuntimeError(f'ADB command failed: {" ".join(full_cmd)}\n{result.stderr.strip()}')
    return result.stdout.strip()


def ensure_device_connected():
    """Ensure at least one device is connected via ADB."""
    output = run_adb_command(['devices'], check=False)
    lines = output.splitlines()
    devices = [line.split()[0] for line in lines if '\tdevice' in line]
    if not devices:
        raise RuntimeError('No ADB devices connected.')
    print(f'[ADB] Connected device(s): {", ".join(devices)}')
    return devices[0]


def push_vcf_to_emulator(batch_number):
    """Push a VCF file to the emulator's storage."""
    ensure_device_connected()
    vcf_file = VCF_DIR / f'batch_{batch_number}.vcf'
    if not vcf_file.exists():
        raise FileNotFoundError(f'VCF file not found: {vcf_file}')
    remote_path = f'/sdcard/batch_{batch_number}.vcf'
    run_adb_command(['push', str(vcf_file), remote_path])
    print(f'[ADB] Pushed VCF to {remote_path}')
    return remote_path


def import_vcf_via_intent(remote_vcf_path):
    """Trigger an Android intent to import the VCF file using the default Contacts app."""
    ensure_device_connected()
    command = [
        'shell',
        'am',
        'start',
        '-a',
        'android.intent.action.VIEW',
        '-d',
        f'file://{remote_vcf_path}',
        '-t',
        'text/x-vcard',
    ]
    run_adb_command(command)
    print(f'[ADB] Triggered contact import for {remote_vcf_path}')


def grant_contact_permissions(package_name='com.android.contacts'):
    """Grant contacts read/write permissions to the stock Contacts app."""
    ensure_device_connected()
    permissions = [
        'android.permission.READ_CONTACTS',
        'android.permission.WRITE_CONTACTS',
        'android.permission.READ_EXTERNAL_STORAGE',
    ]
    for perm in permissions:
        run_adb_command(['shell', 'pm', 'grant', package_name, perm])
        print(f'[ADB] Granted {perm} to {package_name}')


def clear_contacts():
    """Clear the contact database."""
    clear_cmd = ['shell', 'pm', 'clear', 'com.android.providers.contacts']
    run_adb_command(clear_cmd, check=True)


def is_device_rooted():
    """Check if the device is rooted."""
    try:
        output = run_adb_command(['shell', 'su', '-c', 'id'], check=False)
        return 'uid=0(root)' in output
    except (Exception, RuntimeError):
        return False


def restart_adb_as_root():
    """Restart ADB as root if the device supports it."""
    output = run_adb_command(['root'], check=False)
    if 'adb cannot run as root' in output:
        print('[ADB] Root access not available.')
        return False
    time.sleep(2)  # wait for ADB to restart
    print('[ADB] ADB restarted with root access.')
    return True


def start_emulator(emulator_name: str = 'Genymotion') -> None:
    """
    Starts the Genymotion emulator using the `player` command line tool.

    Args:
        emulator_name (str): Optional name of the emulator. Assumes Genymotion's `player` CLI is installed.
    """
    print(f'[INFO] Starting emulator: {emulator_name}')
    try:
        subprocess.Popen(['player', '--vm-name', emulator_name])
    except FileNotFoundError:
        print("[ERROR] Genymotion 'player' binary not found in PATH.")
        sys.exit(1)


def wait_for_device(timeout: int = 60) -> None:
    """
    Waits until an ADB device is connected and ready.

    Args:
        timeout (int): Maximum time (in seconds) to wait.
    """
    print('[INFO] Waiting for emulator/device to be ready...')
    start_time = time.time()
    while True:
        result = run_adb_command(['get-state'], check=True)
        if 'device' in result:
            print('[INFO] Device is ready.')
            return
        if time.time() - start_time > timeout:
            print('[ERROR] Timeout while waiting for device.')
            sys.exit(1)
        time.sleep(2)


def grant_root_permissions() -> None:
    """Grants root permissions to the emulator (if supported)."""
    print('[INFO] Attempting to grant root access...')
    run_adb_command(['root'], check=True)
    run_adb_command(['remount'], check=True)
    print('[INFO] Root access granted.')


def stop_emulator() -> None:
    """Stops the currently running emulator via ADB."""
    print('[INFO] Stopping emulator...')
    run_adb_command(['emu', 'kill'], check=True)


def main():
    """Main function for controlling the emulator and interacting with it via ADB."""
    parser = argparse.ArgumentParser(description='WAxtract - Bulk WhatsApp Valid Contacts Extractor')
    # fmt: off
    parser.add_argument('--input', required=True, help='Path to input TXT file with phone numbers')
    parser.add_argument('--batch-size', type=int, default=5000, help='Number of vcf_contacts per batch')
    parser.add_argument('--output-dir', default='output/', help='Directory to save CSV output')
    parser.add_argument('--delay', type=int, default=30, help='Seconds to wait before DB dump')
    parser.add_argument('--adb-path', default='adb', help='Path to ADB binary')
    parser.add_argument('--auto-cleanup', action='store_true', help='Remove vcf_contacts after each batch')
    # fmt: on

    args = parser.parse_args()

    print(f'📂 Reading vcf_contacts from: {args.input}')
    batches = generate_vcf_batches(args.input, args.batch_size)

    for i, vcf_file in enumerate(batches):
        print(f'📱 Batch {i + 1}/{len(batches)}: Importing {args.batch_size} vcf_contacts...')
        push_vcf_to_emulator(vcf_file)

        print(f'⏳ Waiting {args.delay} seconds for WhatsApp sync...')
        time.sleep(args.delay)

        print('📦 Extracting WhatsApp DB and parsing valid vcf_contacts...')
        contacts = extract_valid_contacts(adb_path=args.adb_path)

        output_file = timestamped_output_path(args.output_dir, prefix='valid_contacts', ext='csv')
        print(f'💾 Saving {len(contacts)} valid vcf_contacts to: {output_file}')
        with open(output_file, 'w') as f:
            f.write('Name,Phone\n')
            for name, phone in contacts:
                f.write(f'{name},{phone}\n')

        if args.auto_cleanup:
            print('🧹 Cleaning up imported vcf_contacts...')
            clear_contacts()

    print('✅ All batches processed successfully.')


if __name__ == '__main__':
    main()
