from flask import Blueprint, render_template, request, redirect
import json
import pandas as pd
import re
import requests


view = Blueprint("view", __name__)


def load_data():
    # Make url request
    url = "http://0.0.0:8081/load-all"
    data = requests.get(url).content.decode("utf-8")

    # Create a DataFrame
    df = pd.read_json(data, orient="records")

    # Dataframe Treatment
    # Split names
    df["split_name"] = df.name.apply(lambda x: x.split("-"))

    # Make first name
    df["first_name"] = (
        df.split_name.apply(lambda x: x[0] if x[0] != x[-1] else None))

    # Make middle name
    df["middle_name"] = df.split_name.apply(lambda x: (
        re.sub(r' +', ' ', " ".join(x[1:-1])) if len(x) >= 3 else None))

    # Make last name
    df["last_name"] = df.split_name.apply(lambda x: x[-1])

    # Duration times from seconds to hours
    df["duration_time"] = df.duration.round().apply(pd.to_timedelta, unit='s')

    df_last_name_time = (
        df[["last_name", "duration"]].groupby("last_name").agg("sum"))
    df_last_name_time.reset_index(inplace=True)

    # Creating a dict
    json = df_last_name_time.to_json(orient='records')
    return json


@view.route("/", methods=["GET"])
def index():
    data = load_data()
    return render_template("index.html", data=data)
