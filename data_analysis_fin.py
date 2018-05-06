# -*- coding: utf-8 -*-
"""
Created on Thu May 03 14:57:05 2018

@author: Dane M4
"""

import pandas as pd
from itertools import combinations
import re
import networkx as nx
from collections import Counter

df = pd.read_csv('top_100_50_years.csv')

lst = [1, 2, 3, 4, 5]
def song_artist_combi(lst):
    colabs = []
    if len(lst) != 1:
        for combo in combinations(lst, 2):  
            colabs.append(combo)
    else:
        return lst
    return colabs


# split on ", " " and " " AND " " & " " featuring " " FEATURING " " x " " X "
def separate_artists(all_artists):
    ret_list = []
    for colab in all_artists:
        colabs = re.split(', | / | with | & | featuring | FEATURING | x | X | feat | feat.',colab)
        ret_list.append(colabs)
    return ret_list

all_artists = df.Arists

artists_separated = separate_artists(all_artists)
#print artists_separated

edges_list = []
for colab in artists_separated:
    edges_list.append(song_artist_combi(colab))
edges_tuples = [item for sublist in edges_list for item in sublist if type(item) == tuple]
#for edge in edges_tuples:
    #print edge

edges_set = set(edges_tuples)

edges = list(edges_set)


nodes_set = set()
for colab in edges:
    for artist in colab:
        nodes_set.add(artist)
nodes = list(nodes_set)

G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

#Returns node with the highest degree in G
def most_collaboritive_artist(Graph):
    winner = ''
    collabs = 0
    for g in Graph:
        if Graph.degree[g] > collabs:
            collabs = Graph.degree[g]
            winner = g
    return winner, collabs

year = []

for y in df['Date']:
    year.append(y[-4:])
    
df['Year'] = year

lil = df[df.Arists.str.contains('LIL\'') == True]

df2 = df[df.Arists.str.contains(', | / | with | & | featuring | FEATURING | x | X | feat | feat.') == True]

df2.sort_values('Date', ascending = False)
df2 = df2.drop_duplicates(['Song'])

year = df2.Year

winner = Counter(year)

print 'The year with the highest number of collabs is ' + str(winner.most_common(1)[0][0]) + ' with ' + str(winner.most_common(1)[0][1])

#Looking for the most collaboritive artist in a year
df3 = df2[df2.Year.str.contains('2017')]

artists_2017 = df3.Arists

separated_2017 = separate_artists(artists_2017)

edges_2017 = []

for colab in separated_2017:
    edges_2017.append(song_artist_combi(colab))
edges_tuples_2017 = [item for sublist in edges_2017 for item in sublist if type(item) == tuple]

edges_set_2017 = set(edges_tuples_2017)

edges_2017 = list(edges_set_2017)

nodes_set_2017 = set()
for colab in edges_2017:
    for artist in colab:
        nodes_set_2017.add(artist)
nodes_2017 = list(nodes_set_2017)

G_2017 = nx.Graph()
G_2017.add_nodes_from(nodes_2017)
G_2017.add_edges_from(edges_2017)

#Returns the average entry, peak, and weeks in the charts for one artist
def mean_artist(artist):
    stats = df2[df2.Arists.str.contains(artist)==True]
    entry = stats.Entry.mean()
    peak = stats.Peak.mean()
    weeks = stats.Weeks.mean()
    return artist + ' -> Entry: ' + str(entry) + ', Peak: ' + str(peak) + ', Weeks: ' + str(weeks) 
    #eturn (entry, peak, weeks)

#Combines two nodes
G = nx.contracted_nodes(G, 'LIL WAYNE', 'LIL\' WAYNE')
G = nx.contracted_nodes(G, 'LIL KIM', 'LIL\' KIM')
#G = nx.contracted_nodes(G, 'LIL SUZY', 'LIL\' SUZY')

#Top 10000 most collaboritive artists 
top= []
for a in sorted(G.degree, key=lambda x: x[1], reverse=True)[:1000]:
    top.append(a[0])

def print_top_100():
    top_100 = top[100:]    
    for a in top_100:
        print(str(top.index(a) + 1) + ': ' +mean_artist(a))

top_cycles = []

for i in range(len(top)):
    top_cycles.append(nx.cycle_basis(G, top[i]))

#Find the largest cycle in a list of cycles
def max_cycle(cycles):
    degree = 0
    winner = []
    for c in cycles:
        if len(c) > degree:
            degree = len(c)
            winner = c
    return winner


#print length, index, name basis of longest cycle in G
def find_longest_cycle():
    win = 0
    
    i = 0
    index = 0
    
    while i < 1000:
        if len(max_cycle(top_cycles[i])) > win:
            win = len(max_cycle(top_cycles[i]))
            index = i
        i += 1
        
    print(win, index, top[index])

#This is the longest cycle, index taken from output    
longest_cycle = max_cycle(top_cycles[684])

print('The longest cycle has ' + str(len(longest_cycle)) + ' nodes and has the root ' + str(top[684]))
print('The most collaboritive artist is ' + str(most_collaboritive_artist(G)[0]) + ' with ' + str(most_collaboritive_artist(G)[1]))
print('The most collaboritive of 2017 is ' + str(most_collaboritive_artist(G_2017)[0]) + ' with ' + str(most_collaboritive_artist(G_2017)[1]))