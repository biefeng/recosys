#!usr/bin/env python
# -*- coding: utf-8 -*-
# fileName: k_means_clustering.py
# time: 2019/12/29 02:33

__author__ = '33504'

import math
import random
from functools import reduce
import pandas as pd
import matplotlib as plt
import seaborn as sns;

sns.set(color_codes=True)


def generate_centroids(k, data):
	return random.sample(data, k)


def distance(x, y):
	dist = 0
	for i in range(len(x)):
		dist += math.pow((x[i] - y[i]), 2)
	return math.sqrt(dist)


def add_to_cluester(item, centroids):
	return item, min(range(len(centroids)), key=lambda i: distance(item, centroids[i]))


def move_centosids(k, kim):
	centroids = []
	for cen in range(k):
		members = [i[0] for i in kim if i[1] == cen]
		if members:
			centroid = [i / len(members) for i in reduce(add_vector, members)]
			centroids.append(centroid)
	return centroids


def add_vector(i, j):
	return [i[k] + j[k] for k in range(len(j))]


def draw_iteration(centroids, iteration):
	centroids_points = pd.DataFrame([[centroids[i][0],
	                                  centroids[i][1],
	                                  i] for i in range(len(centroids))],
	                                columns=['pets', 'star_wars', 'cluster'])
	centroids_points["cluster"] = ["{} centroid".format(i)
	                               for i in range(len(centroids))]
	ds = pd.DataFrame(columns=['pets', 'star_wars', 'cluster'],
	                  data=[[i[0][0], i[0][1], i[1]] for i in iteration])
	full_ds = pd.concat([ds, centroids_points], ignore_index=True)

	g = sns.FacetGrid(data=full_ds, size=5,
	                  hue="cluster",
	                  hue_order=[0, 1, 2, "0 centroid", "1 centroid", "2 centroid"],
	                  palette=["b", "r", "g", "b", "r", "g"],
	                  hue_kws={"s": [20, 20, 20, 500, 500, 500],
	                           "marker": ["o", "o", "o", "+", "+", "+"]})
	g.map(plt.scatter, 'pets', 'star_wars', linewidth=1, edgecolor="w")
	g.add_legend()


def k_means(k, data):
	best_weight = math.inf
	centroids = generate_centroids(k, data)
	while True:
		iteration = list([add_to_cluester(item, centroids) for item in data])
		new_weight = 0
		for i in iteration:
			new_weight += distance(i[0], centroids[i[1]])

		if new_weight < best_weight:
			best_weight = new_weight
		else:
			return iteration
		centroids = move_centosids(k, iteration)
