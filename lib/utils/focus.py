# -*- coding: utf-8 -*-
import re
from lib.conffor import conffor

RULE_FILE = 'config/rules.json'
rule = conffor.load(RULE_FILE)
rule_patterns = [re.compile(keyword, re.I) for keyword in rule["keywords"]]
pickup = rule["pickup"]


def match_focus(message):
    if message is not None:
        for pattern in rule_patterns:
            if pattern.search(message) is not None:
                return True
    return False
