# PLAYERS

PLAYERS_CREATE  = """CREATE TABLE IF NOT EXISTS players (
                                        name text PRIMARY KEY,
                                        profile_link text,
                                        age integer,
                                        height integer,
                                        weight integer,
                                        position text,
                                        shoots text,
                                        team text,
                                        born text,
                                        college text,
                                        high_school text,
                                        recruiting_rank text,
                                        draft text,
                                        nba_debut text,
                                        experience text,
                                        awards text
                                    ); """

PLAYERS_REPLACE = ''' REPLACE INTO players(name,
                                profile_link,
                                age,
                                height,
                                weight,
                                position,
                                shoots,
                                team,
                                born,
                                college,
                                high_school,
                                recruiting_rank,
                                draft,
                                nba_debut,
                                experience,
                                awards)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''


# STATS
STATS_CREATE = """CREATE TABLE IF NOT EXISTS stats (
                                    hash text PRIMARY KEY,
                                    name text,
                                    season text,
                                    age integer,
                                    team text,
                                    league text,
                                    position text,
                                    games integer,
                                    games_started integer,
                                    minutes_played decimal,
                                    field_goals decimal,
                                    field_goal_attempts decimal,
                                    field_goal_percentage decimal,
                                    three_pointers decimal,
                                    three_pointer_attempts decimal,
                                    three_pointer_percentage decimal,
                                    two_pointers decimal,
                                    two_pointer_attempts decimal,
                                    two_pointer_percentage decimal,
                                    effective_field_goal_percentage decimal,
                                    free_throws decimal,
                                    free_throws_accuracy decimal,
                                    free_throws_percentage decimal,
                                    offensive_rebounds decimal,
                                    defensive_rebounds decimal,
                                    total_rebounds decimal,
                                    assists decimal,
                                    steals decimal,
                                    blocks decimal,
                                    turnovers decimal,
                                    personal_fouls decimal,
                                    points decimal,
                                    FOREIGN KEY (name) REFERENCES players (player_name)
                                );"""

STATS_REPLACE =""" REPLACE INTO stats(hash,
                                name,
                                season,
                                age,
                                team,
                                league,
                                position,
                                games,
                                games_started,
                                minutes_played,
                                field_goals,
                                field_goal_attempts,
                                field_goal_percentage,
                                three_pointers,
                                three_pointer_attempts,
                                three_pointer_percentage,
                                two_pointers,
                                two_pointer_attempts,
                                two_pointer_percentage,
                                effective_field_goal_percentage,
                                free_throws,
                                free_throws_accuracy,
                                free_throws_percentage,
                                offensive_rebounds,
                                defensive_rebounds,
                                total_rebounds,
                                assists,
                                steals,
                                blocks,
                                turnovers,
                                personal_fouls,
                                points)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """
    
# Play-by-Play
PBP_CREATE = """CREATE TABLE IF NOT EXISTS pbp (
                                    hash text PRIMARY KEY,
                                    name text,
                                    season text,
                                    age integer,
                                    team text,
                                    league text,
                                    position text,
                                    games integer,
                                    minutes_played decimal,
                                    point_guard_percentage decimal,
                                    shooting_guard_percentage decimal,
                                    small_forward_percentage decimal,
                                    power_forward_percentage decimal,
                                    center_percentage decimal,
                                    on_court_pm decimal,
                                    on_off_pm decimal,
                                    bad_pass_to decimal,
                                    lost_ball_to decimal,
                                    shooting_fouls_com decimal,
                                    offensive_fouls_com decimal,
                                    shooting_fouls_drawn decimal,
                                    offensive_fouls_drawn decimal,
                                    points_generated_by_assists decimal,
                                    and_ones decimal,
                                    fgs_blocked decimal,
                                    FOREIGN KEY (name) REFERENCES players (player_name)
                                );"""

PBP_REPLACE =""" REPLACE INTO pbp (hash,
                                name,
                                season,
                                age,
                                team,
                                league,
                                position,
                                games,
                                minutes_played,
                                point_guard_percentage,
                                shooting_guard_percentage,
                                small_forward_percentage,
                                power_forward_percentage,
                                center_percentage,
                                on_court_pm,
                                on_off_pm,
                                bad_pass_to,
                                lost_ball_to,
                                shooting_fouls_com,
                                offensive_fouls_com,
                                shooting_fouls_drawn,
                                offensive_fouls_drawn,
                                points_generated_by_assists,
                                and_ones,
                                fgs_blocked)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """