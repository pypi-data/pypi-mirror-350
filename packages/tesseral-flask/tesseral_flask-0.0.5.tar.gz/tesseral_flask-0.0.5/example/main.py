from dotenv import load_dotenv
import os
from flask import Flask, jsonify
from tesseral_flask import (
    require_auth,
    organization_id,
    access_token_claims,
    credentials,
)

load_dotenv()

app = Flask(__name__)
app.before_request(
    require_auth(
        api_keys_enabled=True,
        publishable_key=os.getenv("TESSERAL_PUBLISHABLE_KEY") or "",
        config_api_hostname="config.tesseral.com",
    )
)


@app.get("/")
def hello_world():
    return jsonify(
        {
            "organization_id": organization_id(),
            "access_token_claims": access_token_claims().json(),
            "credentials": credentials(),
        }
    )


@app.post("/")
def hello_world_post():
    return jsonify(
        {
            "organization_id": organization_id(),
            "credentials": credentials(),
        }
    )


if __name__ == "__main__":
    app.run(port=8000, debug=True)
