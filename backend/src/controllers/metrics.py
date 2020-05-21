import pandas as pd


def prepare_df(df, column):
    df_grouped = (
        df
        .groupby([column])
        .duration.sum()
        .reset_index()
        .sort_values(by=['duration'], ascending=False)
    )

    df_grouped['duration'] = (
        df_grouped['duration'].apply(lambda x: round(x, 2))
    )

    df_grouped['time'] = (
        df_grouped['duration']
        .round()
        .apply(pd.to_timedelta, unit='s')
    ).astype(str)
    df_grouped.columns = ['name', 'duration', 'time']
    return list(df_grouped.T.to_dict().values())


def total_duration(df):
    return str(pd.to_timedelta(df.duration.sum().round(), unit='s'))


def total_idle(df):
    return str(
        pd.to_timedelta(
            df[df["main_description"] == 'user_idle']
            .duration
            .sum()
            .round(), unit='s')
    )


def metrics_bundle(data, drill_level):
    df = pd.DataFrame(data)
    return dict(
        total_duration=total_duration(df),
        total_idle=total_idle(df),
        table_data=prepare_df(df, drill_level)
    )
