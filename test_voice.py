import pyttsx3

print("Starting RAY's voice...")

engine = pyttsx3.init()

# Speech speed
engine.setProperty("rate", 165)

# Volume
engine.setProperty("volume", 1.0)

print("RAY will speak now...")

engine.say("Hey Flame! This is Ray. I can hear you, and now I can speak to you too.")

engine.runAndWait()

print("RAY finished speaking.")