from core.brain import RayBrain

print("================================")
print("       RAY BRAIN TEST")
print("================================")

ray = RayBrain()

print()
print("YOU: Hey Ray, how are you?")

answer = ray.ask("Hey Ray, how are you?")

print()
print("RAY:", answer)

print()
print("YOU: What should we work on today?")

answer = ray.ask("What should we work on today?")

print()
print("RAY:", answer)

print()
print("================================")
print("RAY BRAIN TEST COMPLETE")
print("================================")