'''
    This file is part of nsmb-tools.

    nsmb-tools is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    nsmb-tools is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with nsmb-tools. If not, see <http://www.gnu.org/licenses/>.
'''
# ClassID Tool
# NameDatabase updating module

import urllib.request
import re

def update_namedatabase(namedatabase_path, urllist_path):
    '''
    Update NameDatabase file
    '''
    try:
        regexp = re.compile(r"\{(?P<URLName>.+)\#(?P<URL>.+)\}")
        with open(urllist_path, "r") as file_obj:
            re_match = regexp.match(file_obj.read())
            if re_match == None:
                raise Exception("URLList is in an invalid format")
            else:
                if re_match.group("URLName") == "NameDatabase_Update":
                    namedatabase_url = re_match.group("URL")
                else:
                    raise Exception("Could not find URL for `NameDatabase_Update` in URLList")
    except Exception as e:
        return ("urllist-parse-failure", str(e))
    try:
        http_obj = urllib.request.urlopen(namedatabase_url)
        new_namedatabase = http_obj.read()
        http_obj.close()
    except Exception as e:
        return ("download-failure", str(e))
    try:
        with open(namedatabase_path, 'wb') as file_obj:
            file_obj.write(new_namedatabase)
    except Exception as e:
        return ("write-failure", str(e))
    return ("success", None)

