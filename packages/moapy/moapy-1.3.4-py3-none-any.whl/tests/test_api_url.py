# import pytest
# from moapy.enum_pre import create_enum_class, do_section_names_from_api
# from moapy.api_url import API_SECTION_DATABASE

# def test_api_enum():
#     pr = "https://moa.midasit.com/backend/wgsd/dbase/sections/"
#     en_H_EN10365_pr = create_enum_class('en_H_EN10365', do_section_names_from_api(pr, "EN 10365:2017", "H_Section"))
#     en_H_AISC05_US_pr = create_enum_class('en_H_AISC05_US', do_section_names_from_api(pr, "AISC05(US)", "H_Section"))
#     en_H_AISC10_US_pr = create_enum_class('en_H_AISC10_US', do_section_names_from_api(pr, "AISC10(US)", "H_Section"))
#     en_H_AISC10_SI_pr = create_enum_class('en_H_AISC10_SI', do_section_names_from_api(pr, "AISC10(SI)", "H_Section"))

# if __name__ == "__main__":
#     test_api_enum()