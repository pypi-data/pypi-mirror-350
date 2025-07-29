import sys

sys.path.insert(0, '../src')

import gwtm_api

if __name__ == "__main__":
    token = "X8yASL3YVhZhgeOYSf0cIinjjLvE0Wl00Eb-Rw"

    swift = gwtm_api.Instrument.get(
        id = 100,
        include_footprint = True,
        api_token=token
    )
    for f in swift:
        projected = f.project(50, 50, 50)
        print(projected)