import sys

sys.path.insert(0, '../src')

import gwtm_api
API_TOKEN = "X8yASL3YVhZhgeOYSf0cIinjjLvE0Wl00Eb-Rw"

def test_candidate_coverage():

    candidate = gwtm_api.Candidate.get(api_token=API_TOKEN, graceid="MS181101ab")
    for c in candidate:
        pointings = gwtm_api.event_tools.candidate_coverage(api_token=API_TOKEN, candidate=c)
        for p in pointings:
            p.dump()

def test_prob_coverage():

    prob, area = gwtm_api.event_tools.calculate_coverage(api_token=API_TOKEN, graceid="MS241203a")
    print(prob, area)

def test_renormed_contours():
    contours = gwtm_api.event_tools.renormed_skymap_contours(api_token=API_TOKEN, graceid="S250118az")
    print(contours)
    
if __name__ == "__main__":
    # gwtm_api.event_tools.plot_coverage(
    #     graceid="S240422ed",
    #     api_token=token
    # )
    test_renormed_contours()
    # pointings = gwtm_api.Pointing.get(
    #     graceid = "S240422ed",
    #     instrument="DECam",
    #     status="completed",
    #     api_token=token
    # )

    # print(len(pointings))

    # prob, area = gwtm_api.event_tools.calculate_coverage(
    #     api_token=token,
    #     graceid="S240422ed",
    #     pointings=pointings,
    #     cache=False,
    #     approximate=False
    # )
    # print(prob, area)