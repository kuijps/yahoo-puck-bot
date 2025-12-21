# yahoo-puck-bot 
this is a blueprint i used to connect to my NHL yahoo fantasy league to do various functions relevant to me and automate decisions I made daily. 

## what it does not have:
- oauth2.json file (you will need to create one in the project folder) : see the yahoo-fantasy-api (Authentication) documentation for setup: https://yahoo-fantasy-api.readthedocs.io/en/latest/authentication.html | Repo: https://github.com/spilchen/yahoo_fantasy_api
- a wrapper or UI: I suggest creating something to run this in a useful way to you. Create a webapp to display the data on load or wrapper that runs it on a schedule. Initailly I chose to wrap the python scripts and use a smtp server to email info daily to help manage my team and strean FAs

## what it does
- gets the nhl scedule for the week and stores in a json and csv format
- connects to your league and runs different functions like get ir cheese and FAs for the week depending on schedule (in progress)
