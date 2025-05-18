'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
from modes import MODE_TO_COLUMN



def summarize_lines(my_df):
    '''
        Sums each player's total of number of lines and  its
        corresponding percentage per act.

        The sum of lines per player per act is in a new
        column named 'PlayerLine'.

        The percentage of lines per player per act is
        in a new column named 'PlayerPercent'

        Args:
            my_df: The pandas dataframe containing the data from the .csv file
        Returns:
            The modified pandas dataframe containing the
            information described above.
    '''
    # Count the number of lines per player per act
    player_lines = my_df.groupby(['Act', 'Player']).size().reset_index(name='LineCount')
    
    # Calculate the total number of lines per act
    act_total_lines = player_lines.groupby('Act')['LineCount'].sum().reset_index(name='TotalLines')
    
    # Merge to associate each player's line count with the total lines of the act
    player_df = pd.merge(player_lines, act_total_lines, on='Act')

    # Compute the percentage of lines for each player within their act
    player_df['LinePercent'] = (player_df['LineCount'] / player_df['TotalLines']) * 100
    
    # Drop the total line count column, as it's no longer needed
    player_df.drop(columns=['TotalLines'], inplace=True)
    
    return player_df


def replace_others(my_df):
    '''
        For each act, keeps the 5 players with the most lines
        throughout the play and groups the other plyaers
        together in a new line where :

        - The 'Act' column contains the act
        - The 'Player' column contains the value 'OTHER'
        - The 'LineCount' column contains the sum
            of the counts of lines in that act of
            all players who are not in the top
            5 players who have the most lines in
            the play
        - The 'PercentCount' column contains the sum
            of the percentages of lines in that
            act of all the players who are not in the
            top 5 players who have the most lines in
            the play

        Returns:
            The df with all players not in the top
            5 for the play grouped as 'OTHER'
    '''
    # TODO : Replace players in each act not in the top 5 by a

    # Sum line count and percentage for "other" players, grouped by act
    top_players = my_df.groupby('Player')['LineCount'].sum().nlargest(5).index
    
    others_df = my_df[~my_df['Player'].isin(top_players)]
    top_df = my_df[my_df['Player'].isin(top_players)]
    
    # Set the player name as 'OTHER' for all grouped entries
    others_summed = others_df.groupby('Act').agg({'LineCount': 'sum', 'LinePercent': 'sum'}).reset_index()
    others_summed['Player'] = 'OTHER'
    
    # Combine the top players and the "OTHER" group into a single dataframe
    final_df = pd.concat([top_df, others_summed], ignore_index=True)
    
    return final_df


def clean_names(my_df):
    '''
        In the dataframe, formats the players'
        names so each word start with a capital letter.

        Returns:
            The df with formatted names
    '''
    # TODO : Clean the player names

    # Capitalize the first letter of each word in the player's name
    my_df['Player'] = my_df['Player'].apply(lambda name: name.title())

    # Add the prefix 'Act ' in front of each act number 
    my_df['Act'] = my_df['Act'].apply(lambda x: f'Act {x}')
    return my_df
