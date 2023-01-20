import pandas as pd
import sqlite3
from .consts import Consts
from datetime import datetime, timedelta
import numpy as np

class ScoreUtils:
    DBNAME = Consts.DBNAME
    @classmethod
    def Update_scores(cls, score_window_size = 30):

        with sqlite3.connect(ScoreUtils.DBNAME) as conn:
            df = pd.read_sql_query(f"SELECT * FROM usage;",conn)
            df.set_index("datetime", inplace=True)
        df.index = pd.to_datetime(df.index)
        now = datetime.now()
        start_score_window = now - timedelta(days=score_window_size)
        mask = (df.index > start_score_window) & (df.index < now)
        scoring_df = df[mask]
        totals = scoring_df.groupby("house_id").sum()
        sel_house = tuple(totals.index)
        with sqlite3.connect(ScoreUtils.DBNAME) as conn:
            df = pd.read_sql_query(f"SELECT house_id,square_meter,occupants FROM houses WHERE house_id IN {sel_house};",conn)
            df.set_index("house_id", inplace=True)
        print(df)
        print(totals)
        totals= pd.merge(totals, df, left_index=True, right_index=True)
        totals["score"] = ScoreUtils.calc_score(totals["occupants"], totals["square_meter"],totals["usage"],totals["generation"])
        record_list = zip(list(totals["score"]),list(totals.index))
        with sqlite3.connect(ScoreUtils.DBNAME) as conn:
            update_query = "UPDATE houses set score = ? where house_id = ?"
            curr = conn.cursor()
            curr.executemany(update_query,record_list)
            conn.commit()

    @classmethod
    def calc_score(cls,occupants, square_meter, usage, generation):
        return (generation-usage)/np.sqrt(np.sqrt(occupants*square_meter))
        
    @classmethod
    def update_worlds(cls):
        n_worlds = 3;
        with sqlite3.connect(ScoreUtils.DBNAME) as conn:
            df = pd.read_sql_query("SELECT house_id, score FROM houses",conn)
            df.set_index("house_id",inplace = True)
        df["level"] = pd.qcut(df["score"],n_worlds, labels=range(1,n_worlds+1))
        df.fillna(0,inplace=True)
        record_list = zip(list(df["level"]),list(df.index))
        with sqlite3.connect(ScoreUtils.DBNAME) as conn:
            update_query = "UPDATE houses set level = ? where house_id = ?"
            curr = conn.cursor()
            curr.executemany(update_query,record_list)
            conn.commit()
    @classmethod
    def leaderboard(cls,house_id):
        with sqlite3.connect(ScoreUtils.DBNAME) as conn:
            df = pd.read_sql_query("SELECT house_id, score FROM houses",conn)
        df.sort_values(by="score", inplace=True)
        df.reset_index(drop=True, inplace=True)
        top = df.iloc[range(3)]
        me = df.loc[df["house_id"] == house_id]
        idx = me.index[0]
        around = df.iloc[range(idx-1,idx+2)]
        ldb = top.append(around)
        return ldb