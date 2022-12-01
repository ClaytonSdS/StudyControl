from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '660')



from kivy.uix.screenmanager import ScreenManager, Screen
import pickle
from kivy.lang import Builder
from kivymd.uix.list import OneLineListItem
from kivy.properties import NumericProperty
from kivy.utils import get_color_from_hex
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.floatlayout import MDFloatLayout

from kivymd.uix.list import MDList
import os

from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.factory import Factory
Factory.register('HoverBehavior', HoverBehavior)

from kivy.uix.dropdown import DropDown
from kivymd.uix.datatables import MDDataTable
import re
import datetime
from datetime import date
from kivymd.uix.pickers import MDTimePicker, MDDatePicker

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.toast import toast
import webbrowser
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog


class Tema():
	def __init__(self, cor_aplicativo, cor_aplicativo_tuple, cor_fundo_trabalho, cor_fundo_trabalho_tuple, cor_widget, cor_widget_hover, cor_fundo_menu_deg1, cor_fundo_menu_deg2, cor_letra_menu, cor_licenca, cor_licenca_texto):
		self.cor_aplicativo = cor_aplicativo
		self.cor_aplicativo_tuple = cor_aplicativo_tuple
		self.cor_fundo_trabalho = cor_fundo_trabalho
		self.cor_fundo_trabalho_tuple = cor_fundo_trabalho_tuple
		self.cor_widget = cor_widget
		self.cor_widget_hover = cor_widget_hover
		self.cor_fundo_menu_deg1 = cor_fundo_menu_deg1
		self.cor_fundo_menu_deg2 = cor_fundo_menu_deg2
		self.cor_letra_menu = cor_letra_menu
		self.cor_licenca = cor_licenca
		self.cor_licenca_texto = cor_licenca_texto

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
Padrao = Tema(cor_aplicativo='686fa3', cor_aplicativo_tuple = [0.3098,0.3411,0.5333], cor_fundo_menu_deg1='464c7e', cor_fundo_menu_deg2='575e91', cor_fundo_trabalho='e6ebfb',
				  cor_fundo_trabalho_tuple=[0.9019, 0.9215, 0.9843, 1], cor_widget='eef2fe', cor_widget_hover='f4f7fe',
				  cor_letra_menu='8793e9', cor_licenca='cedeff', cor_licenca_texto = '686fa3')
tema = read_or_new_pickle(path="tema.p", default=[Padrao, "Padrão"])
tema = pickle.load((open("tema.p", "rb")))
#////////////////////////////////////////////////////////////////////////////
# FUNÇÕES PARA USO EM MAIS DE UMA SCREEN
def filter(data, filter_name='No Simulado'):
	only_theory_exercise = []
	if filter_name == "No Simulado":
		for item in range(len(data)):
			if data[item][2] != "Simulado":
				only_theory_exercise.append(data[item])

	if filter_name == "Simulado":
		for item in range(len(data)):
			if data[item][2] == "Simulado":
				only_theory_exercise.append(data[item])

	return only_theory_exercise
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
	data = CronogramaTableStyle(organizerData(sortData(data)))
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
def splitPercent(string):
	return str(string.split()[0])
def changeZeroEsquerda(string):
	if len(string) >= 2:
		if string[0] == '0':
			return string[1]
	else:
		return string
	if len(string) < 2:
		return string
def changeStatusColor(lista_tuple, color_hex=tema[0].cor_aplicativo):
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
def colorData(lista, color_hex=tema[0].cor_aplicativo):
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
# FUNÇÕES INICIO
def FUNCTION_HorasEstudadas_Total_Weekly():
	data = pickle.load((open("data_timeline.p", "rb")))
	horas_estudadas = []
	horas = []
	minutos = []

	take_actual_week_number = \
	datetime.date(int(str(date.today()).split('-')[0]), int(changeZeroEsquerda(str(date.today()).split('-')[1])),
				  int(changeZeroEsquerda(str(date.today()).split('-')[2]))).isocalendar()[1]
	for x in range(len(data)):
		if data[x][2] == 'Exercicios' or data[x][2] == 'Teoria' or data[x][2] == 'Simulado':
			if data[x][6][2] == 'Estudado':
				if data[x][0].split('-')[0] == str(date.today()).split('-')[0]:
					verificar_semana = datetime.date(int(data[x][0].split('-')[0]), int(changeZeroEsquerda(data[x][0].split('-')[1])), int(changeZeroEsquerda(data[x][0].split('-')[2]))).isocalendar()[1]
					if verificar_semana == take_actual_week_number:
						horas_estudadas.append(data[x][5][0:5])

	for x in range(len(horas_estudadas)):
		horas.append(float(changeZeroEsquerda(horas_estudadas[x].split(':')[0])))
		minutos.append(float(changeZeroEsquerda(horas_estudadas[x].split(':')[1])) / 60)

	horas = sum(horas)
	minutos = sum(minutos)
	if len(str(horas)) >= 3:
		if len(str(horas)) > 8:
			return "9999999h"
		else:
			return str(horas) + 'h'
	else:
		tempo_total_estudado = horas + minutos
		return str(round(tempo_total_estudado, 2)) + 'h'
def FUNCTION_HorasEstudadas_Total():
	data = pickle.load((open("data_timeline.p", "rb")))
	horas_estudadas = []
	horas = []
	minutos = []

	for x in range(len(data)):
		if data[x][2] == 'Exercicios' or data[x][2] == 'Teoria' or data[x][2] == 'Simulado':
			if data[x][6][2] == 'Estudado':
				horas_estudadas.append(data[x][5][0:5])

	for x in range(len(horas_estudadas)):
		horas.append(float(changeZeroEsquerda(horas_estudadas[x].split(':')[0])))
		minutos.append(float(changeZeroEsquerda(horas_estudadas[x].split(':')[1])) / 60)

	horas = sum(horas)
	minutos = sum(minutos)
	if len(str(horas)) >= 3:
		if len(str(horas)) > 8:
			return "9999999h+"
		else:
			return str(horas) + 'h'
	else:
		tempo_total_estudado = horas + minutos
		return str(round(tempo_total_estudado, 2)) + 'h'
def FUNCTION_QuestoesRealizadas_Total():
	data = pickle.load((open("data_timeline.p", "rb")))
	acertos = []
	erros = []

	for x in range(len(data)):
		if data[x][2] == 'Exercicios' or data[x][2] == 'Simulado':
			acertos.append(float(data[x][7]))
			erros.append(float(data[x][8]))

	total_questoes = sum(acertos) + sum(erros)
	total_questoes = str(round(total_questoes))
	if len(total_questoes) > 9:
		return '99999999+'
	else:
		return total_questoes
def FUNCTION_QuestoesRealizadas_Total_Weekly():
	data = pickle.load((open("data_timeline.p", "rb")))
	acertos = []
	erros = []
	take_actual_week_number = \
	datetime.date(int(str(date.today()).split('-')[0]), int(changeZeroEsquerda(str(date.today()).split('-')[1])),
				  int(changeZeroEsquerda(str(date.today()).split('-')[2]))).isocalendar()[1]
	for x in range(len(data)):
		if data[x][2] == 'Exercicios' or data[x][2] == 'Simulado':
			if data[x][0].split('-')[0] == str(date.today()).split('-')[0]:
				verificar_semana = datetime.date(int(data[x][0].split('-')[0]), int(changeZeroEsquerda(data[x][0].split('-')[1])),int(changeZeroEsquerda(data[x][0].split('-')[2]))).isocalendar()[1]
				if verificar_semana == take_actual_week_number:
					acertos.append(float(data[x][7]))
					erros.append(float(data[x][8]))

	total_questoes = sum(acertos) + sum(erros)
	total_questoes = str(round(total_questoes))
	if len(total_questoes) > 9:
		return '99999999'
	else:
		return total_questoes
def FUNCTION_TaxaAcertos_Total():
	taxa_acerto = []
	data = pickle.load((open("data_timeline.p", "rb")))
	taxa_acertos_full = []

	for x in range(len(data)):
		if data[x][2] == 'Exercicios' or data[x][2] == 'Simulado':
			taxa_acerto.append(float(splitPercent(data[x][9])))
			taxa_acertos_full.append(data[x])
	try:
		return str(round(sum(taxa_acerto)/len(taxa_acerto), 2)) + ' %'
	except ZeroDivisionError:
		return str(0)+' %'
def FUNCTION_TaxaAcertos_Total_Weekly():
	taxa_acerto_this_week = []
	data = pickle.load((open("data_timeline.p", "rb")))

	take_actual_week_number = \
	datetime.date(int(str(date.today()).split('-')[0]), int(changeZeroEsquerda(str(date.today()).split('-')[1])),
				  int(changeZeroEsquerda(str(date.today()).split('-')[2]))).isocalendar()[1]
	for x in range(len(data)):
		if data[x][2] == 'Exercicios' or data[x][2] == 'Simulado':
			if data[x][0].split('-')[0] == str(date.today()).split('-')[0]:
				verificar_semana = \
				datetime.date(int(data[x][0].split('-')[0]), int(changeZeroEsquerda(data[x][0].split('-')[1])),
							  int(changeZeroEsquerda(data[x][0].split('-')[2]))).isocalendar()[1]
				if verificar_semana == take_actual_week_number:
					taxa_acerto_this_week.append(float(splitPercent(data[x][9])))

	try:
		return str(round(sum(taxa_acerto_this_week) / len(taxa_acerto_this_week), 2)) + ' %'
	except ZeroDivisionError:
		return str(0) + ' %'
def FUNCTION_SimuladosRealizados_Total():
	data = pickle.load((open("data_timeline.p", "rb")))
	realizados = 0
	for x in range(len(data)):
		if data[x][2] == 'Simulado':
			if data[x][6][2] == 'Estudado' or data[x][7] != '0' or data[x][8] != '0':
				realizados += 1
	realizados = str(round(realizados))
	if len(realizados) > 9:
		return '99999999+'
	else:
		return realizados
def FUNCTION_SimuladosRealizados_Total_Weekly():
	data = pickle.load((open("data_timeline.p", "rb")))
	realizados = 0
	take_actual_week_number = \
	datetime.date(int(str(date.today()).split('-')[0]), int(changeZeroEsquerda(str(date.today()).split('-')[1])),
				  int(changeZeroEsquerda(str(date.today()).split('-')[2]))).isocalendar()[1]

	for x in range(len(data)):
		if data[x][2] == 'Simulado':
			if data[x][0].split('-')[0] == str(date.today()).split('-')[0]:
				verificar_semana = datetime.date(int(data[x][0].split('-')[0]), int(changeZeroEsquerda(data[x][0].split('-')[1])), int(changeZeroEsquerda(data[x][0].split('-')[2]))).isocalendar()[1]
				if verificar_semana == take_actual_week_number:
					if data[x][6][2] == 'Estudado' or data[x][7] != '0' or data[x][8] != '0':
						realizados += 1

	realizados = str(round(realizados))
	if len(realizados) > 9:
		return '99999999'
	else:
		return realizados
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
def changeZeroEsquerda(string):
	if len(string) >= 2:
		if string[0] == '0':
			return string[1]
		else:
			return string
	else:
		return string
def calcularTaxaAcerto(acertos, erros):
	if acertos != 0 and erros !=0:
		return str(round(float(acertos/(acertos+erros) * 100), 2)) + ' %'
	if acertos == 0 and erros == 0:
		return "0.0 %"
	else:
		return str(round(float(acertos/(acertos+erros) * 100), 2)) + ' %'

#////////////////////////////////////////////////////////////////////////////
# FUNÇÕES DA PAGINA ESTATISTICAS
def FUNCTION_TaxaAcertos_Geral():
	taxa_acerto = []
	data = pickle.load((open("data_timeline.p", "rb")))
	taxa_acertos_full = []

	for x in range(len(data)):
		if data[x][2] == 'Exercicios':
			taxa_acerto.append(float(splitPercent(data[x][9])))
			taxa_acertos_full.append(data[x])
	try:
		return str(round(sum(taxa_acerto)/len(taxa_acerto), 2)) + ' %'
	except ZeroDivisionError:
		return str(0)+' %'
def FUNCTION_TaxaAcertos_Materias(materia):
	taxa_acerto = []
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_materia = str(materia)

	def splitPercent(string):
		return str(string.split()[0])

	for x in range(len(data)):
		if data[x][2] == 'Exercicios' and data[x][3] == str(nome_materia):
			taxa_acerto.append(float(splitPercent(data[x][9])))

	try:
		return str(round(sum(taxa_acerto)/len(taxa_acerto), 2)) + ' %'
	except ZeroDivisionError:
		return str(0)+' %'
def FUNCTION_TaxaAcertos_Materias_ThisWeek(materia):
	today = date.today()
	taxa_acerto_this_week = []
	taxa_acerto_last_week = []
	nome_materia = str(materia)
	data = pickle.load((open("data_timeline.p", "rb")))

	take_actual_week_number  = datetime.date(int(str(date.today()).split('-')[0]), int(changeZeroEsquerda(str(date.today()).split('-')[1])), int(changeZeroEsquerda(str(date.today()).split('-')[2]))).isocalendar()[1]
	for x in range(len(data)):
		if data[x][2] == 'Exercicios' and data[x][3] == str(nome_materia):
			if data[x][0].split('-')[0] == str(date.today()).split('-')[0]:
				verificar_semana = datetime.date(int(data[x][0].split('-')[0]), int(changeZeroEsquerda(data[x][0].split('-')[1])), int(changeZeroEsquerda(data[x][0].split('-')[2]))).isocalendar()[1]
				if verificar_semana == take_actual_week_number:
					taxa_acerto_this_week.append(float(splitPercent(data[x][9])))

	try:
		return str(round(sum(taxa_acerto_this_week)/len(taxa_acerto_this_week), 2)) + ' %'
	except ZeroDivisionError:
		return str(0)+' %'
def FUNCTION_TaxaAcertos_Materias_LastWeek(materia):
	today = date.today()
	taxa_acerto_this_week = []
	taxa_acerto_last_week = []
	nome_materia = str(materia)
	data = pickle.load((open("data_timeline.p", "rb")))

	take_actual_week_number = \
	datetime.date(int(str(date.today()).split('-')[0]), int(changeZeroEsquerda(str(date.today()).split('-')[1])),
				  int(changeZeroEsquerda(str(date.today()).split('-')[2]))).isocalendar()[1]
	for x in range(len(data)):
		if data[x][2] == 'Exercicios' and data[x][3] == str(nome_materia):
			if data[x][0].split('-')[0] == str(date.today()).split('-')[0]:
				verificar_semana = \
				datetime.date(int(data[x][0].split('-')[0]), int(changeZeroEsquerda(data[x][0].split('-')[1])),
							  int(changeZeroEsquerda(data[x][0].split('-')[2]))).isocalendar()[1]
				if verificar_semana == take_actual_week_number - 1:
					taxa_acerto_last_week.append(float(splitPercent(data[x][9])))
	try:
		return str(round(sum(taxa_acerto_last_week) / len(taxa_acerto_last_week), 2)) + ' %'

	except ZeroDivisionError:
		return str(0) + ' %'
def FUNCTION_TaxaAcertos_Materias_Weekly(materia):
	initial_value = float(splitPercent(FUNCTION_TaxaAcertos_Materias_LastWeek(str(materia))))
	final_value = float(splitPercent(FUNCTION_TaxaAcertos_Materias_ThisWeek(str(materia))))
	if final_value == 0 and initial_value == 0:
		return '0.0 %'
	else:
		if final_value >= 0:
			return str(final_value) + ' %'
		else:
			return str(final_value) + ' %'
def FUNCTION_TaxaAcertos_Topicos(materia, topico):
	taxa_acerto = []
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_materia = str(materia)
	nome_topico = str(topico)
	for x in range(len(data)):
		if data[x][2] == 'Exercicios' and data[x][3] == nome_materia and data[x][4] == nome_topico:
			taxa_acerto.append(float(splitPercent(data[x][9])))
	try:
		return str(round(sum(taxa_acerto)/len(taxa_acerto), 2)) + ' %'
	except ZeroDivisionError:
		return str(0)+' %'
def FUNCTION_TaxaAcertos_Topicos_Weekly(materia, topico):
	taxa_acerto_this_week = []
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_materia = str(materia)
	nome_topico = str(topico)

	take_actual_week_number = \
	datetime.date(int(str(date.today()).split('-')[0]), int(changeZeroEsquerda(str(date.today()).split('-')[1])),
				  int(changeZeroEsquerda(str(date.today()).split('-')[2]))).isocalendar()[1]
	for x in range(len(data)):
		if data[x][2] == 'Exercicios' and data[x][3] == str(nome_materia) and data[x][4] == nome_topico:
			if data[x][0].split('-')[0] == str(date.today()).split('-')[0]:
				verificar_semana = \
				datetime.date(int(data[x][0].split('-')[0]), int(changeZeroEsquerda(data[x][0].split('-')[1])),
							  int(changeZeroEsquerda(data[x][0].split('-')[2]))).isocalendar()[1]
				if verificar_semana == take_actual_week_number:
					taxa_acerto_this_week.append(float(splitPercent(data[x][9])))

	try:
		return str(round(sum(taxa_acerto_this_week) / len(taxa_acerto_this_week), 2)) + ' %'
	except ZeroDivisionError:
		return str(0) + ' %'
def FUNCTION_HorasEstudadas_Geral():
	data = pickle.load((open("data_timeline.p", "rb")))
	horas_estudadas = []

	horas = []
	minutos = []
	for x in range(len(data)):
		if data[x][2] != "Simulado":
			if data[x][6][2] == 'Estudado':
				horas_estudadas.append(data[x][5][0:5])

	for x in range(len(horas_estudadas)):
		horas.append(float(changeZeroEsquerda(horas_estudadas[x].split(':')[0])))
		minutos.append(float(changeZeroEsquerda(horas_estudadas[x].split(':')[1])) / 60)

	horas = sum(horas)
	minutos = sum(minutos)
	if len(str(horas)) >= 3:
		if len(str(horas)) > 8:
			return "9999999h+"
		else:
			return str(horas) + 'h'
	else:
		tempo_total_estudado = horas + minutos
		return str(round(tempo_total_estudado, 2)) + 'h'
def FUNCTION_HorasEstudadas_Materias(materia):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_materia = str(materia)
	horas_estudadas = []

	horas = []
	minutos = []

	for x in range(len(data)):
		if data[x][2] != "Simulado":
			if data[x][3] == str(nome_materia):
				if data[x][6][2] == 'Estudado':
					horas_estudadas.append(data[x][5][0:5])

	for x in range(len(horas_estudadas)):
		horas.append(float(changeZeroEsquerda(horas_estudadas[x].split(':')[0])))
		minutos.append(float(changeZeroEsquerda(horas_estudadas[x].split(':')[1])) / 60)

	horas = sum(horas)
	minutos = sum(minutos)
	if len(str(horas)) >= 3:
		if len(str(horas)) > 8:
			return "9999999h+"
		else:
			return str(horas) + 'h'
	else:
		tempo_total_estudado = horas + minutos
		return str(round(tempo_total_estudado, 2)) + 'h'
def FUNCTION_HorasEstudadas_Materias_Weekly(materia):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_materia = str(materia)
	horas_estudadas = []

	horas = []
	minutos = []

	take_actual_week_number = \
	datetime.date(int(str(date.today()).split('-')[0]), int(changeZeroEsquerda(str(date.today()).split('-')[1])),
				  int(changeZeroEsquerda(str(date.today()).split('-')[2]))).isocalendar()[1]
	for x in range(len(data)):
		if data[x][2] != "Simulado":
			if data[x][3] == str(nome_materia):
				if data[x][0].split('-')[0] == str(date.today()).split('-')[0]:
					verificar_semana = \
					datetime.date(int(data[x][0].split('-')[0]), int(changeZeroEsquerda(data[x][0].split('-')[1])),
								  int(changeZeroEsquerda(data[x][0].split('-')[2]))).isocalendar()[1]
					if verificar_semana == take_actual_week_number:
						if data[x][6][2] == 'Estudado':
							horas_estudadas.append(data[x][5][0:5])

	for x in range(len(horas_estudadas)):
		horas.append(float(changeZeroEsquerda(horas_estudadas[x].split(':')[0])))
		minutos.append(float(changeZeroEsquerda(horas_estudadas[x].split(':')[1])) / 60)

	horas = sum(horas)
	minutos = sum(minutos)
	if len(str(horas)) >= 3:
		if len(str(horas)) > 8:
			return "9999999h"
		else:
			return str(horas) + 'h'
	else:
		tempo_total_estudado = horas + minutos
		return str(round(tempo_total_estudado, 2)) + 'h'
def FUNCTION_HorasEstudadas_Topicos(materia, topico):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_materia = str(materia)
	nome_topico = str(topico)
	horas_estudadas = []

	horas = []
	minutos = []


	for x in range(len(data)):
		if data[x][2] != "Simulado":
			if data[x][3] == str(nome_materia) and data[x][4] == nome_topico:
				if data[x][6][2] == 'Estudado':
					horas_estudadas.append(data[x][5][0:5])

	for x in range(len(horas_estudadas)):
		horas.append(float(changeZeroEsquerda(horas_estudadas[x].split(':')[0])))
		minutos.append(float(changeZeroEsquerda(horas_estudadas[x].split(':')[1])) / 60)

	horas = sum(horas)
	minutos = sum(minutos)
	if len(str(horas)) >= 3:
		if len(str(horas)) > 8:
			return "9999999h+"
		else:
			return str(horas) + 'h'
	else:
		tempo_total_estudado = horas + minutos
		return str(round(tempo_total_estudado, 2)) + 'h'
def FUNCTION_HorasEstudadas_Topicos_Weekly(materia, topico):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_materia = str(materia)
	nome_topico = str(topico)
	horas_estudadas = []

	horas = []
	minutos = []

	take_actual_week_number = \
	datetime.date(int(str(date.today()).split('-')[0]), int(changeZeroEsquerda(str(date.today()).split('-')[1])),
				  int(changeZeroEsquerda(str(date.today()).split('-')[2]))).isocalendar()[1]
	for x in range(len(data)):
		if data[x][2] != "Simulado":
			if data[x][3] == str(nome_materia) and data[x][4] == nome_topico:
				if data[x][0].split('-')[0] == str(date.today()).split('-')[0]:
					verificar_semana = datetime.date(int(data[x][0].split('-')[0]), int(changeZeroEsquerda(data[x][0].split('-')[1])),int(changeZeroEsquerda(data[x][0].split('-')[2]))).isocalendar()[1]
					if verificar_semana == take_actual_week_number:
						if data[x][6][2] == 'Estudado':
							horas_estudadas.append(data[x][5][0:5])

	for x in range(len(horas_estudadas)):
		horas.append(float(changeZeroEsquerda(horas_estudadas[x].split(':')[0])))
		minutos.append(float(changeZeroEsquerda(horas_estudadas[x].split(':')[1])) / 60)

	horas = sum(horas)
	minutos = sum(minutos)
	if len(str(horas)) >= 3:
		if len(str(horas)) > 8:
			return "9999999h"
		else:
			return str(horas) + 'h'
	else:
		tempo_total_estudado = horas + minutos
		return str(round(tempo_total_estudado, 2)) + 'h'
def FUNCTION_QuestoesRealizadas_Geral():
	data = pickle.load((open("data_timeline.p", "rb")))
	acertos = []
	erros = []

	for x in range(len(data)):
		if data[x][2] == 'Exercicios':
			acertos.append(float(data[x][7]))
			erros.append(float(data[x][8]))

	total_questoes = sum(acertos) + sum(erros)
	total_questoes = str(round(total_questoes))
	if len(str(total_questoes)) > 9:
		return '99999999+'
	else:
		return str(total_questoes)
def FUNCTION_QuestoesRealizadas_Materias(materia):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_materia = str(materia)
	acertos = []
	erros = []

	for x in range(len(data)):
		if data[x][2] == 'Exercicios':
			if data[x][3] == str(nome_materia):
				acertos.append(float(data[x][7]))
				erros.append(float(data[x][8]))

	total_questoes = sum(acertos) + sum(erros)
	if len(str(total_questoes)) > 9:
		return '99999999+'
	else:
		return str(total_questoes)
def FUNCTION_QuestoesRealizadas_Materias_Weekly(materia):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_materia = str(materia)
	acertos = []
	erros = []
	take_actual_week_number = \
	datetime.date(int(str(date.today()).split('-')[0]), int(changeZeroEsquerda(str(date.today()).split('-')[1])),
				  int(changeZeroEsquerda(str(date.today()).split('-')[2]))).isocalendar()[1]
	for x in range(len(data)):
		if data[x][2] == 'Exercicios':
			if data[x][3] == str(nome_materia):
				if data[x][0].split('-')[0] == str(date.today()).split('-')[0]:
					verificar_semana = \
					datetime.date(int(data[x][0].split('-')[0]), int(changeZeroEsquerda(data[x][0].split('-')[1])),
								  int(changeZeroEsquerda(data[x][0].split('-')[2]))).isocalendar()[1]
					if verificar_semana == take_actual_week_number:
						acertos.append(float(data[x][7]))
						erros.append(float(data[x][8]))

	total_questoes = sum(acertos) + sum(erros)
	if len(str(total_questoes)) > 9:
		return '99999999'
	else:
		return str(total_questoes)
def FUNCTION_QuestoesRealizadas_Topicos(materia, topico):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_materia = str(materia)
	nome_topico = str(topico)
	acertos = []
	erros = []

	for x in range(len(data)):
		if data[x][2] == 'Exercicios':
			if data[x][3] == str(nome_materia) and data[x][4] == nome_topico:
				acertos.append(float(data[x][7]))
				erros.append(float(data[x][8]))

	total_questoes = sum(acertos) + sum(erros)
	if len(str(total_questoes)) > 9:
		return '99999999+'
	else:
		return str(total_questoes)
def FUNCTION_QuestoesRealizadas_Topicos_Weekly(materia, topico):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_materia = str(materia)
	nome_topico = str(topico)
	acertos = []
	erros = []
	take_actual_week_number = \
	datetime.date(int(str(date.today()).split('-')[0]), int(changeZeroEsquerda(str(date.today()).split('-')[1])),
				  int(changeZeroEsquerda(str(date.today()).split('-')[2]))).isocalendar()[1]

	for x in range(len(data)):
		if data[x][2] == 'Exercicios':
			if data[x][3] == str(nome_materia) and data[x][4] == nome_topico:
				if data[x][0].split('-')[0] == str(date.today()).split('-')[0]:
					verificar_semana = \
					datetime.date(int(data[x][0].split('-')[0]), int(changeZeroEsquerda(data[x][0].split('-')[1])),
								  int(changeZeroEsquerda(data[x][0].split('-')[2]))).isocalendar()[1]
					if verificar_semana == take_actual_week_number:
						acertos.append(float(data[x][7]))
						erros.append(float(data[x][8]))

	total_questoes = sum(acertos) + sum(erros)
	if len(str(total_questoes)) > 9:
		return '99999999'
	else:
		return str(total_questoes)
def FUNCTION_Acertos_Materias(materia):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_materia = str(materia)
	acertos = []

	for x in range(len(data)):
		if data[x][2] == 'Exercicios':
			if data[x][3] == str(nome_materia):
				acertos.append(float(data[x][7]))

	total_acertos = sum(acertos)
	if len(str(total_acertos)) > 5:
		return '99999+'
	else:
		return str(total_acertos)
def FUNCTION_Acertos_Materias_Weekly(materia):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_materia = str(materia)
	acertos = []

	take_actual_week_number = \
	datetime.date(int(str(date.today()).split('-')[0]), int(changeZeroEsquerda(str(date.today()).split('-')[1])),
				  int(changeZeroEsquerda(str(date.today()).split('-')[2]))).isocalendar()[1]
	for x in range(len(data)):
		if data[x][2] == 'Exercicios':
			if data[x][3] == str(nome_materia):
				if data[x][0].split('-')[0] == str(date.today()).split('-')[0]:
					verificar_semana = \
					datetime.date(int(data[x][0].split('-')[0]), int(changeZeroEsquerda(data[x][0].split('-')[1])),
								  int(changeZeroEsquerda(data[x][0].split('-')[2]))).isocalendar()[1]
					if verificar_semana == take_actual_week_number:
						acertos.append(float(data[x][7]))

	total_acertos = sum(acertos)
	if len(str(total_acertos)) > 5:
		return '99999'
	else:
		return str(total_acertos)
def FUNCTION_Acertos_Topicos(materia, topico):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_materia = str(materia)
	nome_topico = str(topico)
	acertos = []

	for x in range(len(data)):
		if data[x][2] == 'Exercicios':
			if data[x][3] == str(nome_materia) and data[x][4] == nome_topico:
				acertos.append(float(data[x][7]))

	total_acertos = sum(acertos)
	if len(str(total_acertos)) > 5:
		return '99999+'
	else:
		return str(total_acertos)
def FUNCTION_Acertos_Topicos_Weekly(materia, topico):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_materia = str(materia)
	nome_topico = str(topico)
	acertos = []
	take_actual_week_number = \
	datetime.date(int(str(date.today()).split('-')[0]), int(changeZeroEsquerda(str(date.today()).split('-')[1])),
				  int(changeZeroEsquerda(str(date.today()).split('-')[2]))).isocalendar()[1]

	for x in range(len(data)):
		if data[x][2] == 'Exercicios':
			if data[x][3] == str(nome_materia) and data[x][4] == nome_topico:
				if data[x][0].split('-')[0] == str(date.today()).split('-')[0]:
					verificar_semana = \
					datetime.date(int(data[x][0].split('-')[0]), int(changeZeroEsquerda(data[x][0].split('-')[1])),
								  int(changeZeroEsquerda(data[x][0].split('-')[2]))).isocalendar()[1]
					if verificar_semana == take_actual_week_number:
						acertos.append(float(data[x][7]))

	total_acertos = sum(acertos)
	if len(str(total_acertos)) > 5:
		return '99999'
	else:
		return str(total_acertos)
def FUNCTION_Erros_Materias(materia):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_materia = str(materia)
	erros = []

	for x in range(len(data)):
		if data[x][2] == 'Exercicios':
			if data[x][3] == str(nome_materia):
				erros.append(float(data[x][8]))

	total_erros = sum(erros)
	if len(str(total_erros)) > 5:
		return '99999+'
	else:
		return str(total_erros)
def FUNCTION_Erros_Materias_Weekly(materia):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_materia = str(materia)
	erros = []

	take_actual_week_number = \
	datetime.date(int(str(date.today()).split('-')[0]), int(changeZeroEsquerda(str(date.today()).split('-')[1])),
				  int(changeZeroEsquerda(str(date.today()).split('-')[2]))).isocalendar()[1]
	for x in range(len(data)):
		if data[x][2] == 'Exercicios':
			if data[x][3] == str(nome_materia):
				if data[x][0].split('-')[0] == str(date.today()).split('-')[0]:
					verificar_semana = \
					datetime.date(int(data[x][0].split('-')[0]), int(changeZeroEsquerda(data[x][0].split('-')[1])),
								  int(changeZeroEsquerda(data[x][0].split('-')[2]))).isocalendar()[1]
					if verificar_semana == take_actual_week_number:
						erros.append(float(data[x][8]))

	total_erros = sum(erros)
	if len(str(total_erros)) > 5:
		return '99999'
	else:
		return str(total_erros)
def FUNCTION_Erros_Topicos(materia, topico):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_materia = str(materia)
	nome_topico = str(topico)
	erros = []

	for x in range(len(data)):
		if data[x][2] == 'Exercicios':
			if data[x][3] == str(nome_materia) and data[x][4] == nome_topico:
				erros.append(float(data[x][8]))

	total_erros = sum(erros)
	if len(str(total_erros)) > 5:
		return '99999+'
	else:
		return str(total_erros)
def FUNCTION_Erros_Topicos_Weekly(materia, topico):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_materia = str(materia)
	nome_topico = str(topico)
	erros = []
	take_actual_week_number = \
	datetime.date(int(str(date.today()).split('-')[0]), int(changeZeroEsquerda(str(date.today()).split('-')[1])),
				  int(changeZeroEsquerda(str(date.today()).split('-')[2]))).isocalendar()[1]

	for x in range(len(data)):
		if data[x][2] == 'Exercicios':
			if data[x][3] == str(nome_materia) and data[x][4] == nome_topico:
				if data[x][0].split('-')[0] == str(date.today()).split('-')[0]:
					verificar_semana = \
					datetime.date(int(data[x][0].split('-')[0]), int(changeZeroEsquerda(data[x][0].split('-')[1])),
								  int(changeZeroEsquerda(data[x][0].split('-')[2]))).isocalendar()[1]
					if verificar_semana == take_actual_week_number:
						erros.append(float(data[x][8]))

	total_erros = sum(erros)
	if len(str(total_erros)) > 5:
		return '99999'
	else:
		return str(total_erros)

#////////////////////////////////////////////////////////////////////////////
# FUNÇÕES DA PAGINA SIMULADOS
def FUNCTION_TaxaAcertos_Simulados(nome_simulado):
	taxa_acerto = []
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_simulado = str(nome_simulado)

	def splitPercent(string):
		return str(string.split()[0])

	for x in range(len(data)):
		if data[x][2] == 'Simulado' and data[x][3] == str(nome_simulado):
			taxa_acerto.append(float(splitPercent(data[x][9])))

	try:
		return str(round(sum(taxa_acerto)/len(taxa_acerto), 2)) + ' %'
	except ZeroDivisionError:
		return str(0)+' %'
def FUNCTION_TaxaAcertos_Simulados_ThisWeek(nome_simulado):
	today = date.today()
	taxa_acerto_this_week = []
	taxa_acerto_last_week = []
	nome_simulado = str(nome_simulado)
	data = pickle.load((open("data_timeline.p", "rb")))

	take_actual_week_number  = datetime.date(int(str(date.today()).split('-')[0]), int(changeZeroEsquerda(str(date.today()).split('-')[1])), int(changeZeroEsquerda(str(date.today()).split('-')[2]))).isocalendar()[1]
	for x in range(len(data)):
		if data[x][2] == 'Simulado' and data[x][3] == str(nome_simulado):
			if data[x][0].split('-')[0] == str(date.today()).split('-')[0]:
				verificar_semana = datetime.date(int(data[x][0].split('-')[0]), int(changeZeroEsquerda(data[x][0].split('-')[1])), int(changeZeroEsquerda(data[x][0].split('-')[2]))).isocalendar()[1]
				if verificar_semana == take_actual_week_number:
					taxa_acerto_this_week.append(float(splitPercent(data[x][9])))

	try:
		return str(round(sum(taxa_acerto_this_week)/len(taxa_acerto_this_week), 2)) + ' %'
	except ZeroDivisionError:
		return str(0)+' %'
def FUNCTION_HorasEstudadas_Simulados(nome_simulado):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_materia = str(nome_simulado)
	horas_estudadas = []

	horas = []
	minutos = []

	for x in range(len(data)):
		if data[x][2] == 'Simulado':
			if data[x][3] == str(nome_simulado):
				if data[x][6][2] == 'Estudado':
					horas_estudadas.append(data[x][5][0:5])

	for x in range(len(horas_estudadas)):
		horas.append(float(changeZeroEsquerda(horas_estudadas[x].split(':')[0])))
		minutos.append(float(changeZeroEsquerda(horas_estudadas[x].split(':')[1])) / 60)

	horas = sum(horas)
	minutos = sum(minutos)
	if len(str(horas)) >= 3:
		if len(str(horas)) > 8:
			return "9999999h+"
		else:
			return str(horas) + 'h'
	else:
		tempo_total_estudado = horas + minutos
		return str(round(tempo_total_estudado, 2)) + 'h'
def FUNCTION_HorasEstudadas_Simulados_Weekly(nome_simulado):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_simulado = str(nome_simulado)
	horas_estudadas = []

	horas = []
	minutos = []

	take_actual_week_number = \
	datetime.date(int(str(date.today()).split('-')[0]), int(changeZeroEsquerda(str(date.today()).split('-')[1])),
				  int(changeZeroEsquerda(str(date.today()).split('-')[2]))).isocalendar()[1]
	for x in range(len(data)):
		if data[x][2] == 'Simulado' and data[x][6][2] == 'Estudado':
			if data[x][3] == str(nome_simulado):
				if data[x][0].split('-')[0] == str(date.today()).split('-')[0]:
					verificar_semana = \
					datetime.date(int(data[x][0].split('-')[0]), int(changeZeroEsquerda(data[x][0].split('-')[1])),
								  int(changeZeroEsquerda(data[x][0].split('-')[2]))).isocalendar()[1]
					if verificar_semana == take_actual_week_number:
						horas_estudadas.append(data[x][5][0:5])

	for x in range(len(horas_estudadas)):
		horas.append(float(changeZeroEsquerda(horas_estudadas[x].split(':')[0])))
		minutos.append(float(changeZeroEsquerda(horas_estudadas[x].split(':')[1])) / 60)

	horas = sum(horas)
	minutos = sum(minutos)
	if len(str(horas)) >= 3:
		if len(str(horas)) > 8:
			return "9999999h"
		else:
			return str(horas) + 'h'
	else:
		tempo_total_estudado = horas + minutos
		return str(round(tempo_total_estudado, 2)) + 'h'
def FUNCTION_QuestoesRealizadas_Simulados(nome_simulado):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_simulado = str(nome_simulado)
	acertos = []
	erros = []

	for x in range(len(data)):
		if data[x][2] == 'Simulado':
			if data[x][3] == str(nome_simulado):
				acertos.append(float(data[x][7]))
				erros.append(float(data[x][8]))

	total_questoes = sum(acertos) + sum(erros)
	total_questoes = str(round(total_questoes))
	if len(total_questoes) > 9:
		return '99999999+'
	else:
		return total_questoes
def FUNCTION_QuestoesRealizadas_Simulados_Weekly(nome_simulado):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_simulado = str(nome_simulado)
	acertos = []
	erros = []
	take_actual_week_number = \
	datetime.date(int(str(date.today()).split('-')[0]), int(changeZeroEsquerda(str(date.today()).split('-')[1])),
				  int(changeZeroEsquerda(str(date.today()).split('-')[2]))).isocalendar()[1]
	for x in range(len(data)):
		if data[x][2] == 'Simulado':
			if data[x][3] == str(nome_simulado):
				if data[x][0].split('-')[0] == str(date.today()).split('-')[0]:
					verificar_semana = \
					datetime.date(int(data[x][0].split('-')[0]), int(changeZeroEsquerda(data[x][0].split('-')[1])),
								  int(changeZeroEsquerda(data[x][0].split('-')[2]))).isocalendar()[1]
					if verificar_semana == take_actual_week_number:
						acertos.append(float(data[x][7]))
						erros.append(float(data[x][8]))

	total_questoes = sum(acertos) + sum(erros)
	total_questoes = str(round(total_questoes))
	if len(total_questoes) > 9:
		return '99999999'
	else:
		return total_questoes
def FUNCTION_Acertos_Simulados(nome_simulado):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_simulado = str(nome_simulado)
	acertos = []

	for x in range(len(data)):
		if data[x][2] == 'Simulado':
			if data[x][3] == str(nome_simulado):
				acertos.append(float(data[x][7]))

	total_acertos = sum(acertos)
	total_acertos = str(round(total_acertos))
	if len(total_acertos) > 9:
		return '99999999+'
	else:
		return total_acertos
def FUNCTION_Acertos_Simulados_Weekly(nome_simulado):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_simulado = str(nome_simulado)
	acertos = []

	take_actual_week_number = \
	datetime.date(int(str(date.today()).split('-')[0]), int(changeZeroEsquerda(str(date.today()).split('-')[1])),
				  int(changeZeroEsquerda(str(date.today()).split('-')[2]))).isocalendar()[1]
	for x in range(len(data)):
		if data[x][2] == 'Simulado':
			if data[x][3] == str(nome_simulado):
				if data[x][0].split('-')[0] == str(date.today()).split('-')[0]:
					verificar_semana = \
					datetime.date(int(data[x][0].split('-')[0]), int(changeZeroEsquerda(data[x][0].split('-')[1])),
								  int(changeZeroEsquerda(data[x][0].split('-')[2]))).isocalendar()[1]
					if verificar_semana == take_actual_week_number:
						acertos.append(float(data[x][7]))

	total_acertos = sum(acertos)
	total_acertos = str(round(total_acertos))
	if len(total_acertos) > 9:
		return '99999999'
	else:
		return total_acertos
def FUNCTION_Erros_Simulados(nome_simulado):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_simulado = str(nome_simulado)
	erros = []

	for x in range(len(data)):
		if data[x][2] == 'Simulado':
			if data[x][3] == str(nome_simulado):
				erros.append(float(data[x][8]))

	total_erros = sum(erros)
	total_erros = str(round(total_erros))
	if len(total_erros) > 9:
		return '99999999+'
	else:
		return total_erros
def FUNCTION_Erros_Simulados_Weekly(nome_simulado):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_simulado = str(nome_simulado)
	erros = []

	take_actual_week_number = \
	datetime.date(int(str(date.today()).split('-')[0]), int(changeZeroEsquerda(str(date.today()).split('-')[1])),
				  int(changeZeroEsquerda(str(date.today()).split('-')[2]))).isocalendar()[1]
	for x in range(len(data)):
		if data[x][2] == 'Simulado':
			if data[x][3] == str(nome_simulado):
				if data[x][0].split('-')[0] == str(date.today()).split('-')[0]:
					verificar_semana = \
					datetime.date(int(data[x][0].split('-')[0]), int(changeZeroEsquerda(data[x][0].split('-')[1])),
								  int(changeZeroEsquerda(data[x][0].split('-')[2]))).isocalendar()[1]
					if verificar_semana == take_actual_week_number:
						erros.append(float(data[x][8]))

	total_erros = sum(erros)
	total_erros = str(round(total_erros))
	if len(total_erros) > 9:
		return '99999999'
	else:
		return total_erros
def FUNCTION_Simulados_Realizados(nome_simulado):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_simulado = str(nome_simulado)
	realizados = 0
	for x in range(len(data)):
		if data[x][2] == 'Simulado':
			if data[x][3] == str(nome_simulado):
				if data[x][6][2] == 'Estudado' or data[x][7] != '0' or data[x][8] != '0':
					realizados += 1
	realizados = str(round(realizados))
	if len(realizados) > 9:
		return '99999999+'
	else:
		return realizados
def FUNCTION_Simulados_Realizados_Weekly(nome_simulado):
	data = pickle.load((open("data_timeline.p", "rb")))
	nome_simulado = str(nome_simulado)
	realizados = 0
	take_actual_week_number = \
	datetime.date(int(str(date.today()).split('-')[0]), int(changeZeroEsquerda(str(date.today()).split('-')[1])),
				  int(changeZeroEsquerda(str(date.today()).split('-')[2]))).isocalendar()[1]

	for x in range(len(data)):
		if data[x][2] == 'Simulado':
			if data[x][3] == str(nome_simulado):
				if data[x][0].split('-')[0] == str(date.today()).split('-')[0]:
					verificar_semana = \
					datetime.date(int(data[x][0].split('-')[0]), int(changeZeroEsquerda(data[x][0].split('-')[1])),
								  int(changeZeroEsquerda(data[x][0].split('-')[2]))).isocalendar()[1]
					if verificar_semana == take_actual_week_number:
						if data[x][6][2] == 'Estudado' or data[x][7] != '0' or data[x][8] != '0':
							realizados += 1
	realizados = str(round(realizados))
	if len(realizados) > 9:
		return '99999999'
	else:
		return realizados
def simulado_destaque_finder():
	data = pickle.load((open("data_timeline.p", "rb")))
	simulados = pickle.load((open("simulados.p", "rb")))
	simulados_and_TaxaAcertos = {}
	for item in range(len(simulados)):
		simulados_and_TaxaAcertos[simulados[item]] = float(splitPercent(FUNCTION_TaxaAcertos_Simulados(simulados[item])))
	try:
		max_taxa = list(simulados_and_TaxaAcertos.values()).index(max(list(simulados_and_TaxaAcertos.values())))
		return list(simulados_and_TaxaAcertos.keys())[max_taxa]
	except ValueError:
		return "Sem Simulado"
#////////////////////////////////////////////////////////////////////////////

class ButtonGrid_Menu_v2 (ButtonBehavior, MDBoxLayout, HoverBehavior):
	pass


class ButtonGridBlue(ButtonBehavior, MDBoxLayout, HoverBehavior):
	tema = pickle.load((open("tema.p", "rb")))
	cor = StringProperty(tema[0].cor_aplicativo)

class MDBoxLayout_Hover(MDBoxLayout, HoverBehavior):
	Padrao = Tema(cor_aplicativo='686fa3', cor_aplicativo_tuple=[0.3098, 0.3411, 0.5333], cor_fundo_menu_deg1='464c7e',
				  cor_fundo_menu_deg2='575e91', cor_fundo_trabalho='e6ebfb',
				  cor_fundo_trabalho_tuple=[0.9019, 0.9215, 0.9843, 1], cor_widget='eef2fe', cor_widget_hover='f4f7fe',
				  cor_letra_menu='8793e9', cor_licenca='cedeff', cor_licenca_texto='686fa3')

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

	tema = read_or_new_pickle(path="tema.p", default=[Padrao, "Padrão"])
	tema = pickle.load((open("tema.p", "rb")))
	cor = StringProperty(tema[0].cor_widget)

class MDBoxLayout_Hover_Blue(MDBoxLayout, HoverBehavior):
	tema = pickle.load((open("tema.p", "rb")))
	cor = StringProperty(tema[0].cor_aplicativo)

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
	tema = pickle.load((open("tema.p", "rb")))
	cor_aplicativo = tema[0].cor_aplicativo
	cor_widget = tema[0].cor_widget

class Zoom_acertos_erros (MDFloatLayout):
	tema = pickle.load((open("tema.p", "rb")))
	cor_aplicativo = tema[0].cor_aplicativo
	cor_widget = tema[0].cor_widget


class Conteudo(MDList):
	def __init__(self, lista, **kwargs):
		self.data = pickle.load((open("data_subjects_topics.p", "rb")))
		super().__init__(**kwargs)
		for topico in list(lista):
			if topico == "":
				pass
			else:
				self.add_widget(OneLineListItem(text ="[color=686fa3]  {}[/color]".format(topico)))

class SpinnerOptions(SpinnerOption):
	def __init__(self, **kwargs):
		super(SpinnerOptions, self).__init__(**kwargs)
		self.background_normal = ''
		self.background_color = get_color_from_hex('#{}'.format(InvisionStudy.cor_widgets_default_str))
		self.height = 40
		self.color = get_color_from_hex('#{}'.format(InvisionStudy.cor_principal_aplicativo_str))

class SpinnerDropdown(DropDown):
	def __init__(self, **kwargs):
		super(SpinnerDropdown, self).__init__(**kwargs)
		self.auto_width = True
		self.color =  get_color_from_hex('#{}'.format(InvisionStudy.cor_widgets_default_str))

class ButtonGrid(ButtonBehavior, MDBoxLayout, HoverBehavior):

	tema = pickle.load((open("tema.p", "rb")))
	cor = StringProperty(tema[0].cor_widget)

	def time_delay(self):
		def delay_color_change(dt):
			self.cor = tema[0].cor_widget
		Clock.schedule_once(delay_color_change, 0.1)

class SpinnerOptions_Blue(SpinnerOption):
	def __init__(self, **kwargs):
		super(SpinnerOptions, self).__init__(**kwargs)
		self.background_normal = ''
		self.background_color = get_color_from_hex('#FFFFFF')
		self.height = 40
		#self.color = get_color_from_hex('#FFFFFF')

class SpinnerDropdown_Blue(DropDown):
	def __init__(self, **kwargs):
		super(SpinnerDropdown, self).__init__(**kwargs)
		self.auto_width = True
		self.color = get_color_from_hex('#FFFFFF')


class Inicio(Screen):
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

	# ALTERAR FOTO
	user_picture = StringProperty('')
	path_user = read_or_new_pickle(path="path.p", default=["Invision Code"])
	change_picture_ = None

	class Conteudo_AlterarImagem(MDFloatLayout, HoverBehavior):
		path_example = r"Carlos Santos"

	def change_picture(self, root, *args):
		self.tema = pickle.load((open("tema.p", "rb")))
		if not self.change_picture_:
			self.change_picture_ = MDDialog(
				title=f'[color={self.cor_aplicativo}]Alterar Nome[/color]',
				md_bg_color=self.tema[0].cor_fundo_trabalho_tuple,
				type="custom",
				auto_dismiss=True,
				content_cls=self.Conteudo_AlterarImagem(),
				buttons=[
					MDFlatButton(
						text=f"[color={self.cor_aplicativo}][b]CANCELAR[/color][/b]",
						theme_text_color="Custom",
						on_release=self.close_change_picture),
					MDFlatButton(
						text=f"[color={self.cor_aplicativo}][b]ALTERAR[/color][/b]",
						theme_text_color="Custom",
						on_release=root.alterar_foto)])

		self.change_picture_.open()

	def close_change_picture(self, obj):
		self.change_picture_.dismiss()

	def alterar_foto(self, *args):
		path = str(self.change_picture_.content_cls.ids.user_picture_path.text)
		path = ' '.join(path.split())
		if len(path) <= 15:
			paths = pickle.load((open("path.p", "rb")))
			paths.clear()
			paths.append(path)
			pickle.dump(paths, open("path.p", "wb"))
			self.user_picture = "{}".format(paths[0])
			self.change_picture_.dismiss()
			self.change_picture_.content_cls.ids.user_picture_path.text = ""
			toast("Nome Alterado Com Sucesso.")
		else:
			toast("Atenção: Limite Máximo de Caractere é 15.")



	data = read_or_new_pickle(path="data_subjects_topics.p", default={})

	tema = pickle.load((open("tema.p", "rb")))
	cor_aplicativo = StringProperty(tema[0].cor_aplicativo)

	# MOSTRAR INFORMAÇÕES DE CADASTRO
	show_info_ = None
	class Conteudo_ShowInfo(MDFloatLayout, HoverBehavior):
		cor_aplicativo = '686fa3'
		cor_widget = 'eef2fe'
		simulado_name_dynamic = StringProperty('')
	def show_info(self, root, *args):
		if not self.show_info_:
			self.show_info_ = MDDialog(
				title=f'[color={self.cor_aplicativo}][b]Informações de Cadastro[/b][/color]',
				text = f"[color={self.cor_aplicativo}]\n[b]Nome do Usuário:[/b] Clayton Silva dos Santos\n\n[b]Email:[/b] clayton_box@outlook.com\n\n[b]Tema:[/b] Padrão\n\n[b]Plano de Utilização:[/b] Plano Anual Standard\n\n[b]Data de Expiração:[/b] 03/03/2022\n\n[b]Status:[/b] Ativo\n\n[/color]",
				md_bg_color=self.tema[0].cor_fundo_trabalho_tuple,
				type="custom",
				size_hint=[0.4, 0.4],
				auto_dismiss=True)
		self.show_info_.open()
	def close_show_info_(self, obj):
		self.show_info_.dismiss()

	# CRIAR MATÉRIA
	criar_nova_materia  = None
	class Conteudo_CriarNovaMateria(MDFloatLayout, HoverBehavior):
		cor_aplicativo = '686fa3'
		cor_widget = 'eef2fe'
		simulado_name_dynamic = StringProperty('')
	def criar_materia(self, root, *args):
		self.tema = pickle.load((open("tema.p", "rb")))
		if not self.criar_nova_materia:
			self.criar_nova_materia = MDDialog(
					title=f'[color={self.cor_aplicativo}]Criar Nova Matéria[/color]',
					md_bg_color=self.tema[0].cor_fundo_trabalho_tuple,
					type="custom",
					auto_dismiss=True,
					content_cls=self.Conteudo_CriarNovaMateria(),
					buttons=[
						MDFlatButton(
							text=f"[color={self.cor_aplicativo}][b]CANCELAR[/color][/b]",
							theme_text_color="Custom",
							on_release=self.close_criar_nova_materia),
						MDFlatButton(
							text=f"[color={self.cor_aplicativo}][b]CRIAR MATÉRIA[/color][/b]",
							theme_text_color="Custom",
							on_release=root.criar_materia_addFunction)])

		self.criar_nova_materia.open()
	def close_criar_nova_materia(self, obj):
		self.criar_nova_materia.dismiss()
	def criar_materia_addFunction(self, root, *args):
		new_materia_name = ' '.join(self.criar_nova_materia.content_cls.ids.materia_name.text.split()).lower().title()
		self.data = pickle.load((open("data_subjects_topics.p", "rb")))
		todas_materias = list(self.data.keys())

		if new_materia_name == "":
			toast("Atenção: Nome invalido.")

		if  new_materia_name in todas_materias:
			toast('Atenção: Notamos que já existe uma matéria com o nome {}.'.format(new_materia_name))

		if len(new_materia_name) > 15:
			toast('Atenção: O limite máximo de caracteres são 15.')

		if not new_materia_name in todas_materias and len(new_materia_name) <= 15 and new_materia_name != "":
			self.data = pickle.load((open("data_subjects_topics.p", "rb")))
			self.data[new_materia_name] = [[], []]
			pickle.dump(self.data, open("data_subjects_topics.p", "wb"))
			self.criar_nova_materia.content_cls.ids.materia_name.text = ''
			toast('Matéria {} foi criada com sucesso!'.format(new_materia_name))
			#self.criar_nova_materia.dismiss()
			try:
				new_data_refreshed = pickle.load((open("data_subjects_topics.p", "rb")))
				materia_sort = list(new_data_refreshed.keys())
				materia_sort.sort()
				self.remover_materia_.content_cls.ids.spinnerMaterias_.values = materia_sort
			except AttributeError: pass
			try:
				new_data_refreshed = pickle.load((open("data_subjects_topics.p", "rb")))
				materia_sort = list(new_data_refreshed.keys())
				materia_sort.sort()
				self.criar_novo_topico.content_cls.ids.spinnerMaterias_.values = materia_sort
			except AttributeError: pass
			try:
				new_data_refreshed = pickle.load((open("data_subjects_topics.p", "rb")))
				materia_sort = list(new_data_refreshed.keys())
				materia_sort.sort()
				self.remover_topico_.content_cls.ids.spinnerMaterias_.values = materia_sort
			except AttributeError:pass
			try:
				if self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_categoria.text == "Teoria" or self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_categoria.text == "Exercicios":
					new_data_refreshed = pickle.load((open("data_subjects_topics.p", "rb")))
					materia_sort = list(new_data_refreshed.keys())
					materia_sort.sort()
					self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_materia.values = materia_sort
			except AttributeError: pass

	class Topicos_Spinner(Spinner):
		def __init__(self, **kwargs):
			super().__init__(**kwargs)
			self.tema = pickle.load((open("tema.p", "rb")))
			self.dropdown_cls = SpinnerDropdown
			self.option_cls = SpinnerOptions
			self.color = self.tema[0].cor_aplicativo_tuple
			self.bold = True
			self.dropdown_cls.max_height = self.height * 2 + 2 * 2
			self.text = "Tópicos"

	# REMOVER MATÉRIA
	remover_materia_ = None
	class Conteudo_RemoverMateria(MDFloatLayout, HoverBehavior):
		cor_aplicativo = '686fa3'
		cor_widget = 'eef2fe'
		simulado_name_dynamic = StringProperty('')
	class Materias_Spinner(Spinner):
		def __init__(self, **kwargs):
			super().__init__(**kwargs)
			self.tema = pickle.load((open("tema.p", "rb")))
			self.data = pickle.load((open("data_subjects_topics.p", "rb")))
			self.dropdown_cls = SpinnerDropdown
			self.option_cls = SpinnerOptions
			self.color = self.tema[0].cor_aplicativo_tuple
			self.bold = True
			self.dropdown_cls.max_height = self.height * 2 + 2 * 2
			self.text = "Matérias"
			self.materias = list(self.data.keys())
			self.materias.sort()
			self.values = self.materias
	def remover_materia(self, root, *args):
		self.tema = pickle.load((open("tema.p", "rb")))
		if not self.remover_materia_:
			self.remover_materia_ = MDDialog(
				title=f'[color={self.cor_aplicativo}]Remover Matéria[/color]',
				md_bg_color=self.tema[0].cor_fundo_trabalho_tuple,
				type="custom",
				auto_dismiss=True,
				content_cls=self.Conteudo_RemoverMateria(),
				buttons=[
					MDFlatButton(
						text=f"[color={self.cor_aplicativo}][b]CANCELAR[/color][/b]",
						theme_text_color="Custom",
						on_release=self.close_remove_materia),
					MDFlatButton(
						text=f"[color={self.cor_aplicativo}][b]EXCLUIR MATÉRIA[/color][/b]",
						theme_text_color="Custom",
						on_release=root.remover_materia_removeFunction)])

		self.remover_materia_.open()
	def close_remove_materia(self, obj):
		self.remover_materia_.dismiss()
	def remover_materia_removeFunction(self, root, *args):
		materia2remove = str(self.remover_materia_.content_cls.ids.spinnerMaterias_.text)
		self.data = pickle.load((open("data_subjects_topics.p", "rb")))
		if materia2remove == "Matérias":
			toast("Atenção: Nenhuma matéria selecionada.")

		if materia2remove != "Matérias":
			self.remover_materia_.content_cls.ids.spinnerMaterias_.text = 'Matérias'
			del self.data[materia2remove]
			pickle.dump(self.data, open("data_subjects_topics.p", "wb"))
			toast(f'Matéria {materia2remove} foi removida com sucesso')
			new_data_refreshed = pickle.load((open("data_subjects_topics.p", "rb")))
			new_data_refreshed = list(new_data_refreshed.keys())
			new_data_refreshed.sort()
			self.remover_materia_.content_cls.ids.spinnerMaterias_.values = new_data_refreshed
			try:
				new_data_refreshed = pickle.load((open("data_subjects_topics.p", "rb")))
				materia_sort = list(new_data_refreshed.keys())
				materia_sort.sort()
				self.criar_novo_topico.content_cls.ids.spinnerMaterias_.values = materia_sort
				if materia2remove == self.criar_novo_topico.content_cls.ids.spinnerMaterias_.text:
					self.criar_novo_topico.content_cls.ids.spinnerMaterias_.text = "Matérias"
			except AttributeError: pass
			try:
				if self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_categoria.text == "Teoria" or  self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_categoria.text == "Exercicios":
					self.data_refreshed = pickle.load((open("data_subjects_topics.p", "rb")))
					self.subjects_sort = list(self.data_refreshed.keys())
					self.subjects_sort.sort()
					self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_materia.values = self.subjects_sort
					if self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_materia.text == materia2remove:

						self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_materia.text = "Matérias"
						self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_topico.text = "Tópicos"
						self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_topico.values = []
						self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_materia.values = self.subjects_sort

			except AttributeError:
				pass

	# CRIAR TÓPICO
	criar_novo_topico = None
	class Conteudo_CriarNovoTopico(MDFloatLayout, HoverBehavior):
		cor_aplicativo = '686fa3'
		cor_widget = 'eef2fe'
		simulado_name_dynamic = StringProperty('')
	def criar_topico(self, root, *args):
		self.tema = pickle.load((open("tema.p", "rb")))
		if not self.criar_novo_topico:
			self.criar_novo_topico = MDDialog(
					title=f'[color={self.cor_aplicativo}]Criar Novo Tópico[/color]',
					md_bg_color=self.tema[0].cor_fundo_trabalho_tuple,
					type="custom",
					auto_dismiss=True,
					content_cls=self.Conteudo_CriarNovoTopico(),
					buttons=[
						MDFlatButton(
							text=f"[color={self.cor_aplicativo}][b]CANCELAR[/color][/b]",
							theme_text_color="Custom",
							on_release=self.close_criar_novo_topico),
						MDFlatButton(
							text=f"[color={self.cor_aplicativo}][b]CRIAR TÓPICO[/color][/b]",
							theme_text_color="Custom",
							on_release=root.criar_topico_addFunction)])
		self.criar_novo_topico.open()
	def close_criar_novo_topico(self, obj):
		self.criar_novo_topico.dismiss()
	def criar_topico_addFunction(self, root, *args):
		materia_escolhida = self.criar_novo_topico.content_cls.ids.spinnerMaterias_.text
		new_topico_name = ' '.join(self.criar_novo_topico.content_cls.ids.topico_name.text.split()).lower().title()
		self.data = pickle.load((open("data_subjects_topics.p", "rb")))

		if new_topico_name == "" or materia_escolhida == "Matérias":
			toast("Atenção: Nome invalido.")

		if len(new_topico_name) > 15:
			toast('Atenção: O limite máximo de caracteres são 15.')

		if materia_escolhida != "Matérias" and len(new_topico_name) <= 15 and new_topico_name != "":
			materia_escolhida_topicos_existententes = self.data[materia_escolhida][1]
			if new_topico_name in list(materia_escolhida_topicos_existententes):
				toast('Atenção: Notamos que já existe um Tópico {} em {}.'.format(new_topico_name, materia_escolhida))

			if not new_topico_name in list(materia_escolhida_topicos_existententes):
				self.data[materia_escolhida][1].append(new_topico_name)
				pickle.dump(self.data, open("data_subjects_topics.p", "wb"))
				self.criar_novo_topico.content_cls.ids.topico_name.text = ""
				toast('Tópico {} adicionado com sucesso à matéria {}'.format(new_topico_name, materia_escolhida))
				try:
					materia_escolhida_remover_dialog = self.remover_topico_.content_cls.ids.spinnerMaterias_.text
					if materia_escolhida_remover_dialog == materia_escolhida:
						self.data_refreshed = pickle.load((open("data_subjects_topics.p", "rb")))
						self.data_refreshed = list(self.data_refreshed[materia_escolhida][1])
						self.data_refreshed.sort()
						self.remover_topico_.content_cls.ids.spinnerTopicos_.text = "Tópicos"
						self.remover_topico_.content_cls.ids.spinnerTopicos_.values = self.data_refreshed
				except AttributeError: pass
				try:
					if self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_categoria.text == "Teoria" or self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_categoria.text == "Exercicios":
						if self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_materia.text == materia_escolhida:
							self.data_refreshed = pickle.load((open("data_subjects_topics.p", "rb")))
							self.data_refreshed = list(self.data_refreshed[materia_escolhida][1])
							self.data_refreshed.sort()
							self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_topico.values = self.data_refreshed
				except AttributeError:
					pass


	# REMOVER TÓPICO
	remover_topico_ = None
	class Conteudo_RemoverTopico(MDFloatLayout, HoverBehavior):
		cor_aplicativo = '686fa3'
		cor_widget = 'eef2fe'
		simulado_name_dynamic = StringProperty('')

		def refresh_TopicosSpinner(self, root, *args):
			materia_escolhida = self.ids.spinnerMaterias_.text
			if materia_escolhida != "Matérias":
				self.data = pickle.load((open("data_subjects_topics.p", "rb")))
				materia_topicos = list(self.data[materia_escolhida][1])
				materia_topicos.sort()
				self.ids.spinnerTopicos_.text = "Tópicos"
				self.ids.spinnerTopicos_.values = materia_topicos
	def remover_topico(self, root, *args):
		self.tema = pickle.load((open("tema.p", "rb")))
		if not self.remover_topico_:
			self.remover_topico_ = MDDialog(
					title=f'[color={self.cor_aplicativo}]Remover Tópico[/color]',
					md_bg_color=self.tema[0].cor_fundo_trabalho_tuple,
					type="custom",
					auto_dismiss=True,
					content_cls=self.Conteudo_RemoverTopico(),
					buttons=[
						MDFlatButton(
							text=f"[color={self.cor_aplicativo}][b]CANCELAR[/color][/b]",
							theme_text_color="Custom",
							on_release=self.close_remover_topico),
						MDFlatButton(
							text=f"[color={self.cor_aplicativo}][b]EXCLUIR TÓPICO[/color][/b]",
							theme_text_color="Custom",
							on_release=root.remover_topico_removeFunction)])
		self.remover_topico_.open()
	def close_remover_topico(self, obj):
		self.remover_topico_.dismiss()
	def remover_topico_removeFunction(self, root, *args):
		materia_escolhida = self.remover_topico_.content_cls.ids.spinnerMaterias_.text
		topico_escolhido = self.remover_topico_.content_cls.ids.spinnerTopicos_.text
		if materia_escolhida != "Matérias" and topico_escolhido != "Tópicos":
			self.data = pickle.load((open("data_subjects_topics.p", "rb")))
			self.data[materia_escolhida][1].remove(topico_escolhido)
			pickle.dump(self.data, open("data_subjects_topics.p", "wb"))
			self.data_refreshed = pickle.load((open("data_subjects_topics.p", "rb")))
			self.data_refreshed = list(self.data_refreshed[materia_escolhida][1])
			self.data_refreshed.sort()
			self.remover_topico_.content_cls.ids.spinnerTopicos_.text = "Tópicos"
			self.remover_topico_.content_cls.ids.spinnerTopicos_.values = self.data_refreshed
			toast('Tópico {} removido com sucesso da matéria {}'.format(topico_escolhido, materia_escolhida))
		try:
			if self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_categoria.text == "Teoria" or self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_categoria.text == "Exercicios":
				if self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_materia.text == materia_escolhida:
					self.data_refreshed = pickle.load((open("data_subjects_topics.p", "rb")))
					self.data_refreshed = list(self.data_refreshed[materia_escolhida][1])
					self.data_refreshed.sort()
					self.manager.get_screen(
						'Cronograma').adicionar_item.content_cls.ids.spinner_topico.values = self.data_refreshed
				if self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_topico.text == topico_escolhido:
					self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_topico.text = "Tópicos"
		except AttributeError:
			pass


	materia_next_event_name = StringProperty('Sem Matéria')
	materia_next_event_data = StringProperty('00/00/0000')
	materia_next_event_time = StringProperty('00h00min')

	simulado_next_event_name = StringProperty('Sem Simulado')
	simulado_next_event_data = StringProperty('00/00/0000')
	simulado_next_event_time = StringProperty('00h00min')

	taxa_acertos = StringProperty('0.0 %')
	taxa_acertos_ThisWeek = StringProperty('0.0 %')
	horas_estudadas = StringProperty('0h')
	horas_estudadas_ThisWeek = StringProperty('0h')
	questoes_realizadas = StringProperty('0')
	questoes_realizadas_ThisWeek = StringProperty('0')
	simulados_realizados = StringProperty('0')
	simulados_realizados_ThisWeek = StringProperty('0')
	value = NumericProperty(250)

	def OpenFileManager(self):
		pass

	def textColor(self):
		self.ids.button_cronograma_texto.color = get_color_from_hex('#ffffff')

	def on_enter(self, *args):
		paths = pickle.load((open("path.p", "rb")))
		self.user_picture = r"{}".format(paths[0])

		self.data_cronograma = pickle.load((open("data_timeline.p", "rb")))
		next_event = filter(sortData(onlyTimeGreater(eliminar_EscolhasRepetidas(self.data_cronograma))))
		next_event_simulados = filter(sortData(onlyTimeGreater(eliminar_EscolhasRepetidas(self.data_cronograma))), "Simulado")

		def nextEvento_Teorias_Exercicios(dt):
			data_cronograma = pickle.load((open("data_timeline.p", "rb")))
			next_event = filter(sortData(onlyTimeGreater(eliminar_EscolhasRepetidas(data_cronograma))))
			if len(next_event) != 0:
				self.materia_next_event_name = next_event[0][3]
				self.materia_next_event_data = changeData(next_event[0][0])
				self.materia_next_event_time = changeTime(next_event[0][1])
			if len(next_event) == 0:
				self.materia_next_event_name = 'Sem Matéria'
				self.materia_next_event_data = '00/00/0000'
				self.materia_next_event_time = '00h00min'
		def nextEvento_Simulados(dt):
			data_cronograma = pickle.load((open("data_timeline.p", "rb")))
			next_event_simulados = filter(sortData(onlyTimeGreater(eliminar_EscolhasRepetidas(self.data_cronograma))), "Simulado")
			if len(next_event_simulados) != 0:
				self.simulado_next_event_name = next_event_simulados[0][3]
				self.simulado_next_event_data = changeData(next_event_simulados[0][0])
				self.simulado_next_event_time = changeTime(next_event_simulados[0][1])
			if len(next_event_simulados) == 0:
				self.simulado_next_event_name = 'Sem Simulado'
				self.simulado_next_event_data = '00/00/0000'
				self.simulado_next_event_time = '00h00min'

		# ALTERAR SIMULADOS
		if len(next_event_simulados) != 0:
			self.simulado_next_event_name = next_event_simulados[0][3]
			self.simulado_next_event_data = changeData(next_event_simulados[0][0])
			self.simulado_next_event_time = changeTime(next_event_simulados[0][1])
		if len(next_event_simulados) == 0:
			self.simulado_next_event_name = 'Sem Simulado'
			self.simulado_next_event_data = '00/00/0000'
			self.simulado_next_event_time = '00h00min'

		# ALTERAR EXERCICIOS | TEORIAS
		if len(next_event) != 0:
			self.materia_next_event_name = next_event[0][3]
			self.materia_next_event_data = changeData(next_event[0][0])
			self.materia_next_event_time = changeTime(next_event[0][1])
		if len(next_event) == 0:
			self.materia_next_event_name = 'Sem Matéria'
			self.materia_next_event_data = '00/00/0000'
			self.materia_next_event_time = '00h00min'

		Clock.schedule_interval(nextEvento_Teorias_Exercicios, 30)
		Clock.schedule_interval(nextEvento_Simulados, 30)

		self.taxa_acertos = FUNCTION_TaxaAcertos_Total()
		self.taxa_acertos_ThisWeek = FUNCTION_TaxaAcertos_Total_Weekly()
		self.horas_estudadas = FUNCTION_HorasEstudadas_Total()
		self.horas_estudadas_ThisWeek = FUNCTION_HorasEstudadas_Total_Weekly()
		self.questoes_realizadas = FUNCTION_QuestoesRealizadas_Total()
		self.questoes_realizadas_ThisWeek = FUNCTION_QuestoesRealizadas_Total_Weekly()
		self.simulados_realizados = FUNCTION_SimuladosRealizados_Total()
		self.simulados_realizados_ThisWeek = FUNCTION_SimuladosRealizados_Total_Weekly()


class Cronograma(Screen):

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

	# ALTERAR FOTO
	user_picture = StringProperty('')
	path_user = read_or_new_pickle(path="path.p", default=["Invision Code"])
	change_picture_ = None

	class Conteudo_AlterarImagem(MDFloatLayout, HoverBehavior):
		path_example = r"Carlos Santos"

	def change_picture(self, root, *args):
		self.tema = pickle.load((open("tema.p", "rb")))
		if not self.change_picture_:
			self.change_picture_ = MDDialog(
				title=f'[color={self.cor_aplicativo}]Alterar Nome[/color]',
				md_bg_color=self.tema[0].cor_fundo_trabalho_tuple,
				type="custom",
				auto_dismiss=True,
				content_cls=self.Conteudo_AlterarImagem(),
				buttons=[
					MDFlatButton(
						text=f"[color={self.cor_aplicativo}][b]CANCELAR[/color][/b]",
						theme_text_color="Custom",
						on_release=self.close_change_picture),
					MDFlatButton(
						text=f"[color={self.cor_aplicativo}][b]ALTERAR[/color][/b]",
						theme_text_color="Custom",
						on_release=root.alterar_foto)])

		self.change_picture_.open()

	def close_change_picture(self, obj):
		self.change_picture_.dismiss()

	def alterar_foto(self, *args):
		path = str(self.change_picture_.content_cls.ids.user_picture_path.text)
		path = ' '.join(path.split())
		if len(path) <= 15:
			paths = pickle.load((open("path.p", "rb")))
			paths.clear()
			paths.append(path)
			pickle.dump(paths, open("path.p", "wb"))
			self.user_picture = "{}".format(paths[0])
			self.change_picture_.dismiss()
			self.change_picture_.content_cls.ids.user_picture_path.text = ""
			toast("Nome Alterado Com Sucesso.")
		else:
			toast("Atenção: Limite Máximo de Caractere é 15.")

	Padrao = Tema(cor_aplicativo='686fa3', cor_aplicativo_tuple=[0.3098, 0.3411, 0.5333], cor_fundo_menu_deg1='464c7e',
				  cor_fundo_menu_deg2='575e91', cor_fundo_trabalho='e6ebfb',
				  cor_fundo_trabalho_tuple=[0.9019, 0.9215, 0.9843, 1], cor_widget='eef2fe', cor_widget_hover='f4f7fe',
				  cor_letra_menu='8793e9', cor_licenca='cedeff', cor_licenca_texto='686fa3')

	tema = read_or_new_pickle(path="tema.p", default=[Padrao, "Padrão"])
	tema = pickle.load((open("tema.p", "rb")))
	cor_aplicativo = StringProperty(tema[0].cor_aplicativo)
	dialog10 = None
	confirmar_remover = None
	index_value = StringProperty()

	info_cronograma_item = None
	class Conteudo_InfoCronograma(MDFloatLayout):
		cor_aplicativo = '686fa3'
		cor_widget = 'eef2fe'
		info_data = StringProperty('26/02/2022')
	def info_cronograma(self, *args):
		try:
			if not self.info_cronograma_item:
				self.tema = pickle.load((open("tema.p", "rb")))
				self.info_cronograma_item = MDDialog(
					title=f'[color={self.cor_aplicativo}]Informações[/color]',
					md_bg_color=self.tema[0].cor_fundo_trabalho_tuple,
					type="custom",
					auto_dismiss=True,
					content_cls=self.Conteudo_InfoCronograma(),
					buttons=[
						MDFlatButton(
							text=f"[color={self.cor_aplicativo}][b]ALTERAR QUANTIDADE[/color][/b]",
							theme_text_color="Custom",
							on_release=self.alterar_quantidade_function)])
			self.info_cronograma_item.open()
		except AttributeError:
			pass
	def close_info_cronograma_item_dialog(self, obj):
		self.info_cronograma_item.dismiss()

	def alterar_quantidade_function(self, *args):
		def rebuildDataStyle(lista, color_hex=self.tema[0].cor_aplicativo):
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

		def default_data(string):
			return '-'.join([string.split('/')[2], string.split('/')[1], string.split('/')[0]])

		def default_horario(string):
			return string.split("h")[0] + ':' + string.split("h")[1].split("min")[0] + ":" + "00"

		def atualizar_acertos_erros(acertos, erros, option):
			data_in_list = []
			data = pickle.load((open("data_timeline.p", "rb")))
			print("BRUTO, \n", data)
			data = organizerData(sortData(data))
			for y in range(len(data)):
				data_in_list.append([])
				for x in range(len(data[y])):
					data_in_list[y].append(data[y][x])

			data_styled = CronogramaTableStyle(colorData(data))

			for x in range(len(data)):
				if data_styled[x] == option[0]:
					data_in_list[x][0] = default_data(data_in_list[x][0])
					data_in_list[x][1] = default_horario(data_in_list[x][1])
					data_in_list[x][5] = default_horario(data_in_list[x][5])
					data_in_list[x][7] = str(acertos)
					data_in_list[x][8] = str(erros)
					data_in_list[x][9] = str(calcularTaxaAcerto(int(acertos), int(erros)))

			for x in range(len(data_in_list)):
				try:
					data_in_list[x][0] = default_data(data_in_list[x][0])
					data_in_list[x][1] = default_horario(data_in_list[x][1])
					data_in_list[x][5] = default_horario(data_in_list[x][5])
				except IndexError: pass

			for j in range(len(data_in_list)):
				data_in_list[j] = tuple(data_in_list[j])

			print('DATA FINALIZADO0', data_in_list)
			pickle.dump(data_in_list, open("data_timeline.p", "wb"))
			return data_in_list

		item_selecionado = list(self.ids.cronograma22.children[0].children[0].get_row_checks())

		self.acertos = self.info_cronograma_item.content_cls.ids.acertos_valor.text
		self.erros = self.info_cronograma_item.content_cls.ids.erros_valor.text

		if self.acertos == "": toast("Atenção: Valor invalido para acertos.")

		if self.erros == "": toast("Atenção: Valor invalido para erros.")

		if self.acertos != "" and self.erros != "":
			self.acertos = int(self.info_cronograma_item.content_cls.ids.acertos_valor.text)
			self.erros = int(self.info_cronograma_item.content_cls.ids.erros_valor.text)
			item_selecionado = rebuildDataStyle(item_selecionado)

			#######################################################################################
			# problema está aqui
			atualizar_acertos_erros(self.acertos, self.erros, item_selecionado)
			#######################################################################################

			self.info_cronograma_item.content_cls.ids.taxaAcerto_valor.text = f'[b]{calcularTaxaAcerto(self.acertos, self.erros)}[/b]'
			self.info_cronograma_item.dismiss()

			toast('Quantidade Alterada com Sucesso.')

			try:
				data_cronograma = pickle.load((open("data_timeline.p", "rb")))
				DataSearched = SearchByData(data_cronograma, str(self.data_selecionada))
				self.ids.cronograma22.children[0].children[0].update_row_data(self, AutoSizeTableRowsNum_Cronograma(
					DataSearched, InvisionStudy.rows_per_page_cronograma + 1))

				def refreshChecks(dt):
					try:
						self.ids.cronograma22.children[0].children[0].DoubleClickRefreshChecks()
					except IndexError:
						pass

				Clock.schedule_once(refreshChecks, 1.10)

			except AttributeError:
				today = date.today()
				data_cronograma = pickle.load((open("data_timeline.p", "rb")))
				DataSearched_today = SearchByData(data_cronograma, str(today))

				def refreshChecks(dt):
					try:
						self.ids.cronograma22.children[0].children[0].DoubleClickRefreshChecks()
					except IndexError:
						pass

				Clock.schedule_once(refreshChecks, 1.10)
	# TUDO CERTO NESSA FUNÇÃO
	def alterar_acertos_erros(self):
		def rebuildDataStyle(lista, color_hex=self.tema[0].cor_aplicativo):
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
		def finder(option):
			data = pickle.load((open("data_timeline.p", "rb")))
			data_styled = CronogramaTableStyle(colorData(organizerData(sortData(data))))
			data = organizerData(sortData(data))
			for x in range(len(data_styled)):
				if data_styled[x] == option[0]:
					return data[x]

		try:
			item_selecionado = list(self.ids.cronograma22.children[0].children[0].get_row_checks())
			if len(self.ids.cronograma22.children[0].children[0].get_row_checks()) == 1 and item_selecionado[0][2] != f'[color=#{self.tema[0].cor_aplicativo}]Teoria[/color]' and item_selecionado[0] != [' ', ' ', ' ',' ', ' ',' ']:
				self.data_exercicios = pickle.load((open("data_timeline.p", "rb")))
				self.data_exercicios = colorData(organizerData(sortData(self.data_exercicios)))

				self.info_cronograma()
				item_selecionado = rebuildDataStyle(item_selecionado)
				data_encontrado = finder(item_selecionado)

				self.info_cronograma_item.content_cls.ids.info_data.text = f'[b]Data[/b]\n{str(data_encontrado[0])}'
				self.info_cronograma_item.content_cls.ids.info_horario.text = f'[b]Horário[/b]\n{str(data_encontrado[1])}'
				self.info_cronograma_item.content_cls.ids.info_categoria.text = f'[b]Categoria[/b]\n{str(data_encontrado[2])}'
				self.info_cronograma_item.content_cls.ids.info_materia.text = f'[b]Matéria[/b]\n{str(data_encontrado[3])}'
				self.info_cronograma_item.content_cls.ids.info_topico.text = f'[b]Tópico[/b]\n{str(data_encontrado[4])}'
				self.info_cronograma_item.content_cls.ids.info_duracao.text = f'[b]Duração[/b]\n{str(data_encontrado[5])}'
				self.info_cronograma_item.content_cls.ids.acertos_valor.text = str(data_encontrado[7])
				self.info_cronograma_item.content_cls.ids.erros_valor.text = str(data_encontrado[8])
				self.info_cronograma_item.content_cls.ids.taxaAcerto_valor.text = f'[b]{str(data_encontrado[9])}[/b]'

			if len(self.ids.cronograma22.children[0].children[0].get_row_checks()) > 1:
				toast("Atenção: Selecione Apenas Um Item.")
		except IndexError:
			toast("Atenção: Nenhum Item Selecionado.")

		try:
			if item_selecionado[0][2] == f'[color=#{self.tema[0].cor_aplicativo}]Teoria[/color]':
				toast("Atenção: Teoria Não Possui Questões")
			if item_selecionado[0] == [' ', ' ', ' ', ' ', ' ', ' ']:
				toast("Atenção: Esse Item Não Possui Questões")
		except IndexError:
			pass


	value = NumericProperty(250)

	estudado = StringProperty()
	estudado_data = StringProperty()
	nao_estudado = StringProperty()
	nao_estudado_data = StringProperty()

	next_event_name = StringProperty()
	next_event_data = StringProperty()
	next_event_time = StringProperty()

	saveData_ = []
	saveTime_ = []
	saveDuration_ = []
	# ////////////////////////////////////////////////////////////////////////////
	# TABELA CRONOGRAMA
	class Tabela_Cronograma(MDBoxLayout):
		def __init__(self,**kwargs):
			super().__init__(**kwargs)
			self.data_exercicios = pickle.load((open("data_timeline.p", "rb")))
			self.today = date.today()
			self.data_today = SearchByData(self.data_exercicios, str(self.today))
			self.tema = pickle.load((open("tema.p", "rb")))
			data_table_cronograma = MDDataTable(
				background_color_header=get_color_from_hex("#{}".format(self.tema[0].cor_widget)),
				background_color_selected_cell=get_color_from_hex("#{}".format(self.tema[0].cor_widget_hover)),
				background_color_cell= get_color_from_hex("#{}".format(self.tema[0].cor_widget)),
				size_hint=(1, 1),
				elevation=0,
				check=True,
				use_pagination=True,
				rows_num=InvisionStudy.rows_per_page_cronograma,
				column_data=[(f"[color=#{self.tema[0].cor_aplicativo}]Data[/color]", dp(InvisionStudy.tabela_cronograma_dp_data - 2)),
							 (f"[color=#{self.tema[0].cor_aplicativo}]Horário[/color]", dp(InvisionStudy.tabela_cronograma_dp_horario - 4)),
							 (f"[color={self.tema[0].cor_aplicativo}]Categoria[/color]", dp(InvisionStudy.tabela_cronograma_dp_categoria) - 3),
							 (f"[color=#{self.tema[0].cor_aplicativo}]Matéria[/color]", dp(InvisionStudy.tabela_cronograma_dp_materia)),
							 (f"[color=#{self.tema[0].cor_aplicativo}]Tópico[/color]", dp(InvisionStudy.tabela_cronograma_dp_topico)),
							 (f"[color=#{self.tema[0].cor_aplicativo}]Status[/color]", dp(InvisionStudy.tabela_cronograma_dp_status ))],
				row_data=AutoSizeTableRowsNum_Cronograma(self.data_today, InvisionStudy.rows_per_page_cronograma + 1))
			#self.data_table_cronograma.bind(on_row_press=self.on_row_press)
			self.add_widget(data_table_cronograma)

	# FUNÇÕES E WIDGETS RELACIONADOS PARA CRIAR NOVA MATERIA
	adicionar_item = None
	class Conteudo_AdicionarItem(MDFloatLayout, HoverBehavior):
		saveData = []
		saveTime = []
		saveDuration = []
		duration_dialog_ = None
		tema = pickle.load((open("tema.p", "rb")))
		cor_aplicativo = StringProperty(tema[0].cor_aplicativo)

		class Conteudo_Duration(MDFloatLayout, HoverBehavior):
			pass
		def duration_dialog(self, root, *args):
			if not self.duration_dialog_:
				self.tema = pickle.load((open("tema.p", "rb")))
				self.duration_dialog_ = MDDialog(
					title=f'[color={self.cor_aplicativo}]Duração Do Seu Item[/color]',
					md_bg_color=self.tema[0].cor_fundo_trabalho_tuple,
					type="custom",
					content_cls=self.Conteudo_Duration(),
					auto_dismiss=True,
					buttons=[
						MDFlatButton(
							text=f"[color={self.cor_aplicativo}][b]CANCELAR[/color][/b]",
							theme_text_color="Custom",
							on_release=self.close_duration_dialog
						),
						MDFlatButton(
							text=f"[color={self.cor_aplicativo}][b]CONCLUIR[/color][/b]",
							theme_text_color="Custom",
							on_press = self.on_saveDuration,
							on_release=self.close_duration_dialog
						)
					]
				)

			self.duration_dialog_.open()
		def close_duration_dialog(self, obj):
			self.duration_dialog_.dismiss()
		def on_saveDuration(self, *args):
			horas = self.duration_dialog_.content_cls.ids.horas_.text
			minutos = self.duration_dialog_.content_cls.ids.minutos_.text
			self.saveDuration.clear()
			self.saveDuration.append(horas+":"+minutos)
			Cronograma.saveDuration_.clear()
			Cronograma.saveDuration_.append(horas+":"+minutos)
		def get_time(self, instance, time):
			return time
		def on_saveTime(self, instance, time):
			self.saveTime.clear()
			self.saveTime.append(str(time))
			Cronograma.saveTime_.clear()
			Cronograma.saveTime_.append(str(time))
		def show_time_picker(self):
			from datetime import datetime

			time_dialog = MDTimePicker()
			time_dialog.bind(time=self.get_time, on_save=self.on_saveTime)

			self.tema = pickle.load((open("tema.p", "rb")))
			# COR DOS MENUS
			time_dialog.primary_color = get_color_from_hex('#{}'.format(self.tema[0].cor_fundo_menu_deg1))
			time_dialog.accent_color = get_color_from_hex('#{}'.format(self.tema[0].cor_widget))
			time_dialog.selector_color = get_color_from_hex('#{}'.format(self.tema[0].cor_aplicativo))
			time_dialog.text_toolbar_color = get_color_from_hex('#{}'.format(self.tema[0].cor_widget_hover))

			# COR DOS TEXTOS
			time_dialog.text_color = get_color_from_hex('#{}'.format(self.tema[0].cor_aplicativo))
			time_dialog.text_current_color = get_color_from_hex('#{}'.format(self.tema[0].cor_fundo_menu_deg2))
			time_dialog.text_button_color = get_color_from_hex('#{}'.format(self.tema[0].cor_widget_hover))

			def convertMilitaryHour(string):
				converter = {'13': '01', '14': '02', '15': '03', '16': '04', '17': '05', '18': '06', '19': '07',
							 '20': '08',
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
		def on_saveData(self, instance, value, date_range):
			self.saveData.clear()
			self.saveData.append(value)
			Cronograma.saveData_.clear()
			Cronograma.saveData_.append(value)
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
			# date_dialog.mode = 'range'

			self.tema = pickle.load((open("tema.p", "rb")))
			# COR DOS MENUS
			date_dialog.primary_color = ("#{}".format(self.tema[0].cor_fundo_menu_deg1))
			date_dialog.accent_color = get_color_from_hex("#{}".format(self.tema[0].cor_widget))
			date_dialog.selector_color = get_color_from_hex("#{}".format(self.tema[0].cor_fundo_menu_deg2))
			date_dialog.text_toolbar_color = get_color_from_hex("#{}".format(self.tema[0].cor_widget))

			# COR DOS TEXTOS
			date_dialog.text_color = get_color_from_hex("#{}".format(self.tema[0].cor_aplicativo))
			date_dialog.text_current_color = get_color_from_hex("#{}".format(self.tema[0].cor_aplicativo))
			date_dialog.text_button_color = get_color_from_hex("#{}".format(self.tema[0].cor_aplicativo))
			try:
				date_dialog.year = int(str(self.saveData[0])[0:4])
				date_dialog.month = int(month(str(str(self.saveData[0])[5:7])))
			except AttributeError:pass
			except IndexError:pass

			date_dialog.open()
		def update_materia(self, *args):
			spinner_name = self.ids.spinner_materia.text
			self.data = pickle.load((open("data_subjects_topics.p", "rb")))

			if spinner_name != "Matérias" and spinner_name != "Nome Simulado":
				if self.ids.spinner_categoria.text == 'Teoria' or self.ids.spinner_categoria.text == 'Exercicios':
					self.ids.spinner_topico.text = "Tópicos"
					self.sorted = self.data[self.ids.spinner_materia.text][1]
					self.sorted.sort()
					self.ids.spinner_topico.values = self.sorted

			if self.ids.spinner_categoria.text == 'Simulado': pass
		def update_categoria(self, *args):
			spinner_name = self.ids.spinner_categoria.text
			self.data = pickle.load((open("data_subjects_topics.p", "rb")))
			self.simulados = pickle.load((open("simulados.p", "rb")))

			if spinner_name == 'Teoria' or spinner_name == 'Exercicios' or spinner_name == "Categorias":
				self.ids.spinner_materia.text = "Matérias"
				self.ids.spinner_topico.text = "Tópicos"
				self.topics = list(self.data.keys())
				self.topics.sort()
				self.ids.spinner_materia.values = self.topics

			if spinner_name == 'Simulado':
				self.simus = self.simulados
				self.simus.sort()
				self.ids.spinner_materia.values = self.simus
				self.ids.spinner_topico.text = "Personalizado"
				self.ids.spinner_materia.text = 'Nome Simulado'
				self.ids.spinner_topico.values = []

	class CategoriasSpinner(Spinner):
		def __init__(self, **kwargs):
			super().__init__(**kwargs)
			self.lista = ['Teoria', 'Exercicios', 'Simulado']
			self.lista.sort()
			self.values = self.lista
			self.dropdown_cls = SpinnerDropdown
			self.option_cls = SpinnerOptions
			self.tema = pickle.load((open("tema.p", "rb")))
			self.text = "Categoria"
			self.color = self.tema[0].cor_aplicativo_tuple
			self.bold = True
			self.dropdown_cls.max_height = self.height * 2 + 2 * 4
	class AllMateriasSpinner(Spinner):
		def __init__(self, **kwargs):
			super().__init__(**kwargs)
			self.dropdown_cls = SpinnerDropdown
			self.option_cls = SpinnerOptions
			self.tema = pickle.load((open("tema.p", "rb")))
			self.color = self.tema[0].cor_aplicativo_tuple
			self.bold = True
			self.dropdown_cls.max_height = self.height * 2 + 2 * 4
			self.text = "Matérias"
	class TopicosSpinner(Spinner):
		def __init__(self, **kwargs):
			super().__init__(**kwargs)
			self.dropdown_cls = SpinnerDropdown
			self.option_cls = SpinnerOptions
			self.tema = pickle.load((open("tema.p", "rb")))
			self.color = self.tema[0].cor_aplicativo_tuple
			self.bold = True
			self.dropdown_cls.max_height = self.height * 2 + 2 * 4
			self.text = "Tópicos"
	def adicionar_item_dialog(self, root, *args):
		if not self.adicionar_item:
			self.tema = pickle.load((open("tema.p", "rb")))
			self.adicionar_item = MDDialog(
				title=f'[color={self.cor_aplicativo}]Novo Item Cronograma[/color]',
				md_bg_color=self.tema[0].cor_fundo_trabalho_tuple,
				type="custom",
				auto_dismiss=False,
				content_cls=self.Conteudo_AdicionarItem(),
				buttons=[
					MDFlatButton(
						text=f"[color={self.cor_aplicativo}][b]CANCELAR[/color][/b]",
						theme_text_color="Custom",
						on_release=self.close_adicionar_itema_
					),
					MDFlatButton(
						text=f"[color={self.cor_aplicativo}][b]ADICIONAR ITEM[/color][/b]",
						theme_text_color="Custom",
						on_press=root.add_to_cronograma)])
		self.adicionar_item.open()
	def add_to_cronograma(self, *args):
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

		data = self.saveData_
		horario = self.saveTime_
		duracao = self.saveDuration_
		categoria = self.adicionar_item.content_cls.ids.spinner_categoria.text
		materia = self.adicionar_item.content_cls.ids.spinner_materia.text
		topico = self.adicionar_item.content_cls.ids.spinner_topico.text

		if categoria != "Simulados":
			if len(self.saveData_) > 0 and len(self.saveTime_) > 0 and len(self.saveDuration_) > 0 and categoria != "Categoria" and materia != "Matérias" and topico != "Tópicos" and duracao[0] != "00:00":
				horas = duracao[0].split(":")[0]
				minutos = duracao[0].split(":")[1]
				lista_data = [[]]
				lista_data[0].append(str(self.saveData_[0]))
				lista_data[0].append(self.saveTime_[0])

				if lista_data[0] not in lista_data_to_check:
					if len(horas) == 1:
						horas = '0' + horas
					if len(horas) == 2:
						horas = horas
					if len(minutos) == 1:
						minutos = '0' + minutos
					if len(minutos) == 2:
						minutos = minutos

					duration = horas + ':' + minutos + ':00'
					self.data_cronograma = pickle.load((open("data_timeline.p", "rb")))
					self.data_cronograma.append((str(data[0]), str(horario[0]), categoria, materia, topico, duration,("alert-circle", [1, 0, 0, 1], "Não Estudado"), '0', '0', '0.0 %'))
					pickle.dump(self.data_cronograma, open("data_timeline.p", "wb"))
					toast("Novo Item Adicionado Com Sucesso!")

					self.add_to_cronograma_refresh_table(self.saveData_[0])

					self.adicionar_item.content_cls.duration_dialog_.content_cls.ids.horas_.text = "00"
					self.adicionar_item.content_cls.duration_dialog_.content_cls.ids.minutos_.text = "00"

					# RESETAR PADROES DEFAULT
					self.saveData_.clear()
					self.saveTime_.clear()
					self.saveDuration_.clear()

					self.data_cronograma = pickle.load((open("data_timeline.p", "rb")))
					next_event = filter(sortData(onlyTimeGreater(eliminar_EscolhasRepetidas(self.data_cronograma))))

					if len(next_event) != 0:
						self.next_event_name = next_event[0][3]
						self.next_event_data = changeData(next_event[0][0])
						self.next_event_time = changeTime(next_event[0][1])
					if len(next_event) == 0:
						self.next_event_name = 'Sem Matéria'
						self.next_event_data = '00/00/0000'
						self.next_event_time = '00h00min'

				else:
					toast("Atenção: Já existe um evento para o dia {} às {}.".format(changeData(str(self.saveData_[0])), changeTime(self.saveTime_[0])))
			else:
				toast("Atenção: Todos os campos devem ser preenchidos.")
		if categoria == "Simulados":
			if len(self.saveData_) > 0 and len(self.saveTime_) > 0 and len(self.saveDuration_) > 0 and categoria != "Categoria" and materia != "Matérias" and topico != "Tópicos" and duracao[0] != "00:00":
				horas = duracao[0].split(":")[0]
				minutos = duracao[0].split(":")[1]
				lista_data = [[]]
				lista_data[0].append(str(self.saveData_[0]))
				lista_data[0].append(self.saveTime_[0])

				if lista_data[0] not in lista_data_to_check:
					if len(horas) == 1:
						horas = '0' + horas
					if len(horas) == 2:
						horas = horas
					if len(minutos) == 1:
						minutos = '0' + minutos
					if len(minutos) == 2:
						minutos = minutos

					duration = horas + ':' + minutos + ':00'
					self.data_cronograma = pickle.load((open("data_timeline.p", "rb")))
					self.data_cronograma.append((str(data[0]), str(horario[0]), categoria, materia, topico, duration,("alert-circle", [1, 0, 0, 1], "Não Estudado"), '0', '0', '0.0 %'))
					pickle.dump(self.data_cronograma, open("data_timeline.p", "wb"))
					toast("Novo Item Adicionado Com Sucesso!")

					self.add_to_cronograma_refresh_table(self.saveData_[0])

					self.adicionar_item.content_cls.duration_dialog_.content_cls.ids.horas_.text = "00"
					self.adicionar_item.content_cls.duration_dialog_.content_cls.ids.minutos_.text = "00"

					# RESETAR PADROES DEFAULT
					self.saveData_.clear()
					self.saveTime_.clear()
					self.saveDuration_.clear()

				else:
					toast("Atenção: Já existe um evento para o dia {} às {}.".format(changeData(str(self.saveData_[0])), changeTime(self.saveTime_[0])))
			else:
				toast("Atenção: Todos os campos devem ser preenchidos.")
	def add_to_cronograma_refresh_table(self, valor, *args):
		nova_data = str(valor)
		today = str(date.today())
		try:
			if nova_data == str(self.data_selecionada):
				data_cronograma = pickle.load((open("data_timeline.p", "rb")))
				DataSearched_Today = SearchByData(data_cronograma, str(self.data_selecionada))
				self.ids.cronograma22.children[0].children[0].update_row_data(self, AutoSizeTableRowsNum_Cronograma(DataSearched_Today, InvisionStudy.rows_per_page_cronograma + 1))
				def refreshChecks(dt):
					try: self.ids.cronograma22.children[0].children[0].DoubleClickRefreshChecks()
					except IndexError: pass
				Clock.schedule_once(refreshChecks, 1.10)

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
					except ValueError:
						pass
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

		except AttributeError:
			if nova_data == str(today):
				data_cronograma = pickle.load((open("data_timeline.p", "rb")))
				DataSearched = SearchByData(data_cronograma, str(today))
				self.ids.cronograma22.children[0].children[0].update_row_data(self, AutoSizeTableRowsNum_Cronograma(DataSearched, InvisionStudy.rows_per_page_cronograma + 1))
				def refreshChecks(dt):
					try: self.ids.cronograma22.children[0].children[0].DoubleClickRefreshChecks()
					except IndexError: pass
				Clock.schedule_once(refreshChecks, 1.10)

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
					except ValueError:
						pass
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
	def close_adicionar_itema_(self, obj):
		self.adicionar_item.dismiss()

	# ////////////////////////////////////////////////////////////////////////////
	# FUNÇÕES E WIDGETS RELACIONADOS PARA REMOVER ITEM DO CRONOGRAMA
	def confirmar_remover_dialog(self, root, *args):
		try:
			if len(root.ids.cronograma22.children[0].children[0].get_row_checks()) > 0:
				if not self.confirmar_remover:
					self.tema = pickle.load((open("tema.p", "rb")))
					self.confirmar_remover = MDDialog(
						title=f'[color={self.cor_aplicativo}]Remover Item[/color]',
						md_bg_color=self.tema[0].cor_fundo_trabalho_tuple,
						type="custom",
						auto_dismiss=True,
						text=f"[color={self.cor_aplicativo}]Você deseja remover [b]esses items[/b] do seu cronograma?\nEsse processo é irreversível e irá [b]remover permanentemente[/b] esses items.[/color]",
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
	def removerItemCronograma(self,root):
			def rebuildDataStyle(lista, color_hex=self.tema[0].cor_aplicativo):
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

			options = list(root.ids.cronograma22.children[0].children[0].get_row_checks())
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

			self.data_cronograma = pickle.load((open("data_timeline.p", "rb")))
			next_event = filter(sortData(onlyTimeGreater(eliminar_EscolhasRepetidas(self.data_cronograma))))

			if len(next_event) != 0:
				self.next_event_name = next_event[0][3]
				self.next_event_data = changeData(next_event[0][0])
				self.next_event_time = changeTime(next_event[0][1])
			if len(next_event) == 0:
				self.next_event_name = 'Sem Matéria'
				self.next_event_data = '00/00/0000'
				self.next_event_time = '00h00min'

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
				self.ids.cronograma22.children[0].children[0].update_row_data(self, AutoSizeTableRowsNum(DataSearched,
																							 InvisionStudy.rows_per_page_cronograma + 1))
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
				self.ids.cronograma22.children[0].children[0].update_row_data(self, AutoSizeTableRowsNum(DataSearched_today,
																							 InvisionStudy.rows_per_page_cronograma + 1))
				if len(options) == 1:
					toast("Item Removido Com Sucesso!")

				if len(options) > 1:
					toast("Items Removidos Com Sucesso!")

				def refreshChecks(dt):
					try:
						self.ids.cronograma22.children[0].children[0].DoubleClickRefreshChecks()

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
						label = string.split(']')[1].split("[")[0]
						return label
					except IndexError:
						pass

				for x in range(len(step14)):
					if step14[x] == [' ', ' ', ' ', ' ', ' ', ' ', ' ']: pass

					else:
						# DEFAULT PARA A DATA
						step14[x][0] = str(step14[x][0][15:25][-4:] + '-' + step14[x][0][15:25][-7:-5] + '-' + step14[x][0][15:25][-10:-8])

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

			def rebuildDataStyle(lista, color_hex=self.tema[0].cor_aplicativo):
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

			def Estudado(lista, select, color_hex=self.tema[0].cor_aplicativo):
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

			def LastEstudado(lista, select, color_hex=self.tema[0].cor_aplicativo):
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

			options = list(root.ids.cronograma22.children[0].children[0].get_row_checks())
			data_cronograma = colorData(organizerData(sortData(data_cronograma)))
			estudadoList = rebuildDataStyle(options)


			estudados = LastEstudado(data_cronograma, estudadoList)
			# COMEÇO DOS PROBLEMAS
			estudados = defaultStyle(estudados)
			estudados = CronogramaTableStyle(organizerData(sortData(estudados)))

			data_cronograma = Estudado(data_cronograma, estudadoList)
			data_cronograma = defaultStyle(data_cronograma)
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
						num = encontrarNumeroPagina(DataSearched, estudados[0], InvisionStudy.rows_per_page_cronograma)
						if len(estudados) == 0:
							pass
						else:
							toast("Status Alterado Com Sucesso!")
							self.ids.cronograma22.children[0].children[0].update_row_data(self, AutoSizeTableRowsNum_Cronograma(DataSearched,InvisionStudy.rows_per_page_cronograma + 1))
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
					num = encontrarNumeroPagina(DataSearched_today, estudados[0], InvisionStudy.rows_per_page_cronograma)
					if len(estudados) == 0:
						pass
					else:
						toast("Status Alterado Com Sucesso!")
						self.ids.cronograma22.children[0].children[0].update_row_data(self, AutoSizeTableRowsNum_Cronograma(DataSearched_today, InvisionStudy.rows_per_page_cronograma + 1))

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

		if self.ids.cronograma22.children[0].children[0].get_row_checks() != [] and len(self.ids.cronograma22.children[0].children[0].get_row_checks()) > 0:
			def defaultStyle(lista):
				step14 = []
				for i in range(len(lista)):
					step14.append([])
				for y in range(len(step14)):
					for x in range(len(lista[y])):
						if x == 6:
							step14[y].append(list(lista[y][x]))
						else:
							step14[y].append(lista[y][x])

				def RegEx(string):
					try:
						label = string.split(']')[1].split("[")[0]
						return label
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
			def rebuildDataStyle(lista, color_hex=self.tema[0].cor_aplicativo):
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
			def NaoEstudado(lista, select, color_hex=self.tema[0].cor_aplicativo):
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
			def LastNaoEstudado(lista, select, color_hex=self.tema[0].cor_aplicativo):
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
						num = encontrarNumeroPagina(DataSearched, naoestudados[0], InvisionStudy.rows_per_page_cronograma)
						if len(naoestudados) == 0: pass
						else:
							self.ids.cronograma22.children[0].children[0].update_row_data(self, AutoSizeTableRowsNum_Cronograma(DataSearched, InvisionStudy.rows_per_page_cronograma + 1))
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
					num = encontrarNumeroPagina(DataSearched_today, naoestudados[0], InvisionStudy.rows_per_page_cronograma)
					if len(naoestudados) == 0: pass
					else:
						self.ids.cronograma22.children[0].children[0].update_row_data(self, AutoSizeTableRowsNum_Cronograma(DataSearched_today, InvisionStudy.rows_per_page_cronograma + 1))
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
		self.tema = pickle.load((open("tema.p", "rb")))
		# COR DOS MENUS
		date_dialog.primary_color = ("#{}".format(self.tema[0].cor_fundo_menu_deg2))
		date_dialog.accent_color = get_color_from_hex("#{}".format(self.tema[0].cor_widget))
		date_dialog.selector_color = get_color_from_hex("#{}".format(self.tema[0].cor_fundo_menu_deg2))
		date_dialog.text_toolbar_color = get_color_from_hex("#{}".format(self.tema[0].cor_widget))

		# COR DOS TEXTOS
		date_dialog.text_color = get_color_from_hex("#{}".format(self.tema[0].cor_aplicativo))
		date_dialog.text_current_color = get_color_from_hex("#{}".format(self.tema[0].cor_aplicativo))
		date_dialog.text_button_color = get_color_from_hex("#{}".format(self.tema[0].cor_aplicativo))
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
			self.ids.cronograma22.children[0].children[0].update_row_data(self, AutoSizeTableRowsNum_Cronograma(DataSearched, InvisionStudy.rows_per_page_cronograma + 1))
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
		paths = pickle.load((open("path.p", "rb")))
		self.user_picture = r"{}".format(paths[0])
		#self.ids.cronograma22.children[0].children[0].bind(on_row_press=self.on_row_press)

		def nextEvento(dt):
			data_cronograma = pickle.load((open("data_timeline.p", "rb")))
			next_event = filter(sortData(onlyTimeGreater(eliminar_EscolhasRepetidas(data_cronograma))))
			if len(next_event) != 0:
				self.next_event_name = next_event[0][3]
				self.next_event_data = changeData(next_event[0][0])
				self.next_event_time = changeTime(next_event[0][1])
			if len(next_event) == 0:
				self.next_event_name = 'Sem Matéria'
				self.next_event_data = '00/00/0000'
				self.next_event_time = '00h00min'

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
		today = date.today()
		try:
			self.estudado_data = changeData(str(self.data_selecionada))
			self.nao_estudado_data = changeData(str(self.data_selecionada))
			self.estudado = count_Estudado(True, str(self.data_selecionada))
			self.nao_estudado = count_Estudado(False, str(self.data_selecionada))
		except AttributeError:
			try:
				self.estudado_data = changeData(str(today))
				self.nao_estudado_data = changeData(str(today))
				self.estudado = count_Estudado(True, str(today))
				self.nao_estudado = count_Estudado(False, str(today))
			except ValueError:
				self.estudado = '0.0 %'
				self.nao_estudado = '0.0 %'

		data_cronograma = pickle.load((open("data_timeline.p", "rb")))

		next_event = filter(sortData(onlyTimeGreater(eliminar_EscolhasRepetidas(data_cronograma))))

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
	def refresh_cronograma_item(self):

		self.data = pickle.load((open("data_subjects_topics.p", "rb")))
		self.manager.get_screen("Cronograma_CriarItem").ids.spinnerCategorias.text = "Categorias"
		self.manager.get_screen("Cronograma_CriarItem").ids.spinnerAllMaterias.text = "Matérias"
		self.manager.get_screen("Cronograma_CriarItem").ids.spinnerTopicos.text = "Tópicos"
		self.manager.get_screen("Cronograma_CriarItem").ids.spinnerAllMaterias.values = tuple(self.data.keys())
		self.manager.current = 'Cronograma_CriarItem'


class Simulados(Screen):
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

	tema = pickle.load((open("tema.p", "rb")))
	cor_aplicativo = StringProperty(tema[0].cor_aplicativo)
	cor_widget = 'eef2fe'
	criar_novo_simulado_dialog = None
	remover_simulado_dialog = None
	dialog11 = None

	class Conteudo_CriarNovoSimulado(MDFloatLayout, HoverBehavior):
		cor_aplicativo = '686fa3'
		cor_widget = 'eef2fe'
		simulado_name_dynamic = StringProperty('')

		def on_enter(self):
			def refresh_name(dt):
				self.simulado_name_dynamic = str(self.ids.simulado_name.text)
			Clock.schedule_interval(refresh_name, 1)

	class Conteudo_RemoverSimulado(MDFloatLayout):
		cor_aplicativo = '686fa3'
		cor_widget = 'eef2fe'
		simulado_name_dynamic = StringProperty('')

	class Simulados_Spinner(Spinner):
		def __init__(self, **kwargs):
			super().__init__(**kwargs)
			self.tema = pickle.load((open("tema.p", "rb")))
			self.simulados = pickle.load((open("simulados.p", "rb")))
			self.simulados.sort()
			self.values = self.simulados
			self.dropdown_cls = SpinnerDropdown
			self.option_cls = SpinnerOptions
			self.color = self.tema[0].cor_aplicativo_tuple
			self.bold = True
			self.dropdown_cls.max_height = self.height * 2 + 2 * 2
			self.text = "Simulados"



	# SIMULADO DE DESTAQUE
	simulado_destaque_nome = StringProperty('Sem Simulado')
	# TAXA DE ACERTO
	taxa_acertos_simulados = StringProperty('0.0 %')
	taxa_acertos_simulados_ThisWeek = StringProperty('+0.0 %')
	# HORAS ESTUDADAS
	horas_estudadas_simulados = StringProperty('0h')
	horas_estudadas_simulados_ThisWeek = StringProperty('0h')
	# SIMULADOS REALIZAD0S
	simulados_realizados = StringProperty('0')
	simulados_realizados_ThisWeek = StringProperty('0')
	# QUESTOES REALIZADAS
	questoes_realizadas_simulados = StringProperty('0')
	questoes_realizadas_simulados_ThisWeek = StringProperty('0')
	# Acertos
	acertos_simulados = StringProperty('0')
	acertos_simulados_ThisWeek = StringProperty('0')
	# Erros
	erros_simulados = StringProperty('0')
	erros_simulados_ThisWeek = StringProperty('0')

	# ALTERAR FOTO
	user_picture = StringProperty('')
	path_user = read_or_new_pickle(path="path.p", default=["Invision Code"])
	change_picture_ = None

	class Conteudo_AlterarImagem(MDFloatLayout, HoverBehavior):
		path_example = r"Carlos Santos"

	def change_picture(self, root, *args):
		self.tema = pickle.load((open("tema.p", "rb")))
		if not self.change_picture_:
			self.change_picture_ = MDDialog(
				title=f'[color={self.cor_aplicativo}]Alterar Nome[/color]',
				md_bg_color=self.tema[0].cor_fundo_trabalho_tuple,
				type="custom",
				auto_dismiss=True,
				content_cls=self.Conteudo_AlterarImagem(),
				buttons=[
					MDFlatButton(
						text=f"[color={self.cor_aplicativo}][b]CANCELAR[/color][/b]",
						theme_text_color="Custom",
						on_release=self.close_change_picture),
					MDFlatButton(
						text=f"[color={self.cor_aplicativo}][b]ALTERAR[/color][/b]",
						theme_text_color="Custom",
						on_release=root.alterar_foto)])

		self.change_picture_.open()

	def close_change_picture(self, obj):
		self.change_picture_.dismiss()

	def alterar_foto(self, *args):
		path = str(self.change_picture_.content_cls.ids.user_picture_path.text)
		path = ' '.join(path.split())
		if len(path) <= 15:
			paths = pickle.load((open("path.p", "rb")))
			paths.clear()
			paths.append(path)
			pickle.dump(paths, open("path.p", "wb"))
			self.user_picture = "{}".format(paths[0])
			self.change_picture_.dismiss()
			self.change_picture_.content_cls.ids.user_picture_path.text = ""
			toast("Nome Alterado Com Sucesso.")
		else:
			toast("Atenção: Limite Máximo de Caractere é 15.")

	simulados = read_or_new_pickle(path="simulados.p", default=[])

	def remover_simulado(self, root, *args):
		try:
			self.tema = pickle.load((open("tema.p", "rb")))
			if not self.remover_simulado_dialog:
				self.remover_simulado_dialog = MDDialog(
					title=f'[color={self.cor_aplicativo}]Remover Simulado[/color]',
					md_bg_color=self.tema[0].cor_fundo_trabalho_tuple,
					type="custom",
					auto_dismiss=True,
					content_cls=self.Conteudo_RemoverSimulado(),
					buttons=[
						MDFlatButton(
							text=f"[color={self.cor_aplicativo}][b]CANCELAR[/color][/b]",
							theme_text_color="Custom",
							on_release=self.close_remover_simulado_dialog),
						MDFlatButton(
							text=f"[color={self.cor_aplicativo}][b]EXCLUIR SIMULADO[/color][/b]",
							theme_text_color="Custom",
							on_release=root.remover_simulado_removeFunction)])

			new_data_refreshed = pickle.load((open("simulados.p", "rb")))
			self.remover_simulado_dialog.content_cls.ids.spinnerSimulados.values = new_data_refreshed
			self.remover_simulado_dialog.open()
		except AttributeError:
			pass
	def close_remover_simulado_dialog(self, obj):
		self.remover_simulado_dialog.dismiss()
	def remover_simulado_removeFunction(self, root, *args):
		simulado_name = str(self.remover_simulado_dialog.content_cls.ids.spinnerSimulados.text)
		simulados = pickle.load((open("simulados.p", "rb")))

		if simulado_name != 'Simulados':
			simulados.remove(str(simulado_name))
			pickle.dump(simulados, open("simulados.p", "wb"))
			self.remover_simulado_dialog.content_cls.ids.spinnerSimulados.text = 'Simulados'
			new_data_refreshed = pickle.load((open("simulados.p", "rb")))
			new_data_refreshed.sort()
			self.remover_simulado_dialog.content_cls.ids.spinnerSimulados.values = new_data_refreshed

			self.ids.spinnerSimulados2.values = new_data_refreshed

			toast('Simulado {} Removido Com Sucesso!'.format(simulado_name))
			self.simulado_destaque_nome = str(simulado_destaque_finder())

			if self.ids.spinnerSimulados2.text == simulado_name:
				self.ids.spinnerSimulados2.text = 'Simulados'
				self.ids.spinnerSimulados2.values = new_data_refreshed
			else:
				self.ids.spinnerSimulados2.values = new_data_refreshed

			try:
				if self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_categoria.text == "Simulado":
					if self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_materia.text == simulado_name:
						new_data_refreshed = pickle.load((open("simulados.p", "rb")))
						new_data_refreshed.sort()
						self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_materia.text = "Nome Simulado"
						self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_materia.values = new_data_refreshed
			except AttributeError:
				pass
			#elf.criar_novo_simulado_dialog.dismiss()
		else:
			toast('Atenção: Nenhum Simulado Selecionado!')

	# ////////////////////////////////////////////////////////////////////////////
	# FUNÇÕES PARA ABRIR E FECHAR BOX DIALOG, CRIAR NOVO SIMULADO
	def criar_simulado(self, root, *args):
		try:
			self.tema = pickle.load((open("tema.p", "rb")))
			if not self.criar_novo_simulado_dialog:
				self.criar_novo_simulado_dialog = MDDialog(
					title=f'[color={self.cor_aplicativo}]Criar Novo Simulado[/color]',
					md_bg_color=self.tema[0].cor_fundo_trabalho_tuple,
					type="custom",
					auto_dismiss=True,
					content_cls=self.Conteudo_CriarNovoSimulado(),
					buttons=[
						MDFlatButton(
							text=f"[color={self.cor_aplicativo}][b]CANCELAR[/color][/b]",
							theme_text_color="Custom",
							on_release=self.close_criar_novo_simulado_dialog),
						MDFlatButton(
							text=f"[color={self.cor_aplicativo}][b]CRIAR SIMULADO[/color][/b]",
							theme_text_color="Custom",
							on_release=root.criar_simulado_addFunction)])

			self.criar_novo_simulado_dialog.open()
		except AttributeError:
			pass
	def close_criar_novo_simulado_dialog(self, obj):
		self.criar_novo_simulado_dialog.dismiss()
	def criar_simulado_addFunction(self, root, *args):
		new_simulado_name = ' '.join(self.criar_novo_simulado_dialog.content_cls.ids.simulado_name.text.split()).lower().title()
		simulados = pickle.load((open("simulados.p", "rb")))

		if  new_simulado_name in simulados:
			toast('Atenção: Já Existe Um Simulado Com o Nome {}.'.format(new_simulado_name))

		if len(new_simulado_name) > 15:
			toast('Atenção: O Limite Máximo de Caracter é 15')

		if not new_simulado_name in simulados and len(new_simulado_name) <= 15:
			simulados.append(new_simulado_name)
			pickle.dump(simulados, open("simulados.p", "wb"))
			new_data_refreshed = pickle.load((open("simulados.p", "rb")))
			new_data_refreshed.sort()
			self.ids.spinnerSimulados2.values = new_data_refreshed

			self.criar_novo_simulado_dialog.content_cls.ids.simulado_name.text = ''
			toast('Simulado {}, Criado Com Sucesso!'.format(new_simulado_name))
			self.criar_novo_simulado_dialog.dismiss()
			try:
				if self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_categoria.text == "Simulado":
					new_data_refreshed = pickle.load((open("simulados.p", "rb")))
					new_data_refreshed.sort()
					self.manager.get_screen('Cronograma').adicionar_item.content_cls.ids.spinner_materia.values = new_data_refreshed
			except AttributeError:
				pass

	# FUNÇÃO PARA ADICIONAR NOVO SIMULADO AO CRONOGRAMA
	def adicionar_item(self):
		self.manager.get_screen("Cronograma_CriarItem").ids.spinnerCategorias.text = 'Simulado'
		self.manager.current = 'Cronograma_CriarItem'

	# FUNÇÃO PARA ATUALIZAR DADOS ESTATISTICOS DOS SIMULADOS
	def atualizar_info_simulados(self):
		simulado_selecionado = str(self.ids.spinnerSimulados2.text)
		self.taxa_acertos_simulados = FUNCTION_TaxaAcertos_Simulados(simulado_selecionado)
		self.taxa_acertos_simulados_ThisWeek = FUNCTION_TaxaAcertos_Simulados_ThisWeek(simulado_selecionado)
		self.horas_estudadas_simulados = FUNCTION_HorasEstudadas_Simulados(simulado_selecionado)
		self.horas_estudadas_simulados_ThisWeek = FUNCTION_HorasEstudadas_Simulados_Weekly(simulado_selecionado)
		self.questoes_realizadas_simulados = FUNCTION_QuestoesRealizadas_Simulados(simulado_selecionado)
		self.questoes_realizadas_simulados_ThisWeek = FUNCTION_QuestoesRealizadas_Simulados_Weekly(simulado_selecionado)
		self.acertos_simulados = FUNCTION_Acertos_Simulados(simulado_selecionado)
		self.acertos_simulados_ThisWeek = FUNCTION_Acertos_Simulados_Weekly(simulado_selecionado)
		self.erros_simulados = FUNCTION_Erros_Simulados(simulado_selecionado)
		self.erros_simulados_ThisWeek = FUNCTION_Erros_Simulados_Weekly(simulado_selecionado)
		self.simulados_realizados = FUNCTION_Simulados_Realizados(simulado_selecionado)
		self.simulados_realizados_ThisWeek = FUNCTION_Simulados_Realizados_Weekly(simulado_selecionado)
		#self.simulado_destaque_nome = simulado_destaque_finder()

	# FUNÇÕES AO ENTRAR E SAIR DA PÁGINA SIMULADOS
	def on_enter(self, *args):
		paths = pickle.load((open("path.p", "rb")))
		self.user_picture = r"{}".format(paths[0])

		simulados = pickle.load((open("simulados.p", "rb")))
		simulados.sort()
		self.ids.spinnerSimulados2.text = 'Simulados'
		self.ids.spinnerSimulados2.values = simulados
		self.simulado_destaque_nome = str(simulado_destaque_finder())

	def on_leave(self, *args):
		self.ids.spinnerSimulados2.text = 'Simulados'
		self.ids.spinnerSimulados2.values = []

class Estatisticas(Screen):
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

	tema = pickle.load((open("tema.p", "rb")))
	cor_aplicativo = StringProperty(tema[0].cor_aplicativo)

	# TAXA DE ACERTO
	taxa_acertos_geral = StringProperty('0.0 %')
	taxa_acertos_materias = StringProperty('0.0 %')
	taxa_acertos_materias_ThisWeek = StringProperty('+0.0 %')
	taxa_acertos_topicos = StringProperty('0.0 %')
	taxa_acertos_topicos_ThisWeek = StringProperty('0.0 %')

	# HORAS ESTUDADAS
	horas_estudadas_geral = StringProperty('0h')
	horas_estudadas_materias = StringProperty('0h')
	horas_estudadas_materias_ThisWeek = StringProperty('0h')
	horas_estudadas_topicos = StringProperty('0h')
	horas_estudadas_topicos_ThisWeek = StringProperty('0h')

	# QUESTOES REALIZADAS
	questoes_realizadas_geral = StringProperty('0')
	questoes_realizadas_materias = StringProperty('0')
	questoes_realizadas_materias_ThisWeek = StringProperty('0')
	questoes_realizadas_topicos = StringProperty('0')
	questoes_realizadas_topicos_ThisWeek = StringProperty('0')

	# Acertos
	acertos_materias = StringProperty('0')
	acertos_materias_ThisWeek = StringProperty('0')
	acertos_topicos = StringProperty('0')
	acertos_topicos_ThisWeek = StringProperty('0')

	# Erros
	erros_materias = StringProperty('0')
	erros_materias_ThisWeek = StringProperty('0')
	erros_topicos = StringProperty('0')
	erros_topicos_ThisWeek = StringProperty('0')


	def atualizar_materias_info(self,root, *args):
		self.taxa_acertos_materias = FUNCTION_TaxaAcertos_Materias(str(root.ids.spinnerAllMaterias.text))
		self.taxa_acertos_materias_ThisWeek = FUNCTION_TaxaAcertos_Materias_Weekly(str(root.ids.spinnerAllMaterias.text))
		self.horas_estudadas_materias = FUNCTION_HorasEstudadas_Materias(str(root.ids.spinnerAllMaterias.text))
		self.horas_estudadas_materias_ThisWeek = FUNCTION_HorasEstudadas_Materias_Weekly(str(root.ids.spinnerAllMaterias.text))
		self.questoes_realizadas_materias = FUNCTION_QuestoesRealizadas_Materias(str(root.ids.spinnerAllMaterias.text))
		self.questoes_realizadas_materias_ThisWeek = FUNCTION_QuestoesRealizadas_Materias_Weekly(str(root.ids.spinnerAllMaterias.text))
		self.acertos_materias = FUNCTION_Acertos_Materias(str(root.ids.spinnerAllMaterias.text))
		self.acertos_materias_ThisWeek = FUNCTION_Acertos_Materias_Weekly(str(root.ids.spinnerAllMaterias.text))
		self.erros_materias = FUNCTION_Erros_Materias(str(root.ids.spinnerAllMaterias.text))
		self.erros_materias_ThisWeek = FUNCTION_Erros_Materias_Weekly(str(root.ids.spinnerAllMaterias.text))

	def gerar_relatorio(self):
		#gerar_relatorio_materias()
		a = 2

	# ALTERAR FOTO
	user_picture = StringProperty('')
	path_user = read_or_new_pickle(path="path.p", default=["Invision Code"])
	change_picture_ = None

	class Conteudo_AlterarImagem(MDFloatLayout, HoverBehavior):
		path_example = r"Carlos Santos"
	def change_picture(self, root, *args):
		self.tema = pickle.load((open("tema.p", "rb")))
		if not self.change_picture_:
			self.change_picture_ = MDDialog(
				title=f'[color={self.cor_aplicativo}]Alterar Nome[/color]',
				md_bg_color=self.tema[0].cor_fundo_trabalho_tuple,
				type="custom",
				auto_dismiss=True,
				content_cls=self.Conteudo_AlterarImagem(),
				buttons=[
					MDFlatButton(
						text=f"[color={self.cor_aplicativo}][b]CANCELAR[/color][/b]",
						theme_text_color="Custom",
						on_release=self.close_change_picture),
					MDFlatButton(
						text=f"[color={self.cor_aplicativo}][b]ALTERAR[/color][/b]",
						theme_text_color="Custom",
						on_release=root.alterar_foto)])

		self.change_picture_.open()
	def close_change_picture(self, obj):
		self.change_picture_.dismiss()
	def alterar_foto(self, *args):
		path = str(self.change_picture_.content_cls.ids.user_picture_path.text)
		path = ' '.join(path.split())
		if len(path) <= 15:
			paths = pickle.load((open("path.p", "rb")))
			paths.clear()
			paths.append(path)
			pickle.dump(paths, open("path.p", "wb"))
			self.user_picture = "{}".format(paths[0])
			self.change_picture_.dismiss()
			self.change_picture_.content_cls.ids.user_picture_path.text = ""
			toast("Nome Alterado Com Sucesso.")
		else:
			toast("Atenção: Limite Máximo de Caractere é 15.")



	def atualizar_topicos_info(self, root, *args):
		self.taxa_acertos_topicos = FUNCTION_TaxaAcertos_Topicos(str(root.ids.spinnerAllMaterias.text), str(root.ids.spinnerTopicos.text))
		self.taxa_acertos_topicos_ThisWeek = FUNCTION_TaxaAcertos_Topicos_Weekly(str(root.ids.spinnerAllMaterias.text), str(root.ids.spinnerTopicos.text))
		self.horas_estudadas_topicos = FUNCTION_HorasEstudadas_Topicos(str(root.ids.spinnerAllMaterias.text), str(root.ids.spinnerTopicos.text))
		self.horas_estudadas_topicos_ThisWeek = FUNCTION_HorasEstudadas_Topicos_Weekly(str(root.ids.spinnerAllMaterias.text), str(root.ids.spinnerTopicos.text))
		self.questoes_realizadas_topicos = FUNCTION_QuestoesRealizadas_Topicos(str(root.ids.spinnerAllMaterias.text), str(root.ids.spinnerTopicos.text))
		self.questoes_realizadas_topicos_ThisWeek = FUNCTION_QuestoesRealizadas_Topicos_Weekly(str(root.ids.spinnerAllMaterias.text), str(root.ids.spinnerTopicos.text))
		self.acertos_topicos = FUNCTION_Acertos_Topicos(str(root.ids.spinnerAllMaterias.text), str(root.ids.spinnerTopicos.text))
		self.acertos_topicos_ThisWeek = FUNCTION_Acertos_Topicos_Weekly(str(root.ids.spinnerAllMaterias.text), str(root.ids.spinnerTopicos.text))
		self.erros_topicos = FUNCTION_Erros_Topicos(str(root.ids.spinnerAllMaterias.text), str(root.ids.spinnerTopicos.text))
		self.erros_topicos_ThisWeek = FUNCTION_Erros_Topicos_Weekly(str(root.ids.spinnerAllMaterias.text), str(root.ids.spinnerTopicos.text))
	def refreshTopicosSpinner(self, root, *args):
		self.data = pickle.load((open("data_subjects_topics.p", "rb")))
		if root.ids.spinnerAllMaterias.text != "Matérias":
			root.ids.spinnerTopicos.values = ()
			root.ids.spinnerTopicos.values = self.data[root.ids.spinnerAllMaterias.text][1]
			root.ids.spinnerTopicos.text = "Tópicos"
	class AllMateriasSpinner(Spinner):
		def __init__(self, **kwargs):
			super().__init__(**kwargs)
			self.dropdown_cls = SpinnerDropdown
			self.option_cls = SpinnerOptions
			self.color = get_color_from_hex('#{}'.format(InvisionStudy.cor_widgets_default))
			self.bold = True
			self.dropdown_cls.max_height = self.height * 2 + 2 * 4
			self.text = "Matérias"
	class TopicosSpinner(Spinner):
		def __init__(self, **kwargs):
			super().__init__(**kwargs)
			self.dropdown_cls = SpinnerDropdown_Blue
			self.option_cls = SpinnerOptions_Blue
			self.bold = True
			self.dropdown_cls.max_height = self.height * 2 + 2 * 4
			self.text = "Tópicos"
	def on_enter(self, *args):
		paths = pickle.load((open("path.p", "rb")))
		self.user_picture = r"{}".format(paths[0])

		self.taxa_acertos_geral = FUNCTION_TaxaAcertos_Geral()
		self.horas_estudadas_geral = FUNCTION_HorasEstudadas_Geral()
		self.questoes_realizadas_geral = FUNCTION_QuestoesRealizadas_Geral()

		self.data = pickle.load((open("data_subjects_topics.p", "rb")))
		self.ids.spinnerAllMaterias.text = 'Matérias'
		self.ids.spinnerAllMaterias.values = tuple(self.data.keys())
		self.ids.spinnerTopicos.values = []
		self.ids.spinnerTopicos.text = 'Tópicos'


class Configuracoes(Screen):
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

	tema = pickle.load((open("tema.p", "rb")))
	cor_aplicativo = StringProperty(tema[0].cor_aplicativo)
	# ALTERAR FOTO
	user_picture = StringProperty('')
	path_user = read_or_new_pickle(path="path.p", default=["Invision Code"])
	change_picture_ = None

	class Conteudo_AlterarImagem(MDFloatLayout, HoverBehavior):
		path_example = r"Carlos Santos"

	def change_picture(self, root, *args):
		self.tema = pickle.load((open("tema.p", "rb")))
		if not self.change_picture_:
			self.change_picture_ = MDDialog(
				title=f'[color={self.cor_aplicativo}]Alterar Nome[/color]',
				md_bg_color=self.tema[0].cor_fundo_trabalho_tuple,
				type="custom",
				auto_dismiss=True,
				content_cls=self.Conteudo_AlterarImagem(),
				buttons=[
					MDFlatButton(
						text=f"[color={self.cor_aplicativo}][b]CANCELAR[/color][/b]",
						theme_text_color="Custom",
						on_release=self.close_change_picture),
					MDFlatButton(
						text=f"[color={self.cor_aplicativo}][b]ALTERAR[/color][/b]",
						theme_text_color="Custom",
						on_release=root.alterar_foto)])

		self.change_picture_.open()
	def close_change_picture(self, obj):
		self.change_picture_.dismiss()
	def alterar_foto(self, *args):
		path = str(self.change_picture_.content_cls.ids.user_picture_path.text)
		path = ' '.join(path.split())
		if len(path) <= 15:
			paths = pickle.load((open("path.p", "rb")))
			paths.clear()
			paths.append(path)
			pickle.dump(paths, open("path.p", "wb"))
			self.user_picture = "{}".format(paths[0])
			self.change_picture_.dismiss()
			self.change_picture_.content_cls.ids.user_picture_path.text = ""
			toast("Nome Alterado Com Sucesso.")
		else:
			toast("Atenção: Limite Máximo de Caractere é 15.")

	# SESSAO DE DUVIDAS
	show_help_  = None
	class Conteudo_ShowHelp(MDFloatLayout, HoverBehavior):
		cor_aplicativo = '686fa3'
		cor_widget = 'eef2fe'
		simulado_name_dynamic = StringProperty('')
	def show_help(self, root, *args):
		if not self.show_help_:
			self.show_help_ = MDDialog(
					title=f'[color={self.cor_aplicativo}]Dúvidas Frequentes[/color]',
					md_bg_color=self.tema[0].cor_fundo_trabalho_tuple,
					type="custom",
					auto_dismiss=False,
					content_cls=self.Conteudo_ShowHelp(),
					buttons=[
						MDFlatButton(
							text=f"[color={self.cor_aplicativo}][b]CANCELAR[/color][/b]",
							theme_text_color="Custom",
							on_release=self.close_show_help)])

		self.show_help_.open()
	def close_show_help(self, obj):
		self.show_help_.dismiss()

	Padrao = Tema(cor_aplicativo='686fa3', cor_aplicativo_tuple = [0.3098,0.3411,0.5333], cor_fundo_menu_deg1='464c7e', cor_fundo_menu_deg2='575e91', cor_fundo_trabalho='e6ebfb',
				  cor_fundo_trabalho_tuple=[0.9019, 0.9215, 0.9843, 1], cor_widget='eef2fe', cor_widget_hover='f4f7fe',
				  cor_letra_menu='8793e9', cor_licenca='cedeff', cor_licenca_texto = '686fa3')

	Vintage = Tema(cor_aplicativo='5e5e5e', cor_aplicativo_tuple=[0.3686, 0.3686, 0.3686], cor_fundo_menu_deg1='e15c5d',
				  cor_fundo_menu_deg2='d75354', cor_fundo_trabalho='f6f3ea',
				  cor_fundo_trabalho_tuple=[0.9647, 0.9529, 0.9176, 1], cor_widget='f2eee3', cor_widget_hover='faf7ef',
				  cor_letra_menu='952f2f', cor_licenca='00a19c', cor_licenca_texto='faf8f2')

	Blue = Tema(cor_aplicativo='30435a', cor_aplicativo_tuple=[0.1804, 0.2353, 0.3294], cor_fundo_menu_deg1='174965',
				   cor_fundo_menu_deg2='14435e', cor_fundo_trabalho='eeeeee',
				   cor_fundo_trabalho_tuple=[0.9333, 0.9333, 0.9333, 1], cor_widget='f4f4f4', cor_widget_hover='f7f8fc',
				   cor_letra_menu='aaaaaa', cor_licenca='558caa', cor_licenca_texto='eeeeee')

	StudyGram = Tema(cor_aplicativo='424b3f', cor_aplicativo_tuple=[0.2588, 0.2941, 0.2471], cor_fundo_menu_deg1='556052',
				cor_fundo_menu_deg2='445040', cor_fundo_trabalho='f2efea',
				cor_fundo_trabalho_tuple=[0.9490, 0.9372, 0.9176, 1], cor_widget='ede7dc', cor_widget_hover='f0e4cf',
				cor_letra_menu='b4a894', cor_licenca='af6b58', cor_licenca_texto='f2efea')

	Pink = Tema(cor_aplicativo='ffffff', cor_aplicativo_tuple=[1,1,1], cor_fundo_menu_deg1='3e065f',
				cor_fundo_menu_deg2='380655', cor_fundo_trabalho='2a0b35',
				cor_fundo_trabalho_tuple=[0.1647, 0.04313, 0.2078, 1], cor_widget='5e3079', cor_widget_hover='ca6bed',
				cor_letra_menu='903bc2', cor_licenca='8e06c2', cor_licenca_texto='ffffff')

	Desbloquear = Tema(cor_aplicativo='474747', cor_aplicativo_tuple=[0.2784, 0.2784, 0.2784], cor_fundo_menu_deg1='6c4a49',
				cor_fundo_menu_deg2='644342', cor_fundo_trabalho='fcf3f3',
				cor_fundo_trabalho_tuple=[0.9882, 0.9529, 0.9529, 1], cor_widget='faedee', cor_widget_hover='fae4e5',
				cor_letra_menu='c6afaf', cor_licenca='ddbdbe', cor_licenca_texto='fae4e5')

	One_Year = Tema(cor_aplicativo='ffffff', cor_aplicativo_tuple=[1,1,1],
					   cor_fundo_menu_deg1='ca3e47',
					   cor_fundo_menu_deg2='bf363f', cor_fundo_trabalho='525252',
					   cor_fundo_trabalho_tuple=[0.3215, 0.3215, 0.3215, 1], cor_widget='6c6b6b',
					   cor_widget_hover='343333',
					   cor_letra_menu='dadada', cor_licenca='414040', cor_licenca_texto='6c6b6b')

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
	tema = read_or_new_pickle(path="tema.p", default=[Padrao, "Padrão"])
	tema = pickle.load((open("tema.p", "rb")))

	alterar_tema_dialog = None
	remover_simulado_dialog = None

	cor_principal_perfil = StringProperty(tema[0].cor_letra_menu)
	cor_principal_cronograma = StringProperty(tema[0].cor_letra_menu)
	cor_principal_exercicios = StringProperty(tema[0].cor_letra_menu)
	cor_principal_simulados = StringProperty(tema[0].cor_letra_menu)
	cor_principal_stats = StringProperty(tema[0].cor_letra_menu)
	cor_principal_timer = StringProperty(tema[0].cor_letra_menu)
	cor_principal_help = StringProperty(tema[0].cor_letra_menu)
	cor_principal_settings = StringProperty(tema[0].cor_letra_menu)
	cor_principal_deslogar = StringProperty(tema[0].cor_letra_menu)

	cor_aplicativo = StringProperty(tema[0].cor_aplicativo)
	cor_fundo_menu_deg1 = StringProperty(tema[0].cor_fundo_menu_deg1)
	cor_fundo_menu_deg2 = StringProperty(tema[0].cor_fundo_menu_deg2)
	cor_menu_letra = StringProperty(tema[0].cor_letra_menu)
	cor_licenca = StringProperty(tema[0].cor_licenca)
	cor_licenca_texto = StringProperty(tema[0].cor_licenca_texto)
	cor_widget_hover = StringProperty(tema[0].cor_widget_hover)
	cor_widget = StringProperty(tema[0].cor_widget)
	cor_fundo = StringProperty(tema[0].cor_fundo_trabalho)
	cor_fundo_trabalho_tuple = tema[0].cor_fundo_trabalho_tuple

	class Conteudo_AlterarTema(MDFloatLayout):
		tema = pickle.load((open("tema.p", "rb")))
		cor_aplicativo = StringProperty(tema[0].cor_aplicativo)
		cor_aplicativo_tuple = tema[0].cor_aplicativo_tuple
		cor_widget = StringProperty(tema[0].cor_widget)
		cor_fundo = StringProperty(tema[0].cor_fundo_trabalho)
		simulado_name_dynamic = StringProperty('')
	class Temas_Spinner(Spinner):
		def __init__(self, **kwargs):
			super().__init__(**kwargs)
			self.tema = pickle.load((open("tema.p", "rb")))
			self.dropdown_cls = SpinnerDropdown
			self.option_cls = SpinnerOptions
			self.color = self.tema[0].cor_aplicativo_tuple
			self.bold = True
			self.dropdown_cls.max_height = self.height * 2 + 2 * 2
			#self.text = "Padrão"
			self.themes = ["Padrão"]
			self.ord = ["Vintage", "Ocean", "Florest", "Sakura", "Light Pink", "Night"]
			self.ord.sort()
			for x in range(len(self.ord)):
				self.themes.append(self.ord[x])
			self.values = self.themes
	def alterar_tema(self, root, *args):
		self.tema = pickle.load((open("tema.p", "rb")))
		if not self.alterar_tema_dialog:
				self.alterar_tema_dialog = MDDialog(
					title=f'[color={self.cor_aplicativo}]Alterar Tema[/color]',
					md_bg_color=self.tema[0].cor_fundo_trabalho_tuple,
					type="custom",
					auto_dismiss=True,
					content_cls=self.Conteudo_AlterarTema(),
					buttons=[
						MDFlatButton(
							text=f"[color={self.cor_aplicativo}][b]CANCELAR[/color][/b]",
							theme_text_color="Custom",
							on_release=self.close_alterar_tema_dialog),
						MDFlatButton(
							text=f"[color={self.cor_aplicativo}][b]ALTERAR TEMA[/color][/b]",
							theme_text_color="Custom",
							on_release=root.alterar_tema_Function)])

			#new_data_refreshed = pickle.load((open("simulados.p", "rb")))
			#self.remover_simulado_dialog.content_cls.ids.spinnerSimulados.values = new_data_refreshed
		self.alterar_tema_dialog.content_cls.ids.spinnerTemas.text = self.tema[1]
		self.alterar_tema_dialog.open()
	def alterar_tema_Function(self, root, *args):
		todos_temas = {"Padrão":self.Padrao, "Vintage":self.Vintage, "Ocean":self.Blue, "Florest":self.StudyGram, "Sakura":self.Pink, "Light Pink":self.Desbloquear, "Night":self.One_Year}
		tema = pickle.load((open("tema.p", "rb")))
		tema.clear()
		novo_tema_escolhido = str(self.alterar_tema_dialog.content_cls.ids.spinnerTemas.text)
		tema.append(todos_temas[novo_tema_escolhido])
		tema.append(novo_tema_escolhido)
		toast(f"Tema atualizado com sucesso, para visualizar seu novo tema reinicie o aplicativo.")
		pickle.dump(tema, open("tema.p", "wb"))
	def close_alterar_tema_dialog(self, obj):
		self.alterar_tema_dialog.dismiss()


	def renovar_plano(self):
		webbrowser.open("http://google.com", new=1)

	def insta(self):
		webbrowser.open("http://instagram.com/invisioncode", new=1)

	def youtube(self):
		webbrowser.open("https://www.youtube.com/channel/UCW7HrgdojZp-5ianxLxI4JQ", new=1)

	def sugestao(self):
		webbrowser.open("https://docs.google.com/forms/u/2/d/e/1FAIpQLScwg554jgtWvWnqt6-JuhDK07-xXDI53RgNYw1VIt5HZVQkdw/viewform", new=1)

	def suporte(self):
		webbrowser.open("https://docs.google.com/forms/d/e/1FAIpQLSeiDTuqEowykk0fXt8kcwSRzuwWSD2rxCCtrCNIgJn4qFsN5Q/viewform", new=1)



	def on_enter(self, *args):
		paths = pickle.load((open("path.p", "rb")))
		self.user_picture = r"{}".format(paths[0])

		tema = pickle.load((open("tema.p", "rb")))


class WindowManager(ScreenManager):
	pass

class InvisionStudy(MDApp):

	Padrao = Tema(cor_aplicativo='686fa3', cor_aplicativo_tuple=[0.3098, 0.3411, 0.5333], cor_fundo_menu_deg1='464c7e',
				  cor_fundo_menu_deg2='575e91', cor_fundo_trabalho='e6ebfb',
				  cor_fundo_trabalho_tuple=[0.9019, 0.9215, 0.9843, 1], cor_widget='eef2fe', cor_widget_hover='f4f7fe',
				  cor_letra_menu='8793e9', cor_licenca='cedeff', cor_licenca_texto='686fa3')

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
	tema = read_or_new_pickle(path="tema.p", default=[Padrao, "Padrão"])
	tema = pickle.load((open("tema.p", "rb")))


	cor_principal_icone_fundo = StringProperty(tema[0].cor_letra_menu)
	cor_principal_icone_fundo_def = StringProperty(tema[0].cor_letra_menu)
	cor_principal_icone_fundo_hover = StringProperty(tema[0].cor_widget_hover)
	cor_principal_aplicativo = StringProperty(tema[0].cor_aplicativo)
	cor_principal_aplicativo_tuple = list(tema[0].cor_aplicativo_tuple)
	cor_letras_outras = tema[0].cor_letra_menu
	cor_menu_deg1 = tema[0].cor_fundo_menu_deg1
	cor_menu_deg2 = tema[0].cor_fundo_menu_deg2
	cor_licenca_texto = tema[0].cor_licenca_texto
	cor_licenca = tema[0].cor_licenca

	cor_fundo_area_de_trabalho = StringProperty(tema[0].cor_fundo_trabalho)
	cor_barra_inferior_licenca = StringProperty(tema[0].cor_licenca)
	cor_widgets_default = StringProperty(tema[0].cor_widget)
	cor_widgets_hover = StringProperty(tema[0].cor_widget_hover)
	cor_principal_aplicativo_str = tema[0].cor_aplicativo
	cor_widgets_default_str = tema[0].cor_widget
	menu_unselected_color = tema[0].cor_letra_menu
	menu_selected_color = tema[0].cor_widget_hover
	cor_botoes_texto_default = tema[0].cor_aplicativo
	cor_botoes_menu_selected = tema[0].cor_licenca
	cor_botoes_menu_hover = tema[0].cor_widget_hover
	cor_botoes_default = tema[0].cor_letra_menu
	cor_principal_perfil = StringProperty(tema[0].cor_letra_menu)
	cor_principal_cronograma = StringProperty(tema[0].cor_letra_menu)
	cor_principal_exercicios = StringProperty(tema[0].cor_letra_menu)
	cor_principal_simulados = StringProperty(tema[0].cor_letra_menu)
	cor_principal_stats = StringProperty(tema[0].cor_letra_menu)
	cor_principal_timer = StringProperty(tema[0].cor_letra_menu)
	cor_principal_help = StringProperty(tema[0].cor_letra_menu)
	cor_principal_settings = StringProperty(tema[0].cor_letra_menu)
	cor_principal_deslogar = StringProperty(tema[0].cor_letra_menu)
	#-----------------------------------------------------------------------#

	font_size_title_1 = NumericProperty(42)
	font_size_title_2 = NumericProperty(30)
	font_size_title_3 = NumericProperty(23)

	font_size_normal_1 = NumericProperty(18)
	font_size_normal_2 = NumericProperty(15)

	font_cronograma_materias_estudadas_percent = 42
	font_cronograma_materias_estudadas_other_text = 18

	rows_per_page_cronograma = 4
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

	def on_start(self):
		Padrao = Tema(cor_aplicativo='686fa3', cor_aplicativo_tuple=[0.3098, 0.3411, 0.5333],
					  cor_fundo_menu_deg1='464c7e', cor_fundo_menu_deg2='575e91', cor_fundo_trabalho='e6ebfb',
					  cor_fundo_trabalho_tuple=[0.9019, 0.9215, 0.9843, 1], cor_widget='eef2fe',
					  cor_widget_hover='f4f7fe',
					  cor_letra_menu='8793e9', cor_licenca='cedeff', cor_licenca_texto='686fa3')

		Vintage = Tema(cor_aplicativo='5e5e5e', cor_aplicativo_tuple=[0.3686, 0.3686, 0.3686],
					   cor_fundo_menu_deg1='e15c5d',
					   cor_fundo_menu_deg2='d75354', cor_fundo_trabalho='f6f3ea',
					   cor_fundo_trabalho_tuple=[0.9647, 0.9529, 0.9176, 1], cor_widget='f2eee3',
					   cor_widget_hover='faf7ef',
					   cor_letra_menu='952f2f', cor_licenca='00a19c', cor_licenca_texto='faf8f2')

		Blue = Tema(cor_aplicativo='2e3c51', cor_aplicativo_tuple=[0.1804, 0.2353, 0.3294],
					cor_fundo_menu_deg1='334257',
					cor_fundo_menu_deg2='2d3b50', cor_fundo_trabalho='eeeeee',
					cor_fundo_trabalho_tuple=[0.9333, 0.9333, 0.9333, 1], cor_widget='f4f4f4',
					cor_widget_hover='e5e6e8',
					cor_letra_menu='eeeeee', cor_licenca='00a19c', cor_licenca_texto='eeeeee')

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

		tema = read_or_new_pickle(path="tema.p", default=[Blue, "Blue"])
		tema = pickle.load((open("tema.p", "rb")))
		self.cor_principal_perfil = self.menu_selected_color

	def build(self):
		self.title = 'StudyControl'
		self.icon = 'icons\icon.png'
		return Builder.load_file('StudyControl.kv')



if __name__ == '__main__':
	StudyControl().run()


