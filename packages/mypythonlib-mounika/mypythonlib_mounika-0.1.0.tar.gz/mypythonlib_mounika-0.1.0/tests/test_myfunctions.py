from mypythonlib import myfunctions

def test_haversine():
    # Amsterdam to Berlin
    result = myfunctions.haversine(4.895168, 52.370216, 13.404954, 52.520008)
    assert abs(result - 576.6625818456291) < 1e-6

