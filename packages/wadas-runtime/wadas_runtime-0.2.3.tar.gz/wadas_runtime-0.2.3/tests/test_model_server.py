import wadas_runtime as wadas
import pytest
import threading
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime
import os


class DummyHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        if self.path.endswith("/organizations_login"):
            self._set_headers()
            self.wfile.write(json.dumps({"org_code": "dummy_org"}).encode())
        elif self.path.endswith("/orgs/dummy_org/nodes"):
            print(f"Received POST request {post_data}")
            request_data = json.loads(post_data)
            self._set_headers()
            self.wfile.write(
                json.dumps(
                    {
                        "id": 1,
                        "hwid": request_data["hwid"],
                        "enabled": True,
                        "is_banned": False,
                        "banned_at": None,
                        "ban_reason": None,
                        "created_at": datetime.datetime.now().isoformat(),
                        "enabled_models": ["model1"],
                    }
                ).encode()
            )
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    def do_GET(self):
        print(f"Received GET request for path: {self.path}")
        if self.path.endswith("/server_status"):
            self._set_headers()
            response = {"status": "READY"}
            self.wfile.write(json.dumps(response).encode())
        elif self.path.endswith("/nodes/1/models"):
            self._set_headers()
            response = [
                {
                    "name": "model1",
                    "released_at": "2024-01-01",
                    "expiration_dt": "2025-01-01",
                    "type": "classification",
                    "path": "classification/ov_model1/",
                    "is_default": True,
                }
            ]
            self.wfile.write(json.dumps(response).encode())
        elif self.path.endswith("/nodes/1/models?model_name=model1"):
            self._set_headers()
            # Simulate binary file download (e.g., model file)
            self.wfile.write(b"dummy model content")
        else:
            print("Path not found")
            self._set_headers(404)
            response = {"error": "Not found"}
            self.wfile.write(json.dumps(response).encode())


@pytest.fixture(scope="module", autouse=True)
def dummy_server():
    server = HTTPServer(("localhost", 8081), DummyHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield
    server.shutdown()
    thread.join()


def test_status(dummy_server):
    server = wadas.WADASModelServer("http://localhost:8081")
    assert server.status() is True


def test_login(dummy_server):
    server = wadas.WADASModelServer("http://localhost:8081")
    org_code = server.login(username="user", password="pass")
    assert org_code == "dummy_org"


def test_register_node(dummy_server):
    # Patch get_hardware_fingerprint to match dummy_hwid
    server = wadas.WADASModelServer("http://localhost:8081")
    user_id = server.register_node(org_code="dummy_org")
    assert user_id == "1"


def test_available_models(dummy_server):
    server = wadas.WADASModelServer("http://localhost:8081")
    models = server.available_models(user_id="1")
    assert isinstance(models, list)
    assert models[0]["name"] == "model1"
    assert models[0]["released_at"] == "2024-01-01"
    assert models[0]["expires_on"] == "2025-01-01"
    assert models[0]["type"] == "classification"
    assert models[0]["path"] == "classification/ov_model1/"
    assert models[0]["is_default"] is True


def test_non_existing_user(dummy_server):
    pytest.xfail(reason="Test for non-existing user")
    server = wadas.WADASModelServer("http://localhost:8081")
    models = server.available_models(user_id="999")
    assert models == [] or models is None


def test_download_model(dummy_server):
    server = wadas.WADASModelServer("http://localhost:8081")
    # Assuming the method is download_model(user_id, model_name)
    success = server.download_model(
        user_id="1", model_name="model1", model_path="dummy_path_success.bin"
    )
    assert success
    # Check if the file exists and is not empty
    with open("dummy_path_success.bin", "rb") as f:
        content = f.read()
    assert len(content) > 0
    assert content == b"dummy model content"
    os.remove("dummy_path_success.bin")
