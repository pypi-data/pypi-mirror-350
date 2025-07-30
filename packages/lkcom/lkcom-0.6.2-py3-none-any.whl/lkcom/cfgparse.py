"""lkcom - a Python library of useful routines.

This module contains routines to read and parse INI config files.

Copyright 2015-2023 Lukas Kontenis
Contact: dse.ssd@gmail.com
"""
import numpy as np
import configparser as cfg
import re
import sys
import os.path
import io
import zipfile
from pathlib import Path

from lkcom.util import isarray, isnone, issmth, isstring


def read_cfg(FileName):
    """
    Read the configuration file for the dataset given by FileName.
    """
    try:
        if(isarray(FileName)):
            numF = len(FileName)
            config = np.ndarray(numF, cfg.RawConfigParser)

            for indF in range(0, numF):
                config[indF] = read_cfg(FileName[indF])

            return config

        # Parse SigMon files
        m = re.search(r"SigMon.\.dat$", FileName)
        if not isnone(m):
            CfgFileName = FileName[:m.end()-5] + '.ini'
        else:
            if Path(FileName).suffix == '.zip':
                # Look for INI files inside the ZIP archive
                zip_contents = zipfile.ZipFile(FileName).namelist()
                for zip_file_name in zip_contents:
                    if Path(zip_file_name).suffix == '.ini':
                        CfgFileName = zip_file_name
                        config = cfg.RawConfigParser()
                        config.read_file(io.TextIOWrapper(zipfile.ZipFile(FileName).open(CfgFileName)))
                        return config

            else:
                # Parse timestamp files
                m = re.search(r'.._.._.._\....', FileName)
                if(issmth(m)):
                    CfgFileName = FileName[:m.end()] + '_.ini'
                else:
                    CfgFileName = FileName[:FileName.rfind('.')] + ".ini"

        if not os.path.isfile(CfgFileName):
            print("Could not locate config file '" + CfgFileName + "'")
            return None

        config = cfg.RawConfigParser()
        config.read(CfgFileName)
    except Exception:
        print("Cannot read config file:", sys.exc_info()[0])
        return None

    return config


def get_cfg_section(config, section_str):
    """
    Get a section in the config file.
    """

    sections = config.sections()

    if(section_str in sections):
        return config[section_str]
    else:
        return None


def get_head_val(config, section_str, key_str, cast_to=None, default_val=None):
    """
    Get the value of the given key from the given section.
    """

    sec = get_cfg_section(config, section_str)
    if sec:
        val = sec.get(key_str, None)

        if(isstring(val)):
            val = val.strip(r'"')

        if(isnone(val)):
            val = default_val
        elif(not isnone(cast_to)):
            if(cast_to == "float"):
                val = float(val)
            elif(cast_to == "int"):
                val = int(val)
            else:
                print("Unknown cast target type")

        # Return empty string as none
        if val == '':
            val = None

        return val

    else:
        return None
