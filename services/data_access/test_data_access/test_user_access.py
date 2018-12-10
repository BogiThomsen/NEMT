import data_access.user.app.user_data_access as x

#Testies

#x.post_user("LarsAllan", "1234567", "Second_Breakfast47")

##remember to find id
#id_to_remove = "dummyid"
#x.delete_user(id_to_remove)

test_id = "5c067e0f6025271da8e45fab"
#x.put_username(id_to_change_name, "Changed Username")

#x.put_password(id_to_change_name, "newPassword")
#print(get_user(id_to_change_name))
#print(get_user("5c0678f36025271d7857066b"))

user = x.get_user(("default username"))
db = x.connect_to_db()
print(db.count_documents({"username": "Changed username"}))
print(x.get_user("default username"))

#x.post_to_user(x.get_user_id_by_username("LarsAllan"), "dummy_device_id123", "available_devices")

#x.delete_from_user(x.get_user_id_by_username("LarsAllan"), "dummy_device_id123", "available_devices")

#x.post_to_user(test_id, "rule1", "rules")
#x.post_to_user(test_id, "rule2", "rules")
#x.post_to_user(test_id, "rule3", "rules")
#x.post_to_user(test_id, "rule4", "rules")
#x.post_to_user(test_id, "rule5", "rules")
#x.post_to_user(test_id, "rule6", "rules")

#x.delete_from_user(test_id, "rule1", "rules")