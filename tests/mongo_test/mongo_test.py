# -*- coding: utf-8 -*-
import os
from random import randint
from conffor import conffor
from database import mongo_orm
from database.mongo_orm import Person

uid_base = randint(86344422, 986344422)
PERSON_LENGTH = 5
EXPORT_STORE_FILE = './twitter_relations.test.json'

info = {
    "name": "testname",
    "uid": uid_base,
    "protect": False,
    "friends_count": 4,
    "friends": ["asdf", "agd", "234f", "dfas"]
}

def connect_mongo():
    conf_file = 'tests/mongo_test/mongo_unit_test.json'
    config = conffor.load(conf_file)
    mongo_conf = config['mongo']
    mongo_orm.set_connect(**mongo_conf)

def setup_module():
    connect_mongo()

def people_info_save(info):
    mongo_orm.people_save(**info)

def save_many_same_test():
    people_info_save(info)
    people_info_save(info)
    people_info_save(info)
    assert Person.objects().count() is 1
    # It should save as only one, and not raise error.

def save_many_diff_test():
    for i in range(0, PERSON_LENGTH):
        people_info_save(info)
        info["uid"] = info["uid"] + 1
    assert Person.objects().count() == 1 + i

def person_find_test():
    index = uid_base
    people = mongo_orm.people_find(name=info['name'])
    assert people.name == info['name']
    for i in range(0, PERSON_LENGTH):
        people = mongo_orm.people_find(uid=index+i)
        assert people.uid == index+i

def person_read_all_test():
    index = uid_base
    for people in Person.objects().order_by("uid"):
        assert people.uid == index
        index += 1

def get_person_uids_test():
    index = uid_base
    uids = mongo_orm.get_uids()
    assert len(uids) is PERSON_LENGTH
    for i in range(0, PERSON_LENGTH):
        assert index+i in uids

def export_person_collection_test():
    mongo_orm.export_person(EXPORT_STORE_FILE, seed_name=info['name'], limit=10)

def person_del_all_test():
    for people in Person.objects():
        people.delete()
    assert Person.objects().count() is 0

def teardown_module():
    Person.drop_collection()
    if os.path.isfile(EXPORT_STORE_FILE):
        os.remove(EXPORT_STORE_FILE)

if __name__ == '__main__':
    connect_mongo()
    save_many_same_test()
    save_many_diff_test()
    person_find_test()
    person_read_all_test()
    get_person_uids_test()
    export_person_collection_test()
    person_del_all_test()
    teardown_module()
