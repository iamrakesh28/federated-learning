from server import Server
from flask import request
from flask_api import FlaskAPI

app = FlaskAPI(__name__)
server_kali = Server("kali", "model")

@app.route("/", methods=['GET', 'POST'])
def index():
    """
    Home Page
    """

    if request.method == 'POST':
        if request.data.get('send') == True:
            server_kali.validate_update_data(request.data)
            return "Success"
        else:
            return server_kali.read_weights()
    else:
        if request.args.get('send') == True:
            server_kali.validate_update_data(request.args)
            return "Success"
        else:
            return server_kali.read_weights()

def main():
    app.run(debug=True, threaded=True)

if __name__ == "__main__":
    main()
