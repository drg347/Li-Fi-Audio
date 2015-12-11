# pygame_demo_01.py

import pygame
import serial

pygame.init()  # Initializes pygame

pge = pygame.event.get()
ser = serial.Serial('COM3', 9600)

note_freq_map = {'C1': 33,
				'CS1': 35,
				'D1': 37,
				'DS1': 39,
				'E1': 41,
				'F1': 44,
				'FS1': 46,
				'G1': 49,
				'GS1': 52,
				'A1': 55,
				'AS1': 58,
				'B1': 62,
				'C2': 65,
				'CS2': 69,
				'D2': 73,
				'DS2': 78,
				'E2': 82,
				'F2': 87,
				'0': 0}

key_note_map = {pygame.K_q: 'C1',
				pygame.K_2: 'CS1',
				pygame.K_w: 'D1',
				pygame.K_3: 'DS1',
				pygame.K_e: 'E1',
				pygame.K_r: 'F1',
				pygame.K_5: 'FS1',
				pygame.K_t: 'G1',
				pygame.K_6: 'GS1',
				pygame.K_y: 'A1',
				pygame.K_7: 'AS1',
				pygame.K_u: 'B1',
				pygame.K_i: 'C2',
				pygame.K_9: 'CS2',
				pygame.K_o: 'D2',
				pygame.K_0: 'DS2',
				pygame.K_p: 'E2',
				pygame.K_LEFTBRACKET: 'F2'
				}

print 'Press k to exit (exit on un-press)'

stop = False
note = 'A1'
freq = 0
while stop == False:

	pge = pygame.event.get()

	for event in pge:
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_k:
				stop = True
				break
			try:
				note = key_note_map[event.key]
			except KeyError as k:
				note = '0'
			try: 
				freq = note_freq_map[note]
			except KeyError as k:
				freq = 0
			# Check if 'q' key was pressed
			

		if event.type == pygame.KEYUP:
			ser.write(str(freq))

print 'stop = ', stop

pygame.quit()

print 'end of program'

