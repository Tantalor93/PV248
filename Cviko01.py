import re
from collections import Counter

composerRegex = re.compile("^Composer: (.*)$")
centuryRegex = re.compile("^Composition Year: (..)..$")
composerCounter = Counter()
centuryCounter = Counter()
f = open('scorelib.txt', 'r', encoding='utf-8')
for line in f:
    strippedLine = line.strip()
    composerMatch = composerRegex.match(strippedLine)
    centuryMatch = centuryRegex.match(strippedLine)
    if composerMatch is not None:
        composerCounter[composerMatch.group(1)] += 1
    if centuryMatch is not None:
        centuryCounter[centuryMatch.group(1)] += 1

print(composerCounter)
print(centuryCounter)
