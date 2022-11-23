from flask import Flask, render_template, request
import requests
from . import bp as main
from config import Config
app = Flask(__name__)

@main.route('/', methods=['GET'])
def homepage():
    return render_template('homepage.html.j2')

@main.route('/ApexSearch', methods=['GET', 'POST'])
def ApexSearcher():
    apexlegendsapi_key = "041b5fe9786befdfd842644f425b8139"
    if request.method =='POST':
        player = request.form.get("player")
        platform = request.form.get("platform")
        url = f'https://api.mozambiquehe.re/bridge?auth={apexlegendsapi_key}&player={player}&platform={platform}'
        response = requests.get(url)
        if not response.ok:
            error_string = "We had an Unexpected Error"
            return render_template('apexsearch.html.j2', error = error_string)
    
        data = response.json()
        gamer_dict={
                "apex_platform": data["global"]["platform"],
                "apex_season":data["global"]["rank"]["rankedSeason"],
                "player_name": data["global"]["name"],
                "apex_level": data["global"]["level"],
                "apex_rank": data["global"]["rank"]["rankDiv"]
            }
        return render_template('apexsearch.html.j2', gamer_data = gamer_dict)
    return render_template('apexsearch.html.j2')