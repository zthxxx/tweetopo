from src.scripts import crawling_detail, crawling_relation, \
    export_persons, export_relation, hit_rules, merge_detail, \
    mutual_friends, select_hub, select_secondout

workflow = [
    crawling_relation,
    export_relation,
    mutual_friends,
    select_hub,
    select_secondout,
    crawling_detail,
    export_persons,
    hit_rules,
    merge_detail
]
