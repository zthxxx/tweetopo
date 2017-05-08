# -*- coding: utf-8 -*-
from random import randint
from conffor import conffor
from database import mongo_orm
from database.mongo_orm import Person

uid_base = randint(86344422, 986344422)

info = {
    "name": "testname",
    "uid": uid_base,
    "friends_count": 4,
    "friends": ["asdf", "agd", "234f", "dfas"]
}

def connect_mongo():
    conf_file = 'tests/mongo_test/mongo_unit.json'
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
    assert Person.objects().count() == 1
    # It should save as only one, and not raise error.

def save_many_diff_test():
    for i in range(0, 3):
        people_info_save(info)
        info["uid"] = info["uid"] + 1
    assert Person.objects().count() == 1 + i

def person_find_test():
    index = uid_base
    for i in range(0, 3):
        assert mongo_orm.people_find(uid=index+i)

def person_read_all_test():
    global uid_base
    for people in Person.objects().order_by("uid"):
        assert people.uid == uid_base
        uid_base += 1

def person_del_all_test():
    for people in Person.objects():
        people.delete()
    assert Person.objects().count() == 0

def teardown_module():
    Person.drop_collection()


if __name__ == '__main__':
    connect_mongo()
    save_many_same_test()
    save_many_diff_test()
    person_find_test()
    person_read_all_test()
    person_del_all_test()
    teardown_module()
