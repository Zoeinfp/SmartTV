import os
from sogetv_app.views import app

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "LandingCuteProject-32d0ea6a0b8e.json"
app.secret_key = '2pf323uaj#2s8oc#85z7xincioz@qe_gl16cv@lyb^ocyndf!%'

if __name__ == "__main__":
    app.run()
