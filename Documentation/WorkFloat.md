# Work Flow Documentation

<div style="text-align: justify">

Detailed work flow documentation for the F1™ Fantasy league data processing code. Documentation created on 02/11/2024 and maintained regularly. This code does not provide API access to the F1™ Fantasy database or F1™ official website.

## Disclaimer

This document is unofficial and is not associated in any way with the Formula 1 companies. F1, FORMULA ONE, FORMULA 1, FIA FORMULA ONE WORLD CHAMPIONSHIP, GRAND PRIX and related marks are trade marks of Formula One Licensing B.V.

## Concept

This repository serves to produce figures, reports, statistics, and analysis for the F1™ Fantasy game and, more specifically, a private league within that game-space. The league has been running for many years, as such there is a vast back-catalog of data, not only from the official constructors and drivers, but from participants in the annual leagues.

## Repository Structure

* Main Repository:
  * config
    * Lineup_Formats
      * Colours, drivers, linestyles, fontsizes, etc. for the F1™ constructors and F1™ Fantasy perks and tokens.
    * Manager_Formats
      * Colours, linestyles, team names, fontsizes, etc. for the participating F1™ Fantasy members, along with annual team entries.
    * SeasonInfo json file.
  * Data
    * Year Folder
      * Manager Folders
        * Entered team(s) results json file.
      * Lineup Folders
        * F1™ constructors and drivers results json files.
      * Support json files.
  * Documentation
    * Relevant README and documentation files.
  * Finances
    * Entry fee documentation.
  * Prizes
    * Annual prize name and qualification json files.
  * Reports
    * HTML outputs of Jupyter notebooks for each race report.
  * src
    * Support files for operation of the repository.
  * primary scripts.

## Season Launch

TBC

## Lineup

This section details the work flow for logging, analysis, plotting, and outputting the weekly scores and values of the F1™ constructors and drivers within the F1™ Fantasy system. Since there exists no API to access these scores and values, the data is inputted manually into a JSON config file located within the Data/Year tree, where Year is dependent on which year the scores are accounted for. From there, run Lineup.py to pull this data in and start to process it.

### Config File Input

The JSON config file is essentially a dictionary containing the following keys: Name, Race, Driver Names, Constructor Names. This file is created by the season launch script, so there is no need to manually input the Driver or Constructor names. The first key, "Name", is an example key, showing the associated list values ['Points', 'Values'], which refer to the current total score and the race weekend value within the F1™ Fantasy game. The key 'Race' should have a list value with one string contained within the list, more are possible but will be ignored. The race value should be the race name as detailed in the SeasonInfo.json file within the Config directory tree. This entry is used to name the output file, and to ensure weekly scores can be accurately counted.

### Data Processing

Lineup.py focuses on producing the results based on the completed weekly race results. It then uses these weekly files to populate season-long results and statistics dictionaries to finally use to produce plots. The reason it does this for every week is due to the manual data input. Occasionally mistakes are made, or scores change, and to prevent this having to be changed at every instance, the code looks through the individual weekly files. That way, only this file need be adjusted.

</div>
