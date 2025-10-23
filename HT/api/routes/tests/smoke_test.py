import requests, os

API_URL = os.getenv("API_URL", "http://localhost:5000")

def test_health():
    r = requests.get(f"{API_URL}/health")
    assert r.status_code == 200
    print("Health OK:", r.json())

def test_neural_simulate():
    r = requests.get(f"{API_URL}/resonance/neural", params={"simulate": "true"})
    assert r.status_code == 200 or r.status_code == 503
    print("Neural endpoint checked:", r.status_code)

if __name__ == "__main__":
    test_health()
    test_neural_simulate()
