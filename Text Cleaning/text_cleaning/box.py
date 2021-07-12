from boxsdk import DevelopmentClient


def box_upload(csv_file):
    '''
    Notes:  On the Box API site, go to your app and change settings:
            1. read and write all files and folders to Box - should be activated
            2. Manage users and manage groups - should be activated
            3. Make API calls using as-user header - should be activated
    '''
    client = DevelopmentClient()

    root_folder = client.folder('0').get()
    child_folders = root_folder.get_items(limit=100, offset=0)

    for child in child_folders:
        if child['name'] == 'Data+ Clean CSV Text':
            folder = client.folder(child['id']).get()
            break

    new_file = folder.upload(csv_file)

    print(f'File {new_file.name} was uploaded to {folder.name}')


def auto_upload(csv_file):
    import sys
    f1 = sys.stdin

    with open('./dev_token.cfg', 'r') as f:
        sys.stdin = f
        box_upload(csv_file)

    sys.stdin = f1

if __name__ == '__main__':

    with open("./dev_token.cfg/dev_token.cfg", "r") as f:
        dev_token = f.readline()
    print(dev_token)
