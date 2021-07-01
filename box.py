from boxsdk import Client, OAuth2
from boxsdk.network.default_network import DefaultNetwork
from pprint import pformat

client_id = None
client_secret = None
access_token = None

with open('app.cfg', 'r') as app_cfg:
    client_id = app_cfg.readline()
    client_secret = app_cfg.readline()
    access_token = app_cfg.readline()

# class LoggingNetwork(DefaultNetwork):
#     def request(self, method, url, access_token, **kwargs):
#         """ Base class override. Pretty-prints outgoing requests and incoming responses. """
#         print('\x1b[36m{} {} {}\x1b[0m').format(method, url, pformat(kwargs))
#         response = super(LoggingNetwork, self).request(
#             method, url, access_token, **kwargs
#         )
#         if response.ok:
#             print('\x1b[32m{}\x1b[0m').format(response.content)
#         else:
#             print('\x1b[31m{}\n{}\n{}\x1b[0m').format(
#                 response.status_code,
#                 response.headers,
#                 pformat(response.content),
#             )
#         return response
#
#
# oauth2 = OAuth2(client_id, client_secret, access_token=access_token)
# client = Client(oauth2, LoggingNetwork())

from boxsdk import DevelopmentClient

print(access_token)
client = DevelopmentClient()

root_folder = client.folder('0').get()
child_folders = root_folder.get_items(limit=100, offset=0)

for child in child_folders:
    if child['name'] == 'Data+ Clean CSV Text':
        folder = client.folder(child['id']).get()
        break

file_1 = folder.get_items(limit=1, offset=0)
for file in file_1:
    f = file.get()
    print(f.content())
