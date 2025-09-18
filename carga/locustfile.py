from locust import HttpUser, task, between, LoadTestShape
from faker import Faker
import requests

class TodoWithAuthUserAsync(HttpUser):
    fake = Faker()
    wait_time = between(1, 2)
    token = None
    host = "http://localhost:3042"

    def on_start(self):
        auth_response = requests.post(
            "http://0.0.0.0:3052/api/v1/oauth/login?email=teste%40example.com&password=Senha!123"
        )

        if auth_response.status_code == 201:
            self.token = auth_response.json()["access_token"]
        else:
            self.token = None
            print(f"Erro ao autenticar: {auth_response.json()}")


    @task
    def criar_todo_async(self):
        if not self.token:
            return

        self.client.post(
            "/api/v1/todos/async",
            headers={"Authorization": f"Bearer {self.token}"},
            json={
                "title": self.fake.name(),
                "description": self.fake.text(max_nb_chars=100),
                "state": "todo"
            },
            name='Async'
        )
        
class TodoWithAuthUserSync(HttpUser):
    fake = Faker()
    wait_time = between(1, 2)
    token = None
    host = "http://localhost:3040"

    def on_start(self):
        auth_response = requests.post(
            "http://0.0.0.0:3050/api/v1/oauth/login?email=teste%40example.com&password=Senha!123"
        )

        if auth_response.status_code == 201:
            self.token = auth_response.json()["access_token"]
        else:
            self.token = None
            print(f"Erro ao autenticar: {auth_response.json()}")


    @task
    def criar_todo(self):
        if not self.token:
            return

        self.client.post(
            "/api/v1/todos",
            headers={"Authorization": f"Bearer {self.token}"},
            json={
                "title": self.fake.name(),
                "description": self.fake.text(max_nb_chars=100),
                "state": "todo"
            },
            name='Sync'
        )

class StageShape(LoadTestShape):
    """
    Exemplo: durações são relativas (por estágio) e convertidas internamente
    para tempos cumulativos.
    """

    # ### Baixa carga 10 minutos
    # stages = [
    #     {"duration": 120, "users": 10, "spawn_rate": 2},
    #     {"duration": 180, "users": 50, "spawn_rate": 5},
    #     {"duration": 300, "users": 200, "spawn_rate": 10},
    #     {"duration": 120, "users": 500, "spawn_rate": 20},
    #     {"duration": 120, "users": 100, "spawn_rate": 10},
    # ]

    # ### Alta carga - 1 hora
    # stages = [
    #     {"duration": 600,  "users": 100,  "spawn_rate": 10},
    #     {"duration": 900,  "users": 500,  "spawn_rate": 20},
    #     {"duration": 1200, "users": 1000, "spawn_rate": 50},
    #     {"duration": 1200, "users": 3000, "spawn_rate": 100},
    #     {"duration": 600,  "users": 800,  "spawn_rate": 50},
    #     {"duration": 300,  "users": 100,  "spawn_rate": 20},
    # ]

    def __init__(self):
        super().__init__()
        cum = 0
        self._stages_cum = []
        for s in self.stages:
            cum += s["duration"]
            s_copy = s.copy()
            s_copy["end_time"] = cum
            self._stages_cum.append(s_copy)

    def tick(self):
        run_time = self.get_run_time()
        for s in self._stages_cum:
            if run_time < s["end_time"]:
                return s["users"], s["spawn_rate"]
        return None
