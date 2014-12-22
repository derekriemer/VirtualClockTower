import pyaudio
import wave
import sys
import time



def openAudio(audio):
	#use the builtin wave file players.
	sound = wave.open(audio, 'rb')
	#return the sound object created, so that we can use it later.
	return sound

def play(sound):
	CHUNK = 1024
	# instantiate PyAudio (1)
	p = pyaudio.PyAudio()
	def callback(in_data, frame_count, time_info, status):
		data = sound.readframes(frame_count)
		return (data, pyaudio.paContinue)
	
	# open stream using callback (3)
	stream = p.open(format=p.get_format_from_width(sound.getsampwidth()),
					channels=sound.getnchannels(),
					rate=sound.getframerate(),
					output=True,
					stream_callback=callback)
	
	# start the stream (4)
	stream.start_stream()
	
	# wait for stream to finish (5)
	while stream.is_active():
		time.sleep(0.1)
	
	# stop stream (6)
	stream.stop_stream()
	stream.close()
	# close PyAudio (7)
	p.terminate()
	sound.rewind()
	
	
def main():
	prev_min=time.localtime().tm_min
	prev_hour=time.localtime().tm_hour
	while True:
		files=[]
		local_time=time.localtime()
		hour=local_time.tm_hour
		min = local_time.tm_min
		if hour < 8 or hour >= 22:
			time.sleep(5)
			continue
		if min == prev_min:
			time.sleep(1)
			continue
		if min==0:
			files=["15","30","45","0"]
		elif min==15:
			files=['15']
		elif min==30:
			files=['15','30']
		elif min==45:
			files=['15','30','45']
		for name in files:
			d=openAudio(name+".wav")
			play(d)                                                                      
			d.close()
		if (hour != prev_hour) and min == 0:
			audio=openAudio("bell.wav")
			if hour==0:
				d=12
			elif hour< 12:
				d=hour
			else:
				d = hour-12
			for r in range(d):
				play(audio)
			audio.close()
		prev_min=min
		prev_hour=hour
		time.sleep(1)


main()