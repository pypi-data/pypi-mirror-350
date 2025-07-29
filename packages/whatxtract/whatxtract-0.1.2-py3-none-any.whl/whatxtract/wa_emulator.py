#!/usr/bin/env python3
"""WAxtract - Bulk WhatsApp Valid Contacts Extractor."""

import argparse
from time import sleep
from pathlib import Path

from whatxtract.utils import write_tuples_to_csv, generate_vcf_batches, timestamped_output_path
from whatxtract.db_parser import extract_valid_contacts
from whatxtract.logging_setup import setup_logger
from whatxtract.adb_controller import (
    set_adb_path,
    stop_emulator,
    clear_contacts,
    start_emulator,
    wait_for_device,
    push_vcf_to_emulator,
    grant_root_permissions,
)


def parse_args():
    """Parse command-line arguments."""
    # fmt: off
    parser = argparse.ArgumentParser(description='WAxtract - Bulk WhatsApp Valid Contacts Extractor')
    parser.add_argument(
        '--input', '-i', type=str, required=True, help='Path to input .txt file (one number per line)'
    )
    parser.add_argument(
        '--output', '--output-dir', '-o',
        type=str, default=str(Path.cwd() / 'waxtract_output'),
        help="Directory to save the output CSV file. Defaults to './waxtract_output' if not specified.",
    )
    parser.add_argument(
        '--batch-size', '-b', type=int, default=5000, help='Number of contacts per VCF batch'
    )
    parser.add_argument(
        '--wait-time', '-w', '--delay', '-d',
        type=int, default=300,  # Default is 5 minutes = 300 seconds
        help='Time to wait after importing contacts for WhatsApp to sync (in seconds)',
    )
    parser.add_argument(
        '--mode', '-m',
        choices=['emulator'], default='emulator',
        help="Operation mode (currently only 'emulator' is supported)",
    )
    parser.add_argument(
        '--adb-path', '--adb', '-a', help='Path to the ADB binary to use (overrides default auto-detected one)'
    )
    parser.add_argument(
        '--auto-cleanup', '--cleanup', '-c', action='store_true', help='Remove vcf_contacts after each batch'
    )
    return parser.parse_args()


def main():
    """Main function for running the WhatsApp emulator."""
    args = parse_args()

    logger = setup_logger('whatxtract')

    if args.adb_path:
        print(f'⚙️ Setting adb path: {args.adb_path}')
        set_adb_path(args.adb_path)

    print(f'📂 Reading vcf_contacts from: {args.input}')
    vcf_files = generate_vcf_batches(args.input, args.batch_size)

    if args.mode == 'emulator':
        print('🧰 Starting emulator and preparing environment...')
        start_emulator()
        wait_for_device()
        grant_root_permissions()

        all_valid_contacts = []

        for idx, vcf_path in enumerate(vcf_files, 1):
            clear_contacts()
            print(f'📱 Batch {idx}/{len(vcf_files)}: Importing {vcf_path.name}')
            push_vcf_to_emulator(vcf_path)

            print(f'⏳ Waiting {args.wait_time} seconds for WhatsApp sync...')
            # TODO: adb-based WhatsApp open commands instead of fixed wait time
            sleep(args.wait_time)

            print('📦 Extracting WhatsApp DB and parsing valid vcf_contacts...')
            valid_contacts = extract_valid_contacts()

            print(f'🔍 Found {len(valid_contacts)} valid WhatsApp contacts in batch {idx}')
            all_valid_contacts.extend(valid_contacts)

            output_file = timestamped_output_path(args.output_dir, prefix='valid_contacts', ext='csv')
            print(f'💾 Saving {len(valid_contacts)} valid vcf_contacts to: {output_file}')

            write_tuples_to_csv(valid_contacts, ['Name', 'Number'], output_file)

            if args.auto_cleanup:
                print('🧹 Cleaning up imported vcf_contacts...')
                clear_contacts()

        stop_emulator()

        output_file = timestamped_output_path(args.output_dir, prefix='all_valid_contacts', ext='csv')
        print(f'💾 Saving results to {output_file}')
        write_tuples_to_csv(all_valid_contacts, ['Name', 'Number'], output_file)

        logger.info(f'✅ Extraction complete. Total valid contacts: {len(all_valid_contacts)}')


if __name__ == '__main__':
    main()
