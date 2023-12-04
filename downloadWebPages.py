
from pywebcopy import save_webpage

url = 'https://kb.froglogic.com/misc/find-process-for-window/'
download_folder = '/home/srinath/Downloads/WebPages'

kwargs = {'bypass_robots': True, 'project_name': 'recognisable-name'}

save_webpage(url, download_folder, **kwargs)

kwargs = {'bypass_robots': True, 'project_name': 'recognisable-name'}

save_webpage(url, download_folder, **kwargs)



