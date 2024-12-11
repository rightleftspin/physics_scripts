

f = open("./pyrochlore_nn.txt", 'r')

clusters = map(lambda x: x.strip().split(":"), f.readlines())

new_clusters = []
for cluster in clusters:
    temp = list(map(lambda x: int(x), cluster[1].split()))
    for i in `






