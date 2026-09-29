from agent import analyze_incident

incident = """
Our production API is returning 503 errors.
Users are unable to log in.
The problem started after a deployment.
"""

result = analyze_incident(incident)

print("\n==============================")
print("       OPSMIND ANALYSIS")
print("==============================\n")

print(result["analysis"])

print("\n==============================")
print("     HINDSIGHT MEMORIES")
print("==============================\n")

for memory in result["memories"]:
    print("-", memory)