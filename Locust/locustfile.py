from locust import Locust, TaskSet, task

class UserTaskSet(TaskSet):
    @task
    def login(self):
        requests.post('http://web-app-api:5000/v1/users/authenticate',
                      json={'username': username, 'password': password})




class UserLocust(Locust):
    task_set = UserTaskSet
    min_wait = 5000
    max_wait = 15000
