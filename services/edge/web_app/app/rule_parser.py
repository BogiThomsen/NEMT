
def parse_rule(rule):
    condition = rule["condition"].split()
    device_name = condition[0].split('.')[0]
    sensor_name = condition[0].split('.')[1]
    operator = condition[1]
    val = condition[2].split('.')[1]

    actions = rule["invocations"]
    act_result = []

    for action in actions:
        dev_name = action.split('.')[0]
        act_name = action.split('.')[1]
        act_result.append({"device_name": dev_name, "action_name": act_name})

    return {"id": rule["id"], "name": rule["name"], "condition_device": device_name, "sensor_name": sensor_name, "operator": operator, "value": val, "actions": act_result}


def prettify_rule(parsed_rule, devices, sensors, actions):
    parsed_rule["condition_device"] = find_prettyname(parsed_rule["condition_device"], devices)
    parsed_rule["sensor_name"] = find_prettyname(parsed_rule["sensor_name"], sensors)
    for act in parsed_rule["actions"]:
        act["device_name"] = find_prettyname(act["device_name"], devices)
        act["action_name"] = find_prettyname(act["action_name"], actions)

    return parsed_rule


def find_prettyname(string, collection):
    result = ""
    for col in collection:
        if col["name"] == string:
            result = col["prettyname"]

    return result
