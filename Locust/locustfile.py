from locust import Locust, TaskSet, task, HttpLocust

class UserTaskSet(TaskSet):
    user_id = '5c157799a8568b000b92e9c4'
    access_token = 'b0436d96c40128c9312c05d04eaf4440875876485fd24b4779b235e3'
    deviceList = ["5c15779b438c8700184c3da8", "5c1577a4438c8700184c3dae", "5c1577ad438c8700184c3db4"]
    device_id = "5c1577ad438c8700184c3db4"
    action_list = ["5c1577aee3dcad000bdc8cc2", "5c1577b0e3dcad000bdc8cc4"]
    sensor_list = ["5c1577b117d37c000b6a9f7b"]


    @task(1)
    def login(self):
        self.client.post('/v1/users/authenticate',
                      json={'username': 'test5', 'password': 'test5'})
    @task(8)
    def get_devices(self):
        self.client.get("/v1/users/{}/devices".format(self.user_id), json = {'accessToken': self.access_token, 'data': {
            "deviceList": self.deviceList}}).json()
    @task(4)
    def get_actions(self):
        self.client.get("/v1/users/{0}/devices/{1}/actions".format(self.user_id, self.device_id),
                        json={'accessToken': self.access_token, 'data': {"actionList": self.action_list}}).json()
    @task(4)
    def get_sensors(self):
            self.client.get("/v1/users/{0}/devices/{1}/sensors".format(self.user_id, self.device_id),
                        json={'accessToken': self.access_token, 'data': {"sensorList": self.sensor_list}}).json()

class DeviceTaskSet(TaskSet):
    device_token = "170.34.94.158:5687"
    sensor_name = "sensor005"
    value = "3"
    @task
    def patch_sensors(self):
        data = {
            "deviceToken": self.device_token,
            "sensorName": self.sensor_name,
            "value": self.value
        }

        self.client.patch("/v1/patchSensor", json=data)

class DeviceLocust(HttpLocust):
    weight = 4
    task_set = DeviceTaskSet
    min_wait = 10000
    max_wait = 10000
class UserLocust(HttpLocust):
    weight = 1
    task_set = UserTaskSet
    min_wait = 5000
    max_wait = 8000
