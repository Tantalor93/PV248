import json
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, LabelSet
from numpy import pi

def createPartyShort(party):
    if "short" in party:
        name = party["short"]
    else:
        output = ""
        for i in party["name"].split():
            output += i[0]
        name = output
    return name


input = json.load(open("election.json", encoding='UTF-8'))

others = {"votes": 0, "parties": list(), "short": "ostatní", "name": "ostatní", "share": 0}

parties = list()

for party in input:
    if party["share"] < 1:
        others["votes"] += party["votes"]
        name = createPartyShort(party)
        others["parties"].append(name)
        others["share"] += party["share"]
    else:
        parties.append(party)

parties.append(others)

votes = list()
names = list()
colors = list()
for party in parties:
    votes.append(party["votes"])
    if "short" in party:
        names.append(party["short"])
    else:
        name = createPartyShort(party)
        names.append(name)
    if "color" in party:
        colors.append(party["color"])
    else:
        colors.append("grey")

## bar chart
src = ColumnDataSource(dict(x=list(range(0, len(parties))), y=votes, labels=names, color=colors))

p = figure()
labels = LabelSet(x='x', y='y', text='labels', level='glyph',
                  x_offset=-13.5, y_offset=0, source=src, render_mode='canvas')
p.vbar(source=src, x='x', top='y', bottom=0, width=0.7, color='color', legend='labels')
p.add_layout(labels)

## pie chart

p2 = figure(x_range=(-1, 1), y_range=(-1, 1))
percents = list()
j = 0
for i in parties:
    if j == 0:
        percents.append((i["share"]) / 100)
    else:
        percents.append(i["share"] / 100 + percents[j - 1])
    j = j + 1

percents.insert(0, 0)

starts = [p * 2 * pi for p in percents[:-1]]
ends = [p * 2 * pi for p in percents[1:]]

src2 = ColumnDataSource(dict(x=list(range(0, len(parties))), y=votes, labels=names, color=colors, starts=starts, ends=ends))

p2.wedge(x=0, y=0, radius=1, start_angle='starts', end_angle='ends', color='color', source=src2, legend='labels')

show(p2)
show(p)
