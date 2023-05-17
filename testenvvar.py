import os
os.environ["data_config_filename"]="testfilename"
os.environ["data_config_MFC"]["filename"]=="testfilename"
print(os.environ.get("data_config_filename"))
print(os.environ["data_config_MFC"]["filename"])
print(os.environ)
