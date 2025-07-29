"""For quick testing purposes."""

import os
import csv
import json

STORE_PATH = 'D:\\PyCharm\\test\\model-storage.json'


def extract_chat_list():
    """Extract chat list from WAMS DB."""
    with open(STORE_PATH, encoding='utf-8') as _:
        snapshot_data = json.load(_)

        # Extract only id and name
        data_list = snapshot_data['chat']

        print('Total chats:', len(data_list))
        for i, data in enumerate(data_list, 1):
            print(f'[{i:03}] {data["id"].split("@")[0]:<15} {data["name"]}')


def extract_contacts():
    """Extract contacts from WAMS DB."""
    with open(STORE_PATH, encoding='utf-8') as _:
        snapshot_data = json.load(_)

        data_list = snapshot_data['contact']
        data_list = [x for x in data_list if x.get('isAddressBookContact') and x.get('phoneNumber')]
        print('Total Contacts:', len(data_list))
        for i, data in enumerate(data_list, 1):
            print(f'[{i}] {data}')
            # print(
            #     f"[{i:03}] "
            #     f"{data['id']:<18} "
            #     f"{data.get('phoneNumber','PN'):<15} "
            #     f"{data.get('name','name'):<20} "
            #     f"{data.get('pushname','pushname'):<20}"
            # )

        headers = ['id', 'name', 'shortName', 'phoneNumber']

        export_data_list = []
        for d in data_list:
            export_data_list.append({k: d.get(k, '') for k in headers})

        filename = 'D:\\PyCharm\\test\\contacts.csv'
        filepath = os.path.join(os.getcwd(), filename)
        with open(filepath, 'w', newline='', encoding='utf-8') as _:
            writer = csv.DictWriter(_, fieldnames=headers)
            writer.writeheader()
            writer.writerows(export_data_list)


if __name__ == '__main__':
    extract_contacts()
