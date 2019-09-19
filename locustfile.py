from locust import HttpLocust, TaskSet


def index(l):
    l.client.get("/")

def producto1(l):
    l.client.get("/producto/2/detalle/")

def producto2(l):
    l.client.get("producto/4/detalle/")

class UserBehavior(TaskSet):
    tasks = {index: 20, producto1: 3, producto2: 5}

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 5000