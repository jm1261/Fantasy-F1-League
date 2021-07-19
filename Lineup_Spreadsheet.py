import os
import xlsxwriter as xlsx
import Functions.Maths as maths
import Functions.SeasonInfo as si
import Functions.Plotting as plot
import Functions.Dictionary as dct
import Functions.Organisation as org

''' Organisation '''
year = '2021'
root = os.path.join(
    os.getcwd(),
    year)
spreadsheet_name = f'Fantasy F1 {year}.xlsx'
filepath = os.path.join(
    root,
    spreadsheet_name)
lineup_dir = os.path.join(
    root,
    'Lineup')
format_dir = os.path.join(
    root,
    '..',
    'Formats')
plot_dir = os.path.join(
    root,
    'Figures')
org.check_dir_exists(dir_path=plot_dir)

''' Config Files '''
info = org.get_config(
    config_path=os.path.join(
        root,
        '..',
        'Info.config'
    )).items()
lineup = org.get_config(
    config_path=os.path.join(
        root,
        '..',
        'Lineup.config'
    )).items()
driver_points = org.get_config(
    config_path=os.path.join(
        lineup_dir,
        'Driver_Points.config'
    )).items()
driver_values = org.get_config(
    config_path=os.path.join(
        lineup_dir,
        'Driver_Values.config'
    )).items()
team_points = org.get_config(
    config_path=os.path.join(
        lineup_dir,
        'Team_Points.config'
    )).items()
team_values = org.get_config(
    config_path=os.path.join(
        lineup_dir,
        'Team_Values.config'
    )).items()

''' Correct Dictionaries '''
dct.delta_points(
    dictionary=driver_points,
    out_path=os.path.join(
        lineup_dir,
        'Individual_Driver_Points.config'))
dct.delta_points(
    dictionary=team_points,
    out_path=os.path.join(
        lineup_dir,
        'Individual_Team_Points.config'))
individual_driver_points = org.get_config(
    config_path=os.path.join(
        lineup_dir,
        'Individual_Driver_Points.config'
    )).items()
individual_team_points = org.get_config(
    config_path=os.path.join(
        lineup_dir,
        'Individual_Team_Points.config'
    )).items()
dct.delta_values(
    dictionary=driver_values,
    out_path=os.path.join(
        lineup_dir,
        'Delta_Driver_Values.config'))
dct.delta_values(
    dictionary=team_values,
    out_path=os.path.join(
        lineup_dir,
        'Delta_Team_Values.config'))
delta_driver_values = org.get_config(
    config_path=os.path.join(
        lineup_dir,
        'Delta_Driver_Values.config'
    )).items()
delta_team_values = org.get_config(
    config_path=os.path.join(
        lineup_dir,
        'Delta_Team_Values.config'
    )).items()
dct.points_per_value(
    points_dict=individual_driver_points,
    values_dict=driver_values,
    out_path=os.path.join(
        lineup_dir,
        'Driver_PPVs.config'),
    average=False)
dct.points_per_value(
    points_dict=individual_driver_points,
    values_dict=driver_values,
    out_path=os.path.join(
        lineup_dir,
        'Average_Driver_PPVs.config'),
    average=True)
dct.points_per_value(
    points_dict=individual_team_points,
    values_dict=team_values,
    out_path=os.path.join(
        lineup_dir,
        'Team_PPVs.config'),
    average=False)
dct.points_per_value(
    points_dict=individual_team_points,
    values_dict=team_values,
    out_path=os.path.join(
        lineup_dir,
        'Average_Team_PPVs.config'),
    average=True)
driver_ppv = org.get_config(
    config_path=os.path.join(
        lineup_dir,
        'Driver_PPVs.config'
    )).items()
average_driver_ppv = org.get_config(
    config_path=os.path.join(
        lineup_dir,
        'Average_Driver_PPVs.config'
    )).items()
team_ppv = org.get_config(
    config_path=os.path.join(
        lineup_dir,
        'Team_PPVs.config'
    )).items()
average_team_ppv = org.get_config(
    config_path=os.path.join(
        lineup_dir,
        'Average_Team_PPVs.config'
    )).items()

''' Create Spreadsheet '''
workbook = xlsx.Workbook(filepath)

''' Create Cell Formats '''
header_format = workbook.add_format(
    org.get_config(
        config_path=os.path.join(
            format_dir,
            'Header.config'
        )
    ).items())
red_format = workbook.add_format(
    org.get_config(
        config_path=os.path.join(
            format_dir,
            'Red.config'
        )
    ).items())
data_format = workbook.add_format(
    org.get_config(
        config_path=os.path.join(
            format_dir,
            'Data.config'
        )
    ).items())

''' Create Sheets '''
driver_sheet = workbook.add_worksheet('Drivers')
team_sheet = workbook.add_worksheet('Teams')

''' Count Races, Drivers, and Teams '''
season_length, races = si.season_length(dictionary=info)
teams, drivers, index = si.teams_drivers(dictionary=lineup)
stats = si.statistics(dictionary=info)
rsf = si.races_so_far(dictionary=driver_points)

''' Print Season Parameters '''
print(f'The season is {season_length} races long, the races are {races}.\n'
      f'There are {len(teams)} teams, who are {teams}.\n'
      f'There are {len(drivers)} drivers, who are {drivers}.\n'
      f'To date there have been {rsf} races, these are {races[0: rsf]}.')

''' Add Races Row Headers '''
driver_sheet.write_column(
    row=1,
    col=0,
    data=races,
    cell_format=header_format)  # Points
driver_sheet.write_column(
    row=1,
    col=2 + len(drivers),
    data=races,
    cell_format=header_format)  # Values
team_sheet.write_column(
    row=1,
    col=0,
    data=races,
    cell_format=header_format)  # Points
team_sheet.write_column(
    row=1,
    col=2 + len(teams),
    data=races,
    cell_format=header_format)  # Values

''' Update Data From Config '''
driver_sheet.write(
    0,
    0,
    'Points',
    red_format)
column = 1
for driver, points in driver_points:
    driver_sheet.write_column(
        row=1,
        col=column,
        data=points,
        cell_format=data_format)
    column += 1
column += 1
driver_sheet.write(
    0,
    column,
    'Values',
    red_format)
column += 1
for driver, values in driver_values:
    driver_sheet.write_column(
        row=1,
        col=column,
        data=values,
        cell_format=data_format)
    column += 1
team_sheet.write(
    0,
    0,
    'Points',
    red_format)
column = 1
for team, points in team_points:
    team_sheet.write_column(
        row=1,
        col=column,
        data=points,
        cell_format=data_format)
    column += 1
column += 1
team_sheet.write(
    0,
    column,
    'Values',
    red_format)
column += 1
for team, values in team_values:
    team_sheet.write_column(
        row=1,
        col=column,
        data=values,
        cell_format=data_format)
    column += 1

''' Write Names With Colours '''
for i in range(0, len(drivers)):
    cell_format = workbook.add_format(
        org.get_config(
            config_path=os.path.join(
                format_dir,
                f'{index[i]}.config'
                )
        ).items())
    driver_sheet.write(
        0,
        1 + i,
        f'{drivers[i]}',
        cell_format)
    driver_sheet.write(
        0,
        3 + len(drivers) + i,
        f'{drivers[i]}',
        cell_format)
for i in range(0, len(teams)):
    cell_format = workbook.add_format(
        org.get_config(
            config_path=os.path.join(
                format_dir,
                f'{teams[i]}.config'
            )
        ).items())
    team_sheet.write(
        0,
        1 + i,
        f'{teams[i]}',
        cell_format)
    team_sheet.write(
        0,
        3 + len(teams) + i,
        f'{teams[i]}',
        cell_format)

''' Totals And Averages '''
dtp, dap = maths.total_average_dict(
    dictionary=driver_points)  # driver total/average points
dtv, dav = maths.total_average_dict(
    dictionary=driver_values)  # driver total/average values
dxp, dmp, dstdp = maths.min_max_variance_dict(
    dictionary=driver_points)  # driver min/max/stddev points
dxv, dmv, dstdv = maths.min_max_variance_dict(
    dictionary=driver_values)  # driver min/max/stddev values
dtptv = [dtp[i] / dtv[i]
         for i in range(0, len(dtp))]  # driver total points/value
dapav = [dap[i] / dav[i]
         for i in range(0, len(dap))]  # driver average points/value
drp = [dxp[i] - dmp[i]
       for i in range(0, len(dxp))]  # driver range of points
drv = [dxv[i] - dmv[i]
       for i in range(0, len(dxv))]  # driver range of values
ttp, tap = maths.total_average_dict(
    dictionary=team_points)  # team total/average points
ttv, tav = maths.total_average_dict(
    dictionary=team_values)  # team total/average values
txp, tmp, tstdp = maths.min_max_variance_dict(
    dictionary=team_points)  # team min/max/stddev points
txv, tmv, tstdv = maths.min_max_variance_dict(
    dictionary=team_values)  # team min/max/stddev values
ttptv = [ttp[i] / ttv[i]
         for i in range(0, len(ttp))]  # team total points/value
tapav = [tap[i] / tav[i]
         for i in range(0, len(tap))]  # team average points/value
trp = [txp[i] - tmp[i]
       for i in range(0, len(txp))]  # team range of points
trv = [txv[i] - tmv[i]
       for i in range(0, len(txv))]  # team range of values

''' Write Statistics Row Headers '''
driver_sheet.write_column(
    2 + len(races),
    0,
    stats,
    header_format)
driver_sheet.write_column(
    2 + len(races),
    2 + len(drivers),
    stats,
    header_format)
team_sheet.write_column(
    2 + len(races),
    0,
    stats,
    header_format)
team_sheet.write_column(
    2 + len(races),
    2 + len(teams),
    stats,
    header_format)

''' Write Statistics To Sheet - Check Order'''
driver_points_stats = [dtp, dtptv, dap, dapav, dstdp, dxp, dmp, drp]
driver_values_stats = [dtv, dtptv, dav, dapav, dstdv, dxv, dmv, drv]
team_points_stats = [ttp, ttptv, tap, tapav, tstdp, txp, tmp, trp]
team_values_stats = [ttv, ttptv, tav, tapav, tstdv, txv, tmv, trv]
for i in range(0, len(driver_points_stats)):
    driver_sheet.write_row(
        2 + i + len(races),
        1,
        driver_points_stats[i],
        data_format)
    driver_sheet.write_row(
        2 + i + len(races),
        3 + len(drivers),
        driver_values_stats[i])
    team_sheet.write_row(
        2 + i + len(races),
        1,
        team_points_stats[i],
        data_format)
    team_sheet.write_row(
        2 + i + len(races),
        3 + len(teams),
        team_values_stats[i],
        data_format)

''' Get Team Colours For Plotting '''
driver_colours = plot.plotting_colours(
    root=format_dir,
    array=drivers,
    index=index,
    drivers=True)
team_colours = plot.plotting_colours(
    root=format_dir,
    array=teams,
    index=teams,
    teams=True)

''' Plotting '''
for i in range(0, len(races[0: rsf])):
    print(f'Processing {races[i]}')
    races_plot_dir = os.path.join(
        plot_dir,
        f'{races[i]}')
    org.check_dir_exists(dir_path=races_plot_dir)
    
    ''' Points '''
    plot.season_plot(
        dictionary=individual_driver_points,
        races_array=races[0: i + 1],
        colour_dict=driver_colours,
        title=f'{races[i]} Driver Points',
        y_label='Points',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Driver_Points_Line.png'))
    plot.season_plot(
        dictionary=driver_points,
        races_array=races[0: i + 1],
        colour_dict=driver_colours,
        title=f'{races[i]} Cumulative Driver Points',
        y_label='Points',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Cumulative_Driver_Points_Line.png'))
    plot.season_plot(
        dictionary=individual_team_points,
        races_array=races[0: i + 1],
        colour_dict=team_colours,
        title=f'{races[i]} Team Points',
        y_label='Points',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Team_Points_Line.png'))
    plot.season_plot(
        dictionary=team_points,
        races_array=races[0: i + 1],
        colour_dict=team_colours,
        title=f'{races[i]} Cumulative Team Points',
        y_label='Points',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Cumulative_Team_Points_Line.png'))
    plot.average_plot(
        dictionary=individual_driver_points,
        races_array=races[0: i + 1],
        colour_dict=driver_colours,
        y_label='Average Points',
        title=f'{races[i]} Average Driver Points',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Average_Driver_Points_Line.png'))
    plot.average_plot(
        dictionary=individual_team_points,
        races_array=races[0: i + 1],
        colour_dict=team_colours,
        y_label='Average Points',
        title=f'{races[i]} Average Team Points',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Average_Team_Points_Line.png'))

    ''' Values '''
    plot.season_plot(
        dictionary=driver_values,
        races_array=races[0: i + 1],
        colour_dict=driver_colours,
        title=f'{races[i]} Driver Values',
        y_label='Values [$M]',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Driver_Values_Line.png'))
    plot.season_plot(
        dictionary=delta_driver_values,
        races_array=races[0: i + 1],
        colour_dict=driver_colours,
        title=f'{races[i]} Change In Driver Values',
        y_label='Change In Values [$M]',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Delta_Driver_Values_Line.png'))
    plot.season_plot(
        dictionary=delta_driver_values,
        races_array=races[0: i + 1],
        colour_dict=driver_colours,
        title=f'{races[i]} Total Change In Driver Values',
        y_label='Change In Values [$M]',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Total_Delta_Driver_Values_Line.png'),
        cumulative=True)
    plot.season_plot(
        dictionary=team_values,
        races_array=races[0: i + 1],
        colour_dict=team_colours,
        title=f'{races[i]} Team Values',
        y_label='Values [$M]',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Team_Values_Line.png'))
    plot.season_plot(
        dictionary=delta_team_values,
        races_array=races[0: i + 1],
        colour_dict=team_colours,
        title=f'{races[i]} Change In Team Values',
        y_label='Change In Values [$M]',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Delta_Team_Values_Line.png'))
    plot.season_plot(
        dictionary=delta_team_values,
        races_array=races[0: i + 1],
        colour_dict=team_colours,
        title=f'{races[i]} Total Change In Team Values',
        y_label='Change In Values [$M]',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Total_Delta_Team_Values_Line.png'),
        cumulative=True)    
    plot.average_plot(
        dictionary=driver_values,
        races_array=races[0: i + 1],
        colour_dict=driver_colours,
        y_label='Average Values',
        title=f'{races[i]} Average Driver Values',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Average_Driver_Values_Line.png'))
    plot.average_plot(
        dictionary=team_values,
        races_array=races[0: i + 1],
        colour_dict=team_colours,
        y_label='Average Values',
        title=f'{races[i]} Average Team Values',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Average_Team_Values_Line.png'))

    ''' Points Per Value '''
    plot.season_plot(
        dictionary=driver_ppv,
        races_array=races[0: i + 1],
        colour_dict=driver_colours,
        title=f'{races[i]} Driver Points Per Value',
        y_label='Points/Value [1/$M]',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Driver_PPV_Line.png'))
    plot.season_plot(
        dictionary=average_driver_ppv,
        races_array=races[0: i + 1],
        colour_dict=driver_colours,
        title=f'{races[i]} Driver Average Points Per Value',
        y_label='Average Points/Value [1/$M]',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Driver_PPV_Line.png'))
    plot.season_plot(
        dictionary=team_ppv,
        races_array=races[0: i + 1],
        colour_dict=team_colours,
        title=f'{races[i]} Team Points Per Value',
        y_label='Points/Value [1/$M]',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Team_PPV_Line.png'))
    plot.season_plot(
        dictionary=average_team_ppv,
        races_array=races[0: i + 1],
        colour_dict=team_colours,
        title=f'{races[i]} Team Average Points Per Value',
        y_label='Average Points/Value [1/$M]',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Team_PPV_Line.png'))

    ''' Bar Plots '''
    plot.season_bar(
        dictionary=driver_points,
        races_array=races[0: i],
        colour_dict=driver_colours,
        title=f'{races[i]} Driver Points',
        x_label='Points',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Driver_Points_Bar.png'),
        cumulative=False,
        index=i)
    plot.season_bar(
        dictionary=driver_points,
        races_array=races[0: i],
        colour_dict=driver_colours,
        title=f'{races[i]} Total Driver Points',
        x_label='Points',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Total_Driver_Points_Bar.png'),
        cumulative=True,
        index=False)
    plot.season_bar(
        dictionary=driver_values,
        races_array=races[0: i],
        colour_dict=driver_colours,
        title=f'{races[i]} Driver Values',
        x_label='Values [$M]',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Driver_Values_Bar.png'),
        cumulative=False,
        index=i)
    plot.season_bar(
        dictionary=driver_values,
        races_array=races[0: i],
        colour_dict=driver_colours,
        title=f'{races[i]} Total Driver Values',
        x_label='Values [$M]',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Total_Driver_Values_Bar.png'),
        cumulative=True,
        index=False)
    plot.season_bar(
        dictionary=team_points,
        races_array=races[0: i],
        colour_dict=team_colours,
        title=f'{races[i]} Team Points',
        x_label='Points',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Team_Points_Bar.png'),
        cumulative=False,
        index=i)
    plot.season_bar(
        dictionary=team_points,
        races_array=races[0: i],
        colour_dict=team_colours,
        title=f'{races[i]} Total Team Points',
        x_label='Points',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Total_Team_Points_Bar.png'),
        cumulative=True,
        index=False)
    plot.season_bar(
        dictionary=team_values,
        races_array=races[0: i],
        colour_dict=team_colours,
        title=f'{races[i]} Team Values',
        x_label='Values [$M]',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Team_Values_Bar.png'),
        cumulative=False,
        index=i)
    plot.season_bar(
        dictionary=team_values,
        races_array=races[0: i],
        colour_dict=team_colours,
        title=f'{races[i]} Total Team Values',
        x_label='Values [$M]',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Total_Team_Values_Bar.png'),
        cumulative=True,
        index=False)
    plot.season_bar(
        dictionary=delta_driver_values,
        races_array=races[0: i],
        colour_dict=driver_colours,
        title=f'{races[i]} Change In Driver Values',
        x_label='Change In Values [$M]',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Delta_Driver_Values_Bar.png'),
        cumulative=False,
        index=i)
    plot.season_bar(
        dictionary=delta_driver_values,
        races_array=races[0: i],
        colour_dict=driver_colours,
        title=f'{races[i]} Total Change In Driver Values',
        x_label='Change In Values [$M]',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Total_Delta_Driver_Values_Bar.png'),
        cumulative=True,
        index=False)
    plot.season_bar(
        dictionary=delta_team_values,
        races_array=races[0: i],
        colour_dict=team_colours,
        title=f'{races[i]} Change In Team Values',
        x_label='Change In Values [$M]',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Delta_Team_Values_Bar.png'),
        cumulative=False,
        index=i)
    plot.season_bar(
        dictionary=delta_team_values,
        races_array=races[0: i],
        colour_dict=team_colours,
        title=f'{races[i]} Total Change In Team Values',
        x_label='Change In Values [$M]',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Total_Delta_Team_Values_Bar.png'),
        cumulative=True,
        index=False)
    plot.season_bar(
        dictionary=driver_ppv,
        races_array=races[0: i],
        colour_dict=driver_colours,
        title=f'{races[i]} Driver Points/Value',
        x_label='Points/Value [1/$M]',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Driver_PPV_Bar.png'),
        cumulative=False,
        index=i)
    plot.season_bar(
        dictionary=average_driver_ppv,
        races_array=races[0: i],
        colour_dict=driver_colours,
        title=f'{races[i]} Average Driver Points/Value',
        x_label='Average Points/Value [1/$M]',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Average_Driver_PPV_Bar.png'),
        cumulative=False,
        index=i)
    plot.season_bar(
        dictionary=team_ppv,
        races_array=races[0: i],
        colour_dict=team_colours,
        title=f'{races[i]} Team Points/Value',
        x_label='Points/Value [1/$M]',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Team_PPV_Bar.png'),
        cumulative=False,
        index=i)
    plot.season_bar(
        dictionary=average_team_ppv,
        races_array=races[0: i],
        colour_dict=team_colours,
        title=f'{races[i]} Average Team Points/Value',
        x_label='Average Points/Value [1/$M]',
        out_path=os.path.join(
            races_plot_dir,
            f'{races[i]}_Average_Team_PPV_Bar.png'),
        cumulative=False,
        index=i)

''' Close Workbook '''
workbook.close()
