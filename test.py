
        column += 1
        team_sheet.write_column(
            row=1,
            col=column,
            data=races,
            cell_format=header_format)  # Races
        column += 1
        for key, values in manager_points.items():
            team_sheet.write_column(
                row=1,
                col=column,
                data=values,
                cell_format=data_format)
            column += 1
        team_sheet.write(
            0,
            column,
            'Weekly Total',
            header_format)
        team_sheet.write_column(
            row=1,
            col=column,
            data=season_points,
            cell_format=data_format)
        team_sheet.write(
            len(season_points) + 2,
            column,
            total_points,
            data_format)
        column += 2
        team_sheet.write_column(
            row=1,
            col=column,
            data=races,
            cell_format=header_format)  # Races
        column += 1
        for key, values in manager_values.items():
            team_sheet.write_column(
                row=1,
                col=column,
                data=values,
                cell_format=data_format)
            column += 1
        team_sheet.write(
            0,
            column,
            'Weekly Total',
            header_format)
        team_sheet.write_column(
            row=1,
            col=column,
            data=season_values,
            cell_format=data_format)
        team_sheet.write(
            len(season_points) + 2,
            column,
            total_values,
            data_format)

    ''' Close Workbook '''
    workbook.close()

org.dump_json(
    out_path=os.path.join(
        stats_dir,
        f'{year}_WeeklyScore.config'),
    dictionary=weekly_score_dict)
org.dump_json(
    out_path=os.path.join(
        stats_dir,
        f'{year}_SeasonScore.config'),
    dictionary=season_score_dict)

for index, race in enumerate(races):
    fig, ax = plt.subplots(1, figsize=[10, 7])
    x_values = []
    y_values = []
    for key, points in season_score_dict.items():
        x_values.append(key)
        y_values.append(points[index])
    zipped_lists = zip(y_values, x_values)
    sorted_pairs = sorted(zipped_lists)
    tuples = zip(*sorted_pairs)
    x, y = [list(tuple) for tuple in tuples]
    ax.barh(y, x)
    for i, v in enumerate(x):
        if v < 0:
            ax.text(
                -v,
                i,
                str(round(v, 2)),
                fontweight='bold',
                va='center')
        else:
            ax.text(
                v + (v/50),
                i,
                str(round(v, 2)),
                fontweight='bold',
                va='center')
    ax.set_title(
        f'{race}',
        fontsize=24,
        fontweight='bold')
    ax.set_ylabel(
        'Name',
        fontsize=18,
        fontweight='bold')
    ax.set_xlabel(
        'Races',
        fontsize=18,
        fontweight='bold')
    plt.savefig(
        os.path.join(
            stats_dir,
            f'{race}.png'))
    fig.clf()
    plt.close(fig)
