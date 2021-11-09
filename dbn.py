import json


def check(filename):
  with open(filename, "r") as f:
      return json.load(f)

def update(filename, data):
  with open(filename, "w") as f:
    json.dump(data, f)
  f.close()