#!/usr/bin/python3
""" Check response
"""
import requests

if __name__ == "__main__":
    r = requests.post('http://127.0.0.1:3456/api/v1/auth_session/login')
    if r.status_code != 400:
        print("Wrong status code: {}".format(r.status_code))
        exit(1)
    print("OK", end="")
    