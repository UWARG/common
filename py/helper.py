import TelemMessages

def decode_msg(buf):
	raw_data = buf.getbuffer().tobytes()
	if raw_data[3] == 0x0:
		return TelemMessages.JetsonOdometryData()._decode_one(buf)
	elif raw_data[3] == 0x1:
		return TelemMessages.JetsonMovementRequest()._decode_one(buf)
	elif raw_data[3] == 0x2:
		return TelemMessages.JetsonRelativeMovementCommand()._decode_one(buf)
	elif raw_data[3] == 0x3:
		return TelemMessages.JetsonLandingInitiationCommand()._decode_one(buf)
	elif raw_data[3] == 0x4:
		return TelemMessages.GroundStationWaypoints()._decode_one(buf)
	elif raw_data[3] == 0x5:
		return TelemMessages.GroundStationDisarm()._decode_one(buf)
	elif raw_data[3] == 0x6:
		return TelemMessages.GroundStationPIDValues()._decode_one(buf)
	elif raw_data[3] == 0x7:
		return TelemMessages.GroundStationData()._decode_one(buf)
	elif raw_data[3] == 0x8:
		return TelemMessages.GroundStationPIDSetResponse()._decode_one(buf)
	else:
		return None