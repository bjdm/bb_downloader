import os
import logging
import xml.etree.ElementTree as ElementTree

from bb_downloader.Unit import Unit


def parse_config(config_file='config.xml'):
    if not os.path.isfile(config_file):
        # print('There is no configuration file. Please see the documentation.')
        return None

    config = ElementTree.parse(config_file).getroot()
    units = []
    for unit in config:
        units.append(Unit(
            unit.attrib['name'],
            unit.attrib['code'],
            unit.find('url').attrib['blackboard'],
            unit.find('url').attrib['echo'],
            unit.find('directory').attrib['assessment'],
            unit.find('directory').attrib['recordings'],
            unit.find('directory').attrib['learningresources'],
            int(unit.find('year').text),
            int(unit.find('semester').text)))

    if verify_config():
        return units
    else:
        logging.INFO('There was an error in the configuration')


def verify_config():
    return True
