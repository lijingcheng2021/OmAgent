from .wikienv import WikiEnv
import requests

env = WikiEnv()

def step(env, action):
    attempts = 0
    while attempts < 10:
        try:
            return env.step(action)
        except requests.exceptions.Timeout:
            print(123456)
            attempts += 1