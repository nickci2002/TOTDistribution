# TOTDistribution (v1.1) by Nicholas Inglima
- V1.0 created December 2022-March 2023
- V1.1 created April 2025

## Overview
This is a personal, backend project written in Python. It accesses Nadeo's API (NadeoLiveServices) to receive medal <br> distribution for daily tracks in Trackmania. It gets leaderboard data from Nadeo's API and analyzes them to <br> 
of medals these results to get the medal distributions.

## Dependencies
This program requires the requests and keyring APIs to run. Copy and paste the following into your command line:<br>
```
pip install requests && keyrings
```

## How to Use
This is a command line tool. All calls MUST be written from there. Currently, there are no plans to implement a GUI.
1. Run 'obtain_token.py' to receive your access token for the Nadeo API  <br>
Enter your UbisoftConnect login information to connecto to your account. If you don't have an account, [click here](https://account.ubisoft.com/en-US) to make one.
2. Run 'get_month_data.py' to receive all TOTDs and their leaderboards for a given month <br>
Entering "0" in the program will obtain tracks for the current month, "1" will obtain tracks from the previous month, etc.
3. Run 'get_medal_distribution.py' to analyze the medal data from Step 2 <br>
The input is the same as it is for Step 2.