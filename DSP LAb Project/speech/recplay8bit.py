import pyaudio
import struct
import serial
import math
import numpy as np
from matplotlib import pyplot as plt

plt.ion()
# function to clip the value to unsigned 8-bit range
def clip8(x):
	if x < 0:
		return 0
	elif x > 255:
		return 255
	else:
		return x

# function to convert to 8-bit value
# arr_max is the maximum possible value of original type. eg: for 16 bit = 32767
# arr_min is the minimum possible value of original type. eg: for 16 bit = -32768
def convert8bit(arr, arr_max, arr_min):
    new_arr = np.array(arr, copy=True)
    new_arr.clip(arr_min, arr_max, out=new_arr)
    new_arr -= arr_min
    new_arr //= (arr_max - arr_min + 1)/256
    return new_arr.astype(np.uint8)
	
# initialize serial port to write the audio stream to it with baud rate of 115200
ser = serial.Serial('COM3', 115200)

# no. of frames in a block
BLOCKSIZE = 1024

plt.figure(1)
plt.ylim(0, 255)        # set y-axis limits

plt.xlim(0, BLOCKSIZE)         # set x-axis limits
plt.xlabel('Time (n)')
t = range(0, BLOCKSIZE)
line, = plt.plot([], [], color = 'blue')  # Create empty line
line.set_xdata(t)


# parameters to record audio
WIDTH = 2 		# no. of bytes per sample
CHANNELS = 1 	# no. of channels
RATE = 8000 	# no. of samples per second

# initialize pyaudio and open a stream with above defined parameters
p = pyaudio.PyAudio ()
stream = p.open(format = p.get_format_from_width(WIDTH) ,
				channels = CHANNELS ,
				rate = RATE ,
				input = True ,
				output = False )


#parameters for Amplitude Modulation
gain = 2.0
f0 = 0
theta = 0.0
theta_del = (float(BLOCKSIZE * f0)/RATE - math.floor(BLOCKSIZE * f0/RATE)) * 2.0 * math.pi

output_block = [0 for n in range(0, BLOCKSIZE)]

while True:
	# read 1 block
	input_string = stream.read(BLOCKSIZE)

	# convert the string to binary values using unpack
	input_tuple = struct.unpack('h'*BLOCKSIZE, input_string)

	# can perform any filtering or processing, before convertiing it to 8bit format.
	for n in range(0, BLOCKSIZE):
		# amplitude modulation
		output_block[n] = gain * input_tuple[n] * math.cos(2*math.pi*n*f0/RATE + theta)

	theta = theta + theta_del
	# convert the 16-bit values to 8-bit
	output_tuple_8bit = convert8bit(output_block, 32767, -32768)
	
	# clip the output values to range of 8-bit unsigned numbers
	output_tuple_8bit = [clip8(num) for num in output_tuple_8bit]

	# pack the binary values into a string
	output_string = struct.pack('B'*BLOCKSIZE, *output_tuple_8bit)

	# write the string on the Serial port
	ser.write(output_string)

	line.set_ydata(output_tuple_8bit)
	plt.draw()

pygame.quit()
stream.stop_stream()
stream.close()
p.terminate()
