from locust import Locust, TaskSet, task

class UserTaskSet(TaskSet):
    @task
    def login(self):
        self.client.post('/v1/users/authenticate',
                      json={'username': 'test1', 'password': 'test1'})




class UserLocust(Locust):
    task_set = UserTaskSet
    min_wait = 1000
    max_wait = 3000
