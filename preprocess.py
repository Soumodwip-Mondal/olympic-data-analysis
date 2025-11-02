import streamlit as st
import pandas as pd

def preprosess():
    df_player=pd.read_csv('athlete_events.csv')
    df_region=pd.read_csv('noc_regions.csv')
    df=df_player.merge(right=df_region,on='NOC')
    df = pd.get_dummies(df, columns=['Medal'],)
    # Rename the columns if you want shorter names
    df.rename(columns={
        'Medal_Gold': 'gold',
        'Medal_Silver': 'silver',
        'Medal_Bronze': 'bronze'
    }, inplace=True)
    df[['bronze','gold','silver']]=df[['bronze','gold','silver']].astype('int')
    return df
def preprocess2():
    df_player=pd.read_csv('athlete_events.csv')
    df_region=pd.read_csv('noc_regions.csv')
    df=df_player.merge(right=df_region,on='NOC')
    return df   
