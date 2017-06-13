# -*- coding: utf-8 -*-
import logsetting
from scripts import crawling_relation, export_relation, \
    mutual_friends, select_hub, crawling_detail, export_persons, merge_detail

# see workflow more details in README
if __name__ == "__main__":
    crawling_relation.run()
    export_relation.run()
    mutual_friends.run()
    select_hub.run()
    crawling_detail.run()
    export_persons.run()
    merge_detail.run()
