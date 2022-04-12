from flask import Flask, jsonify, request
from controllers import get_location, get_weather_by_location
from tools import is_valid_ipv4, MyEncoder

app = Flask(__name__)

@app.route("/weather", methods=['GET'])
def get():
    ip = request.args.get('ip')
    lang = request.args.get('lang')

    if ip is None:
        # We assign the source of the request as IP address if no IP param
        ip = request.remote_addr
    else:
        ip = ip.strip()

    if lang is None:
        # Default language as English
        lang = 'en'

    try:
        if not is_valid_ipv4(ip):
            raise Exception("Invalid IP address")

        ip_location = get_location(ip, lang)

        weather = get_weather_by_location(ip_location, lang)
        weather_json = MyEncoder().encode(weather)

        return app.response_class(
            response=weather_json,
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run()