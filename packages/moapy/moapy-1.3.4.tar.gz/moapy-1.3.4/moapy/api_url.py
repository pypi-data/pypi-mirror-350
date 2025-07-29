import os

_set_publish = "DV"  # "DV", "PR"

if os.getenv("GITHUB_ACTIONS") == "true":
    API_PYTHON_EXECUTOR = "https://moa.midasit.com/backend/python-executor/"
    API_SECTION_DATABASE = "https://moa.midasit.com/backend/wgsd/dbase/sections/"
elif _set_publish == "PR":
    API_PYTHON_EXECUTOR = "https://moa.midasit.com/backend/python-executor/"
    API_SECTION_DATABASE = "https://moa.midasit.com/backend/wgsd/dbase/sections/"
elif _set_publish == "DV":
    API_PYTHON_EXECUTOR = "https://moa.rpm.kr-dv-midasit.com/backend/python-executor/"
    API_SECTION_DATABASE = "https://moa.rpm.kr-dv-midasit.com/backend/wgsd/dbase/sections/"
else:
    API_PYTHON_EXECUTOR = "https://moa.midasit.com/backend/python-executor/"
    API_SECTION_DATABASE = "https://moa.midasit.com/backend/wgsd/dbase/sections/"
