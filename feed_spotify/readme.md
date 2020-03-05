This is a quick django app that writes the top 200 songs per country per week into a small mysql db.
The goal is to quickly scrape to different Spotify api's
 - to gather the hits 
 - record advanced audio metrics per Track
 

# To run

- install requirements, as you would
- install mysql db, as you would
- make sure the spotify keys are loaded fine
- python3 manage.py runscripts {}  // order matters
    1) injest_top_charts
    2) injest_spotify_values 
    
# Operational Fixes TODO:
 - Fix oauth
 - get redis or any other k,v store to be the celery broker
 - other small bugs