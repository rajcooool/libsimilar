#!/usr/bin/python3
# -*- coding: utf8 -*-

import itertools
import pandas as pd
import numpy as np
import csv
#from cStringIO import StringIO

np.set_printoptions(threshold=np.inf)

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from sklearn.metrics.pairwise import cosine_similarity

#Name der Datei - muss im gleichen Verzeichnis wie libsimilar.py liegen
filename = 'customer_katkey.csv'

def parse():

	#Schritt 1: Bestimmung der maximalen Spaltenzahl für das Laden der Quelldatei
	#Zwischenschritt: Ersetzen des Leerzeichens zwischen UserID1 ItemID1 durch StringIO
	#Zwischenschritt: Mit del den Speicher freiräumen d.h. das Ergebniss des ersten Einlesens der Datei löschen

	reader1, _ = itertools.tee(csv.reader(StringIO(''.join(l.replace(' ', ',') for l in open(filename)))))
	columns = len(next(reader1))+1
	del reader1

	#Schritt 2: Laden der Datei in einen Pandas Datenframe mit Hilfe der zuvor bestimmten Spaltenzahl
	#Zwischenschritt: Definition von Hilfsvariabel
	#Zwischenschritt: Laden ohne Header, die erste Spalte zum Index machen und für die Spaltenzahl provisorisch eine Laufzahl verwenden

	col_lst_one = [str(x) for x in range(0,columns)]
	col_lst_two = [str(x) for x in range(1,columns)]
	da = pd.read_csv(StringIO(''.join(l.replace(' ', ',') for l in open(filename))),header=None,names=col_lst_one,index_col=0)

	print("\nDataframe da: \n",da)

	#Schritt: Bestimmung der Parameter für das gewünschten Output Format
	#Zwischenschritt: Bestimmung der Anzahl der "einzigartigen" Items
	#Zwischenschritt: Entfernung des NaN Eintrags
	#Zwischenschritt: Generierung eines Index für die Output Matrix
	item_list_dirty = pd.unique(da[col_lst_two].values.ravel())
	item_list_clean = [x for x in item_list_dirty if str(x) != 'nan']
	matrix_index = [str(x) for x in range(0,len(da.index))]

	#print("\nmatrix_index: ",matrix_index)

	#Schritt: Einsortieren aller Ausleihen anhand der Nutzer
	#Zwischenschritt: Generierung eines leeren Pandas Datenframe
	#Zwischenschritt: Loop über eine Loop d.h. über jedes einzelne Medium.
	#Für jedes ausgeliehen Medium wird eine "1" im neuen Dataframe hinterlegt
	#Zwischenschritt: Ersetzen von NaN Einträgen mit 0
	df = pd.DataFrame(columns=sorted(item_list_clean))

	for index, item_id_list_dirty in da.iterrows():
		item_id_list_clean = [x for x in item_id_list_dirty if str(x) != 'nan']
		for item_id in item_id_list_clean:
			df.set_value(index, item_id, 1)

	df = ((df.notnull()).astype('int'))
	df = df.transpose()

	print("\nDataframe df: \n",df)

	return df

def sim_matrix(da):
	#Berechnung des Cosine mit Hilfe der Python Bibliothek
	#sklearn.metrics.pairwise import cosine_similarity
	df = cosine_similarity(da.values)
	return df

def main_func():
	dk = parse()
	matrix = sim_matrix(dk)
	print("\ndk\n",dk)
	print("\ndk Index\n",dk.index.values)
	print("\nMatrix\n",matrix)
	dk[:] = matrix
	dk.columns = dk.index.values
	print("\ndk + matrix\n",dk)

main_func()

#Nicht verwendet - Aber nützlich!
#da = ((da.notnull()).astype('int'))
#da.index.rename('USER IDs', inplace=True)
#db = da.transpose()

