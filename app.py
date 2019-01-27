import os
from sogetv_app.views import app
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "LandingCuteProject-32d0ea6a0b8e.json"

if __name__ == "__main__":
    app.run()
