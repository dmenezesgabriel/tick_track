from flask import Blueprint, render_template, request, redirect, Response
import io
import json
import matplotlib as plt
import pandas as pd
import re
import requests
import urllib.parse


view = Blueprint("view", __name__)


def load_data():
    # Make url request
    url = "http://0.0.0:8081/load-today"
    data = requests.get(url).content.decode("utf-8")

    # Create a DataFrame
    df = pd.read_json(data, orient="records")

    # Dataframe Treatment
    # Split names
    df["split_name"] = df.name.apply(lambda x: x.split("-"))

    # Make first name
    df["first_name"] = (
        df.split_name.apply(lambda x: x[0] if x[0].strip() != x[-1] else None))

    # Make middle name
    df["middle_name"] = df.split_name.apply(lambda x: (
        re.sub(r' +', ' ', " ".join(x[1:-1])).strip() if len(x) >= 3 else None))

    # Make last name
    df["last_name"] = df.split_name.apply(lambda x: x[-1].strip())

    # Duration times from seconds to hours
    df["duration_time"] = df.duration.round().apply(pd.to_timedelta, unit='s')

    # More than 1 minute spent at the window
    df_last_name_time = (
        df[df["duration"] > 60][["last_name", "duration_time"]].groupby("last_name").agg("sum"))
    df_last_name_time.reset_index(inplace=True)

    return df_last_name_time


def create_figure():
    df = load_data()
    chart = df.plot.barh(x="last_name", y="duration_time")
    fig = chart.get_figure()
    return fig


@view.route("/plot.png")
def plot_png():
    fig = create_figure()
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    response = Response(img.getvalue(), mimetype='image/png')
    img.close()
    return response


@view.route("/", methods=["GET"])
def index():
    data = load_data()
    return render_template(
        "index.html", tables=[data.to_html(classes='data', header="true")]
    )
