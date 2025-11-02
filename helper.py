import pandas as pd
import numpy as np
def get_medal_tally(df, country='overall', year='overall'):
    # Remove duplicate medal records
    df_medals = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Sport', 'region', 'City'])
    
    flag = 0  # To detect if we’re showing per-year data
    
    # --- Conditions for filtering ---
    if country == 'overall' and year == 'overall':
        temp_df = df_medals
    elif country != 'overall' and year == 'overall':
        temp_df = df_medals[df_medals['region'] == country]
        flag = 1
    elif country == 'overall' and year != 'overall':
        temp_df = df_medals[df_medals['Year'] == int(year)]
    else:
        temp_df = df_medals[(df_medals['region'] == country) & (df_medals['Year'] == int(year))]
    if flag == 1:
        x = temp_df.groupby('Year')[['bronze', 'silver', 'gold']].sum().sort_values(by='gold', ascending=False).reset_index()
    else:
        x = temp_df.groupby('region')[['bronze', 'silver', 'gold']].sum().sort_values(by='gold', ascending=False).reset_index()
    x['overall'] = x['bronze'] + x['silver'] + x['gold']
    return x

def get_year_country(df):
    year = df['Year'].unique().tolist()
    year.sort()
    year.insert(0, 'overall')
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'overall')
    return year,country
def year_wise_participation(df):
    temp_df=df[['Year','region']]
    temp_df=temp_df.drop_duplicates()
    temp_df=temp_df.groupby('Year')['region'].count().reset_index()
    return temp_df

def data_over_time(df, col):
    temp_df = df.drop_duplicates(['Year', col])
    nations_over_time = temp_df.groupby('Year')[col].count().reset_index()
    nations_over_time.rename(columns={'Year': 'Edition', col: 'count'}, inplace=True)
    return nations_over_time

def year_wise_medal_tally(df, country):
    # Filter rows where at least one medal was won
    temp_df = df[(df['gold'] != 0) | (df['silver'] != 0) | (df['bronze'] != 0)]
    
    # Remove duplicates to avoid counting the same medal multiple times
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event'])
    
    # Filter by country
    new_df = temp_df[temp_df['region'] == country]
    
    # Calculate total medals per row
    new_df['Medal'] = new_df[['gold', 'silver', 'bronze']].sum(axis=1)
    
    # Group by year and sum medals
    final_df = new_df.groupby('Year')['Medal'].sum().reset_index()
    
    return final_df
def most_successful(df, sport):
    sports=df['Sport'].tolist()
    if sport != 'Overall':
        if sport not in sports:
            raise Exception('The input is not valid!')
        temp_df = df[df['Sport'] == sport]
    else:
        temp_df = df[['Name', 'Sport', 'region', 'Season', 'City', 'bronze', 'gold', 'silver']].copy()

    # Calculate total medals per row
    temp_df['medals'] = temp_df[['bronze', 'gold', 'silver']].sum(axis=1)

    # Group by player and count total medals
    temp_df = (
        temp_df.groupby(['Name', 'Sport', 'region'], as_index=False)['medals']
        .sum()
        .sort_values(by='medals', ascending=False)
    )

    temp_df = temp_df.rename(columns={'medals': 'total_medals'})
    return temp_df.head(15)

def most_successfull_in_country(df,country):
    df=df[df['region']==country]
    return most_successful(df,'Overall')

def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df = athlete_df.dropna(subset=['Height', 'Weight'])
    
    if sport != 'Overall':
        athlete_df = athlete_df[athlete_df['Sport'] == sport]
        
    return athlete_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    final['Female']=final['Female'].astype('int64')
    return final
