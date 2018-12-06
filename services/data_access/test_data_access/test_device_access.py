from data_access.device.device_data_access import DeviceAccessLayer
#Testies
x = DeviceAccessLayer()

#x.post_device("newlyAddedDevice1", "mac_address1")
#x.post_device("newlyAddedDevice2", "mac_address2")
#x.post_device("newlyAddedDevice3", "mac_address3")
#x.post_device("newlyAddedDevice4", "mac_address4")
#x.post_device("newlyAddedDevice5", "mac_address5")

#x.delete_device(x.get_device_id_by_name("newlyAddedDevice4"))

#x.put_name(x.get_device_id_by_name("newlyAddedDevice2"), "changedname")

#x.put_last_state(x.get_device_id_by_name("dummyName"), "dummyKey1", 85, "new timestamp")

#x.tester(x.get_device_id_by_name("dummyName"), "dummyKey1")
#print(x.get_device_id_by_name("dummyName"))

#print(x.get_device(x.get_device_id_by_name("dummyName")))

#x.post_sensor(x.get_device_id_by_name("dummyName"), ({'name': 'dummyName1', 'public': True, 'access_tokens': ['at1', 'at2']}))

#x.delete_sensor(x.get_device_id_by_name("dummyName"), "dummyName1")

#x.put_last_state(x.get_device_id_by_name("dummyName"), "dummyId1", 89, "new_time")

dummy_device = { "token": "dummyString",
                 "mac_address": "dummyAddress1",
                 "name": "dummyName",
                 "sensors": [{"id": "dummyId1", "name": "dummyName1", "public": True, "access_tokens": ["at1", "at2"]},
                             {"id": "dummyId2", "name": "dummyName2", "public": False, "access_tokens": ["at1", "at2"]},
                             {"id": "dummyId3", "name": "dummyName3", "public": True, "access_tokens": ["at1"]}],
                 "actions": [{"id": "dummyId1", "name": "dummyName1", "public": False, "access_tokens": ["at1", "at2"]},
                             {"id": "dummyId2", "name": "dummyName2", "public": False, "access_tokens": ["at1", "at3"]},
                             {"id": "dummyId3", "name": "dummyName3", "public": True, "access_tokens": ["at4", "at2"]}],
                 "last_state": {"sensor_values": [{"sensor_id": "dummyId1", "value": "var1", "timestamp": "some_timestamp1"},
                                                  {"sensor_id": "dummyId2", "value": "var2", "timestamp": "some_timestamp2"},
                                                  {"sensor_id": "dummyId3", "value": "var3", "timestamp": "some_timestamp3"}]},
                 "rules": ["id1", "id2", "id3"]}
#x.post_device(dummy_device)
#x.post_rule(x.get_device_id_by_name("dummyName"), "new_rule")

print(x.get_device(x.get_device_id_by_name("dummyName")))
x.post_sensor_access_token(x.get_device_id_by_name("dummyName"), "dummyId1", "my_new_id")
