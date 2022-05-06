import os
import Functions.Maths as math
import Functions.SeasonInfo as si
import Functions.Plotting as plot
import Functions.Spreadsheet as ss
import Functions.Dictionary as dct
import Functions.Organisation as org

''' Organisation '''
year = '2022'
root = os.path.join(
    os.getcwd(),
    year)
spreadsheetname = f'Fantasy F1 {year}.xlsx'
filepath = os.path.join(
    root,
    spreadsheetname)
lineupdir = os.path.join(
    root,
    'Lineup')
formatdir = os.path.join(
    root,
    '..',
    'Formats')
plotdir = os.path.join(
    root,
    'Figures')

''' Correct Dictionaries '''
dct.correct_dictionaries(
    dir_path=lineupdir,
    categories=['Driver', 'Team'])

''' Config Files '''
info = org.get_config(
    config_path=os.path.join(
        root,
        '..',
        'Info.config')).items()
lineup = org.get_config(
    config_path=os.path.join(
        root,
        '..',
        'Lineup.config')).items()
drvrpnts, drvrvals, teampnts, teamvals = dct.get_dictionaries(
    dir_path=lineupdir,
    dictionaries=[
        'Driver_Points',
        'Driver_Values',
        'Team_Points',
        'Team_Values'])
inddrvrpnts, indteampnts, deldrvrvals, delteamvals = dct.get_dictionaries(
    dir_path=lineupdir,
    dictionaries=[
        'Individual_Driver_Points',
        'Individual_Team_Points',
        'Delta_Driver_Values',
        'Delta_Team_Values'])
drvrppv, avgdrvrppv, teamppv, avgteamppv = dct.get_dictionaries(
    dir_path=lineupdir,
    dictionaries=[
        'Driver_PPVs',
        'Average_Driver_PPVs',
        'Team_PPVs',
        'Average_Team_PPVs'])

''' Cound Races, Drivers and Teams '''
season_length, races = si.season_length(dictionary=info)
teams, drivers, index = si.teams_drivers(dictionary=lineup)
stats = si.statistics(dictionary=info)
rsf = si.races_so_far(dictionary=drvrpnts)
print(
    f'The season is {season_length} races long, the races are {races}\n'
    f'There are {len(teams)} teams, who are {teams}\n'
    f'There are {len(drivers)} drivers, who are {drivers}\n'
    f'To date, there have been {rsf} races, these races are {races[0: rsf]}.')

''' Totals and Averages '''
dtp, dap, dtv, dav, dxp, dmp, dstdp, dxv, dmv, dstdv = math.drvr_team_stats(
    points_dict=inddrvrpnts,
    values_dict=drvrvals)
dtptv, dapav, drp, drv = math.drvs_team_calcs(
    total_points=dtp, total_values=dtv,
    average_points=dap, average_values=dav,
    max_points=dxp, min_points=dmp,
    max_values=dxv, min_values=dmv)
ttp, tap, ttv, tav, txp, tmp, tstdp, txv, tmv, tstdv = math.drvr_team_stats(
    points_dict=indteampnts,
    values_dict=teamvals)
ttptv, tapav, trp, trv = math.drvs_team_calcs(
    total_points=ttp, total_values=ttv,
    average_points=tap, average_values=tav,
    max_points=txp, min_points=tmp,
    max_values=txv, min_values=tmv)
drvrpntsstats = [dtp, dtptv, dap, dapav, dstdp, dxp, dmp, drp]
drvrvalsstats = [dtv, dtptv, dav, dapav, dstdv, dxv, dmv, drv]
teampntsstats = [ttp, ttptv, tap, tapav, tstdp, txp, tmp, trp]
teamvalsstats = [ttv, ttptv, tav, tapav, tstdv, txv, tmv, trv]

''' Create Spreadsheet '''
ss.driver_team_spreadsheet(
    file_path=filepath,
    format_dir=formatdir,
    races=races,
    drivers=drivers,
    teams=teams,
    index=index,
    driver_points=drvrpnts,
    driver_values=drvrvals,
    team_points=teampnts,
    team_values=teamvals,
    driver_points_stats=drvrpntsstats,
    driver_values_stats=drvrvalsstats,
    team_points_stats=teampntsstats,
    team_values_stats=teamvalsstats)

''' Plotting '''
drivercolours = plot.plotting_colour(
    root=formatdir,
    array=drivers,
    index=index,
    drivers=True)
teamcolours = plot.plotting_colour(
    root=formatdir,
    array=teams,
    index=teams,
    teams=True)
[plot.plot_dictionary(
    plot_dir=plotdir,
    races=races[0: i + 1],
    race_index=i,
    name='Driver_Points',
    dictionary=inddrvrpnts,
    colours=drivercolours,
    label='Points',
    cumulative=True,
    line=True)
 for i in range(0, len(races[0: rsf]))]  # Cumulative Driver Points Line
[plot.plot_dictionary(
    plot_dir=plotdir,
    races=races[0: i + 1],
    race_index=i,
    name='Team_Points',
    dictionary=indteampnts,
    colours=teamcolours,
    label='Points',
    cumulative=True,
    line=True)
 for i in range(0, len(races[0: rsf]))]  # Cumulative Team Points Line
[plot.plot_dictionary(
    plot_dir=plotdir,
    races=races[0: i + 1],
    race_index=i,
    name='Driver_Points',
    dictionary=inddrvrpnts,
    colours=drivercolours,
    label='Points',
    cumulative=False,
    line=False)
 for i in range(0, len(races[0: rsf]))]  # Driver Points Bar
[plot.plot_dictionary(
    plot_dir=plotdir,
    races=races[0: i + 1],
    race_index=i,
    name='Driver_Points',
    dictionary=inddrvrpnts,
    colours=drivercolours,
    label='Points',
    cumulative=True,
    line=False)
 for i in range(0, len(races[0: rsf]))]  # Cumulative Driver Points Bar
[plot.plot_dictionary(
    plot_dir=plotdir,
    races=races[0: i + 1],
    race_index=i,
    name='Team_Points',
    dictionary=indteampnts,
    colours=teamcolours,
    label='Points',
    cumulative=False,
    line=False)
 for i in range(0, len(races[0: rsf]))]  # Team Points Bar
[plot.plot_dictionary(
    plot_dir=plotdir,
    races=races[0: i + 1],
    race_index=i,
    name='Team_Points',
    dictionary=indteampnts,
    colours=teamcolours,
    label='Points',
    cumulative=True,
    line=False)
 for i in range(0, len(races[0: rsf]))]  # Cumulative Team Points Bar
[plot.plot_dictionary(
    plot_dir=plotdir,
    races=races[0: i + 1],
    race_index=i,
    name='Driver_Values',
    dictionary=drvrvals,
    colours=drivercolours,
    label='Values [$M]',
    cumulative=False,
    line=True)
 for i in range(0, len(races[0: rsf]))]  # Driver Values Line
[plot.plot_dictionary(
    plot_dir=plotdir,
    races=races[0: i + 1],
    race_index=i,
    name='Team_Values',
    dictionary=teamvals,
    colours=teamcolours,
    label='Values [$M]',
    cumulative=False,
    line=True)
 for i in range(0, len(races[0: rsf]))]  # Team Values Line
[plot.plot_dictionary(
    plot_dir=plotdir,
    races=races[0: i + 1],
    race_index=i,
    name='Driver_Values',
    dictionary=drvrvals,
    colours=drivercolours,
    label='Values [$M]',
    cumulative=False,
    line=False)
 for i in range(0, len(races[0: rsf]))]  # Driver Values Bar
[plot.plot_dictionary(
    plot_dir=plotdir,
    races=races[0: i + 1],
    race_index=i,
    name='Team_Values',
    dictionary=teamvals,
    colours=teamcolours,
    label='Values [$M]',
    cumulative=False,
    line=False)
 for i in range(0, len(races[0: rsf]))]  # Team Values Bar
[plot.plot_dictionary(
    plot_dir=plotdir,
    races=races[0: i + 1],
    race_index=i,
    name='Delta_Driver_Values',
    dictionary=deldrvrvals,
    colours=drivercolours,
    label='Change In Values [$M]',
    cumulative=False,
    line=False)
 for i in range(0, len(races[0: rsf]))]  # Delta Driver Values Bar
[plot.plot_dictionary(
    plot_dir=plotdir,
    races=races[0: i + 1],
    race_index=i,
    name='Delta_Team_Values',
    dictionary=delteamvals,
    colours=teamcolours,
    label='Change In Values [$M]',
    cumulative=False,
    line=False)
 for i in range(0, len(races[0: rsf]))]  # Delta Team Values Bar
[plot.plot_dictionary(
    plot_dir=plotdir,
    races=races[0: i + 1],
    race_index=i,
    name='Delta_Driver_Values',
    dictionary=deldrvrvals,
    colours=drivercolours,
    label='Change In Values [$M]',
    cumulative=True,
    line=True)
 for i in range(0, len(races[0: rsf]))]  # Cumulative Delta Driver Values Line
[plot.plot_dictionary(
    plot_dir=plotdir,
    races=races[0: i + 1],
    race_index=i,
    name='Delta_Team_Values',
    dictionary=delteamvals,
    colours=teamcolours,
    label='Change In Values [$M]',
    cumulative=True,
    line=True)
 for i in range(0, len(races[0: rsf]))]  # Cumulative Delta Team Values Line
[plot.plot_dictionary(
    plot_dir=plotdir,
    races=races[0: i + 1],
    race_index=i,
    name='Average_Driver_PPV',
    dictionary=avgdrvrppv,
    colours=drivercolours,
    label='Points/Value [1/$M]',
    cumulative=False,
    line=True)
 for i in range(0, len(races[0: rsf]))]  # Average Driver PPV Line
[plot.plot_dictionary(
    plot_dir=plotdir,
    races=races[0: i + 1],
    race_index=i,
    name='Average_Team_PPV',
    dictionary=avgteamppv,
    colours=teamcolours,
    label='Points/Value [1/$M]',
    cumulative=False,
    line=True)
 for i in range(0, len(races[0: rsf]))]  # Average Team PPV Line
[plot.plot_dictionary(
    plot_dir=plotdir,
    races=races[0: i + 1],
    race_index=i,
    name='Driver_PPV',
    dictionary=drvrppv,
    colours=drivercolours,
    label='Points/Value [1/$M]',
    cumulative=False,
    line=False)
 for i in range(0, len(races[0: rsf]))]  # Driver PPV Bar
[plot.plot_dictionary(
    plot_dir=plotdir,
    races=races[0: i + 1],
    race_index=i,
    name='Average_Driver_PPV',
    dictionary=avgdrvrppv,
    colours=drivercolours,
    label='Points/Value [1/$M]',
    cumulative=False,
    line=False)
 for i in range(0, len(races[0: rsf]))]  # Average Driver PPV Bar
[plot.plot_dictionary(
    plot_dir=plotdir,
    races=races[0: i + 1],
    race_index=i,
    name='Team_PPV',
    dictionary=teamppv,
    colours=teamcolours,
    label='Points/Value [1/$M]',
    cumulative=False,
    line=False)
 for i in range(0, len(races[0: rsf]))]  # Team PPV Bar
[plot.plot_dictionary(
    plot_dir=plotdir,
    races=races[0: i + 1],
    race_index=i,
    name='Average_Team_PPV',
    dictionary=avgteamppv,
    colours=teamcolours,
    label='Points/Value [1/$M]',
    cumulative=False,
    line=False)
 for i in range(0, len(races[0: rsf]))]  # Average Team PPV Bar
