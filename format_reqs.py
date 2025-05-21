# Constant for URLs
NANDO_LIVE = "https://live-services.trackmania.nadeo.live/api/token"
#"https://live-services.trackmania.nadeo.live/api/token/"
#"leaderboard/group/map?scores[gjt2DWATrQ_NdrbrXG0G9oDpTfh]=15800&scores[XiGZvMOqIgT3_g0TdeFa0lxMp46]=17500"


# Obtains URL of TOTDs in the current month
#   offset --> The month we're searching for, relative to the current month
def get_tl_url(offset: int):
	return NANDO_LIVE + "/campaign/month?length=1&offset=" + str(offset)


# Obtains URL for the leaderboard of the current track
#   groupId --> The leaderboard session from when the track was TOTD
#   mapUid ---> The unique ID of the current track
#   offset ---> The position in the leaderboards we are starting from
def get_lb_url(groupId: str, mapUid: str, offset: int):
	group_url = "group/" + groupId + "/"
	map_url = "map/" + mapUid + "/"
	position_url = "top?length=100&onlyWorld=true&offset=" + str(offset)
	return NANDO_LIVE + "/leaderboard/" + group_url + map_url + position_url


# Obtains URL for the current track
#   mapUid ---> The unique ID of the current track
def get_map_url(mapUid: str):
	return NANDO_LIVE + "/map/" + mapUid