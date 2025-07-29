"""Utility functions for the WhatXtract package."""

import os
import csv
import sys
import json
import time
from typing import Any
from pathlib import Path
from datetime import datetime
from functools import wraps

from faker import Faker

from whatxtract.constants import VCF_DIR, OUTPUT_DIR, VCF_TEMPLATE, WAMS_DB_PATH, VCF_BATCH_SIZE
from whatxtract.logging_setup import logger


class DotDict(dict):
    """Dictionary with dot notation access to keys."""

    def __getattr__(self, key, default: Any = None):
        try:
            return self[key]
        except KeyError:
            return default

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError(f'No such attribute: {key}') from Exception


class DummyError(Exception):
    """Used only to trick linters, never raised."""

    pass


def timed(func):
    """Decorator that logs the execution time of the decorated function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        duration = end - start
        logger.debug(f'[>⏱   {func.__name__} took {duration:.3f}s')
        return result

    return wrapper


def load_config_file(config_path=Path('config.json')) -> dict:
    """Loads the configuration file and returns a dictionary."""
    if not config_path.exists() or not config_path.is_file():
        config_path = Path(f'{__package__}.config.json')

        if not config_path.exists() or not config_path.is_file():
            config_path = Path.home() / f'{__package__}.config.json'

    config = {}

    try:
        config = json.loads(config_path.read_text(encoding='utf-8'))
    except FileNotFoundError:
        logger.debug('Config file not found.')
    except json.JSONDecodeError:
        logger.warning('Invalid JSON in config file. Skipping.')

    return DotDict(config)


def get_timestamp(fmt='%Y_%m_%d_%H_%M'):
    """Returns current time formatted as a string."""
    return datetime.now().strftime(fmt)


def timestamped_output_path(
    output_dir: str, prefix: str = 'output', ext: str = 'txt', fmt: str = '%Y_%m_%d_%H_%M'
) -> Path:
    """
    Generate a timestamped file path inside the given output directory.

    Args:
        output_dir (str): Base directory where the file will be saved.
        prefix (str): Prefix for the filename.
        ext (str): File extension without dot.
        fmt (str): Format string for the timestamp. Default is '%Y_%m_%d_%H_%M'.

    Returns:
        Path: A full path to the output file with timestamped name.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    filename = f'{prefix}_{get_timestamp(fmt=fmt)}.{ext}'
    return Path(output_dir) / filename


def write_dicts_to_csv(data: list[dict], headers: list[str], output_path: Path) -> None:
    """
    Writes a list of dicts to a CSV file.

    Args:
        data (list[dict]): A list of dictionaries.
        headers (list[str]): A list of headers for the CSV file.
        output_path (Path): The full path to the output CSV file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

    with output_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

    logger.info(f'✅ Saved {len(data)} contacts to: {output_path}')


def write_tuples_to_csv(data: list[tuple[str, str]], headers: list[str], output_path: Path) -> None:
    """
    Write a list of tuples to a CSV file.

    Args:
        data (list[tuple[str, str]]): A list of (name, number) tuples.
        headers (list[str]): A list of headers for the CSV file.
        output_path (Path): The full path to the output CSV file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

    with output_path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)

    logger.info(f'✅ Saved {len(data)} contacts to {output_path}')


def get_digits(number: str) -> str:
    """Strips common formatting characters from phone numbers."""
    # This is valid and works: ''.join(filter(str.isdigit, number))
    # To suppress PyCharms type checking warming using lambda
    return ''.join(filter(lambda c: c.isdigit, number))


def read_numbers_from_txt(file_path) -> list[str]:
    """
    Reads a text file with one phone number per line.

    Args:
        file_path (str or Path): Path to the input text file.

    Returns:
        List[str]: A list of cleaned phone numbers.
    """
    file_path = Path(file_path)
    if not file_path.exists() or not file_path.is_file():
        logger.error(f'Input file not found: {file_path}')
        sys.exit(1)

    logger.info(f'Reading numbers from {file_path}')
    with file_path.open('r', encoding='utf-8') as f:
        numbers = [get_digits(line.strip()) for line in f if line.strip()]
        if not numbers:
            logger.error(f'No numbers found in input file: {file_path}.')
            sys.exit(1)
        return numbers


def append_to_file(filename: str, number: str):
    """Append a string on a new line to a text file."""
    with (OUTPUT_DIR / filename).open('a', encoding='utf-8') as f:
        f.write(number + '\n')


def chunk_list(data_list: list[Any], chunk_size: int) -> list[list[Any]]:
    """
    Splits a list of strings into smaller lists (chunks) of the given batch size.

    Args:
        data_list (List[str]): The list to be split.
        chunk_size (int): Number of items per chunk.

    Returns:
        List[List[str]]: List of chunks (batches).
    """
    return [data_list[i : i + chunk_size] for i in range(0, len(data_list), chunk_size)]


def extract_chat_list_from_json_db(db_path=WAMS_DB_PATH, output_file=OUTPUT_DIR / 'extracted_chat_list.csv'):
    """Extract chat list from WAMS DB."""
    with db_path.open('r', encoding='utf-8') as file:
        snapshot_data = json.load(file)

        # Extract only id and name
        data_list = snapshot_data['chat']

        logger.info(f'Total chats: {len(data_list)}')
        for i, data in enumerate(data_list, 1):
            logger.debug(f'[{i:03}] {data["id"].split("@")[0]:<15} {data["name"]}')

        headers = ['id', 'name', 'shortName', 'phoneNumber']

        export_data_list = []
        for d in data_list:
            export_data_list.append({k: d.get(k, '') for k in headers})

        with output_file.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(export_data_list)

            logger.info(f'Extracted {len(export_data_list)} contacts. saved to: {output_file}')


def extract_contacts_from_json_db(db_path=WAMS_DB_PATH, output_file=OUTPUT_DIR / 'extracted_contacts.csv'):
    """Extract contacts from WAMS DB."""
    with db_path.open('r', encoding='utf-8') as file:
        db_data = json.load(file)

        data_list = db_data['contact']
        data_list = [x for x in data_list if x.get('isAddressBookContact') and x.get('phoneNumber')]
        logger.info('Total Contacts:', len(data_list))
        for i, d in enumerate(data_list, 1):
            logger.debug(
                f'[{i:^3}] {d["id"]:<20} '
                f'{d.get("phoneNumber", "PN"):<15} '
                f'{d.get("name", "name"):<20} '
                f'{d.get("pushname", "pushname"):<20}'
            )

        headers = ['id', 'name', 'shortName', 'phoneNumber']
        export_data_list = [{k: d.get(k, '') for k in headers} for d in data_list]
        with output_file.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(export_data_list)

            logger.info(f'Extracted {len(export_data_list)} contacts. Saved to: {output_file}')


def generate_vcf_batches(input_file: str, batch_size: int = VCF_BATCH_SIZE) -> list[Path]:
    """
    Read phone numbers from a text file, split them into batches, and generate corresponding VCF files.

    Each contact is stored in vCard 3.0 format with only the phone number as the full name (FN)
    and telephone (TEL) fields. The last name (N) field is marked with the batch ID to group them.

    Args:
        input_file (str): Path to a .txt file containing one phone number per line.
        batch_size (int, optional): Maximum number of contacts per VCF file. Defaults to 5000.

    Returns:
        List[Path]: A list of file paths pointing to the generated .vcf files.
    """
    numbers = read_numbers_from_txt(input_file)
    logger.info(f'Loaded {len(numbers)} numbers. Generating VCF batches...')

    fake = Faker()
    generated_files = []
    chunks = chunk_list(numbers, batch_size)
    for i, chunk in enumerate(chunks, start=1):
        fn = fake.first_name()
        ln = fake.last_name()
        vcf_content = '\n'.join(
            VCF_TEMPLATE.format(
                first=fn,
                last=ln,
                full=f'{fn} {ln}',
                tel=f'+1 {number}' if len(number) == 10 else number,
            )
            for number in chunk
        )

        vcf_path = VCF_DIR / f'batch_{i:04d}.vcf'
        vcf_path.write_text(vcf_content, encoding='utf-8')
        logger.info(f'[ + ] Generated: {vcf_path}')
        generated_files.append(vcf_path)

    return generated_files


def ensure_output_dir(path: str) -> None:
    """Ensure the output directory exists and is writable."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    if not os.access(path, os.W_OK):
        raise Exception(f'[ x ] Directory: {path} is not writable: {path}')


def get_adb_path() -> Path:
    """To be used when emulator mode is coded."""
    return Path('adb')
