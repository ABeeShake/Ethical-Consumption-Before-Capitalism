from boxsdk import DevelopmentClient


def box_upload(csv_file):
    '''
    Notes: Create a text file named app.cfg in pycharm. Add the following info in order:
            1. Client ID
            2. Client Secret
            3. Developer Token

            On the Box API site, go to your app and change settings:
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

if __name__ == '__main__':
    with open('./app.cfg', 'r') as app_cfg:
        client_id = app_cfg.readline()
        client_secret = app_cfg.readline()
        access_token = app_cfg.readline()

    print(access_token)