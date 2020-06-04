import pandas as pd


def make_descriptions(df):
    df['split_name'] = df['name'].apply(lambda x: x.split('-'))
    df['main_description'] = df['split_name'].apply(lambda x: x[-1])
    df['detailed_description'] = (
        df['split_name'].apply(
            lambda x: ','.join(x[1:-1])
            if len(x) > 2 else (
                 ','.join(x[0:-1]) if len(x) > 1 else None
            )
        )
    )
    df['more_details'] = (
        df['split_name'].apply(lambda x: x[0] if len(x) > 2 else None))
    return df


def make_chart_data(df, column):
    df_grouped = (
        df
        .groupby([column])
        .duration.sum()
        .reset_index()
        .sort_values(by=['duration'], ascending=False)
    )

    # df_grouped['duration'] = (
    #     df_grouped['duration'].apply(lambda x: round(x, 2))
    # )

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
    df_detail = make_descriptions(df)
    return dict(
        total_duration=total_duration(df_detail),
        total_idle=total_idle(df_detail),
        table_data=make_chart_data(df_detail, drill_level)
    )
