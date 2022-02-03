# setup
move data into data/ as desired

# installation
pip3 install shareplum

fix timeout issue by modifying site-packages/shareplum/folder.py
line 10, set self.timeout to something large (eg: 500) (will require a better solution)

# usage
python3 sharepoint/sharepoint.py
