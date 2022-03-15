from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


from kivy.uix.screenmanager import ScreenManager, Screen

import pickle
from kivymd.uix.dialog import MDDialog

from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem

from kivy.properties import ListProperty, NumericProperty
from kivy.utils import get_color_from_hex

from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout

from kivy.core.window import Window

from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.floatlayout import MDFloatLayout

from kivymd.uix.list import MDList
import os

from kivy.uix.spinner import Spinner, SpinnerOption

from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine, MDExpansionPanelThreeLine
from kivy.factory import Factory
Factory.register('HoverBehavior', HoverBehavior)
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dropdownitem import MDDropDownItem
from kivy.uix.dropdown import DropDown
#from kivymd.uix.picker import MDDatePicker
from kivymd.uix.datatables import MDDataTable
from kivy.app import App
import re
import datetime
from datetime import date
#MagicBehavior
from kivymd.uix.behaviors import MagicBehavior
from kivymd.uix.pickers import MDTimePicker, MDDatePicker
from kivymd.uix.spinner import MDSpinner
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.toast import toast
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
#from kivymd_extensions.filemanager import FileManager
from kivy_gradient import Gradient
from kivy_garden.graph import Graph, LinePlot
import numpy as np
from kivy.uix.boxlayout import BoxLayout
import matplotlib.pyplot as plt
from functools import partial
from kivy.core.text import Label as CoreLabel
from kivymd.uix.tooltip import MDTooltip

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt


#////////////////////////////////////////////////////////////////////////////
# FUNÇÕES PARA USO EM MAIS DE UMA SCREEN
def changeTime(label):
	return label.split(':')[0] + 'h' + label.split(':')[1] + 'min'
def changeData(label):
	text = label.split('-')
	separator = '/'
	return separator.join([text[2], text[1], text[0]])
def SearchByData(lista, string):
	step18 = []
	for i in range(len(lista)):
		step18.append([])

	for y in range(len(step18)):
		for x in range(len(lista[y])):
			step18[y].append(lista[y][x])

	step19 = []

	for w in range(len(step18)):
		if step18[w][0] == str(string):
			step19.append(step18[w])

	for w in range(len(step19)):
		step19[w] = tuple(step19[w])

	return step19
def sortData(lista):
	step1 = []

	# JUNTAR HORÁRIO COM DATA E ORGANIZAR NOVAMENTE OS DADOS
	for items in range(len(lista)):
		step1.append([])

	for index in range(len(step1)):
		step1[index].append(lista[index][0] + ' ' + lista[index][1])

		for x in range(2, len(lista[0])):
			step1[index].append(lista[index][x])

	# CONVERTER PARA TUPLAR [[]] -> [()]
	for valor in range(len(step1)):
		step1[valor] = tuple(step1[valor])

	# ORGANIZAR DE ACORDO COM A DATA
	from datetime import datetime
	sorted_list = sorted(step1, key=lambda t: datetime.strptime(t[0], '%Y-%m-%d %H:%M:%S'))

	step2 = []
	for i in range(len(sorted_list)):
		step2.append([])

	for y in range(len(step2)):
		# DESAGRUPAR A DATA DO HORÁRIO E REFAZER OS ITEMS
		for slices in range(len(sorted_list[y][0].split())):
			step2[y].append(sorted_list[y][0].split()[slices])

		for z in range(1, len(sorted_list[0])):
			step2[y].append(sorted_list[y][z])

	for x in range(len(step2)):
		step2[x][9] = calcularTaxaAcerto(int(step2[x][7]), int(step2[x][8]))

	# CONVERTER PARA TUPLAR [[]] -> [()]
	for w in range(len(step2)):
		step2[w] = tuple(step2[w])

	return step2
def organizerData(lista):
	# Coloca o padrão de horas em 00h00min e coloca padrão nas datas em day/month/year

	step3 = []
	for i in range(len(lista)):
		step3.append([])

	# CONVERTER TUPLA PARA LISTA [()] - > [[]]
	for y in range(len(step3)):
		for x in range(len(lista[y])):
			step3[y].append(lista[y][x])

	def changeTime(label):
		return label.split(':')[0] + 'h' + label.split(':')[1] + 'min'

	def changeData(label):
		text = label.split('-')
		separator = '/'
		return separator.join([text[2], text[1], text[0]])

	# APLICAR AS FUNÇÕES PARA AS HORAS E DATAS
	for w in range(len(step3)):
		step3[w][0] = changeData(step3[w][0])
		step3[w][1] = changeTime(step3[w][1])
		step3[w][5] = changeTime(step3[w][5])

	# CONVERTER PARA TUPLAR [[]] -> [()]
	for j in range(len(step3)):
		step3[j] = tuple(step3[j])

	return step3
def encontrarNumeroPagina(data, name_to_search, size):
	# data_cronograma = pickle.load((open("data_timeline.p", "rb")))
	data = CronogramaTableStyle(organizerData(sortData(data)))
	print('data: ', data)
	# SEPARAR EM 5 ELEMENTOS POR LISTA
	list_separator = list()
	for i in range(0, len(data), size):
		list_separator.append(data[i:i + size])

	# SEPARAR EM PÁGINA DICT[X] COM VALORES CONTENDO OS ITEMS DA PÁGINA X
	dict_order = {}
	for x in range(len(list_separator)):
		dict_order[x + 1] = list_separator[x]

	# PROCURAR O ELEMENTO DESEJADO (NAME_TO_SEARCH) EM DICT_ORDER E RETORNAR A PÁGINA QUE SE ENCONTRA (X)
	for num_page in range(1, len(dict_order.keys()) + 1):
		for index in range(len(dict_order[num_page])):
			if dict_order[num_page][index] == name_to_search:
				return int(num_page)
#////////////////////////////////////////////////////////////////////////////

def onlyToday(lista):
  from datetime import date
  today = date.today()

  todayList = []

  for x in range(len(lista)):
    if lista[x][0] == str(today):
      todayList.append(lista[x])

  return todayList

def timeInterval(lista, dt):
  time_now = str(datetime.datetime.now().strftime("%H:%M:%S"))

  time_interval = ['','','']

  time_interval[0] = (datetime.datetime.now() - datetime.timedelta(minutes=dt)).strftime("%H:%M:%S")
  time_interval[1] = time_now
  time_interval[2] = (datetime.datetime.now() + datetime.timedelta(minutes=dt)).strftime("%H:%M:%S")

  data_in_interval = []
  data_not_in_interval = []


  for x in range(len(lista)):
    # ESTÁ NO INTERVALO DE [t+dt, t-dt]
    if lista[x][1] in time_interval:
      data_in_interval.append(lista[x])

    # NÃO ESTÁ NO INTERVALO DE [t+dt, t-dt]
    if lista[x][1] not in time_interval:
      data_not_in_interval.append(lista[x])

  try:
    if len(data_in_interval) > 0:
      return data_in_interval[0]

    if len(data_in_interval) == 0:
      return data_not_in_interval[0]

  except IndexError:
    return []


def today_only(lista):
	from datetime import date
	today = str(date.today())

	def changeData(label):
		text = label.split('-')
		separator = '/'
		return separator.join([text[2], text[1], text[0]])

	today = changeData(today)

	step8 = []
	step9 = []

	for i in range(len(lista)):
		step8.append([])

	# CONVERTER TUPLA PARA LISTA [()] - > [[]]
	for y in range(len(step8)):
		for x in range(len(lista[y])):
			step8[y].append(lista[y][x])

	# VERIFICAR SE O DIA É MAIOR OU IGUAL AO DIA ATUAL
	for h in range(len(step8)):

		# VERIFICAR SE O MêS QUE ESTAMOS É MAIOR QUE OU IGUAL O MÊS DOS DADOS
		if str(step8[h][0][15:17]) == today[0:2] and str(step8[h][0][18:20]) == today[3:5] and str(step8[h][0][21:25]) == today[6:10]:
			step9.append(step8[h])

		# MÊS MENOR DO QUE O MÊS QUE ESTAMOS
		if str(step8[h][0][18:20]) < today:
			pass

	# CONVERTER PARA TUPLAR [[]] -> [()]
	for j in range(len(step9)):
		step9[j] = tuple(step9[j])

	return step9

def changeStatusColor(lista_tuple, color_hex='686fa3'):
    step5 = []
    for i in range(len(lista_tuple)):
        step5.append([])

    # CONVERTER TUPLA PARA LISTA [()] - > [[]]
    for y in range(len(step5)):
    	step5[y].append(lista_tuple[y])

    if step5[2][0] == 'Não Estudado':
	    step5[1][0] = [1,0,0,1]
	    step5[0] = step5[0][0]
	    step5[1] = step5[1][0]
	    step5[2] = '[color=#{}]'.format(color_hex) + step5[2][0] + '[/color]'

    if step5[2][0] == 'Estudado':
        step5[1][0] = [39 / 256, 174 / 256, 96 / 256, 1]
        step5[0] = step5[0][0]
        step5[1] = step5[1][0]
        step5[2] = '[color=#{}]'.format(color_hex) + step5[2][0] + '[/color]'

    step5 = tuple(step5)

    return step5

def colorData(lista, color_hex='686fa3'):
	step4 = []
	for i in range(len(lista)):
		step4.append([])

	# CONVERTER TUPLA PARA LISTA [()] - > [[]]
	for y in range(len(step4)):
		for x in range(len(lista[y])):
			step4[y].append(lista[y][x])

	# APLICAR AS FUNÇÕES PARA AS HORAS E DATAS
	for w in range(len(step4)):
		step4[w][0] = '[color=#{}]'.format(color_hex) + step4[w][0] + '[/color]'
		step4[w][1] = '[color=#{}]'.format(color_hex) + step4[w][1] + '[/color]'
		step4[w][2] = '[color=#{}]'.format(color_hex) + step4[w][2] + '[/color]'
		step4[w][3] = '[color=#{}]'.format(color_hex) + step4[w][3] + '[/color]'
		step4[w][4] = '[color=#{}]'.format(color_hex) + step4[w][4] + '[/color]'
		step4[w][5] = '[color=#{}]'.format(color_hex) + step4[w][5] + '[/color]'
		#step4[w][7] = '[color=#{}]'.format(color_hex) + step4[w][7] + '[/color]'
		#step4[w][8] = '[color=#{}]'.format(color_hex) + step4[w][8] + '[/color]'
		#step4[w][9] = '[color=#{}]'.format(color_hex) + step4[w][9] + '[/color]'
		step4[w][6] = changeStatusColor(step4[w][6])


	# CONVERTER PARA TUPLAR [[]] -> [()]
	for j in range(len(step4)):
		step4[j] = tuple(step4[j])

	return step4

def createEmptyRowRemoveCronograma(lista):
	step10 = []
	for i in range(len(lista) + 1):
		step10.append([])

	# CONVERTER TUPLA PARA LISTA [()] - > [[]]
	for y in range(len(step10) - 1):
		for x in range(len(lista[y])):
			step10[y].append(lista[y][x])

	step10[len(lista)] = [' ', ' ', ' ', ' ', ' ', ' ', ' ']

	# CONVERTER PARA TUPLAR [[]] -> [()]
	for j in range(len(step10)):
		step10[j] = tuple(step10[j])

	return step10

def SearchBar(lista, string):
	def SearchByName(lista, string):
			step16 = []
			for i in range(len(lista)):
				step16.append([])

			# CONVERTER TUPLA PARA LISTA [()] - > [[]]
			for y in range(len(step16)):
				for x in range(len(lista[y])):
					step16[y].append(lista[y][x])

			step17 = []

			# VERIFICAR SE A MATÉRIA É IGUAL AO NOME DA LISTA
			for w in range(len(step16)):
				if step16[w][3] == str(string):
					step17.append(step16[w])

			# CONVERTER PARA TUPLAR [[]] -> [()]
			for w in range(len(step17)):
				step17[w] = tuple(step17[w])

			return step17

	def SearchByData(lista, string):
			step18 = []
			for i in range(len(lista)):
				step18.append([])

			# CONVERTER TUPLA PARA LISTA [()] - > [[]]
			for y in range(len(step18)):
				for x in range(len(lista[y])):
					step18[y].append(lista[y][x])

			step19 = []

			# VERIFICAR SE A DATA É IGUAL A DATA DA LISTA
			for w in range(len(step18)):
				if step18[w][0] == str(string):
					step19.append(step18[w])

			# CONVERTER PARA TUPLAR [[]] -> [()]
			for w in range(len(step19)):
				step19[w] = tuple(step19[w])

			return step19

	def SearchByTime(lista, string):
			step20 = []
			for i in range(len(lista)):
				step20.append([])

			# CONVERTER TUPLA PARA LISTA [()] - > [[]]
			for y in range(len(step20)):
				for x in range(len(lista[y])):
					step20[y].append(lista[y][x])

			step21 = []

			# VERIFICAR SE O TEMPO É IGUAL AO TEMPO DA LISTA
			for w in range(len(step20)):
				if step20[w][1] == str(string):
					step21.append(step20[w])

			# CONVERTER PARA TUPLAR [[]] -> [()]
			for w in range(len(step21)):
				step21[w] = tuple(step21[w])

			return step21

	def SearchByCategoria(lista, string):
			step21 = []
			for i in range(len(lista)):
				step21.append([])

			# CONVERTER TUPLA PARA LISTA [()] - > [[]]
			for y in range(len(step21)):
				for x in range(len(lista[y])):
					step21[y].append(lista[y][x])

			step22 = []

			# VERIFICAR SE O TEMPO É IGUAL AO TEMPO DA LISTA
			for w in range(len(step21)):
				if step21[w][2] == str(string):
					step22.append(step21[w])

			# CONVERTER PARA TUPLAR [[]] -> [()]
			for w in range(len(step22)):
				step22[w] = tuple(step22[w])

			return step22

	nome = ' '.join(string.split()).lower().title()

	data_cronograma = pickle.load((open("data_timeline.p", "rb")))


	materias = pickle.load((open("data_subjects_topics.p", "rb")))
	materias = list(materias.keys())

	categorias = ['Teoria', 'Exercicios']

	# DataByName = colorData(SearchByName(organizerData(sortData(data_cronograma)), str(nome)))
	DataSearched = []


	# NOME PESQUISADO É UMA MATÉRIA
	if nome in materias:
		DataSearched = colorData(
			SearchByName(organizerData(sortData(lista)), str(nome)))

	# NOME PESQUISADO É UMA CATEGORIA
	if nome in categorias:
		DataSearched = colorData(
			SearchByCategoria(organizerData(sortData(lista)), str(nome)))

	# NOME PESQUISADO É UMA DATA
	if len(DataSearched) == 0:
		DataSearched = colorData(
				SearchByData(organizerData(sortData(lista)), str(string)))

	# NOME PESQUISADO É UM HORÁRIO
	if len(DataSearched) == 0:
		DataSearched = colorData(
					SearchByTime(organizerData(sortData(lista)), str(string)))

	#if string == '' or string == ' ':
		#DataSearched = colorData(organizerData(sortData(data_cronograma)))

	return DataSearched

def separadorDicionario():
  data_cronograma = pickle.load((open("data_timeline.p", "rb")))
  data_in_list_style = []
  new_format = []

  estudados = []
  nao_estudados = []

  for y in range(len(data_cronograma)):
    data_in_list_style.append([])
    new_format.append([])
    for x in range(len(data_cronograma[y])):
      if x == 6:
        data_in_list_style[y].append(list(data_cronograma[y][x]))
      else:
        data_in_list_style[y].append(data_cronograma[y][x])

  datas_label = []
  data_in_dict = {}

  for x in range(len(data_in_list_style)):
    new_format[x].append(data_in_list_style[x][0])
    new_format[x].append(data_in_list_style[x][6][2])

  for w in range(len(new_format)):
    if new_format[w][0] not in datas_label:
      datas_label.append(new_format[w][0])

  for x in range(len(datas_label)):
    data_in_dict[datas_label[x]] = []

  for index in range(len(new_format)):
    data_in_dict[new_format[index][0]].append(new_format[index][1])

  return data_in_dict

def porcentagem(item1, item2, lista, answer):
	total = len(lista)
	item_1 = lista.count(item1)
	item_2 = lista.count(item2)

	item_1_porcentagem = round(item_1 / total, 2)*100
	item_2_porcentagem = round(item_2 / total, 2)*100

	if answer == 1:
		return item_1_porcentagem
	if answer == 2:
		return item_2_porcentagem

def plotEstudados_Bar(state):
	data_cronograma = pickle.load((open("data_timeline.p", "rb")))
	data_in_list_style = []
	estudados = []
	nao_estudados = []

	for y in range(len(data_cronograma)):
		data_in_list_style.append([])
		for x in range(len(data_cronograma[y])):
			if x == 6:
				data_in_list_style[y].append(list(data_cronograma[y][x]))
			else:
				data_in_list_style[y].append(data_cronograma[y][x])

	# ADICIONAR ESTUDADOS EM ESTUDADOS E NÃO ESTUDADOS EM NÃO_ESTUDADOS
	for x in range(len(data_in_list_style)):
		if data_in_list_style[x][6][2] == 'Estudado':
			estudados.append(data_in_list_style[x])
		if data_in_list_style[x][6][2] == 'Não Estudado':
			nao_estudados.append(data_in_list_style[x])

	plot_estudados = []
	plot_nao_estudados = []

	plot_estudados_count = {}
	plot_nao_estudados_count = {}

	total = {}

	# GUARDAR SÓ AS DATAS PARA ESTUDADOS E NAO ESTUDADOS
	for index in range(len(estudados)):
		plot_estudados.append(estudados[index][0])

	for index in range(len(nao_estudados)):
		plot_nao_estudados.append(nao_estudados[index][0])

	# ORGANIZAR AS QUANTIDADES E AS DATAS PARA ESTUDADOS/ NÃO ESTUDADOS E TOTAL (PARA USO DO CALCULO PERCENTUAL)
	for count in range(len(plot_estudados)):
		plot_estudados_count[plot_estudados[count]] = plot_estudados.count(plot_estudados[count])

	for count in range(len(plot_nao_estudados)):
		plot_nao_estudados_count[plot_nao_estudados[count]] = plot_nao_estudados.count(plot_nao_estudados[count])

	if state == True:
		return plot_estudados_count

	if state == False:
		return plot_nao_estudados_count

#////////////////////////////////////////////////////////////////////////////
# FUNÇÕES DA CRONOGRAMA
def onlyTimeGreater(lista):
	today = date.today()
	time_now = str(datetime.datetime.now().strftime("%H:%M:%S"))
	to_do = []
	if len(lista) == 0:
		pass

	else:
		# REMOVER ITEM COM HÓRARIO MENOR QUE O HORÁRIO ATUAL
		for x in range(len(lista)):
			if lista[x][0] == str(today):
				if lista[x][1] >= str(time_now):
					to_do.append(lista[x])

			if lista[x][0] > str(today):
				to_do.append(lista[x])



			if str(lista[x][1]) < str(time_now):
				pass



	return to_do
def eliminar_EscolhasRepetidas(lista):
	duplicates = []

	def list_diff(a, b):
		return [x for x in a if x not in b]

	if len(lista) == 0:
		return []

	# APENAS UMA ÚNICA OPÇÃO
	if len(lista) == 1:
		return lista

	# MAIS DE UMA OPÇÃO PARA O INTERVALO ESCOLHIDO
	if len(lista) > 1:

		# CHECAR SE HÁ ITENS REPETIDOS E ADICIONAR A DUPLICATES
		for y in lista:
			if lista.count(y) > 1 and y not in duplicates:
				duplicates.append(y)

		# ENCONTRAR A DIFERENÇA ENTRE DUPLICATES E LISTA
		data = list_diff(lista, duplicates)

		# ADICIONAR OS ELEMENTOS REPETIDOS UMA UNICA VEZ EM DATA_DIFF
		for w in range(len(data)):
			data.append(data[w])

		# ELEMENTOS REPETIDOS APAGADOS
		return data
def estudados(data):
	dias = list(data.keys())
	for i in range(len(dias)):
		data[dias[i]] = porcentagem('Estudado', 'Não Estudado', data[dias[i]], 1)

	return data
def nao_estudados(data):
	dias = list(data.keys())
	for i in range(len(dias)):
		data[dias[i]] = porcentagem('Estudado', 'Não Estudado', data[dias[i]], 2)

	return data
def CronogramaTableStyle(lista):
	step7 = []
	for i in range(len(lista)):
		step7.append([])

	# CONVERTER TUPLA PARA LISTA [()] - > [[]]
	for y in range(len(step7)):
		for x in range(len(lista[y])):
			step7[y].append(lista[y][x])

	# TIRAR A COLUNA DE DURAÇÃO, ACERTOS, ERROS, RENDIMENTO

	for x in range(len(step7)):
		step7[x].remove(step7[x][-1])

	for x in range(len(step7)):
		step7[x].remove(step7[x][-1])

	for x in range(len(step7)):
		step7[x].remove(step7[x][-1])

	for x in range(len(step7)):
		step7[x].remove(step7[x][-2])

	# CONVERTER PARA TUPLAR [[]] -> [()]
	for j in range(len(step7)):
		step7[j] = tuple(step7[j])

	return step7
def createEmptyRow(lista):
	step6 = []
	for i in range(len(lista) + 1):
		step6.append([])

	# CONVERTER TUPLA PARA LISTA [()] - > [[]]
	for y in range(len(step6) - 1):
		for x in range(len(lista[y])):
			step6[y].append(lista[y][x])

	step6[len(lista)] = [' ', ' ', ' ', ' ', ' ', ' ']

	# CONVERTER PARA TUPLAR [[]] -> [()]
	for j in range(len(step6)):
		step6[j] = tuple(step6[j])

	return step6
def AutoSizeTableRowsNum_Cronograma(lista, rows_per_page):
	lista = CronogramaTableStyle(colorData(organizerData(sortData(lista))))

	if len(lista) == 0:
		return createEmptyRow(createEmptyRow(lista))

	if len(lista) == 1:
		return createEmptyRow(lista)

	if len(lista) > 1:
		def sequence(rows_per_page, data):
			a = {}
			a[0] = rows_per_page
			for i in list(range(1, len(data))):
				a[i] = a[i - 1] + 5
			return list(a.values())

		divisores = sequence(rows_per_page, lista)
		if len(lista) in divisores:
			return createEmptyRow(lista)
		else:
			return lista

#////////////////////////////////////////////////////////////////////////////
# FUNÇÕES DA PAGINA EXERCICIOS
def AutoSizeTableRowsNum_Exercicios(lista, rows_per_page):
	lista = ExerciciosTableStyle(colorDataExercicios(organizerData(sortData(lista))))
	if len(lista) == 0:
		return createEmptyRowExercicios(createEmptyRowExercicios(lista))

	if len(lista) == 1:
		return createEmptyRowExercicios(lista)

	if len(lista) > 1:
		def sequence(rows_per_page, data):
			a = {}
			a[0] = rows_per_page
			for i in list(range(1, len(data))):
				a[i] = a[i - 1] + 5
				return list(a.values())

		divisores = sequence(rows_per_page, lista)
		if len(lista) in divisores:
			return createEmptyRowExercicios(lista)
		else:
			return lista
def findBestRendimento(full_datetime, state):
	data_cronograma = pickle.load((open("data_timeline.p", "rb")))
	DataSearched_today = SearchByData(data_cronograma, str(full_datetime))

	def splitPercent(string):
		return str(string.split()[0])

	data_in_list = []
	data_only_exercicios = []
	rendimentos = []

	for x in range(len(DataSearched_today)):
		data_in_list.append([])

	for y in range(len(data_in_list)):
		for x in range(len(DataSearched_today[y])):
			data_in_list[y].append(DataSearched_today[y][x])

	for exercicios in range(len(data_in_list)):
		if data_in_list[exercicios][2] == 'Exercicios':
			data_only_exercicios.append(data_in_list[exercicios])
			rendimentos.append(splitPercent(data_in_list[exercicios][9]))

	for x in range(len(rendimentos)):
		rendimentos[x] = float(rendimentos[x])

	min_rendimento = rendimentos.index(min(rendimentos))
	max_rendimento = rendimentos.index(max(rendimentos))

	min_rendimento_info = []
	min_rendimento_info.append(data_in_list[min_rendimento][9])
	min_rendimento_info.append(data_in_list[min_rendimento][3])
	min_rendimento_info.append(data_in_list[min_rendimento][4])

	max_rendimento_info = []
	max_rendimento_info.append(data_in_list[max_rendimento][9])
	max_rendimento_info.append(data_in_list[max_rendimento][3])
	max_rendimento_info.append(data_in_list[max_rendimento][4])

	if state == False:
		return min_rendimento_info

	if state == True:
		return max_rendimento_info
def ExerciciosTableStyle(lista):
	step7 = []
	exercicios_only = []

	for i in range(len(lista)):
		step7.append([])

	# CONVERTER TUPLA PARA LISTA [()] - > [[]]
	for y in range(len(step7)):
		for x in range(len(lista[y])):
			step7[y].append(lista[y][x])

	# TIRAR A COLUNA DE DURAÇÃO,Status
	for x in range(len(step7)):
		step7[x].remove(step7[x][5])

	for x in range(len(step7)):
		step7[x].remove(step7[x][5])

	for i in range(len(step7)):
		if step7[i][2][15:25] == 'Exercicios':
			exercicios_only.append(step7[i])

	# CONVERTER PARA TUPLAR [[]] -> [()]
	for j in range(len(exercicios_only)):
		exercicios_only[j] = tuple(exercicios_only[j])

	return exercicios_only
def createEmptyRowExercicios(lista):
	step6 = []
	for i in range(len(lista) + 1):
		step6.append([])

	# CONVERTER TUPLA PARA LISTA [()] - > [[]]
	for y in range(len(step6) - 1):
		for x in range(len(lista[y])):
			step6[y].append(lista[y][x])

	step6[len(lista)] = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

	# CONVERTER PARA TUPLAR [[]] -> [()]
	for j in range(len(step6)):
		step6[j] = tuple(step6[j])

	return step6
def graph_bar_acertos_erros_functionFinder(data, day):
	DataSearched = SearchByData(data, str(day))
	exercicios_only = []
	acertos_and_erros = {'acertos': [], 'erros': []}
	for y in range(len(DataSearched)):
		if DataSearched[y][2] == 'Exercicios':
			exercicios_only.append(DataSearched[y])

	for erros in range(len(exercicios_only)):
		acertos_and_erros['acertos'].append(int(exercicios_only[erros][7]))
		acertos_and_erros['erros'].append(int(exercicios_only[erros][8]))

	result_to_plot = {"Acertos": sum(acertos_and_erros['acertos']), "Erros": sum(acertos_and_erros['erros'])}

	return result_to_plot
def graph_bar_acertos_erros_functionPloter(self, data, day, page_zero):
	estudados = graph_bar_acertos_erros_functionFinder(data, str(day))

	fig2, ax2 = plt.subplots(nrows=1, ncols=1, figsize=(
	int(self.ids.acertos_erros_bar_plot.size[0] / 3), int(self.ids.acertos_erros_bar_plot.size[1] / 3)))
	# DEFINIR IMAGEM E COR TRANSPARENTE PARA AS MARGENS DO GRÁFICO
	fig2 = plt.figure(facecolor=(1.0, 0.0, 0.0, 0.0))
	ax2 = fig2.add_subplot(1, 1, 1)

	x = list(estudados.keys())
	y = list(estudados.values())

	# PLOTAGEM DO GRÁFICO DE BARRAS
	plt.bar(x, y, color=[f'#{self.cor_aplicativo}'])
	plt.xticks(rotation=0)
	plt.grid(True, alpha=0.2)

	# DEIXAR TRANSPARENTE AS BORDAS E O FUNDO PRINCIPAL DO GRÁFICO
	ax2 = plt.axes()
	ax2.set_facecolor((1, 0, 0, 0))
	ax2.spines['bottom'].set_visible(False)
	ax2.spines['top'].set_visible(False)
	ax2.spines['left'].set_visible(False)
	ax2.spines['right'].set_visible(False)

	# COR DOS NOMES DOS EIXOS + DADOS DOS EIXOS + CRIAÇÃO DA FIGURA
	ax2.xaxis.label.set_color(f'#{self.cor_aplicativo}')
	ax2.yaxis.label.set_color(f'#{self.cor_aplicativo}')
	ax2.tick_params(axis='x', colors=f'#{self.cor_aplicativo}')
	ax2.tick_params(axis='y', colors=f'#{self.cor_aplicativo}')
	ax2.xaxis.set_tick_params(labelsize=6.8)
	ax2.yaxis.set_tick_params(labelsize=8)

	if page_zero == True:
		self.ids.acertos_erros_bar_plot.add_widget(FigureCanvasKivyAgg(plt.gcf()))
		plt.close(fig2)
		plt.close('all')
		del fig2
		del ax2
		del estudados
	if page_zero == False:
		self.acertos_erros_zoom_dialog.content_cls.ids.graph_acertos_erros.add_widget(FigureCanvasKivyAgg(plt.gcf()))
		#plt.close()
		plt.close(fig2)
		plt.close('all')
		plt.cla()
		plt.clf()
		del fig2
		del ax2
		del estudados
def changeZeroEsquerda(string):
	if len(string) >= 2:
		if string[0] == '0':
			return string[1]
		else:
			return string
	else:
		return string
def transformNumSize(string):
	if len(str(string)) > 4:
		return '9999' + '+'
	else:
		return str(string)
def transformNumSize_this_week(string):
	if len(str(string)) > 4:
		return '9999'
	else:
		return str(string)
def count_acertos(data, validation):
    acertos = []
    erros = []


    for x in range(len(data)):
        if data[x][2] == 'Exercicios':
            acertos.append(int(data[x][7]))
            erros.append(int(data[x][8]))

    if validation == True:
        if acertos == [] or len(acertos) == 0:
            return '0'
        else:
            return transformNumSize(sum(acertos))

    if validation == False:
        if erros == [] or len(erros) == 0:
            return '0'
        else:
            return transformNumSize(sum(erros))
def count_acertos_weekly(data, validation):
	acertos_this_week = []
	erros_this_week = []
	today = date.today()

	take_actual_week_number = \
	datetime.date(int(str(date.today()).split('-')[0]), int(changeZeroEsquerda(str(date.today()).split('-')[1])),
				  int(changeZeroEsquerda(str(date.today()).split('-')[2]))).isocalendar()[1]
	for x in range(len(data)):
		if data[x][2] == 'Exercicios':
			if data[x][0].split('-')[0] == str(date.today()).split('-')[0]:
				verificar_semana = \
				datetime.date(int(data[x][0].split('-')[0]), int(changeZeroEsquerda(data[x][0].split('-')[1])),
							  int(changeZeroEsquerda(data[x][0].split('-')[2]))).isocalendar()[1]
				if verificar_semana == take_actual_week_number:
					acertos_this_week.append(int(data[x][7]))
					erros_this_week.append(int(data[x][8]))

	if validation == True:
		if acertos_this_week == [] or len(acertos_this_week) == 0:
			return '0'
		else:
			return transformNumSize_this_week(str(sum(acertos_this_week)))

	if validation == False:
		if erros_this_week == [] or len(erros_this_week) == 0:
			return '0'
		else:
			return transformNumSize_this_week(str(sum(erros_this_week)))
def colorDataExercicios(lista, color_hex='686fa3'):
	step4 = []
	for i in range(len(lista)):
		step4.append([])

	# CONVERTER TUPLA PARA LISTA [()] - > [[]]
	for y in range(len(step4)):
		for x in range(len(lista[y])):
			step4[y].append(lista[y][x])

	# APLICAR AS FUNÇÕES PARA AS HORAS E DATAS
	for w in range(len(step4)):
		step4[w][0] = '[color=#{}]'.format(color_hex) + step4[w][0] + '[/color]'
		step4[w][1] = '[color=#{}]'.format(color_hex) + step4[w][1] + '[/color]'
		step4[w][2] = '[color=#{}]'.format(color_hex) + step4[w][2] + '[/color]'
		step4[w][3] = '[color=#{}]'.format(color_hex) + step4[w][3] + '[/color]'
		step4[w][4] = '[color=#{}]'.format(color_hex) + step4[w][4] + '[/color]'
		step4[w][5] = '[color=#{}]'.format(color_hex) + step4[w][5] + '[/color]'
		step4[w][7] = '[color=#{}]'.format(color_hex) + step4[w][7] + '[/color]'
		step4[w][8] = '[color=#{}]'.format(color_hex) + step4[w][8] + '[/color]'
		step4[w][9] = '[color=#{}]'.format(color_hex) + step4[w][9] + '[/color]'
		step4[w][6] = changeStatusColor(step4[w][6])


	# CONVERTER PARA TUPLAR [[]] -> [()]
	for j in range(len(step4)):
		step4[j] = tuple(step4[j])

	return step4
def calcularTaxaAcerto(acertos, erros):
  if acertos != 0 and erros !=0:
    return str(round(float(acertos/(acertos+erros) * 100), 2)) + ' %'
  if acertos == 0 and erros == 0:
    return "0.0 %"
  else:
    return str(round(float(acertos/(acertos+erros) * 100), 2)) + ' %'

#////////////////////////////////////////////////////////////////////////////

class ButtonGrid_Menu(ButtonBehavior, MDBoxLayout, HoverBehavior):
	R = NumericProperty(1)
	G = NumericProperty(0.3490)
	B = NumericProperty(0.3490)

	def on_enter(self, **kwargs):
		self.md_bg_color = (0.9882, 0.4784, 0.4784, 1)
		self.R = 0.9882
		self.G = 0.4784
		self.B = 0.4784

	def on_leave(self, **kwargs):
		self.md_bg_color = (1, 0.3490, 0.3490, 1)
		self.R = 1
		self.G = 0.3490
		self.B = 0.3490


class ButtonGrid_Menu_v2 (ButtonBehavior, MDBoxLayout, HoverBehavior):
	pass


class ButtonGrid_Menu_Selected(ButtonBehavior, MDBoxLayout, HoverBehavior):
	R = NumericProperty(0.9282)
	G = NumericProperty(0.4784)
	B = NumericProperty(0.4784)

	def on_enter(self, **kwargs):
		self.R = 0.9282
		self.G = 0.4784
		self.B = 0.4784

	def on_leave(self, **kwargs):
		self.R = 0.9282
		self.G = 0.4784
		self.B = 0.4784

class ButtonGrid(ButtonBehavior, MDBoxLayout, HoverBehavior):
	cor = StringProperty('eef2fe')

	cor_widgets_default = StringProperty('eef2fe')
	cor_widgets_default_disabled = StringProperty('ebeffc')
	cor_widgets_hover = StringProperty('f4f7fe')
	cor_widgets_press = StringProperty('cad1e7')

	R = NumericProperty(0.9333)
	G = NumericProperty(0.9490)
	B = NumericProperty(0.9960)

	def on_enter(self, **kwargs):
		#self.tooltip_text = 'a'
		#self.md_bg_color = (0.8980, 0.9215, 0.9843, 1)
		self.R = 0.9568
		self.G = 0.9686
		self.B = 0.9960


	def on_leave(self, **kwargs):

		#self.md_bg_color = (0.8980, 0.9215, 0.9843, 1)
		self.R = 0.9333
		self.G = 0.9490
		self.B = 0.9960

class ButtonGridBlue(ButtonBehavior, MDBoxLayout, HoverBehavior):
	R = NumericProperty(0.4078)
	G = NumericProperty(0.4353)
	B = NumericProperty(0.6392)

	def on_enter(self, **kwargs):
		#self.md_bg_color = (0.8980, 0.9215, 0.9843, 1)
		self.R = 0.4863
		self.G = 0.5216
		self.B = 0.7804

	def on_leave(self, **kwargs):
		#self.md_bg_color = (0.8980, 0.9215, 0.9843, 1)
		self.R = 0.4078
		self.G = 0.4353
		self.B = 0.6392

class MDBoxLayout_Hover(MDBoxLayout, HoverBehavior):
	cor = StringProperty('eef2fe')
	cor_widgets_default = StringProperty('eef2fe')
	cor_widgets_default_disabled = StringProperty('ebeffc')
	cor_widgets_hover = StringProperty('f4f7fe')


	R = NumericProperty(0.9333)
	G = NumericProperty(0.9490)
	B = NumericProperty(0.9960)

	def on_enter(self, **kwargs):
		#self.md_bg_color = (0.8980, 0.9215, 0.9843, 1)
		self.R = 0.9568
		self.G = 0.9686
		self.B = 0.9960


	def on_leave(self, **kwargs):
		#self.md_bg_color = (0.8980, 0.9215, 0.9843, 1)
		self.R = 0.9333
		self.G = 0.9490
		self.B = 0.9960





class MDFloatLayout_Hover(MDFloatLayout, HoverBehavior):
	R = NumericProperty(0.9333)
	G = NumericProperty(0.9490)
	B = NumericProperty(0.9960)

	def on_enter(self, **kwargs):
		#self.md_bg_color = (0.8980, 0.9215, 0.9843, 1)
		self.R = 0.9568
		self.G = 0.9686
		self.B = 0.9960

	def on_leave(self, **kwargs):
		#self.md_bg_color = (0.8980, 0.9215, 0.9843, 1)
		self.R = 0.9333
		self.G = 0.9490
		self.B = 0.9960


class Content(MDFloatLayout):
    pass

class Content_RemoveTopic_Specific(MDFloatLayout):
    pass

class Conteudo_Acertos_Erros(MDFloatLayout):
	cor_aplicativo = '686fa3'
	cor_widget = 'eef2fe'

class Zoom_acertos_erros (MDFloatLayout):
	cor_aplicativo = '686fa3'
	cor_widget = 'eef2fe'



class Conteudo(MDList):
	def __init__(self, lista, **kwargs):
		self.data = pickle.load((open("data_subjects_topics.p", "rb")))
		super().__init__(**kwargs)
		for topico in list(lista):
			if topico == "":
				pass
			else:
				#[color=686fa3] {} |      [b]{}[/b][/color]
				self.add_widget(OneLineListItem(text ="[color=686fa3]  {}[/color]".format(topico)))

class SpinnerOptions(SpinnerOption):
	def __init__(self, **kwargs):
		super(SpinnerOptions, self).__init__(**kwargs)
		self.background_normal = ''
		self.background_color = [238/255, 242/255, 254/255, 1]  # COLORIR O FUNDO DOS OUTROS ITEMS
		self.height = 30
		self.color = [104 / 255, 111 / 255, 163 / 255, 1]

class SpinnerDropdown(DropDown):
	def __init__(self, **kwargs):
		super(SpinnerDropdown, self).__init__(**kwargs)
		self.auto_width = True
		self.color = [104 / 255, 111 / 255, 163 / 255, 1]



class Inicio(Screen):
	#cor_principal = StringProperty('f54d4d')
	#cor_fundo_principal = StringProperty('e94f4f')
	def OpenFileManager(self):
		pass

	def textColor(self):
		self.ids.button_cronograma_texto.color = get_color_from_hex('#ffffff')


	value = NumericProperty(250)

class Inicio_CriarMateria(Screen):
	dialog = None
	dialog2 = None
	dialog3 = None
	dialog4 = None

	# DIALOGO PARA CONFIRMAR MATERIA CADASTRADA
	def show_alert_confirmed(self, *args):
		if not self.dialog:
			self.dialog = MDDialog(
				md_bg_color = (0.9019, 0.9215, 0.9843,1),
				title="[color=686fa3][b]Matéria Cadastrada![/b][/color]",
				text="[color=686fa3]Sua matéria foi cadastrada com sucesso![/color]",
				buttons=[
					MDFlatButton(
						text="[color=686fa3][b]CONCLUIR[/color][/b]",
						on_release = self.close_dialog
					)
				],
			)
		self.dialog.open()

	# DIALOGO PARA CONFIRMAR SE DESEJA APAGAR A ULTIMA MATÉRIA
	def show_alert_delete_Last(self, root, *args):
		if not self.dialog2:
			self.dialog2 = MDDialog(
				md_bg_color = (0.9019, 0.9215, 0.9843,1),
				title='[color=686fa3][b]Remover Matéria[/color][/b]',
				text="[color=686fa3]Você deseja remover a [b]ultima mátéria[/b] da sua lista?\nEsse processo é irreversível e irá remover todos os eventos relacionados com essa matéria, como cronograma, tópicos, etc. [/color]",

				buttons=[
					MDFlatButton(
						text="[color=686fa3][b]CANCELAR[/color][/b]",
						theme_text_color="Custom",
						on_release = self.close_dialog2
					),
					MDFlatButton(
						text="[color=686fa3][b]REMOVER[/color][/b]",
						theme_text_color="Custom",
						on_press = root.removeMateria_Last,
						on_release = self.close_dialog2

					),
				],
			)
		self.dialog2.open()


	# DIALOGO PARA CONFIRMAR SE DESEJA APAGAR A TODAS AS MATERIAS
	def show_alert_delete_All(self, root, *args):
		if not self.dialog3:
			self.dialog3 = MDDialog(
				#md_bg_color=(0.8980, 0.9215, 0.9843, 1)
				md_bg_color = (0.9019, 0.9215, 0.9843,1),
				title='[color=686fa3][b]Remover Matéria[/color][/b]',
				text="[color=686fa3]Você deseja remover [b]todas às suas mátérias[/b] da sua lista?\nEsse processo é irreversível e irá remover todos os eventos relacionados com essas matérias, como cronograma, tópicos, etc. [/color]",

				buttons=[
					MDFlatButton(
						text="[color=686fa3][b]CANCELAR[/color][/b]",
						theme_text_color="Custom",
						on_release = self.close_dialog3
					),
					MDFlatButton(
						text="[color=686fa3][b]REMOVER[/color][/b]",
						theme_text_color="Custom",
						on_press = root.removeMateria_All,
						on_release = self.close_dialog3

					),
				],
			)
		self.dialog3.open()

	# DIALOGO PARA CONFIRMAR SE DESEJA APAGAR MATERIA ESPECIFICA
	def show_alert_delete_specific(self, root, *args):

		if not self.dialog4:
			self.dialog4 = MDDialog(
				#md_bg_color=(0.8980, 0.9215, 0.9843, 1)
				md_bg_color = (0.9019, 0.9215, 0.9843,1),
				type="custom",
				size_hint=[0.4,0.2],
				content_cls=Content(),
				title='[color=686fa3][b]Remover Matéria[/color][/b]',
				#text="[color=686fa3]Você deseja remover [b]todas às suas mátérias[/b] da sua lista?\nEsse processo é irreversível e irá remover todos os eventos relacionados com essas matérias, como cronograma, tópicos, etc. [/color]",
				auto_dismiss = False,
				buttons=[
					MDFlatButton(
						text="[color=686fa3][b]CANCELAR[/color][/b]",
						theme_text_color="Custom",
						on_release = self.close_dialog4
					),
					MDFlatButton(
						text="[color=686fa3][b]REMOVER[/color][/b]",
						theme_text_color="Custom",
						on_press = root.removeMateria_specific,
						on_release = self.close_dialog4

					),
				],
			)
		self.dialog4.open()

	# CANCELAR DIALOGO DE CONFIRMAÇÃO DE CADASTRO
	def close_dialog(self, obj):
		# Close alert box
		self.dialog.dismiss()

	# CANCELAR DIALOGO DE REMOVER ULTIMA MATÉRIA
	def close_dialog2(self, obj):
		# Close alert box
		self.dialog2.dismiss()

	# CANCELAR DIALOGO DE REMOVER TODAS AS MATERIAS
	def close_dialog3(self, obj):
		# Close alert box
		self.dialog3.dismiss()

	# CANCELAR DIALOGO DE SE DESEJA APAGAR MATERIA ESPECIFICA
	def close_dialog4(self, obj):
		# Close alert box
		self.dialog4.dismiss()

	def read_or_new_pickle(path, default):
		if os.path.isfile(path):
			with open(path, "rb") as f:
				try:
					return pickle.load(f)
				except Exception:  # so many things could go wrong, can't be more specific.
					pass
		with open(path, "wb") as f:
			pickle.dump(default, f)
		return default

	data = read_or_new_pickle(path="data_subjects_topics.p", default={})

	def addMateria(self, root, *args):
		self.data = pickle.load((open("data_subjects_topics.p", "rb")))

		nome_materia = ' '.join(root.ids.materia_input_name.text.split()).lower().title()
		nome_tag = ' '.join(root.ids.tag_materia_input_name.text.split()).upper()

		if nome_materia != "" and  nome_tag != "" and len(nome_tag) == 3 and len(nome_materia) <= 15:

			root.ids.lista.add_widget(OneLineListItem(text='[color=686fa3] {} |      [b]{}[/b][/color]'.format(nome_tag, nome_materia)))
			self.data[nome_materia] = [[nome_tag], []]

			pickle.dump(self.data, open("data_subjects_topics.p", "wb"))

			root.ids.materia_input_name.text = ''
			root.ids.tag_materia_input_name.text = ''
			root.show_alert_confirmed()

		else:
			pass


	class ListaMaterias(MDList, ButtonBehavior, MDBoxLayout, HoverBehavior, ThemableBehavior):
		def __init__(self,**kwargs):
			self.data = pickle.load((open("data_subjects_topics.p", "rb")))
			super().__init__(**kwargs)
			for i in range(len(list(self.data.keys()))):
				self.add_widget(OneLineListItem(text='[color=686fa3] {} |      [b]{}[/b][/color]'.format(str(self.data[list(self.data.keys())[i]][0][0]), list(self.data.keys())[i])))

	def removeMateria_Last(self, root):
		self.data = pickle.load((open("data_subjects_topics.p", "rb")))
		if len(self.data) == 0:
			pass
		else:
			self.ids.lista.remove_widget(self.ids.lista.children[0])
			del self.data[list(self.data.keys())[-1]]

		pickle.dump(self.data, open("data_subjects_topics.p", "wb"))



	def removeMateria_All(self, root, *args):
		self.data = pickle.load((open("data_subjects_topics.p", "rb")))
		self.data = {}
		self.ids.lista.clear_widgets()
		pickle.dump(self.data, open("data_subjects_topics.p", "wb"))


	def removeMateria_specific(self, root, *args):
		self.data = pickle.load((open("data_subjects_topics.p", "rb")))
		name = ' '.join(self.dialog4.content_cls.ids.nome_materia_delete.text.split()).lower().title()

		if name in list(self.data.keys()):
			if len(self.data) == 0:
				pass
			else:
				#self.ids.lista.remove_widget(self.ids.lista.children[0])
				del self.data[name]
				self.ids.lista.clear_widgets()

			for i in range(len(list(self.data.keys()))):
				self.ids.lista.add_widget(OneLineListItem(text='[color=686fa3] {} |      [b]{}[/b][/color]'.format(str(self.data[list(self.data.keys())[i]][0][0]),list(self.data.keys())[i])))

				self.dialog4.content_cls.ids.nome_materia_delete.text = ''

			pickle.dump(self.data, open("data_subjects_topics.p", "wb"))

		else:
			pass

	value = NumericProperty(250)

class Inicio_CriarTopico(Screen):

	dialog5 = None
	dialog6 = None
	dialog7 = None

	# DIALOGO PARA CONFIRMAR SE DESEJA APAGAR MATERIA ESPECIFICA
	def show_alert_delete_specific_topic (self, root, *args):

		if not self.dialog5:
			self.dialog5 = MDDialog(
				# md_bg_color=(0.8980, 0.9215, 0.9843, 1)
				md_bg_color=(0.9019, 0.9215, 0.9843, 1),
				type="custom",
				content_cls=Content_RemoveTopic_Specific(),
				title='[color=686fa3][b]Remover Tópico[/color][/b]',
				# text="[color=686fa3]Você deseja remover [b]todas às suas mátérias[/b] da sua lista?\nEsse processo é irreversível e irá remover todos os eventos relacionados com essas matérias, como cronograma, tópicos, etc. [/color]",
				auto_dismiss=False,
				buttons=[
					MDFlatButton(
						text="[color=686fa3][b]CANCELAR[/color][/b]",
						theme_text_color="Custom",
						on_release=self.close_dialog5
					),
					MDFlatButton(
						text="[color=686fa3][b]REMOVER[/color][/b]",
						theme_text_color="Custom",
						on_press=root.removeTopic_specific,
						on_release=self.close_dialog5

					),
				],
			)
		self.dialog5.open()

	# DIALOGO PARA CONFIRMAR SE DESEJA REMOVER TODAS AS MATERIAS
	def show_alert_delete_all_topic (self, root, *args):
		if not self.dialog6:
			self.dialog6 = MDDialog(
				#md_bg_color=(0.8980, 0.9215, 0.9843, 1)
				md_bg_color = (0.9019, 0.9215, 0.9843,1),
				title='[color=686fa3][b]Remover Tópico[/color][/b]',
				text="[color=686fa3]Você deseja remover [b]todas os seus tópicos[/b] da sua lista?\nEsse processo é irreversível e irá remover todos os eventos relacionados com esses tópicos, como cronograma, etc. [/color]",

				buttons=[
					MDFlatButton(
						text="[color=686fa3][b]CANCELAR[/color][/b]",
						theme_text_color="Custom",
						on_release = self.close_dialog6
					),
					MDFlatButton(
						text="[color=686fa3][b]REMOVER[/color][/b]",
						theme_text_color="Custom",
						on_press = root.removeTopic_all,
						on_release = self.close_dialog6

					),
				],
			)
		self.dialog6.open()


	def show_alert_confirmed_topic(self, *args):
		if not self.dialog7:
			self.dialog7 = MDDialog(
				md_bg_color = (0.9019, 0.9215, 0.9843,1),
				title="[color=686fa3][b]Tópico Cadastrado![/b][/color]",
				text="[color=686fa3]Seu tópico foi cadastrado com sucesso![/color]",
				buttons=[
					MDFlatButton(
						text="[color=686fa3][b]CONCLUIR[/color][/b]",
						on_release = self.close_dialog7
					)
				],
			)
		self.dialog7.open()

	# CANCELAR DIALOGO DE SE DESEJA APAGAR TÓPICO ESPECIFICO
	def close_dialog5(self, obj):
		# Close alert box
		self.dialog5.dismiss()

	# CANCELAR DIALOGO DE SE DESEJA APAGAR TODOS OS TOPICOS
	def close_dialog6(self, obj):
		# Close alert box
		self.dialog6.dismiss()

	# CANCELAR DIALOGO DE CONFIRMAÇÃO PARA TOPICO CADASTRADO
	def close_dialog7(self, obj):
		# Close alert box
		self.dialog7.dismiss()

	def removeTopic_specific(self, root, *args):
		self.data = pickle.load((open("data_subjects_topics.p", "rb")))
		name = ' '.join(self.dialog5.content_cls.ids.nome_topic_delete.text.split()).lower().title()

		# NOME DIFERENTE DE VAZIO
		if name != "":
			for nome_materia in list(self.data.keys()):
					# ENCONTROU O TOPICO INFORMADO
					if name in self.data[nome_materia][1]:
						self.data[nome_materia][1].remove(name)
						pickle.dump(self.data, open("data_subjects_topics.p", "wb"))

					# TOPICO NÃO ENCONTRADO
					else:
						pass

			self.ids.todos_TopicosMaterias.clear_widgets()

			for materia in list(self.data.keys()):
				self.ids.todos_TopicosMaterias.add_widget(MDExpansionPanel(icon="",
																		   content=Conteudo(self.data[materia][1]),
																		   panel_cls=MDExpansionPanelOneLine(
																			   text="[color=686fa3][b]     {}[/color][/b]".format(
																				   materia))))

			self.dialog5.content_cls.ids.nome_topic_delete.text = ''


		# NOME VAZIO
		else:
			pass

	def removeTopic_all(self,root,*args):
		self.data = pickle.load((open("data_subjects_topics.p", "rb")))

		for nome_materia in list(self.data.keys()):
			self.data[nome_materia][1].clear()
			pickle.dump(self.data, open("data_subjects_topics.p", "wb"))

		self.ids.todos_TopicosMaterias.clear_widgets()

		for materia in list(self.data.keys()):
			self.ids.todos_TopicosMaterias.add_widget(MDExpansionPanel(icon="",
																	   content=Conteudo(self.data[materia][1]),
																	   panel_cls=MDExpansionPanelOneLine(
																		   text="[color=686fa3][b]     {}[/color][/b]".format(
																			   materia))))

	class MateriasSpinner(Spinner):
		def __init__(self, **kwargs):
			super().__init__(**kwargs)
			self.dropdown_cls = SpinnerDropdown
			self.option_cls = SpinnerOptions
			self.color = [104 / 255, 111 / 255, 163 / 255, 1]
			self.bold = True
			self.dropdown_cls.max_height = self.height * 2 + 2 * 4

	value = NumericProperty(250)


	def addTopico(self, root, *args):
		self.data = pickle.load((open("data_subjects_topics.p", "rb")))
		nome_topico_bruto = ' '.join(root.ids.name_topico.text.split()).lower().title()

		if root.ids.spinnerMaterias.text != "" and root.ids.spinnerMaterias.text != 'Selecione uma matéria' and root.ids.name_topico.text != "" and len(root.ids.name_topico.text) <= 15:
			self.data[root.ids.spinnerMaterias.text][1].append(nome_topico_bruto)

			# RETORNAR VALORES DEFAULT APÓS TERMINO DA FUNÇÃO ADDTOPICO

			root.ids.spinnerMaterias.text = "Selecione uma matéria"

			self.ids.todos_TopicosMaterias.clear_widgets()
			for materia in list(self.data.keys()):
				self.ids.todos_TopicosMaterias.add_widget(MDExpansionPanel(icon="",
																		   content=Conteudo(self.data[materia][1]),
																		   panel_cls=MDExpansionPanelOneLine(
																			   text="[color=686fa3][b]     {}[/color][/b]".format(materia))))

			pickle.dump(self.data, open("data_subjects_topics.p", "wb"))

			root.show_alert_confirmed_topic()

			root.ids.name_topico.text = ''

		else:
			pass



	class TopicosMaterias (MDBoxLayout):
		def __init__(self, **kwargs):
			self.data = pickle.load((open("data_subjects_topics.p", "rb")))
			super().__init__(**kwargs)
			#self.add_widget(MDExpansionPanelOneLine(text=str(list(self.data.keys())[0]), content=Conteudo()))

			for materia in list(self.data.keys()):
				self.add_widget(MDExpansionPanel(icon="",
												 content=Conteudo(self.data[materia][1]),
												 panel_cls=MDExpansionPanelOneLine(text="[color=686fa3][b]     {}[/color][/b]".format(materia))))




	def on_leave(self, *args):
		self.ids.spinnerMaterias.values = ()
		self.ids.todos_TopicosMaterias.clear_widgets()



	def on_enter(self, *args):
		self.ids.todos_TopicosMaterias.clear_widgets()
		self.data = pickle.load((open("data_subjects_topics.p", "rb")))
		self.ids.spinnerMaterias.values = tuple(self.data.keys())
		self.ids.spinnerMaterias.text = "Selecione uma matéria"

		self.data = pickle.load((open("data_subjects_topics.p", "rb")))
		for materia in list(self.data.keys()):
			self.ids.todos_TopicosMaterias.add_widget(MDExpansionPanel(icon="",
											 content=Conteudo(self.data[materia][1]),
											 panel_cls=MDExpansionPanelOneLine(text="[color=686fa3][b]     {}[/color][/b]".format(materia))))


class Cronograma(Screen):
	dialog10 = None
	confirmar_remover = None
	value = NumericProperty(250)
	cor_aplicativo = '686fa3'
	cor_widget = 'eef2fe'

	estudado = StringProperty()
	estudado_data = StringProperty()
	nao_estudado = StringProperty()
	nao_estudado_data = StringProperty()

	next_event_name = StringProperty()
	next_event_data = StringProperty()
	next_event_time = StringProperty()

	# ////////////////////////////////////////////////////////////////////////////
	# TABELA CRONOGRAMA
	class Tabela_Cronograma(MDBoxLayout):
		def __init__(self,**kwargs):
			super().__init__(**kwargs)
			today = date.today()

			self.data_exercicios = pickle.load((open("data_timeline.p", "rb")))
			self.today = date.today()
			self.data_today = SearchByData(self.data_exercicios, str(self.today))

			data_table_cronograma = MDDataTable(
				background_color_header=get_color_from_hex("#eef2fe"),
				background_color_selected_cell=get_color_from_hex("#f2f5fc"),
				background_color_cell=(0.9333, 0.9490, 0.9960, 1),
				size_hint=(1, 1),
				elevation=0,
				check=True,
				use_pagination=True,
				rows_num=grid.rows_per_page_cronograma,
				column_data=[("[color=#686fa3]Data[/color]", dp(grid.tabela_cronograma_dp_data)),
							 ("[color=#686fa3]Horário[/color]", dp(grid.tabela_cronograma_dp_horario)),
							 ("[color=#686fa3]Categoria[/color]", dp(grid.tabela_cronograma_dp_categoria)),
							 ("[color=#686fa3]Matéria[/color]", dp(grid.tabela_cronograma_dp_materia)),
							 ("[color=#686fa3]Tópico[/color]", dp(grid.tabela_cronograma_dp_topico)),
							 ("[color=#686fa3]Status[/color]", dp(grid.tabela_cronograma_dp_status))],
				row_data=AutoSizeTableRowsNum_Cronograma(self.data_today, grid.rows_per_page_cronograma + 1))

			self.add_widget(data_table_cronograma)

	# ////////////////////////////////////////////////////////////////////////////
	# FUNÇÕES E WIDGETS RELACIONADOS PARA REMOVER ITEM DO CRONOGRAMA
	def confirmar_remover_dialog(self, root, *args):
		try:
			if len(root.ids.cronograma22.children[-1].get_row_checks()) > 0:
				if not self.confirmar_remover:
					self.confirmar_remover = MDDialog(
						title=f'[color={self.cor_aplicativo}]Remover Item[/color]',
						md_bg_color=(0.9019, 0.9215, 0.9843, 1),
						type="custom",
						auto_dismiss=True,
						text=f"[color={self.cor_aplicativo}]Você deseja remover [b]esses items[/b] do seu cronograma?\nEsse processo é irreversível e irá [b]remover permanentemente[/b] esses items.[/color]".format(
							str(grid.cor_principal_aplicativo)),
						buttons=[
							MDFlatButton(
								text=f"[color={self.cor_aplicativo}][b]NÃO[/color][/b]",
								theme_text_color="Custom",
								on_release=self.close_confirmar_remover
							),
							MDFlatButton(
								text=f"[color={self.cor_aplicativo}][b]SIM[/color][/b]",
								theme_text_color="Custom",
								on_release=self.close_remover,
								on_press=self.close_confirmar_remover
							)
						]
					)

				self.confirmar_remover.open()

			else:
				toast("Atenção: Nenhum Item Selecionado.")
		except AttributeError:
			pass
	def close_dialog10(self, obj):
		self.dialog10.dismiss()
	def close_confirmar_remover(self, obj):
		self.confirmar_remover.dismiss()
	def close_remover(self, obj):
		self.removerItemCronograma(self)
	def removerItemCronograma(root, self):
			#root.confirmar_remover_dialog.dismiss()
			def SearchByData(lista, string):
				step18 = []
				for i in range(len(lista)):
					step18.append([])

				# CONVERTER TUPLA PARA LISTA [()] - > [[]]
				for y in range(len(step18)):
					for x in range(len(lista[y])):
						step18[y].append(lista[y][x])
				step19 = []
				# VERIFICAR SE A DATA É IGUAL A DATA DA LISTA
				for w in range(len(step18)):
					if step18[w][0] == str(string):
						step19.append(step18[w])
				# CONVERTER PARA TUPLAR [[]] -> [()]
				for w in range(len(step19)):
					step19[w] = tuple(step19[w])

				return step19
			def rebuildDataStyle(lista, color_hex='686fa3'):
				for x in range(len(lista)):
					if lista[x] == [' ', ' ', ' ', ' ', ' ', ' ', ' ']:
						lista[x] = [' ', ' ', ' ', ' ', ' ', ' ', ' ']

					if lista[x][-1][15:27] == 'Não Estudado':
						lista[x][-1] = (
							'alert-circle', [1, 0, 0, 1], '[color=#{}]Não Estudado[/color]'.format(color_hex))

					if lista[x][-1][15:23] == 'Estudado':
						lista[x][-1] = ("checkbox-marked-circle", [39 / 256, 174 / 256, 96 / 256, 1],
										'[color=#{}]Estudado[/color]'.format(color_hex))

				# CONVERTER PARA TUPLAR [[]] -> [()]
				for w in range(len(lista)):
					lista[w] = tuple(lista[w])

				return lista

			options = list(root.ids.cronograma22.children[-1].get_row_checks())
			options_remove = rebuildDataStyle(options)

			def remover(lista_remover):
				data_cronograma = pickle.load((open("data_timeline.p", "rb")))
				data = CronogramaTableStyle(colorData(organizerData(sortData(data_cronograma))))

				data_cronograma = sortData(data_cronograma)
				remover = lista_remover

				DATA_sem_alterar = []
				DATA_alterado = []
				DATA_remover = []

				# ////////////////////////////////////////////////////////////////////#
				# TRANSFORMAR TODO O ARQUIVO no_alteration_data EM LISTA
				for y in range(len(remover)):
					DATA_remover.append([])
					for x in range(len(remover[y])):
						if x == 5:
							DATA_remover[y].append(list(remover[y][x]))
						else:
							DATA_remover[y].append(remover[y][x])

				for y in range(len(data)):
					DATA_alterado.append([])
					for x in range(len(data[y])):
						if x == 5:
							DATA_alterado[y].append(list(data[y][x]))
						else:
							DATA_alterado[y].append(data[y][x])

				for y in range(len(data_cronograma)):
					DATA_sem_alterar.append([])
					for x in range(len(data_cronograma[y])):
						if x == 6:
							DATA_sem_alterar[y].append(list(data_cronograma[y][x]))
						else:
							DATA_sem_alterar[y].append(data_cronograma[y][x])

				for x in range(len(DATA_remover)):
					for y in range(len(DATA_alterado)):
						if DATA_remover[x] == DATA_alterado[y]:
							try:
								DATA_sem_alterar.remove(DATA_sem_alterar[y])
							except IndexError:
								pass

				for x in range(len(DATA_sem_alterar)):
					DATA_sem_alterar[x][6] = tuple(DATA_sem_alterar[x][6])
					DATA_sem_alterar[x] = tuple(DATA_sem_alterar[x])

				return DATA_sem_alterar

			data_cronograma = remover(options_remove)
			pickle.dump(data_cronograma, open("data_timeline.p", "wb"))

			# REMOVER A PARTIR DA DATA FILTRADA
			try:
				def AutoSizeTableRowsNum(lista, rows_per_page):
					lista = CronogramaTableStyle(colorData(organizerData(sortData(lista))))

					if len(lista) == 0:
						return createEmptyRow(createEmptyRow(lista))

					if len(lista) == 1:
						return createEmptyRow(lista)

					if len(lista) > 1:
						def sequence(rows_per_page, data):
							a = {}
							a[0] = rows_per_page
							for i in list(range(1, len(data))):
								a[i] = a[i - 1] + 5
							return list(a.values())

						divisores = sequence(rows_per_page, lista)
						if len(lista) in divisores:
							return createEmptyRow(lista)
						else:
							return lista
				DataSearched = SearchByData(data_cronograma, str(self.data_selecionada))
				self.ids.cronograma22.children[0].update_row_data(self, AutoSizeTableRowsNum(DataSearched,
																							 grid.rows_per_page_cronograma + 1))
				if len(options) == 1:
					toast("Item Removido Com Sucesso!")

				if len(options) > 1:
					toast("Items Removidos Com Sucesso!")

				def refreshChecks(dt):
					try: self.ids.cronograma22.children[0].DoubleClickRefreshChecks()
					except IndexError: pass

				Clock.schedule_once(refreshChecks, 1)

			# REMOVER A PARTIR DA PAGINA INICIAL DE CRONOGRAMA
			except AttributeError:
				def AutoSizeTableRowsNum(lista, rows_per_page):
					lista = CronogramaTableStyle(colorData(organizerData(sortData(lista))))

					if len(lista) == 0:
						return createEmptyRow(createEmptyRow(lista))

					if len(lista) == 1:
						return createEmptyRow(lista)

					if len(lista) > 1:
						def sequence(rows_per_page, data):
							a = {}
							a[0] = rows_per_page
							for i in list(range(1, len(data))):
								a[i] = a[i - 1] + 5
							return list(a.values())

						divisores = sequence(rows_per_page, lista)
						if len(lista) in divisores:
							return createEmptyRow(lista)
						else:
							return lista

				today = date.today()
				DataSearched_today = SearchByData(data_cronograma, str(today))
				self.ids.cronograma22.children[0].update_row_data(self, AutoSizeTableRowsNum(DataSearched_today,
																							 grid.rows_per_page_cronograma + 1))
				if len(options) == 1:
					toast("Item Removido Com Sucesso!")

				if len(options) > 1:
					toast("Items Removidos Com Sucesso!")

				def refreshChecks(dt):
					try:
						self.ids.cronograma22.children[0].DoubleClickRefreshChecks()

					except IndexError:
						pass
				Clock.schedule_once(refreshChecks, 1)

			# ALTERAR QUANTIDADE DE ESTUDADOS/ NÃO ESTUDADOS
			try:
				try:
					def count_Estudado(state, data):
						data_v = pickle.load((open("data_timeline.p", "rb")))
						count_estudado = 0
						count_naoestudado = 0

						for x in range(len(data_v)):
							if data_v[x][0] == str(data):
								if data_v[x][6][2] == 'Estudado':
									count_estudado += 1

						for x in range(len(data_v)):
							if data_v[x][0] == str(data):
								if data_v[x][6][2] == 'Não Estudado':
									count_naoestudado += 1

						try:
							total = count_estudado + count_naoestudado

							if total == 0:
								total = len(data_v)

							if state == True:
								valor = round(float(count_estudado / total * 100), 2)
								return str(valor) + ' %'

							elif state == False:
								valor = round(float(count_naoestudado / total * 100), 2)
								return str(valor) + ' %'
						except ZeroDivisionError:
							total = 1
					self.estudado = count_Estudado(True, str(self.data_selecionada))
					self.nao_estudado = count_Estudado(False, str(self.data_selecionada))
				except ValueError: pass
			except AttributeError:
				try:
					def count_Estudado(state):
						data_v = pickle.load((open("data_timeline.p", "rb")))
						count_estudado = 0
						count_naoestudado = 0

						from datetime import date
						today = date.today()

						for x in range(len(data_v)):
							if data_v[x][0] == str(today):
								if data_v[x][6][2] == 'Estudado':
									count_estudado += 1

						for x in range(len(data_v)):
							if data_v[x][0] == str(today):
								if data_v[x][6][2] == 'Não Estudado':
									count_naoestudado += 1

						try:
							total = count_estudado + count_naoestudado

							if total == 0:
								total = len(data_v)

							if state == True:
								valor = round(float(count_estudado / total * 100), 2)
								return str(valor) + ' %'

							elif state == False:
								valor = round(float(count_naoestudado / total * 100), 2)
								return str(valor) + ' %'
						except ZeroDivisionError:
							total = 1
					self.estudado = count_Estudado(True)
					self.nao_estudado = count_Estudado(False)
				except ValueError: pass

	# ////////////////////////////////////////////////////////////////////////////
	# CRIAR NOVO ARQUIVO PARA DATA_TIMELINE CASO NÃO TIVER
	def read_or_new_pickle(path, default):
		if os.path.isfile(path):
			with open(path, "rb") as f:
				try:
					return pickle.load(f)
				except Exception:  # so many things could go wrong, can't be more specific.
					pass
		with open(path, "wb") as f:
			pickle.dump(default, f)
		return default
	data_cronograma = read_or_new_pickle(path="data_timeline.p", default=[])

	# ////////////////////////////////////////////////////////////////////////////
	# FUNÇÕES PARA MUDAR STATUS DE ESTUDADO/ NÃO ESTUDADO
	def EstudadoFunction_Home(self, root):
		data_cronograma = pickle.load((open("data_timeline.p", "rb")))


		# IDENTIFICAR TABELA E ROWS CHECK DIFERENTE DE LISTA VAZIA
		if self.ids.cronograma22.children[0].children[0].get_row_checks() != [] and len(self.ids.cronograma22.children[0].children[0].get_row_checks()) > 0:

			def defaultStyle(lista):
				step14 = []
				for i in range(len(lista)):
					step14.append([])

				# CONVERTER TUPLA PARA LISTA [()] - > [[]]
				for y in range(len(step14)):
					for x in range(len(lista[y])):

						if x == 6:
							step14[y].append(list(lista[y][x]))

						else:
							step14[y].append(lista[y][x])

				def RegEx(string):
					try:
						label = re.findall(r'\]+[a-zA-Z0-9]+\[', string)
						label[0] = label[0][1:-1]
						return label[0]
					except IndexError:
						pass

				for x in range(len(step14)):
					if step14[x] == [' ', ' ', ' ', ' ', ' ', ' ', ' ']:
						pass

					else:
						# DEFAULT PARA A DATA
						step14[x][0] = str(
							step14[x][0][15:25][-4:] + '-' + step14[x][0][15:25][-7:-5] + '-' + step14[x][0][15:25][
																								-10:-8])

						# DEFAULT PARA O TEMPO
						step14[x][1] = str(step14[x][1][15:17] + ':' + step14[x][1][18:20] + ':00')

						# DEFAULT PARA CATEGORIA
						for y in range(2, 5):
							step14[x][y] = RegEx(step14[x][y])

						#DEFAULT PARA A DURAÇÃO
						step14[x][5] = str(step14[x][5][15:17] + ':' + step14[x][5][18:20] + ':00')

						# DEFAULT STATUS ESTUDADO - NÃO ESTUDADO
						try:
							if step14[x][6][2][15:27] == 'Não Estudado':
								step14[x][6][2] = 'Não Estudado'

							if step14[x][6][2][15:23] == 'Estudado':
								step14[x][6][2] = 'Estudado'
						except IndexError:
							pass

				for x in range(len(step14)):
					step14[x][6] = tuple(step14[x][6])
					step14[x] = tuple(step14[x])

				return step14

			def rebuildDataStyle(lista, color_hex='686fa3'):
				for x in range(len(lista)):
					if lista[x] == [' ', ' ', ' ', ' ', ' ', ' ', ' ']:
						lista[x] = [' ', ' ', ' ', ' ', ' ', ' ', ' ']

					if lista[x][-1][15:27] == 'Não Estudado':
						lista[x][-1] = (
							'alert-circle', [1, 0, 0, 1], '[color=#{}]Não Estudado[/color]'.format(color_hex))

					if lista[x][-1][15:23] == 'Estudado':
						lista[x][-1] = ("checkbox-marked-circle", [39 / 256, 174 / 256, 96 / 256, 1],
										'[color=#{}]Estudado[/color]'.format(color_hex))

				# CONVERTER PARA TUPLAR [[]] -> [()]
				for w in range(len(lista)):
					lista[w] = tuple(lista[w])

				return lista

			def Estudado(lista, select, color_hex='686fa3'):
				data_sem_duracao = []
				data = []
				mudar_status = []

				step22 = []
				for i in range(len(lista)):
					data.append([])

				# CONVERTER TUPLA PARA LISTA [()] - > [[]]
				for y in range(len(lista)):
					for x in range(len(lista[y])):
						if x == 6:
							data[y].append(list(lista[y][x]))
						else:
							data[y].append(lista[y][x])


				# RETIRAR AS COLUNAS DE DURAÇÃO, ACERTOS, ERROS E RENDIMENTO DA LISTA DATA
				for i in range(len(lista)):
					data_sem_duracao.append([])

				# CONVERTER TUPLA PARA LISTA [()] - > [[]]
				for y in range(len(lista)):
					for x in range(len(lista[y])):
						if x == 6:
							data_sem_duracao[y].append(list(lista[y][x]))
						else:
							data_sem_duracao[y].append(lista[y][x])

				# SELECIONADOS PARA MUDAR STATUS PARA ESTUDADO
				for i in range(len(select)):
					mudar_status.append([])

				# CONVERTER TUPLA PARA LISTA [()] - > [[]]
				for y in range(len(select)):
					for x in range(len(select[y])):
						if x == 5:
							mudar_status[y].append(list(select[y][x]))
						else:
							mudar_status[y].append(select[y][x])


				# TIRAR A COLUNA DE DURAÇÃO, ACERTOS, ERROS, RENDIMENTO
				for x in range(len(data_sem_duracao)):
					data_sem_duracao[x].remove(data_sem_duracao[x][-1])

				for x in range(len(data_sem_duracao)):
					data_sem_duracao[x].remove(data_sem_duracao[x][-1])

				for x in range(len(data_sem_duracao)):
					data_sem_duracao[x].remove(data_sem_duracao[x][-1])

				for x in range(len(data_sem_duracao)):
					data_sem_duracao[x].remove(data_sem_duracao[x][-2])

				# step22 contém agora só elementos que não estão em mudar_status
				for verificador in range(len(data_sem_duracao)):
					if data_sem_duracao[verificador] in mudar_status:
						step22.append(data[verificador])

				def list_diff(a, b):
					return [x for x in a if x not in b]

				data_diff = list_diff(data, step22)  # não selecionados ou seja nao contem o status desejado para trocar

				# COLOCAR ESTUDADO EM TODOS OS ITEMS DA LISTA SELECT
				for x in range(len(step22)):
					if step22[x][6][2] == '[color=#{}]Estudado[/color]'.format(color_hex):
						pass

					else:
						step22[x][6][0] = 'checkbox-marked-circle'
						step22[x][6][1] = [39 / 256, 174 / 256, 96 / 256, 1]
						step22[x][6][2] = '[color=#{}]Estudado[/color]'.format(color_hex)

				if len(data_diff) == 0:
					data_diff = step22

				elif len(data_diff) != 0:
					for item in range(len(step22)):
						data_diff.append(step22[item])

				# CONVERTER PARA TUPLA TODOS OS DADOS DE DATA_DIFF
				for x in range(len(data_diff)):
					data_diff[x][6] = tuple(data_diff[x][6])
					data_diff[x] = tuple(data_diff[x])

				return data_diff

			def LastEstudado(lista, select, color_hex='686fa3'):
				data_sem_duracao = []
				data = []
				mudar_status = []

				step22 = []
				for i in range(len(lista)):
					data.append([])

				# CONVERTER TUPLA PARA LISTA [()] - > [[]]
				for y in range(len(lista)):
					for x in range(len(lista[y])):
						if x == 6:
							data[y].append(list(lista[y][x]))
						else:
							data[y].append(lista[y][x])


				# RETIRAR AS COLUNAS DE DURAÇÃO, ACERTOS, ERROS E RENDIMENTO DA LISTA DATA
				for i in range(len(lista)):
					data_sem_duracao.append([])

				# CONVERTER TUPLA PARA LISTA [()] - > [[]]
				for y in range(len(lista)):
					for x in range(len(lista[y])):
						if x == 6:
							data_sem_duracao[y].append(list(lista[y][x]))
						else:
							data_sem_duracao[y].append(lista[y][x])

				# SELECIONADOS PARA MUDAR STATUS PARA ESTUDADO
				for i in range(len(select)):
					mudar_status.append([])

				# CONVERTER TUPLA PARA LISTA [()] - > [[]]
				for y in range(len(select)):
					for x in range(len(select[y])):
						if x == 5:
							mudar_status[y].append(list(select[y][x]))
						else:
							mudar_status[y].append(select[y][x])

				# TIRAR A COLUNA DE DURAÇÃO, ACERTOS, ERROS, RENDIMENTO
				for x in range(len(data_sem_duracao)):
					data_sem_duracao[x].remove(data_sem_duracao[x][-1])

				for x in range(len(data_sem_duracao)):
					data_sem_duracao[x].remove(data_sem_duracao[x][-1])

				for x in range(len(data_sem_duracao)):
					data_sem_duracao[x].remove(data_sem_duracao[x][-1])

				for x in range(len(data_sem_duracao)):
					data_sem_duracao[x].remove(data_sem_duracao[x][-2])

				# step22 contém agora só elementos que não estão em mudar_status
				for verificador in range(len(data_sem_duracao)):
					if data_sem_duracao[verificador] in mudar_status:
						step22.append(data[verificador])

				# COLOCAR ESTUDADO EM TODOS OS ITEMS DA LISTA SELECT
				for x in range(len(step22)):
					if step22[x][6][2] == '[color=#{}]Estudado[/color]'.format(color_hex):
						pass

					else:
						step22[x][6][0] = 'checkbox-marked-circle'
						step22[x][6][1] = [39 / 256, 174 / 256, 96 / 256, 1]
						step22[x][6][2] = '[color=#{}]Estudado[/color]'.format(color_hex)



				# CONVERTER PARA TUPLA TODOS OS DADOS DE DATA_DIFF
				for x in range(len(step22)):
					step22[x][-1] = tuple(step22[x][-1])
					step22[x] = tuple(step22[x])

				return step22

			options = list(root.ids.cronograma22.children[0].children[0].get_row_checks())        # opções selecionadas para mudar status
			data_cronograma = colorData(organizerData(sortData(data_cronograma)))      # organizar, colorir e sort para o dado bruto
			estudadoList = rebuildDataStyle(options)								   # colocar as opções selecionadas no padrão do dado motificado acima


			estudados = LastEstudado(data_cronograma, estudadoList)
			estudados = defaultStyle(estudados)
			estudados = CronogramaTableStyle(organizerData(sortData(estudados)))

			data_cronograma = Estudado(data_cronograma, estudadoList)                  # aplicar a função estudado para as opções selecionadas em data
			data_cronograma = defaultStyle(data_cronograma)                           # retornar o data modificado para o padrão bruto de data
			pickle.dump(data_cronograma, open("data_timeline.p", "wb"))


			# ALTERAR A QUANTIDADE DE ESTUDADOS E NÃO ESTUDADOS
			try:
				try:
					def count_Estudado(state, data):
						data_v = pickle.load((open("data_timeline.p", "rb")))
						count_estudado = 0
						count_naoestudado = 0

						for x in range(len(data_v)):
							if data_v[x][0] == str(data):
								if data_v[x][6][2] == 'Estudado':
									count_estudado += 1

						for x in range(len(data_v)):
							if data_v[x][0] == str(data):
								if data_v[x][6][2] == 'Não Estudado':
									count_naoestudado += 1

						try:
							total = count_estudado + count_naoestudado

							if total == 0:
								total = len(data_v)

							if state == True:
								valor = round(float(count_estudado / total * 100), 2)
								return str(valor) + ' %'

							elif state == False:
								valor = round(float(count_naoestudado / total * 100), 2)
								return str(valor) + ' %'
						except ZeroDivisionError:
							total = 1
					self.estudado = count_Estudado(True, str(self.data_selecionada))
					self.nao_estudado = count_Estudado(False, str(self.data_selecionada))
				except ValueError: pass
			except AttributeError:
				def count_Estudado(state):
					data_v = pickle.load((open("data_timeline.p", "rb")))
					count_estudado = 0
					count_naoestudado = 0

					from datetime import date
					today = date.today()

					for x in range(len(data_v)):
						if data_v[x][0] == str(today):
							if data_v[x][6][2] == 'Estudado':
								count_estudado += 1

					for x in range(len(data_v)):
						if data_v[x][0] == str(today):
							if data_v[x][6][2] == 'Não Estudado':
								count_naoestudado += 1

					try:
						total = count_estudado + count_naoestudado

						if total == 0:
							total = len(data_v)

						if state == True:
							valor = round(float(count_estudado / total * 100), 2)
							return str(valor) + ' %'

						elif state == False:
							valor = round(float(count_naoestudado / total * 100), 2)
							return str(valor) + ' %'
					except ZeroDivisionError:
						total = 1
				try:
					self.estudado = count_Estudado(True)
					self.nao_estudado = count_Estudado(False)
				except ValueError:
					pass

			# NOVOS DADOS A PARTIR DO BOTAO DE FILTRAR ITEM
			try:
				DataSearched = SearchByData(data_cronograma, str(self.data_selecionada))
				if len(DataSearched) >= 0:
					try:
						num = encontrarNumeroPagina(DataSearched, estudados[0], grid.rows_per_page_cronograma)
						if len(estudados) == 0:
							pass
						else:
							toast("Status Alterado Com Sucesso!")
							self.ids.cronograma22.children[0].children[0].update_row_data(self, AutoSizeTableRowsNum_Cronograma(DataSearched,grid.rows_per_page_cronograma + 1))
							try:
								for i in range(1, num):
									self.ids.cronograma22.children[0].children[0].avancarPagina()
							except TypeError:
								pass

					except IndexError: pass

					def refreshChecks(dt):
						try: self.ids.cronograma22.children[0].children[0].DoubleClickRefreshChecks()
						except IndexError: pass

					Clock.schedule_once(refreshChecks, 1.10)

			# NOVOS DADOS A PARTIR DA PAGINA INICIAL
			except AttributeError:
				today = date.today()
				DataSearched_today = SearchByData(data_cronograma, str(today))

				# AVANÇAR ATÉ A PÁGINA QUE VOCÊ SE ENCONTRA
				try:
					num = encontrarNumeroPagina(DataSearched_today, estudados[0], grid.rows_per_page_cronograma)
					if len(estudados) == 0:
						pass
					else:
						toast("Status Alterado Com Sucesso!")
						self.ids.cronograma22.children[0].children[0].update_row_data(self, AutoSizeTableRowsNum_Cronograma(DataSearched_today, grid.rows_per_page_cronograma + 1))

						try:
							for i in range(1, num):
								self.ids.cronograma22.children[0].children[0].avancarPagina()
						except TypeError:
							pass

				except IndexError:
					pass

				def refreshChecks(dt):
					try: self.ids.cronograma22.children[0].children[0].DoubleClickRefreshChecks()
					except IndexError: pass

				Clock.schedule_once(refreshChecks, 1.10)

		else:
			toast("Atenção: Nenhum Item Selecionado.")
	def NaoEstudadoFunction_Home(self, root):
		validation_tabel = '<kivymd.uix.spinner.spinner.MDSpinner'
		data_cronograma = pickle.load((open("data_timeline.p", "rb")))


		# IDENTIFICAR TABELA E ROWS CHECK DIFERENTE DE LISTA VAZIA
		if self.ids.cronograma22.children[0].children[0].get_row_checks() != [] and len(self.ids.cronograma22.children[0].children[0].get_row_checks()) > 0:

			def defaultStyle(lista):
				step14 = []
				for i in range(len(lista)):
					step14.append([])

				# CONVERTER TUPLA PARA LISTA [()] - > [[]]
				for y in range(len(step14)):
					for x in range(len(lista[y])):

						if x == 6:
							step14[y].append(list(lista[y][x]))

						else:
							step14[y].append(lista[y][x])

				def RegEx(string):
					try:
						label = re.findall(r'\]+[a-zA-Z0-9]+\[', string)
						label[0] = label[0][1:-1]
						return label[0]
					except IndexError:
						pass

				for x in range(len(step14)):
					if step14[x] == [' ', ' ', ' ', ' ', ' ', ' ', ' ']:
						pass

					else:
						# DEFAULT PARA A DATA
						step14[x][0] = str(
							step14[x][0][15:25][-4:] + '-' + step14[x][0][15:25][-7:-5] + '-' + step14[x][0][15:25][
																								-10:-8])

						# DEFAULT PARA O TEMPO
						step14[x][1] = str(step14[x][1][15:17] + ':' + step14[x][1][18:20] + ':00')

						# DEFAULT PARA CATEGORIA
						for y in range(2, 5):
							step14[x][y] = RegEx(step14[x][y])

						#DEFAULT PARA A DURAÇÃO
						step14[x][5] = str(step14[x][5][15:17] + ':' + step14[x][5][18:20] + ':00')

						# DEFAULT STATUS ESTUDADO - NÃO ESTUDADO
						try:
							if step14[x][6][2][15:27] == 'Não Estudado':
								step14[x][6][2] = 'Não Estudado'

							if step14[x][6][2][15:23] == 'Estudado':
								step14[x][6][2] = 'Estudado'
						except IndexError:
							pass

				for x in range(len(step14)):
					step14[x][6] = tuple(step14[x][6])
					step14[x] = tuple(step14[x])

				return step14

			def rebuildDataStyle(lista, color_hex='686fa3'):
				for x in range(len(lista)):
					if lista[x] == [' ', ' ', ' ', ' ', ' ', ' ', ' ']:
						lista[x] = [' ', ' ', ' ', ' ', ' ', ' ', ' ']

					if lista[x][-1][15:27] == 'Não Estudado':
						lista[x][-1] = (
							'alert-circle', [1, 0, 0, 1], '[color=#{}]Não Estudado[/color]'.format(color_hex))

					if lista[x][-1][15:23] == 'Estudado':
						lista[x][-1] = ("checkbox-marked-circle", [39 / 256, 174 / 256, 96 / 256, 1],
										'[color=#{}]Estudado[/color]'.format(color_hex))

				# CONVERTER PARA TUPLAR [[]] -> [()]
				for w in range(len(lista)):
					lista[w] = tuple(lista[w])

				return lista

			def NaoEstudado(lista, select, color_hex='686fa3'):
				data_sem_duracao = []
				data = []
				mudar_status = []

				step22 = []
				for i in range(len(lista)):
					data.append([])

				# CONVERTER TUPLA PARA LISTA [()] - > [[]]
				for y in range(len(lista)):
					for x in range(len(lista[y])):
						if x == 6:
							data[y].append(list(lista[y][x]))
						else:
							data[y].append(lista[y][x])

				# RETIRAR AS COLUNAS DE DURAÇÃO, ACERTOS, ERROS E RENDIMENTO DA LISTA DATA
				for i in range(len(lista)):
					data_sem_duracao.append([])

				# CONVERTER TUPLA PARA LISTA [()] - > [[]]
				for y in range(len(lista)):
					for x in range(len(lista[y])):
						if x == 6:
							data_sem_duracao[y].append(list(lista[y][x]))
						else:
							data_sem_duracao[y].append(lista[y][x])

				# SELECIONADOS PARA MUDAR STATUS PARA ESTUDADO
				for i in range(len(select)):
					mudar_status.append([])

				# CONVERTER TUPLA PARA LISTA [()] - > [[]]
				for y in range(len(select)):
					for x in range(len(select[y])):
						if x == 5:
							mudar_status[y].append(list(select[y][x]))
						else:
							mudar_status[y].append(select[y][x])

				# TIRAR A COLUNA DE DURAÇÃO, ACERTOS, ERROS, RENDIMENTO
				for x in range(len(data_sem_duracao)):
					data_sem_duracao[x].remove(data_sem_duracao[x][-1])

				for x in range(len(data_sem_duracao)):
					data_sem_duracao[x].remove(data_sem_duracao[x][-1])

				for x in range(len(data_sem_duracao)):
					data_sem_duracao[x].remove(data_sem_duracao[x][-1])

				for x in range(len(data_sem_duracao)):
					data_sem_duracao[x].remove(data_sem_duracao[x][-2])

				# step22 contém agora só elementos que não estão em mudar_status
				for verificador in range(len(data_sem_duracao)):
					if data_sem_duracao[verificador] in mudar_status:
						step22.append(data[verificador])

				def list_diff(a, b):
					return [x for x in a if x not in b]

				data_diff = list_diff(data, step22)  # não selecionados ou seja nao contem o status desejado para trocar

				# COLOCAR ESTUDADO EM TODOS OS ITEMS DA LISTA SELECT
				for x in range(len(step22)):
					if step22[x][6][2] == '[color=#{}]Não Estudado[/color]'.format(color_hex):
						pass

					else:
						step22[x][6][0] = 'alert-circle'
						step22[x][6][1] = [1,0,0, 1]
						step22[x][6][2] = '[color=#{}]Não Estudado[/color]'.format(color_hex)

				if len(data_diff) == 0:
					data_diff = step22

				elif len(data_diff) != 0:
					for item in range(len(step22)):
						data_diff.append(step22[item])

				# CONVERTER PARA TUPLA TODOS OS DADOS DE DATA_DIFF
				for x in range(len(data_diff)):
					data_diff[x][6] = tuple(data_diff[x][6])
					data_diff[x] = tuple(data_diff[x])

				return data_diff

			def LastNaoEstudado(lista, select, color_hex='686fa3'):
				data_sem_duracao = []
				data = []
				mudar_status = []

				step22 = []
				for i in range(len(lista)):
					data.append([])

				# CONVERTER TUPLA PARA LISTA [()] - > [[]]
				for y in range(len(lista)):
					for x in range(len(lista[y])):
						if x == 6:
							data[y].append(list(lista[y][x]))
						else:
							data[y].append(lista[y][x])


				# RETIRAR AS COLUNAS DE DURAÇÃO, ACERTOS, ERROS E RENDIMENTO DA LISTA DATA
				for i in range(len(lista)):
					data_sem_duracao.append([])

				# CONVERTER TUPLA PARA LISTA [()] - > [[]]
				for y in range(len(lista)):
					for x in range(len(lista[y])):
						if x == 6:
							data_sem_duracao[y].append(list(lista[y][x]))
						else:
							data_sem_duracao[y].append(lista[y][x])

				# SELECIONADOS PARA MUDAR STATUS PARA ESTUDADO
				for i in range(len(select)):
					mudar_status.append([])

				# CONVERTER TUPLA PARA LISTA [()] - > [[]]
				for y in range(len(select)):
					for x in range(len(select[y])):
						if x == 5:
							mudar_status[y].append(list(select[y][x]))
						else:
							mudar_status[y].append(select[y][x])

				# TIRAR A COLUNA DE DURAÇÃO, ACERTOS, ERROS, RENDIMENTO
				for x in range(len(data_sem_duracao)):
					data_sem_duracao[x].remove(data_sem_duracao[x][-1])

				for x in range(len(data_sem_duracao)):
					data_sem_duracao[x].remove(data_sem_duracao[x][-1])

				for x in range(len(data_sem_duracao)):
					data_sem_duracao[x].remove(data_sem_duracao[x][-1])

				for x in range(len(data_sem_duracao)):
					data_sem_duracao[x].remove(data_sem_duracao[x][-2])

				# step22 contém agora só elementos que não estão em mudar_status
				for verificador in range(len(data_sem_duracao)):
					if data_sem_duracao[verificador] in mudar_status:
						step22.append(data[verificador])

				# COLOCAR ESTUDADO EM TODOS OS ITEMS DA LISTA SELECT
				for x in range(len(step22)):
					if step22[x][6][2] == '[color=#{}]Não Estudado[/color]'.format(color_hex):
						pass

					else:
						step22[x][6][0] = 'alert-circle'
						step22[x][6][1] = [1,0,0, 1]
						step22[x][6][2] = '[color=#{}]Não Estudado[/color]'.format(color_hex)

				# CONVERTER PARA TUPLA TODOS OS DADOS DE DATA_DIFF
				for x in range(len(step22)):
					step22[x][-1] = tuple(step22[x][-1])
					step22[x] = tuple(step22[x])

				return step22

			options = list(root.ids.cronograma22.children[0].children[0].get_row_checks())  # opções selecionadas para mudar status
			data_cronograma = colorData(organizerData(sortData(data_cronograma)))  # organizar, colorir e sort para o dado bruto
			estudadoList = rebuildDataStyle(options)  # colocar as opções selecionadas no padrão do dado motificado acima

			naoestudados = LastNaoEstudado(data_cronograma, estudadoList)
			naoestudados = defaultStyle(naoestudados)
			naoestudados = CronogramaTableStyle(organizerData(sortData(naoestudados)))

			data_cronograma = NaoEstudado(data_cronograma,estudadoList)  # aplicar a função estudado para as opções selecionadas em data
			data_cronograma = defaultStyle(data_cronograma)  # retornar o data modificado para o padrão bruto de data
			pickle.dump(data_cronograma, open("data_timeline.p", "wb"))

			# ALTERAR QUANTIDADE DE ESTUDADOS/ NÃO ESTUDADOS
			try:
				try:
					def count_Estudado(state, data):
						data_v = pickle.load((open("data_timeline.p", "rb")))
						count_estudado = 0
						count_naoestudado = 0

						for x in range(len(data_v)):
							if data_v[x][0] == str(data):
								if data_v[x][6][2] == 'Estudado':
									count_estudado += 1

						for x in range(len(data_v)):
							if data_v[x][0] == str(data):
								if data_v[x][6][2] == 'Não Estudado':
									count_naoestudado += 1

						try:
							total = count_estudado + count_naoestudado

							if total == 0:
								total = len(data_v)

							if state == True:
								valor = round(float(count_estudado / total * 100), 2)
								return str(valor) + ' %'

							elif state == False:
								valor = round(float(count_naoestudado / total * 100), 2)
								return str(valor) + ' %'
						except ZeroDivisionError:
							total = 1
					self.estudado = count_Estudado(True, str(self.data_selecionada))
					self.nao_estudado = count_Estudado(False, str(self.data_selecionada))
				except ValueError: pass
			except AttributeError:
				def count_Estudado(state):
					data_v = pickle.load((open("data_timeline.p", "rb")))
					count_estudado = 0
					count_naoestudado = 0

					from datetime import date
					today = date.today()

					for x in range(len(data_v)):
						if data_v[x][0] == str(today):
							if data_v[x][6][2] == 'Estudado':
								count_estudado += 1

					for x in range(len(data_v)):
						if data_v[x][0] == str(today):
							if data_v[x][6][2] == 'Não Estudado':
								count_naoestudado += 1

					try:
						total = count_estudado + count_naoestudado

						if total == 0:
							total = len(data_v)

						if state == True:
							valor = round(float(count_estudado / total * 100), 2)
							return str(valor) + ' %'

						elif state == False:
							valor = round(float(count_naoestudado / total * 100), 2)
							return str(valor) + ' %'
					except ZeroDivisionError:
						total = 1
				try:
					self.estudado = count_Estudado(True)
					self.nao_estudado = count_Estudado(False)
				except ValueError:
					pass

			# NOVOS DADOS A PARTIR DO BOTÃO DE PESQUISAR
			try:

				DataSearched = SearchByData(data_cronograma, str(self.data_selecionada))

				if len(DataSearched) >= 0:
					try:
						num = encontrarNumeroPagina(DataSearched, naoestudados[0], grid.rows_per_page_cronograma)
						if len(naoestudados) == 0: pass
						else:
							self.ids.cronograma22.children[0].children[0].update_row_data(self, AutoSizeTableRowsNum_Cronograma(DataSearched, grid.rows_per_page_cronograma + 1))
							toast("Status Alterado Com Sucesso!")
							try:
								for i in range(1, num):
									self.ids.cronograma22.children[0].children[0].avancarPagina()
							except TypeError:
								pass
					except IndexError:
						pass


					def refreshChecks(dt):
						try:
							self.ids.cronograma22.children[0].children[0].DoubleClickRefreshChecks()

						except IndexError:
							pass

					Clock.schedule_once(refreshChecks, 1)


			# NOVOS DADOS A PARTIR DA PAGINA INICIAL DO DIA ATUAL
			except AttributeError:
				today = date.today()
				DataSearched_today = SearchByData(data_cronograma, str(today))

				# AVANÇAR ATÉ A PÁGINA QUE VOCÊ SE ENCONTRA
				try:
					num = encontrarNumeroPagina(DataSearched_today, naoestudados[0], grid.rows_per_page_cronograma)
					if len(naoestudados) == 0: pass
					else:
						self.ids.cronograma22.children[0].children[0].update_row_data(self, AutoSizeTableRowsNum_Cronograma(DataSearched_today, grid.rows_per_page_cronograma + 1))
						toast("Status Alterado Com Sucesso!")
						try:
							for i in range(1, num):
								self.ids.cronograma22.children[0].children[0].avancarPagina()
						except TypeError:
							pass
				except IndexError:
					pass

				def refreshChecks(dt):
					try:
						self.ids.cronograma22.children[0].children[0].DoubleClickRefreshChecks()
					except IndexError:
						pass

				Clock.schedule_once(refreshChecks, 1.10)

		else:
			toast("Atenção: Nenhum Item Selecionado.")

	# ////////////////////////////////////////////////////////////////////////////
	# FUNÇÕES PARA ITEM BUSCADO POR DATA
	def show_date_picker(self):
		def month(string):
			if len(string) == 2:
				if string[0] == '0':
					return string[1]

				else:
					return string

		def takeday():
			try:
				return int(month(str(self.saveData[0])[8:10]))

			except AttributeError:
				pass

			except IndexError:
				pass


		date_dialog = MDDatePicker(day=takeday())
		date_dialog.bind(on_save=self.filtrar_item, on_cancel=self.on_cancel)

		date_dialog.min_year = 2019
		date_dialog.max_year = 2037
		#date_dialog.mode = 'range'

		# COR DOS MENUS
		date_dialog.primary_color = ("#{}".format(self.cor_aplicativo))
		date_dialog.accent_color = get_color_from_hex("#{}".format(self.cor_widget))
		date_dialog.selector_color = get_color_from_hex("#{}".format(self.cor_aplicativo))
		date_dialog.text_toolbar_color = get_color_from_hex("#{}".format(self.cor_widget))
		# date_dialog.input_field_background_color = (0.9569, 0.9647, 0.9922, 0.2)

		# COR DOS TEXTOS
		date_dialog.text_color = get_color_from_hex("#{}".format(self.cor_aplicativo))
		date_dialog.text_current_color = get_color_from_hex("#{}".format(self.cor_widget))
		date_dialog.text_button_color = get_color_from_hex("#{}".format(self.cor_aplicativo))
		# date_dialog.input_field_text_color = (0.4078, 0.4353, 0.6392, .5)

		try:
			date_dialog.year = int(str(self.saveData[0])[0:4])
			date_dialog.month = int(month(str(str(self.saveData[0])[5:7])))


		except AttributeError:
			pass

		except IndexError:
			pass

		date_dialog.open()
	def tabela_dados_filtrados (self):
		def count_Estudado(state, data):
			data_v = pickle.load((open("data_timeline.p", "rb")))
			count_estudado = 0
			count_naoestudado = 0


			for x in range(len(data_v)):
				if data_v[x][0] == str(data):
					if data_v[x][6][2] == 'Estudado':
						count_estudado += 1

			for x in range(len(data_v)):
				if data_v[x][0] == str(data):
					if data_v[x][6][2] == 'Não Estudado':
						count_naoestudado += 1

			try:
				total = count_estudado + count_naoestudado

				if total == 0:
					total = len(data_v)

				if state == True:
					valor = round(float(count_estudado / total * 100), 2)
					return str(valor) + ' %'

				elif state == False:
					valor = round(float(count_naoestudado / total * 100), 2)
					return str(valor) + ' %'
			except ZeroDivisionError:
				total = 1

		data_cronograma = pickle.load((open("data_timeline.p", "rb")))

		DataSearched = SearchByData(data_cronograma, str(self.data_selecionada))
		self.estudado_data = changeData(str(self.data_selecionada))
		self.nao_estudado_data = changeData(str(self.data_selecionada))
		try:
			self.estudado = count_Estudado(True, str(self.data_selecionada))
			self.nao_estudado = count_Estudado(False, str(self.data_selecionada))
		except ValueError: pass

		if len(DataSearched) >= 0:
			self.ids.cronograma22.children[0].children[0].update_row_data(self, AutoSizeTableRowsNum_Cronograma(DataSearched, grid.rows_per_page_cronograma + 1))
	def filtrar_item(self, instance, value, date_range):

		self.dataFiltrada = []
		self.dataFiltrada.append(value)
		self.data_selecionada = str(self.dataFiltrada[0])

		def adicionarNewTable(dt):
			self.tabela_dados_filtrados()

		def refreshChecks(dt):
			try: self.ids.cronograma22.children[0].children[0].DoubleClickRefreshChecks()
			except IndexError: pass

		Clock.schedule_once(adicionarNewTable, 0.5)
		Clock.schedule_once(refreshChecks, 1.10)
	def on_cancel(self, instance, value):
		pass

	# ////////////////////////////////////////////////////////////////////////////
	# FUNÇÕES AO ENTRAR NA PÁGINA CRONOGRAMA
	def on_enter(self, *args):

		def nextEvento(dt):
			def changeTime(label):
				return label.split(':')[0] + 'h' + label.split(':')[1] + 'min'

			def changeData(label):
				text = label.split('-')
				separator = '/'
				return separator.join([text[2], text[1], text[0]])

			data_cronograma = pickle.load((open("data_timeline.p", "rb")))
			next_event = sortData(onlyTimeGreater(eliminar_EscolhasRepetidas(data_cronograma)))

			if len(next_event) != 0:
				self.next_event_name = next_event[0][3]
				self.next_event_data = changeData(next_event[0][0])
				self.next_event_time = changeTime(next_event[0][1])

			if len(next_event) == 0:
				self.next_event_name = 'Sem Matéria'
				self.next_event_data = '00/00/0000'
				self.next_event_time = '00h00min'

		def count_Estudado(state):
			data_v = pickle.load((open("data_timeline.p", "rb")))
			count_estudado = 0
			count_naoestudado = 0

			from datetime import date
			today = date.today()

			for x in range(len(data_v)):
				if data_v[x][0] == str(today):
					if data_v[x][6][2] == 'Estudado':
						count_estudado += 1

			for x in range(len(data_v)):
				if data_v[x][0] == str(today):
					if data_v[x][6][2] == 'Não Estudado':
						count_naoestudado += 1

			try:
				total = count_estudado + count_naoestudado

				if total == 0:
					total = len(data_v)

				if state == True:
					valor = round(float(count_estudado / total * 100), 2)
					return str(valor) + ' %'

				elif state == False:
					valor = round(float(count_naoestudado / total * 100), 2)
					return str(valor) + ' %'
			except ZeroDivisionError:
				total = 1

		today = date.today()

		try:
			self.estudado_data = changeData(str(today))
			self.nao_estudado_data =changeData(str(today))
			self.estudado = count_Estudado(True)
			self.nao_estudado = count_Estudado(False)

		except ValueError:
			self.estudado = '0.0 %'
			self.nao_estudado = '0.0 %'

		data_cronograma = pickle.load((open("data_timeline.p", "rb")))

		next_event = sortData(onlyTimeGreater(eliminar_EscolhasRepetidas(data_cronograma)))

		if len(next_event) != 0:
			self.next_event_name = next_event[0][3]
			self.next_event_data = changeData(next_event[0][0])
			self.next_event_time = changeTime(next_event[0][1])

		if len(next_event) == 0:
			self.next_event_name = 'Sem Matéria'
			self.next_event_data = '00/00/0000'
			self.next_event_time = '00h00min'

		Clock.schedule_interval(nextEvento, 30)

		def refreshChecks(dt):
			try:
				self.ids.cronograma22.children[0].children[0].DoubleClickRefreshChecks()
			except IndexError:
				pass


		Clock.schedule_once(refreshChecks, 1.15)


class Cronograma_CriarItem(Screen):
	dialog8 = None
	cor_aplicativo = '686fa3'
	cor_widget = 'eef2fe'
	cor_widget_hover = 'f4f7fe'


	# DIALOGO PARA CONFIRMAR SE DESEJA APAGAR MATERIA ESPECIFICA
	def show_item_confirmation (self, *args):

		if not self.dialog8:
			self.dialog8 = MDDialog(
				# md_bg_color=(0.8980, 0.9215, 0.9843, 1)
				md_bg_color=(0.9019, 0.9215, 0.9843, 1),
				type="custom",
				size_hint=[0.4, 0.1],
				title='[color=686fa3][b]Item Adicionado![/color][/b]',
				text="[color=686fa3]Esse item foi adicionado com sucesso no seu cronograma![/color]",
				auto_dismiss=False,
				buttons=[
					MDFlatButton(
						text="[color=686fa3][b]CONCLUIR[/color][/b]",
						theme_text_color="Custom",
						on_release=self.close_dialog8
					)
				],
			)
		self.dialog8.open()



	# CANCELAR DIALOGO DE SE DESEJA APAGAR TÓPICO ESPECIFICO
	def close_dialog8(self, obj):
		# Close alert box
		self.dialog8.dismiss()

	value = NumericProperty(250)
	align = (1000, 1)



	def refreshTopicosSpinner(self, root, *args):
		self.data = pickle.load((open("data_subjects_topics.p", "rb")))
		if root.ids.spinnerAllMaterias.text != "Matérias":
			root.ids.spinnerTopicos.values = ()
			root.ids.spinnerTopicos.values = self.data[root.ids.spinnerAllMaterias.text][1]
			root.ids.spinnerTopicos.text = "Tópicos"

	class CategoriasSpinner(Spinner):
		def __init__(self, **kwargs):
			super().__init__(**kwargs)
			self.values = ['Teoria', 'Exercicios']
			self.dropdown_cls = SpinnerDropdown
			self.option_cls = SpinnerOptions
			self.color = [104 / 255, 111 / 255, 163 / 255, 1]
			self.bold = True
			self.dropdown_cls.max_height = self.height * 2 + 2 * 4
			self.text = "Categorias"

	class AllMateriasSpinner(Spinner):
		def __init__(self, **kwargs):
			super().__init__(**kwargs)
			self.dropdown_cls = SpinnerDropdown
			self.option_cls = SpinnerOptions
			self.color = [104 / 255, 111 / 255, 163 / 255, 1]
			self.bold = True
			self.dropdown_cls.max_height = self.height * 2 + 2 * 4
			self.text = "Matérias"


	class TopicosSpinner(Spinner):
		def __init__(self, **kwargs):
			super().__init__(**kwargs)
			self.dropdown_cls = SpinnerDropdown
			self.option_cls = SpinnerOptions
			self.color = [104 / 255, 111 / 255, 163 / 255, 1]
			self.bold = True
			self.dropdown_cls.max_height = self.height * 2 + 2 * 4
			self.text = "Tópicos"


	def on_saveData(self, instance, value, date_range):
		self.saveData = []
		self.saveData.append(value)


	def on_cancel(self, instance, value):
		pass

	def show_date_picker(self):
		def month(string):
			if len(string) == 2:
				if string[0] == '0':
					return string[1]

				else:
					return string

		def takeday():
			try:
				return int(month(str(self.saveData[0])[8:10]))

			except AttributeError:
				pass

			except IndexError:
				pass

		date_dialog = MDDatePicker(day=takeday())
		date_dialog.bind(on_save=self.on_saveData, on_cancel=self.on_cancel)

		date_dialog.min_year = 2019
		date_dialog.max_year = 2037
		#date_dialog.mode = 'range'

		# COR DOS MENUS
		date_dialog.primary_color = get_color_from_hex("#{}".format(self.cor_aplicativo))
		date_dialog.accent_color = get_color_from_hex("#{}".format(self.cor_widget))
		date_dialog.selector_color = get_color_from_hex("#{}".format(self.cor_aplicativo))
		date_dialog.text_toolbar_color = get_color_from_hex("#{}".format(self.cor_widget))
		# date_dialog.input_field_background_color = (0.9569, 0.9647, 0.9922, 0.2)

		# COR DOS TEXTOS
		date_dialog.text_color = get_color_from_hex("#{}".format(self.cor_aplicativo))
		date_dialog.text_current_color = get_color_from_hex("#{}".format(self.cor_widget))
		date_dialog.text_button_color = get_color_from_hex("#{}".format(self.cor_aplicativo))
		# date_dialog.input_field_text_color = (0.4078, 0.4353, 0.6392, .5)

		try:
			date_dialog.year = int(str(self.saveData[0])[0:4])
			date_dialog.month = int(month(str(str(self.saveData[0])[5:7])))


		except AttributeError:
			pass

		except IndexError:
			pass

		date_dialog.open()

	def show_time_picker(self):
		from datetime import datetime

		time_dialog = MDTimePicker()
		time_dialog.bind(time=self.get_time, on_save=self.on_saveTime)

		# COR DOS MENUS
		time_dialog.primary_color = get_color_from_hex('#{}'.format(self.cor_widget))
		time_dialog.accent_color = get_color_from_hex('#{}'.format(self.cor_widget_hover))
		time_dialog.selector_color = get_color_from_hex('#{}'.format(self.cor_aplicativo))
		time_dialog.text_toolbar_color = get_color_from_hex('#{}'.format(self.cor_aplicativo))

		# COR DOS TEXTOS
		time_dialog.text_color = get_color_from_hex('#{}'.format(self.cor_aplicativo))
		time_dialog.text_current_color = get_color_from_hex('#{}'.format(self.cor_widget_hover))
		time_dialog.text_button_color = get_color_from_hex('#{}'.format(self.cor_aplicativo))

		def convertMilitaryHour(string):
			converter = {'13': '01', '14': '02', '15': '03', '16': '04', '17': '05', '18': '06', '19': '07', '20': '08',
						 '21': '09', '22': '10', '23': '11', '00': '12'}
			string_split = string.split(':')
			if string_split[0] in list(converter.keys()):
				string_split[0] = converter[string_split[0]]

				time_dialog.am_pm = 'pm'

			return ':'.join(string_split)


		try:
			string = convertMilitaryHour(str(self.saveTime[0]))
			previous_time = datetime.strptime(string, '%H:%M:%S').time()
			time_dialog.set_time(previous_time)

		except AttributeError:
			pass

		except IndexError:
			pass

		time_dialog.open()

	def get_time(self, instance, time):
		return time

	def on_saveTime(self, instance, time):
		self.saveTime = []
		self.saveTime.append(str(time))



	def addToCronograma(self, root):
		def checkData(self):
			data_cronograma = pickle.load((open("data_timeline.p", "rb")))
			data_cronograma_list = []
			data_only_data_and_time = []

			for y in range(len(data_cronograma)):
				data_cronograma_list.append([])
				data_only_data_and_time.append([])
				for x in range(len(data_cronograma[y])):
					if x == 6:
						data_cronograma_list[y].append(list(data_cronograma[y][x]))
					else:
						data_cronograma_list[y].append(data_cronograma[y][x])

			# REMOVER TODAS AS COLUNAS EXCETO DATA E HORÁRIO
			for index in range(len(data_cronograma_list)):
				for item in range(0, 2):
					data_only_data_and_time[index].append(data_cronograma_list[index][item])

			return data_only_data_and_time

		lista_data_to_check = checkData(self)
		len_antigo = len(lista_data_to_check)
		try:
			# ADICIONAR A DATA E O HORÁRIO SELECIONADOS PARA LISTA_DATA, PARA DEPOIS VEFICIAR SE ESSE CONJUNTO DATA + HORARIO JÁ EXISTE NOS DADOS
			try:
				lista_data = [[]]
				lista_data[0].append(str(self.saveData[0]))
				lista_data[0].append(self.saveTime[0])
			except IndexError:
				pass

			# A DATA E O HORÁRIO ESCOLHIDO [NÃO] EXISTEM NOS DADOS
			if root.ids.spinnerCategorias.text != "Categorias" and root.ids.spinnerAllMaterias.text != "Matérias" and root.ids.spinnerTopicos.text != "Tópicos" and len(
					self.saveData) == 1 and len(
				self.saveTime) == 1 and root.ids.duracao_horas.text != "" and root.ids.duracao_minutos.text != "" and len(
				root.ids.duracao_horas.text) <= 2 and len(root.ids.duracao_minutos.text) <= 2 and (
					root.ids.duracao_horas.text + ':' + root.ids.duracao_minutos.text) != "00:00":

				if lista_data[0] not in lista_data_to_check:
					# CONDIÇÕES PARA ADICIONAR ZERO A ESQUERDA SE NECESSÁRIO
					if len(root.ids.duracao_horas.text) == 1:
						root.ids.duracao_horas.text = '0' + root.ids.duracao_horas.text

					if len(root.ids.duracao_horas.text) == 2:
						root.ids.duracao_horas.text = root.ids.duracao_horas.text

					if len(root.ids.duracao_minutos.text) == 1:
						root.ids.duracao_minutos.text = '0' + root.ids.duracao_minutos.text

					if len(root.ids.duracao_horas.text) == 2:
						root.ids.duracao_minutos.text = root.ids.duracao_minutos.text

					duration = root.ids.duracao_horas.text + ':' + root.ids.duracao_minutos.text + ':00'

					self.data_cronograma = pickle.load((open("data_timeline.p", "rb")))

					self.data_cronograma.append(
						(str(self.saveData[0]), str(self.saveTime[0]), root.ids.spinnerCategorias.text,
						 root.ids.spinnerAllMaterias.text, root.ids.spinnerTopicos.text, duration,
						 ("alert-circle", [1, 0, 0, 1], "Não Estudado"), '0','0','0.0 %'))

					root.ids.duracao_horas.text = '00'
					root.ids.duracao_minutos.text = '00'
					root.show_item_confirmation()
					# root.manager.current = 'Cronograma'

					# Refresh Data and Time List
					self.saveTime.clear()
					self.saveData.clear()

					pickle.dump(self.data_cronograma, open("data_timeline.p", "wb"))

					lista_data[0].clear()


				# A DATA E O HORÁRIO ESCOLHIDO [JÁ] EXISTEM NOS DADOS
				else:
					def changeTime(label):
						return label.split(':')[0] + 'h' + label.split(':')[1] + 'min'

					def changeData(label):
						text = label.split('-')
						separator = '/'
						return separator.join([text[2], text[1], text[0]])
					toast("Atenção: Você Já Possui um Evento Adicionado Para o Dia {} às {}".format(changeData(str(self.saveData[0])), changeTime(self.saveTime[0])))

			else:
				toast("Atenção: Todos Os Campos Devem Ser Preenchidos")

		except AttributeError:  # CASO NÃO TIVER SELECIONADO DATA E TEMPO
			toast("Atenção: Todos Os Campos Devem Ser Preenchidos")



	def on_leave(self, *args):
		self.ids.spinnerAllMaterias.values = ()
		self.ids.spinnerAllMaterias.text = "Matérias"
		self.ids.spinnerTopicos.text = 'Tópicos'
		self.ids.spinnerCategorias.text = 'Categorias'
		try:
			self.saveTime.clear()
			self.saveData.clear()
		except AttributeError: pass

	def on_enter(self, *args):
		self.data = pickle.load((open("data_subjects_topics.p", "rb")))
		self.ids.spinnerAllMaterias.values = tuple(self.data.keys())

		self.ids.spinnerAllMaterias.text = "Matérias"
		self.ids.spinnerTopicos.text = 'Tópicos'
		self.ids.spinnerCategorias.text = 'Categorias'

class Cronograma_MATERIAS_estudadas(Screen):
	value = NumericProperty(250)
	cor_aplicativo = '686fa3'
	cor_widget = 'eef2fe'
	cor_graph_estudados_line_default = 'eef2fe'

	zoom = NumericProperty(1)
	zoom2 = NumericProperty(1)

	estudado = StringProperty()
	estudado_data = StringProperty()
	nao_estudado = StringProperty()
	nao_estudado_data = StringProperty()

	next_event_name = StringProperty()
	next_event_data = StringProperty()
	next_event_time = StringProperty()

	def on_cancel(self, instance, value):
		pass

	def zoom_in(self):
		if self.zoom < 8:
			self.zoom *= 2

	def zoom_out(self):
		if self.zoom > 1:
			self.zoom /= 2

	def zoom_in_bar(self):
		if self.zoom2 < 8:
			self.zoom2 *= 2

	def zoom_out_bar(self):
		if self.zoom2 > 1:
			self.zoom2 /= 2

	def on_enter(self, *args):

		def nextEvento(dt):
			def changeTime(label):
				return label.split(':')[0] + 'h' + label.split(':')[1] + 'min'

			def changeData(label):
				text = label.split('-')
				separator = '/'
				return separator.join([text[2], text[1], text[0]])

			data_cronograma = pickle.load((open("data_timeline.p", "rb")))
			next_event = sortData(onlyTimeGreater(eliminar_EscolhasRepetidas(data_cronograma)))

			if len(next_event) != 0:
				self.next_event_name = next_event[0][3]
				self.next_event_data = changeData(next_event[0][0])
				self.next_event_time = changeTime(next_event[0][1])

			if len(next_event) == 0:
				self.next_event_name = 'Sem Matéria'
				self.next_event_data = '00/00/0000'
				self.next_event_time = '00h00min'

		def SearchByData(lista, string):
			step18 = []
			for i in range(len(lista)):
				step18.append([])

			# CONVERTER TUPLA PARA LISTA [()] - > [[]]
			for y in range(len(step18)):
				for x in range(len(lista[y])):
					step18[y].append(lista[y][x])

			step19 = []

			# VERIFICAR SE A DATA É IGUAL A DATA DA LISTA
			for w in range(len(step18)):
				if step18[w][0] == str(string):
					step19.append(step18[w])

			# CONVERTER PARA TUPLAR [[]] -> [()]
			for w in range(len(step19)):
				step19[w] = tuple(step19[w])

			return step19

		def count_Estudado(state):
			data_v = pickle.load((open("data_timeline.p", "rb")))
			count_estudado = 0
			count_naoestudado = 0

			from datetime import date
			today = date.today()

			for x in range(len(data_v)):
				if data_v[x][0] == str(today):
					if data_v[x][6][2] == 'Estudado':
						count_estudado += 1

			for x in range(len(data_v)):
				if data_v[x][0] == str(today):
					if data_v[x][6][2] == 'Não Estudado':
						count_naoestudado += 1

			try:
				total = count_estudado + count_naoestudado

				if total == 0:
					total = len(data_v)

				if state == True:
					valor = round(float(count_estudado / total * 100), 2)
					return str(valor) + ' %'

				elif state == False:
					valor = round(float(count_naoestudado / total * 100), 2)
					return str(valor) + ' %'
			except ZeroDivisionError:
				total = 1

		def changeTime(label):
			return label.split(':')[0] + 'h' + label.split(':')[1] + 'min'

		def changeData(label):
			text = label.split('-')
			separator = '/'
			return separator.join([text[2], text[1], text[0]])

		today = date.today()

		try:
			self.estudado_data = changeData(str(today))
			self.nao_estudado_data =changeData(str(today))
			self.estudado = count_Estudado(True)
			self.nao_estudado = count_Estudado(False)

		except ValueError:
			self.estudado = '0.0 %'
			self.nao_estudado = '0.0 %'

		data_cronograma = pickle.load((open("data_timeline.p", "rb")))

		next_event = sortData(onlyTimeGreater(eliminar_EscolhasRepetidas(data_cronograma)))

		if len(next_event) != 0:
			self.next_event_name = next_event[0][3]
			self.next_event_data = changeData(next_event[0][0])
			self.next_event_time = changeTime(next_event[0][1])

		if len(next_event) == 0:
			self.next_event_name = 'Sem Matéria'
			self.next_event_data = '00/00/0000'
			self.next_event_time = '00h00min'

		Clock.schedule_interval(nextEvento, 30)




		def plot_estudados_bar():
			estudados = plotEstudados_Bar(state=True)

			fig2, ax2 = plt.subplots(nrows=1, ncols=1)
			fig2 = plt.figure(facecolor='#{}'.format(self.cor_widget))
			ax2 = fig2.add_subplot(1, 1, 1)

			x = list(estudados.keys())
			y = list(estudados.values())

			plt.bar(x, y, color=[f'#{self.cor_aplicativo}'])
			plt.xticks(rotation=7)
			plt.grid(True, alpha = 0.2)

			ax2 = plt.axes()
			ax2.set_facecolor('#{}'.format(self.cor_graph_estudados_line_default))
			ax2.spines['bottom'].set_color('#{}'.format(self.cor_graph_estudados_line_default))
			ax2.spines['top'].set_color('#{}'.format(self.cor_graph_estudados_line_default))
			ax2.spines['left'].set_color('#{}'.format(self.cor_graph_estudados_line_default))
			ax2.spines['right'].set_color('#{}'.format(self.cor_graph_estudados_line_default))
			ax2.xaxis.label.set_color(f'#{self.cor_aplicativo}')
			ax2.yaxis.label.set_color(f'#{self.cor_aplicativo}')
			ax2.tick_params(axis='x', colors=f'#{self.cor_aplicativo}')
			ax2.tick_params(axis='y', colors=f'#{self.cor_aplicativo}')
			ax2.xaxis.set_tick_params(labelsize=8)

			self.ids.plot_estudados_bar.add_widget(FigureCanvasKivyAgg(plt.gcf()))

			estudados = []

		def plot_estudados():

			fig, ax = plt.subplots(nrows=1, ncols=1)
			fig = plt.figure(facecolor='#{}'.format(self.cor_widget))
			ax = fig.add_subplot(1, 1, 1)
			plot_data_estudados = estudados(separadorDicionario())
			x = list(plot_data_estudados.keys())
			y = list(plot_data_estudados.values())
			plt.plot(x, y, f'#{self.cor_aplicativo}', marker="o")
			plt.grid(True, alpha=0.2)
			plt.xticks(rotation=7)
			# plt.xlabel('x')
			# plt.ylabel('y')
			ax = plt.axes()
			ax.set_facecolor('#{}'.format(self.cor_graph_estudados_line_default))
			ax.spines['bottom'].set_color('#{}'.format(self.cor_graph_estudados_line_default))
			ax.spines['top'].set_color('#{}'.format(self.cor_graph_estudados_line_default))
			ax.spines['left'].set_color('#{}'.format(self.cor_graph_estudados_line_default))
			ax.spines['right'].set_color('#{}'.format(self.cor_graph_estudados_line_default))
			ax.xaxis.label.set_color(f'#{self.cor_aplicativo}')
			ax.yaxis.label.set_color(f'#{self.cor_aplicativo}')
			ax.tick_params(axis='x', colors=f'#{self.cor_aplicativo}')
			ax.tick_params(axis='y', colors=f'#{self.cor_aplicativo}')
			ax.fill_between(x, y, alpha = 0.2)
			ax.xaxis.set_tick_params(labelsize=8)
			self.ids.plot_estudados_line.add_widget(FigureCanvasKivyAgg(plt.gcf()))

			plot_data_estudados = []

		plot_estudados()
		plot_estudados_bar()

	def on_leave(self, *args):
		self.ids.plot_estudados_line.clear_widgets()
		self.ids.plot_estudados_bar.clear_widgets()

class Cronograma_MATERIAS_nao_estudadas(Screen):
	value = NumericProperty(250)
	cor_aplicativo = '686fa3'
	cor_widget = 'eef2fe'
	cor_graph_estudados_line_default = 'eef2fe'

	zoom = NumericProperty(1.0)
	zoom2 = NumericProperty(1.0)

	estudado = StringProperty()
	estudado_data = StringProperty()
	nao_estudado = StringProperty()
	nao_estudado_data = StringProperty()

	next_event_name = StringProperty()
	next_event_data = StringProperty()
	next_event_time = StringProperty()

	def read_or_new_pickle(path, default):
		if os.path.isfile(path):
			with open(path, "rb") as f:
				try:
					return pickle.load(f)
				except Exception:  # so many things could go wrong, can't be more specific.
					pass
		with open(path, "wb") as f:
			pickle.dump(default, f)
		return default

	data_cronograma = read_or_new_pickle(path="data_timeline.p", default=[])


	def zoom_in(self):
		if self.zoom < 8:
			self.zoom *= 2

	def zoom_out(self):
		if self.zoom > 1:
			self.zoom /= 2

	def zoom_in_bar(self):
		if self.zoom2 < 8:
			self.zoom2 *= 2

	def zoom_out_bar(self):
		if self.zoom2 > 1:
			self.zoom2 /= 2

	def on_enter(self, *args):

		def nextEvento(dt):
			def changeTime(label):
				return label.split(':')[0] + 'h' + label.split(':')[1] + 'min'

			def changeData(label):
				text = label.split('-')
				separator = '/'
				return separator.join([text[2], text[1], text[0]])

			data_cronograma = pickle.load((open("data_timeline.p", "rb")))
			next_event = sortData(onlyTimeGreater(eliminar_EscolhasRepetidas(data_cronograma)))

			if len(next_event) != 0:
				self.next_event_name = next_event[0][3]
				self.next_event_data = changeData(next_event[0][0])
				self.next_event_time = changeTime(next_event[0][1])

			if len(next_event) == 0:
				self.next_event_name = 'Sem Matéria'
				self.next_event_data = '00/00/0000'
				self.next_event_time = '00h00min'

		def SearchByData(lista, string):
			step18 = []
			for i in range(len(lista)):
				step18.append([])

			# CONVERTER TUPLA PARA LISTA [()] - > [[]]
			for y in range(len(step18)):
				for x in range(len(lista[y])):
					step18[y].append(lista[y][x])

			step19 = []

			# VERIFICAR SE A DATA É IGUAL A DATA DA LISTA
			for w in range(len(step18)):
				if step18[w][0] == str(string):
					step19.append(step18[w])

			# CONVERTER PARA TUPLAR [[]] -> [()]
			for w in range(len(step19)):
				step19[w] = tuple(step19[w])

			return step19

		def count_Estudado(state):
			data_v = pickle.load((open("data_timeline.p", "rb")))
			count_estudado = 0
			count_naoestudado = 0

			from datetime import date
			today = date.today()

			for x in range(len(data_v)):
				if data_v[x][0] == str(today):
					if data_v[x][6][2] == 'Estudado':
						count_estudado += 1

			for x in range(len(data_v)):
				if data_v[x][0] == str(today):
					if data_v[x][6][2] == 'Não Estudado':
						count_naoestudado += 1

			try:
				total = count_estudado + count_naoestudado

				if total == 0:
					total = len(data_v)

				if state == True:
					valor = round(float(count_estudado / total * 100), 2)
					return str(valor) + ' %'

				elif state == False:
					valor = round(float(count_naoestudado / total * 100), 2)
					return str(valor) + ' %'
			except ZeroDivisionError:
				total = 1

		def changeTime(label):
			return label.split(':')[0] + 'h' + label.split(':')[1] + 'min'

		def changeData(label):
			text = label.split('-')
			separator = '/'
			return separator.join([text[2], text[1], text[0]])

		today = date.today()

		try:
			self.estudado_data = changeData(str(today))
			self.nao_estudado_data =changeData(str(today))
			self.estudado = count_Estudado(True)
			self.nao_estudado = count_Estudado(False)

		except ValueError:
			self.estudado = '0.0 %'
			self.nao_estudado = '0.0 %'

		def AutoSizeTableRowsNum(lista, rows_per_page):
			lista = CronogramaTableStyle(colorData(organizerData(sortData(lista))))

			if len(lista) == 0:
				return createEmptyRow(createEmptyRow(lista))

			if len(lista) == 1:
				return createEmptyRow(lista)

			if len(lista) > 1:
				def sequence(rows_per_page, data):
					a = {}
					a[0] = rows_per_page
					for i in list(range(1, len(data))):
						a[i] = a[i - 1] + 5
					return list(a.values())

				divisores = sequence(rows_per_page, lista)
				if len(lista) in divisores:
					return createEmptyRow(lista)
				else:
					return lista

		data_cronograma = pickle.load((open("data_timeline.p", "rb")))
		DataSearched_today = SearchByData(data_cronograma, str(today))

		next_event = sortData(onlyTimeGreater(eliminar_EscolhasRepetidas(data_cronograma)))

		if len(next_event) != 0:
			self.next_event_name = next_event[0][3]
			self.next_event_data = changeData(next_event[0][0])
			self.next_event_time = changeTime(next_event[0][1])

		if len(next_event) == 0:
			self.next_event_name = 'Sem Matéria'
			self.next_event_data = '00/00/0000'
			self.next_event_time = '00h00min'

		Clock.schedule_interval(nextEvento, 30)



		def adicionar_Tabela(dt):
			pass
			#self.ids.cronograma22.add_widget(data_tables)
			#self.ids.cronograma22.children[-1].pos_hint = {'center_x': .5,'center_y': .5}

		def remover_spin(dt):
			pass
			#self.ids.cronograma22.remove_widget(self.ids.cronograma22.children[-1])

		#Clock.schedule_once(adicionar_Tabela, 1.05)
		#Clock.schedule_once(remover_spin, 1.05)
		def plot_estudados_bar():
			estudados = plotEstudados_Bar(state=False)

			fig2, ax2 = plt.subplots(nrows=1, ncols=1)
			fig2 = plt.figure(facecolor='#{}'.format(self.cor_widget))
			ax2 = fig2.add_subplot(1, 1, 1)

			x = list(estudados.keys())
			y = list(estudados.values())

			plt.bar(x, y, color=[f'#{self.cor_aplicativo}'])
			plt.xticks(rotation=7)
			plt.grid(True, alpha = 0.2)

			ax2 = plt.axes()
			ax2.set_facecolor('#{}'.format(self.cor_graph_estudados_line_default))
			ax2.spines['bottom'].set_color('#{}'.format(self.cor_graph_estudados_line_default))
			ax2.spines['top'].set_color('#{}'.format(self.cor_graph_estudados_line_default))
			ax2.spines['left'].set_color('#{}'.format(self.cor_graph_estudados_line_default))
			ax2.spines['right'].set_color('#{}'.format(self.cor_graph_estudados_line_default))
			ax2.xaxis.label.set_color(f'#{self.cor_aplicativo}')
			ax2.yaxis.label.set_color(f'#{self.cor_aplicativo}')
			ax2.tick_params(axis='x', colors=f'#{self.cor_aplicativo}')
			ax2.tick_params(axis='y', colors=f'#{self.cor_aplicativo}')
			ax2.xaxis.set_tick_params(labelsize=8)

			self.ids.plot_estudados_bar.add_widget(FigureCanvasKivyAgg(plt.gcf()))

			estudados = []

		def plot_estudados():

			fig, ax = plt.subplots(nrows=1, ncols=1)
			fig = plt.figure(facecolor='#{}'.format(self.cor_widget))
			ax = fig.add_subplot(1, 1, 1)
			plot_data_estudados = nao_estudados(separadorDicionario())
			x = list(plot_data_estudados.keys())
			y = list(plot_data_estudados.values())
			plt.plot(x, y, f'#{self.cor_aplicativo}', marker="o")
			plt.grid(True, alpha=0.2)
			plt.xticks(rotation=7)
			# plt.xlabel('x')
			# plt.ylabel('y')
			ax = plt.axes()
			ax.set_facecolor('#{}'.format(self.cor_graph_estudados_line_default))
			ax.spines['bottom'].set_color('#{}'.format(self.cor_graph_estudados_line_default))
			ax.spines['top'].set_color('#{}'.format(self.cor_graph_estudados_line_default))
			ax.spines['left'].set_color('#{}'.format(self.cor_graph_estudados_line_default))
			ax.spines['right'].set_color('#{}'.format(self.cor_graph_estudados_line_default))
			ax.xaxis.label.set_color(f'#{self.cor_aplicativo}')
			ax.yaxis.label.set_color(f'#{self.cor_aplicativo}')
			ax.tick_params(axis='x', colors=f'#{self.cor_aplicativo}')
			ax.tick_params(axis='y', colors=f'#{self.cor_aplicativo}')
			ax.fill_between(x, y, alpha = 0.2)
			ax.xaxis.set_tick_params(labelsize=8)
			self.ids.plot_estudados_line.add_widget(FigureCanvasKivyAgg(plt.gcf()))

			plot_data_estudados = []

		plot_estudados()
		plot_estudados_bar()

	def on_leave(self, *args):
		self.ids.plot_estudados_line.clear_widgets()
		self.ids.plot_estudados_bar.clear_widgets()


class Rendimento(Screen):
	# CRIAR NOVO ARQUIVO DATA_CRONOGRAMA SE NÃO EXISTIR
	def read_or_new_pickle(path, default):
		if os.path.isfile(path):
			with open(path, "rb") as f:
				try:
					return pickle.load(f)
				except Exception:  # so many things could go wrong, can't be more specific.
					pass
		with open(path, "wb") as f:
			pickle.dump(default, f)
		return default
	data_cronograma = read_or_new_pickle(path="data_timeline.p", default=[])

	dialog10 = None
	dialog11 = None
	acertos_erros_zoom_dialog = None

	zoom_bar_plot = NumericProperty(1)

	confirmar_remover = None
	value = NumericProperty(250)
	cor_aplicativo = '686fa3'
	cor_widget = 'eef2fe'
	cor_widget_hover = 'f4f7fe'
	cor_widget_on_press = 'cad1e7'
	cor_widget_on_leave = 'eef2fe'
	cor_graph_line_default = 'eef2fe'

	acertos = StringProperty()
	acertos_this_week = StringProperty()
	erros = StringProperty()
	erros_this_week = StringProperty()

	today = date.today()



	# ////////////////////////////////////////////////////////////////////////////
	# ATUALIZAR INFORMAÇÕES SOBRE MAIOR E MENOR TAXA DE ACERTO
	try:
		melhor_rendimento_list = findBestRendimento(str(today), True)
		pior_rendimento_list = findBestRendimento(str(today), False)

		melhor_rendimento = StringProperty(melhor_rendimento_list[0])
		materia_melhor_rendimento = StringProperty(melhor_rendimento_list[1])
		topico_melhor_rendimento = StringProperty(melhor_rendimento_list[2])

		pior_rendimento = StringProperty(pior_rendimento_list[0])
		materia_pior_rendimento = StringProperty(pior_rendimento_list[1])
		topico_pior_rendimento = StringProperty(pior_rendimento_list[2])

	except ValueError:
		melhor_rendimento = StringProperty('0.0 %')
		pior_rendimento = StringProperty('0.0 %')
		topico_melhor_rendimento = StringProperty('Sem Tópico')
		materia_melhor_rendimento = StringProperty('Sem Matéria')
		materia_pior_rendimento = StringProperty('Sem Matéria')
		topico_pior_rendimento = StringProperty('Sem Tópico')

	data = StringProperty(str(changeData(str(today))))   # CONVERTER A DATA (ANO-MES-DIA) ---> (DIA/MES/ANO)

	# ////////////////////////////////////////////////////////////////////////////
	# TABELA DOS EXERCICIOS
	class Tabela_Exercicios(MDBoxLayout):
		def __init__(self,**kwargs):
			super().__init__(**kwargs)
			today = date.today()
			#Rendimento.data = changeData(str(today))

			self.data_exercicios = pickle.load((open("data_timeline.p", "rb")))
			self.today = date.today()
			self.data_today = SearchByData(self.data_exercicios, str(self.today))

			data_table_exercicios = MDDataTable(
				background_color_header=get_color_from_hex("#eef2fe"),
				background_color_selected_cell=get_color_from_hex("#f2f5fc"),
				background_color_cell=(0.9333, 0.9490, 0.9960, 1),
				size_hint=(1, 1),
				elevation=0,
				check=True,
				use_pagination=True,
				rows_num=grid.rows_per_page_cronograma,
				column_data=[("[color=#686fa3]Data[/color]", dp(grid.tabela_cronograma_dp_data)),
							 ("[color=#686fa3]Horário[/color]", dp(grid.tabela_cronograma_dp_horario)),
							 ("[color=#686fa3]Categoria[/color]", dp(grid.tabela_cronograma_dp_categoria)),
							 ("[color=#686fa3]Matéria[/color]", dp(grid.tabela_cronograma_dp_materia)),
							 ("[color=#686fa3]Tópico[/color]", dp(grid.tabela_cronograma_dp_topico)),
							 ("[color=#686fa3]Acertos[/color]", dp(grid.tabela_cronograma_dp_acertos)),
							 ("[color=#686fa3]Erros[/color]", dp(grid.tabela_cronograma_dp_erros)),
							 ("[color=#686fa3]Taxa de Acerto[/color]", dp(grid.tabela_cronograma_dp_taxa))],
				row_data=AutoSizeTableRowsNum_Exercicios(self.data_today, grid.rows_per_page_cronograma + 1))

			self.add_widget(data_table_exercicios)


	# ////////////////////////////////////////////////////////////////////////////
	# FUNÇÕES PARA ABRIR E FECHAR BOX DIALOG, ALTERAR QUANTIDADE DE ACERTOS E ERROS
	def dialog_change_Acertos_Erros(self, root, *args):
		try:
			if len(root.ids.tabela_exercicios.children[0].children[0].get_row_checks()) > 0:
				if not self.dialog11:
					self.dialog11 = MDDialog(
						title=f'[color={self.cor_aplicativo}]Alterar Acertos e Erros[/color]',
						md_bg_color=(0.9019, 0.9215, 0.9843, 1),
						type="custom",
						auto_dismiss=True,
						content_cls=Conteudo_Acertos_Erros(),
						buttons=[
							MDFlatButton(
								text=f"[color={self.cor_aplicativo}][b]CANCELAR[/color][/b]",
								theme_text_color="Custom",
								on_release=self.close_dialog_change_Acertos_Erros
							),
							MDFlatButton(
								text=f"[color={self.cor_aplicativo}][b]ALTERAR[/color][/b]",
								theme_text_color="Custom",
								on_release=root.alterar_Acertos_Erros,
								on_press=self.close_dialog_change_Acertos_Erros
							)
						]
					)

				self.dialog11.open()

			else:
				toast("Atenção: Nenhum Item Selecionado.")
		except AttributeError:
			pass
	def change_Acertos_Erros(self):
		pass
	def close_dialog_change_Acertos_Erros(self, obj):
		self.dialog11.dismiss()
	def alterar_Acertos_Erros(self, root):
		acertos = str(self.dialog11.content_cls.ids.acertos.text)
		erros = str(self.dialog11.content_cls.ids.erros.text)
		options_to_change = list(self.ids.tabela_exercicios.children[0].children[0].get_row_checks())

		def encontrarNumeroPagina_Exercicios(data, name_to_search, size):
			def ExerciciosTableStyle_finder(lista):
				step7 = []
				exercicios_only = []

				for i in range(len(lista)):
					step7.append([])

				# CONVERTER TUPLA PARA LISTA [()] - > [[]]
				for y in range(len(step7)):
					for x in range(len(lista[y])):
						step7[y].append(lista[y][x])

				# TIRAR A COLUNA DE DURAÇÃO,Status
				for x in range(len(step7)):
					step7[x].remove(step7[x][5])

				for x in range(len(step7)):
					step7[x].remove(step7[x][5])

				for i in range(len(step7)):
					if step7[i][2] == 'Exercicios':
						exercicios_only.append(step7[i])

				# CONVERTER PARA TUPLAR [[]] -> [()]
				for j in range(len(exercicios_only)):
					exercicios_only[j] = tuple(exercicios_only[j])

				return exercicios_only
			data = ExerciciosTableStyle_finder(organizerData(sortData(data)))
			# SEPARAR EM 5 ELEMENTOS POR LISTA
			list_separator = list()
			for i in range(0, len(data), size):
				list_separator.append(data[i:i + size])

			# SEPARAR EM PÁGINA DICT[X] COM VALORES CONTENDO OS ITEMS DA PÁGINA X
			dict_order = {}
			for x in range(len(list_separator)):
				dict_order[x + 1] = list_separator[x]

			# PROCURAR O ELEMENTO DESEJADO (NAME_TO_SEARCH) EM DICT_ORDER E RETORNAR A PÁGINA QUE SE ENCONTRA (X)
			for num_page in range(1, len(dict_order.keys()) + 1):
				for index in range(len(dict_order[num_page])):
					if dict_order[num_page][index] == name_to_search:
						return int(num_page)
		def calcularTaxaAcerto(acertos, erros):
			if acertos != 0 and erros != 0:
				return str(round(float(acertos / (acertos + erros) * 100), 2)) + ' %'
			if acertos == 0 and erros == 0:
				return "0.0 %"
			else:
				# round(float(count_estudado / total * 100), 2)
				return str(round(float(acertos / (acertos + erros) * 100), 2)) + ' %'
		def alterar(options, acertos, erros):
			data_cronograma = pickle.load((open("data_timeline.p", "rb")))

			def RegEx(string):
				try:
					label = re.findall(r'\]+[a-zA-Z0-9]+\[', string)
					label[0] = label[0][1:-1]
					return label[0]
				except IndexError:
					pass

			def defaultStyle(lista):
				step14 = []
				for i in range(len(lista)):
					step14.append([])
				for y in range(len(step14)):
					for x in range(len(lista[y])):
						step14[y].append(lista[y][x])

				for x in range(len(step14)):
					if step14[x] == [' ', ' ', ' ', ' ', ' ', ' ', ' ']:
						pass
					else:
						step14[x][0] = str(
							step14[x][0][15:25][-4:] + '-' + step14[x][0][15:25][-7:-5] + '-' + step14[x][0][15:25][
																								-10:-8])
						step14[x][1] = str(step14[x][1][15:17] + ':' + step14[x][1][18:20] + ':00')
						step14[x][2] = RegEx(step14[x][2])
						step14[x][3] = RegEx(step14[x][3])
						step14[x][4] = RegEx(step14[x][4])
						step14[x][5] = RegEx(step14[x][5])
						step14[x][6] = RegEx(step14[x][6])
						step14[x][7] = RegEx(step14[x][7])

				for x in range(len(step14)):
					step14[x] = tuple(step14[x])

				return step14

			def calcularTaxaAcerto(acertos, erros):
				if acertos != 0 and erros != 0:
					return str(round(float(acertos/(acertos+erros) * 100), 2)) + ' %'
				if acertos == 0 and erros == 0:
					return "0.0 %"
				else:
					#round(float(count_estudado / total * 100), 2)
					return str(round(float(acertos/(acertos+erros) * 100), 2)) + ' %'

			options_full = defaultStyle(options)

			all_data_in_lista = []
			exercicios_only = []
			options_in_lista = []

			for i in range(len(data_cronograma)):
				all_data_in_lista.append([])
				exercicios_only.append([])
			for i in range(len(options_full)):
				options_in_lista.append([])

			# CONVERTER TUPLA PARA LISTA [()] - > [[]]
			for y in range(len(all_data_in_lista)):
				for x in range(len(data_cronograma[y])):
					all_data_in_lista[y].append(data_cronograma[y][x])
					exercicios_only[y].append(data_cronograma[y][x])
			for y in range(len(options_full)):
				for x in range(len(options_full[y])):
					options_in_lista[y].append(options_full[y][x])

			# TIRAR A COLUNA DE DURAÇÃO,Status
			for x in range(len(exercicios_only)):
				exercicios_only[x].remove(exercicios_only[x][5])
			for x in range(len(exercicios_only)):
				exercicios_only[x].remove(exercicios_only[x][5])
			for x in range(len(exercicios_only)):
				exercicios_only[x].remove(exercicios_only[x][7])

			for x in range(len(options_in_lista)):
				options_in_lista[x].remove(options_in_lista[x][7])

			for x in range(len(exercicios_only)):
				for y in range(len(options_in_lista)):
					if exercicios_only[x] == options_in_lista[y]:
						all_data_in_lista[x][7] = acertos
						all_data_in_lista[x][8] = erros

			for index in range(len(all_data_in_lista)):
				all_data_in_lista[index][9] = calcularTaxaAcerto(int(all_data_in_lista[index][7]),
																 int(all_data_in_lista[index][8]))

			for j in range(len(all_data_in_lista)):
				all_data_in_lista[j] = tuple(all_data_in_lista[j])

			return all_data_in_lista
		def default(options):
			def RegEx(string):
				try:
					label = re.findall(r'\]+[a-zA-Z0-9]+\[', string)
					label[0] = label[0][1:-1]
					return label[0]
				except IndexError:
					pass
			def defaultStyle(lista):
				step14 = []
				for i in range(len(lista)):
					step14.append([])
				for y in range(len(step14)):
					for x in range(len(lista[y])):
						step14[y].append(lista[y][x])

				for x in range(len(step14)):
					if step14[x] == [' ', ' ', ' ', ' ', ' ', ' ', ' ']:
						pass
					else:
						step14[x][0] = str(
							step14[x][0][15:25][-4:] + '-' + step14[x][0][15:25][-7:-5] + '-' + step14[x][0][15:25][
																								-10:-8])
						step14[x][1] = str(step14[x][1][15:17] + ':' + step14[x][1][18:20] + ':00')
						step14[x][2] = RegEx(step14[x][2])
						step14[x][3] = RegEx(step14[x][3])
						step14[x][4] = RegEx(step14[x][4])
						step14[x][5] = RegEx(step14[x][5])
						step14[x][6] = RegEx(step14[x][6])
						step14[x][7] = RegEx(step14[x][7])

				for x in range(len(step14)):
					step14[x] = tuple(step14[x])

				return step14

			def changeTime(label):
				return label.split(':')[0] + 'h' + label.split(':')[1] + 'min'

			def changeData(label):
				text = label.split('-')
				separator = '/'
				return separator.join([text[2], text[1], text[0]])

			default_data = defaultStyle(options)
			default_data_in_lista = []

			for x in range(len(default_data)):
				default_data_in_lista.append([])

			for y in range(len(default_data)):
				for x in range(len(default_data[y])):
					default_data_in_lista[y].append(default_data[y][x])

			for x in range(len(default_data_in_lista)):
				default_data_in_lista[x][0] = changeData(default_data_in_lista[x][0])
				default_data_in_lista[x][1] = changeTime(default_data_in_lista[x][1])
				try:
					default_data_in_lista[x][7] = calcularTaxaAcerto(int(default_data_in_lista[x][5]),int(default_data_in_lista[x][6]))
				except TypeError: pass

			for x in range(len(default_data_in_lista)):
				default_data_in_lista[x] = tuple(default_data_in_lista[x])

			return default_data_in_lista

		if acertos == '00' or acertos == '':
			acertos = '0'
		if erros =='00' or erros =='':
			erros = '0'

		data_cronograma = alterar(options_to_change, acertos, erros)
		pickle.dump(data_cronograma, open("data_timeline.p", "wb"))
		data_cronograma = pickle.load((open("data_timeline.p", "rb")))

		options_last = default(options_to_change)
		option_last_modified = list(options_last[0])
		option_last_modified[5] = acertos
		option_last_modified[6] = erros
		option_last_modified[7] = calcularTaxaAcerto(int(option_last_modified[5]), int(option_last_modified[6]))
		option_last_modified = tuple(option_last_modified)

		# ALTERAR ACERTOS E ERROS DE ITENS FILTRADOS
		try:
			def AutoSizeTableRowsNum(lista, rows_per_page):
				# lista = CronogramaTableStyle(colorData(organizerData(sortData(lista))))
				lista = ExerciciosTableStyle(colorDataExercicios(organizerData(sortData(lista))))

				if len(lista) == 0:
					return createEmptyRowExercicios(createEmptyRowExercicios(lista))

				if len(lista) == 1:
					return createEmptyRowExercicios(lista)

				if len(lista) > 1:
					def sequence(rows_per_page, data):
						a = {}
						a[0] = rows_per_page
						for i in list(range(1, len(data))):
							a[i] = a[i - 1] + 5
						return list(a.values())

					divisores = sequence(rows_per_page, lista)
					if len(lista) in divisores:
						return createEmptyRowExercicios(lista)
					else:
						return lista
			DataSearched = SearchByData(data_cronograma, str(self.data_selecionada))
			num_page_ex = encontrarNumeroPagina_Exercicios(DataSearched, option_last_modified,grid.rows_per_page_cronograma)

			del options_last
			self.acertos = count_acertos(data_cronograma, True)
			self.acertos_this_week = count_acertos_weekly(data_cronograma, True)
			self.erros = count_acertos(data_cronograma, False)
			self.erros_this_week = count_acertos_weekly(data_cronograma, False)
			self.ids.tabela_exercicios.children[0].children[0].update_row_data(self, AutoSizeTableRowsNum(DataSearched,grid.rows_per_page_cronograma + 1))
			try:
				for i in range(1, num_page_ex):
					self.ids.tabela_exercicios.children[0].children[0].avancarPagina()
			except TypeError: pass

			toast('Alteração Concluída com Sucesso.')

			# ATUALIZAR INFORMAÇÕES SOBRE MAIOR E MENOR TAXA DE ACERTO
			try:
				melhor_rendimento_list = findBestRendimento(str(self.data_selecionada), True)
				pior_rendimento_list = findBestRendimento(str(self.data_selecionada), False)

				self.melhor_rendimento = melhor_rendimento_list[0]
				self.materia_melhor_rendimento = melhor_rendimento_list[1]
				self.topico_melhor_rendimento = melhor_rendimento_list[2]

				self.pior_rendimento = pior_rendimento_list[0]
				self.materia_pior_rendimento = pior_rendimento_list[1]
				self.topico_pior_rendimento = pior_rendimento_list[2]

			except ValueError:
				self.melhor_rendimento = '0.0 %'
				self.pior_rendimento = '0.0 %'
				self.topico_melhor_rendimento = 'Sem Tópico'
				self.materia_melhor_rendimento = 'Sem Matéria'
				self.materia_pior_rendimento = 'Sem Matéria'
				self.topico_pior_rendimento = 'Sem Tópico'
			def refreshChecks(dt):
				try:
					self.ids.tabela_exercicios.children[0].children[0].DoubleClickRefreshChecks()
				except IndexError:
					pass

			Clock.schedule_once(refreshChecks, 1)

		# ALTERAR ACERTOS E ERROS DA PÁGINA INICIAL
		except AttributeError:
			today = date.today()
			DataSearched_today = SearchByData(data_cronograma, str(today))
			num_page_ex = encontrarNumeroPagina_Exercicios(DataSearched_today, option_last_modified, grid.rows_per_page_cronograma)

			del options_last
			self.acertos = count_acertos(data_cronograma, True)
			self.acertos_this_week = count_acertos_weekly(data_cronograma, True)
			self.erros = count_acertos(data_cronograma, False)
			self.erros_this_week = count_acertos_weekly(data_cronograma, False)
			self.ids.tabela_exercicios.children[0].children[0].update_row_data(self, AutoSizeTableRowsNum_Exercicios(DataSearched_today,grid.rows_per_page_cronograma + 1))
			try:
				for i in range(1, num_page_ex):
					self.ids.tabela_exercicios.children[0].children[0].avancarPagina()
			except TypeError: pass

			toast('Alteração Concluída com Sucesso.')

			# ATUALIZAR INFORMAÇÕES SOBRE MAIOR E MENOR TAXA DE ACERTO
			try:
				melhor_rendimento_list = findBestRendimento(str(today), True)
				pior_rendimento_list = findBestRendimento(str(today), False)

				self.melhor_rendimento = melhor_rendimento_list[0]
				self.materia_melhor_rendimento = melhor_rendimento_list[1]
				self.topico_melhor_rendimento = melhor_rendimento_list[2]

				self.pior_rendimento = pior_rendimento_list[0]
				self.materia_pior_rendimento = pior_rendimento_list[1]
				self.topico_pior_rendimento = pior_rendimento_list[2]

			except ValueError:
				self.melhor_rendimento = '0.0 %'
				self.pior_rendimento = '0.0 %'
				self.topico_melhor_rendimento = 'Sem Tópico'
				self.materia_melhor_rendimento = 'Sem Matéria'
				self.materia_pior_rendimento = 'Sem Matéria'
				self.topico_pior_rendimento = 'Sem Tópico'
			def refreshChecks(dt):
				try:
					self.ids.tabela_exercicios.children[0].children[0].DoubleClickRefreshChecks()
				except IndexError:
					pass
			Clock.schedule_once(refreshChecks, 1)


	# ////////////////////////////////////////////////////////////////////////////
	# FUNÇÕES RELACIONADAS A FILTRAR ITEM POR DATA, ABRIR CALENDARIO, FILTRAR POR DATA SELECIONADA EM CALENDARIO
	def show_date_picker(self):
		def month(string):
			if len(string) == 2:
				if string[0] == '0':
					return string[1]

				else:
					return string

		def takeday():
			try:
				return int(month(str(self.saveData[0])[8:10]))

			except AttributeError:
				pass

			except IndexError:
				pass

		date_dialog = MDDatePicker(day=takeday())
		date_dialog.bind(on_save=self.filtrar_item, on_cancel=self.on_cancel)

		date_dialog.min_year = 2019
		date_dialog.max_year = 2037
		# date_dialog.mode = 'range'

		# COR DOS MENUS
		date_dialog.primary_color = ("#{}".format(self.cor_aplicativo))
		date_dialog.accent_color = get_color_from_hex("#{}".format(self.cor_widget))
		date_dialog.selector_color = get_color_from_hex("#{}".format(self.cor_aplicativo))
		date_dialog.text_toolbar_color = get_color_from_hex("#{}".format(self.cor_widget))
		# date_dialog.input_field_background_color = (0.9569, 0.9647, 0.9922, 0.2)

		# COR DOS TEXTOS
		date_dialog.text_color = get_color_from_hex("#{}".format(self.cor_aplicativo))
		date_dialog.text_current_color = get_color_from_hex("#{}".format(self.cor_widget))
		date_dialog.text_button_color = get_color_from_hex("#{}".format(self.cor_aplicativo))
		# date_dialog.input_field_text_color = (0.4078, 0.4353, 0.6392, .5)

		try:
			date_dialog.year = int(str(self.saveData[0])[0:4])
			date_dialog.month = int(month(str(str(self.saveData[0])[5:7])))

		except AttributeError:
			pass

		except IndexError:
			pass

		date_dialog.open()
	def filtrar_item(self, instance, value, date_range):

		self.dataFiltrada = []
		self.dataFiltrada.append(value)
		self.data_selecionada = str(self.dataFiltrada[0])

		def adicionarNewTable(dt):
			self.tabela_dados_filtrados()

		def refreshChecks(dt):
			try:
				self.ids.tabela_exercicios.children[0].children[0].DoubleClickRefreshChecks()
			except IndexError:
				pass

		Clock.schedule_once(adicionarNewTable, 0.5)
		Clock.schedule_once(refreshChecks, 1.10)
	def tabela_dados_filtrados(self):

		data_cronograma = pickle.load((open("data_timeline.p", "rb")))

		DataSearched = SearchByData(data_cronograma, str(self.data_selecionada))
		self.data = changeData(str(self.data_selecionada))

		# ATUALIZAR INFORMAÇÕES SOBRE MAIOR E MENOR TAXA DE ACERTO
		try:
			melhor_rendimento_list = findBestRendimento(str(self.data_selecionada), True)
			pior_rendimento_list = findBestRendimento(str(self.data_selecionada), False)

			self.melhor_rendimento = melhor_rendimento_list[0]
			self.materia_melhor_rendimento = melhor_rendimento_list[1]
			self.topico_melhor_rendimento = melhor_rendimento_list[2]

			self.pior_rendimento = pior_rendimento_list[0]
			self.materia_pior_rendimento = pior_rendimento_list[1]
			self.topico_pior_rendimento = pior_rendimento_list[2]

		except ValueError:
			self.melhor_rendimento = '0.0 %'
			self.pior_rendimento = '0.0 %'
			self.topico_melhor_rendimento = 'Sem Tópico'
			self.materia_melhor_rendimento = 'Sem Matéria'
			self.materia_pior_rendimento = 'Sem Matéria'
			self.topico_pior_rendimento = 'Sem Tópico'

		if len(DataSearched) >= 0:
			self.ids.tabela_exercicios.children[0].children[0].update_row_data(self, AutoSizeTableRowsNum_Exercicios(DataSearched,
																							  grid.rows_per_page_cronograma + 1))
	def on_cancel(self, instance, value):
		pass

	# ////////////////////////////////////////////////////////////////////////////
	# FUNÇÕES PARA SEREM ATIVAS AO ENTRAR, SAIR DA PAGINA RENDIMENTOS
	def on_enter(self, *args):
		data_exercicios = pickle.load((open("data_timeline.p", "rb")))

		# CONTAR ACERTOS E ERROS
		self.acertos = count_acertos(data_exercicios, True)
		self.acertos_this_week = count_acertos_weekly(data_exercicios, True)
		self.erros = count_acertos(data_exercicios, False)
		self.erros_this_week = count_acertos_weekly(data_exercicios, False)

		# ENCONTRAR MAIOR E MENOR TAXA DE RENDIMENTO
		try:
			# ATUALIZAR INFORMAÇÕES SOBRE MAIOR E MENOR TAXA DE ACERTO - DATA FILTRADA
			try:
				melhor_rendimento_list = findBestRendimento(str(self.data_selecionada), True)
				pior_rendimento_list = findBestRendimento(str(self.data_selecionada), False)

				self.melhor_rendimento = melhor_rendimento_list[0]
				self.materia_melhor_rendimento = melhor_rendimento_list[1]
				self.topico_melhor_rendimento = melhor_rendimento_list[2]

				self.pior_rendimento = pior_rendimento_list[0]
				self.materia_pior_rendimento = pior_rendimento_list[1]
				self.topico_pior_rendimento = pior_rendimento_list[2]
			except ValueError:
				self.melhor_rendimento = '0.0 %'
				self.pior_rendimento = '0.0 %'
				self.topico_melhor_rendimento = 'Sem Tópico'
				self.materia_melhor_rendimento = 'Sem Matéria'
				self.materia_pior_rendimento = 'Sem Matéria'
				self.topico_pior_rendimento = 'Sem Tópico'
		except AttributeError:
			# ATUALIZAR INFORMAÇÕES SOBRE MAIOR E MENOR TAXA DE ACERTO - TODAY
			try:
				melhor_rendimento_list = findBestRendimento(str(self.today), True)
				pior_rendimento_list = findBestRendimento(str(self.today), False)

				self.melhor_rendimento = melhor_rendimento_list[0]
				self.materia_melhor_rendimento = melhor_rendimento_list[1]
				self.topico_melhor_rendimento = melhor_rendimento_list[2]

				self.pior_rendimento = pior_rendimento_list[0]
				self.materia_pior_rendimento = pior_rendimento_list[1]
				self.topico_pior_rendimento = pior_rendimento_list[2]
			except ValueError:
				self.melhor_rendimento = '0.0 %'
				self.pior_rendimento = '0.0 %'
				self.topico_melhor_rendimento = 'Sem Tópico'
				self.materia_melhor_rendimento = 'Sem Matéria'
				self.materia_pior_rendimento = 'Sem Matéria'
				self.topico_pior_rendimento = 'Sem Tópico'



		def refreshChecks_Exercicios(dt):
			try:
				self.ids.tabela_exercicios.children[0].children[0].DoubleClickRefreshChecks()
			except IndexError:
				pass
		Clock.schedule_once(refreshChecks_Exercicios, 1.15)






class Simulados(Screen):
	pass



class Estatisticas(Screen):
	pass



class Timer(Screen):
	pass



class Help(Screen):
	pass



class Configuracoes(Screen):
	pass

class WindowManager(ScreenManager):
	pass

class grid(MDApp):
	#font_size_title_1 = NumericProperty(42)
	font_size_title_1 = NumericProperty(42)
	font_size_title_2 = NumericProperty(30)
	font_size_title_3 = NumericProperty(23)

	font_size_normal_1 = NumericProperty(18)
	font_size_normal_2 = NumericProperty(15)

	font_cronograma_materias_estudadas_percent = 42
	font_cronograma_materias_estudadas_other_text = 18

	# //////////////////////////////////////////////////////////////////////////
	# CORES GERAIS DO SOFTWARE
	# COR DEFAULT PARA ITEMS DA ÁREA DE TRABALHO

	cor_principal_aplicativo = StringProperty('686fa3')   # azul escuro do aplicativo
	cor_fundo_area_de_trabalho = StringProperty('e6ebfb')
	cor_barra_inferior_licenca = StringProperty('cedeff')
	cor_widgets_default = StringProperty('eef2fe')
	cor_widgets_default_disabled = StringProperty('ebeffc')
	cor_widgets_hover = StringProperty('f4f7fe')
	cor_widgets_press = StringProperty('cad1e7')
	# //////////////////////////////////////////////////////////////////////////



	# //////////////////////////////////////////////////////////////////////////
	# CONFIGURACOES PAGINA CRONOGRAMA
	rows_per_page_cronograma = 5
	data_cronograma = pickle.load((open("data_timeline.p", "rb")))
	tabela = CronogramaTableStyle(colorData(organizerData(sortData(data_cronograma))))
	font_cronograma_botoes_add_remove_status = 22


	font_cronograma_next_materia = 38

	tabela_dp = 20
	# combinacao perfeital: 35,25,25,27,30,30
	tabela_cronograma_dp_data = tabela_dp + 15
	tabela_cronograma_dp_horario = tabela_dp + 5
	tabela_cronograma_dp_categoria = tabela_dp + 5
	tabela_cronograma_dp_materia = tabela_dp + 7
	tabela_cronograma_dp_topico = tabela_dp + 10
	tabela_cronograma_dp_status = tabela_dp + 10
	tabela_cronograma_dp_acertos = tabela_dp
	tabela_cronograma_dp_erros = tabela_dp
	tabela_cronograma_dp_taxa = tabela_dp + 5
	# //////////////////////////////////////////////////////////////////////////



	#//////////////////////////////////////////////////////////////////////////
	# CONFIGURAÇÕES DO MENU LATERAL PRINCIPAL
	# COR DA BORDA DEFAULT ENVOLTA DA IMAGEM DO USUARIO
	cor_principal_icone_fundo = StringProperty('f4f7fe')
	cor_principal_icone_fundo_def = StringProperty('f4f7fe')
	cor_principal_icone_fundo_hover = StringProperty('4e5488')

	# COR DEFAULT PARA OS ICONES E OS BOTOES DO MENU LATERAL PRINCIPAL
	cor_botoes_texto_default = '8793e9'              # cor do texto + icone no menu SEM ser selecionado
	cor_botoes_menu_default = '8793e9'               # cor do texto + icone no menu SEM ser selecionado
	cor_botoes_menu_selected = 'b7c1e0'				 # cor do texto + icone no menu SELECIOANDO
	cor_botoes_menu_hover = 'b7c1e0'				 # cor do texto + icone no menu SELECIOANDO


	# COR DOS ICONES E DOS TEXTOS NOS BOTOES DO MENU LATERAL PRINCIPAL
	cor_principal_texto_perfil = StringProperty(cor_botoes_menu_default)
	cor_principal_icone_perfil = StringProperty(cor_botoes_menu_default)
	cor_principal_texto_cronograma = StringProperty(cor_botoes_menu_default)
	cor_principal_icone_cronograma = StringProperty(cor_botoes_menu_default)
	cor_principal_texto_exercicios = StringProperty(cor_botoes_menu_default)
	cor_principal_icone_exercicios = StringProperty(cor_botoes_menu_default)
	cor_principal_texto_simulados = StringProperty(cor_botoes_menu_default)
	cor_principal_icone_simulados = StringProperty(cor_botoes_menu_default)
	cor_principal_texto_stats = StringProperty(cor_botoes_menu_default)
	cor_principal_icone_stats = StringProperty(cor_botoes_menu_default)
	cor_principal_texto_timer = StringProperty(cor_botoes_menu_default)
	cor_principal_icone_timer = StringProperty(cor_botoes_menu_default)
	cor_principal_texto_help = StringProperty(cor_botoes_menu_default)
	cor_principal_icone_help = StringProperty(cor_botoes_menu_default)
	cor_principal_texto_settings = StringProperty(cor_botoes_menu_default)
	cor_principal_icone_settings = StringProperty(cor_botoes_menu_default)
	cor_principal_texto_deslogar = StringProperty(cor_botoes_menu_default)
	cor_principal_icone_deslogar = StringProperty(cor_botoes_menu_default)
	# //////////////////////////////////////////////////////////////////////////

	def build(self):
		return Builder.load_file('grid.kv')



if __name__ == '__main__':
	#Window.size = (1280,720)
	#Window.fullscreen = True
	Window.maximize()
	grid().run()


