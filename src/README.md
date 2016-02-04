# VendAsta Foosball Ladder

This is the code repository for the site found at http://foosball.vendasta.com.
It uses Google's App Engine and Python, with Jinja2 templating.

# VendAsta SC2 Ladder
foos 10-2
- Improved apis to be more restful
- Added api to get matches for a player
- Added api to get suggested 1v1 opponents for a player
- Added directive to search for matches
- Added dashboard for logged in player
- Added directive for displaying player stats

foos 10-1
- Open matches now displayed in chronological order.
- Match now removed after being closed.
- Upload nav item now only displayed if user logged in.
- Selecting match to upload now displayed in table.

foos 10
- added new site based on angularjs material UI

foos 9-2
- updated sc2reader lib to support most recent replay version

foos 9-1
- added support for uploading replays from Legacy of the Void yay!

foos 8-2
- fixed bug where could not calculate average last game played if player rank did not have last game played

foos-8-1
- score only calculated after closing match
- now only taking into account 2v2 games when considering last game played during match making algorithm

foos-8
- Added player details page

foos-7-1
- Improved matchmaking algorithm to take into account when last game was played

foos-7
- Added King of the Hill mode

foos-6
- Added ability to edit player's participation in season

foos-5
- Added ability to create seasons and matches