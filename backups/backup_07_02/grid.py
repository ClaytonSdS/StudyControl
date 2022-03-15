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

from kivymd.uix.pickers import MDTimePicker, MDDatePicker
from kivymd.uix.spinner import MDSpinner
from kivy.clock import Clock

from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.gridlayout import MDGridLayout

from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
#from kivymd_extensions.filemanager import FileManager
from kivy_gradient import Gradient


def onlyToday(lista):
  from datetime import date
  today = date.today()

  todayList = []

  for x in range(len(lista)):
    if lista[x][0] == str(today):
      todayList.append(lista[x])

  return todayList


def eliminar_EscolhasRepetidas(lista):
	duplicates = []

	def list_diff(a, b):
		return [x for x in a if x not in b]

	if len(lista) == 0:
		print('sem opções para hoje')
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

def onlyTimeGreater(lista):
	today = date.today()
	time_now = str(datetime.datetime.now().strftime("%H:%M:%S"))
	to_do = []
	if len(lista) == 0:
		pass

	else:
		# REMOVER ITEM COM HÓRARIO MENOR QUE O HORÁRIO ATUAL
		for x in range(len(lista)):
			if lista[x][1] >= str(time_now) and lista[x][0] >= str(today):
				to_do.append(lista[x])

			if str(lista[x][1]) < str(time_now):
				pass



	return to_do

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

# FUNÇÕES PARA O CRONOGRAMA
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
		step4[w][6] = changeStatusColor(step4[w][6])

	# CONVERTER PARA TUPLAR [[]] -> [()]
	for j in range(len(step4)):
		step4[j] = tuple(step4[j])

	return step4


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
		#self.width = 150
		#self.background_normal = ''
		#self.background_color = [238 / 255, 242 / 255, 254 / 255, 1]  # blue colour




class Inicio(Screen):
	#cor_principal = StringProperty('f54d4d')
	#cor_fundo_principal = StringProperty('e94f4f')
	def OpenFileManager(self):
		print('oi')

	def textColor(self):
		self.ids.button_cronograma_texto.color = get_color_from_hex('#ffffff')








	value = NumericProperty(250)
	align = (1000,1)


	def change_align(self,**kwargs):
		# ICON POSITION UPDATE
		self.ids.toggle_button_icon.size_hint = (0.4,50)
		self.ids.user_button_icon.size_hint = (0.4, 50)
		self.ids.cronograma_button_icon.size_hint = (0.4, 50)
		self.ids.rendimento_button_icon.size_hint = (0.4, 50)
		self.ids.simulados_button_icon.size_hint = (0.4, 50)
		self.ids.stats_button_icon.size_hint = (0.4, 50)
		self.ids.timer_button_icon.size_hint = (0.4, 50)
		self.ids.help_button_icon.size_hint = (0.4, 50)
		self.ids.settings_button_icon.size_hint = (0.4, 50)

		# LABELS UPDATE
		self.ids.toggle_button_label.text = "[b]Essentials Study[/b]"
		self.ids.user_button_label.text = "[b]Seu Perfil[/b]"
		self.ids.cronograma_button_label.text = "[b]Seu Cronograma[/b]"
		self.ids.rendimento_button_label.text = "[b]Seu Rendimento[/b]"
		self.ids.simulados_button_label.text = "[b]Seus Simulados[/b]"
		self.ids.stats_button_label.text = "[b]Suas Estatísticas[/b]"
		self.ids.timer_button_label.text = "[b]Seu Temporizador[/b]"
		self.ids.help_button_label.text = "[b]Ajuda/Dúvidas[/b]"
		self.ids.settings_button_label.text = "[b]Suas Configurações[/b]"

	def refresh_align(self,**kwargs):
		# ICON POSITION RESET
		self.ids.toggle_button_icon.size_hint = (1000,1)
		self.ids.user_button_icon.size_hint = (1000,1)
		self.ids.cronograma_button_icon.size_hint = (1000, 1)
		self.ids.rendimento_button_icon.size_hint = (1000, 1)
		self.ids.simulados_button_icon.size_hint = (1000, 1)
		self.ids.stats_button_icon.size_hint = (1000, 1)
		self.ids.timer_button_icon.size_hint = (1000, 1)
		self.ids.help_button_icon.size_hint = (1000, 1)
		self.ids.settings_button_icon.size_hint = (1000, 1)

		# LABELS RESET
		self.ids.toggle_button_label.text = ""
		self.ids.user_button_label.text = ""
		self.ids.cronograma_button_label.text = ""
		self.ids.rendimento_button_label.text = ""
		self.ids.simulados_button_label.text = ""
		self.ids.stats_button_label.text = ""
		self.ids.timer_button_label.text = ""
		self.ids.help_button_label.text = ""
		self.ids.settings_button_label.text = ""

	def change_width(self,**kwargs):
		self.value = 250

	def refresh_width(self,**kwargs):
		self.value = 50


class Inicio_CriarMateria(Screen):
	dialog = None
	dialog2 = None
	dialog3 = None
	dialog4 = None


	#print(Factory.Content().ids.nome_materia_delete.text)
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

		if nome_materia != "" and  nome_tag != "" and len(nome_tag) == 3 and len(nome_materia) <= 24:

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





	value = NumericProperty(50)
	align = (1000,1)

	def change_align(self,**kwargs):
		# ICON POSITION UPDATE
		self.ids.toggle_button_icon.size_hint = (0.4,50)
		self.ids.user_button_icon.size_hint = (0.4, 50)
		self.ids.cronograma_button_icon.size_hint = (0.4, 50)
		self.ids.rendimento_button_icon.size_hint = (0.4, 50)
		self.ids.simulados_button_icon.size_hint = (0.4, 50)
		self.ids.stats_button_icon.size_hint = (0.4, 50)
		self.ids.timer_button_icon.size_hint = (0.4, 50)
		self.ids.help_button_icon.size_hint = (0.4, 50)
		self.ids.settings_button_icon.size_hint = (0.4, 50)

		# LABELS UPDATE
		self.ids.toggle_button_label.text = "[b]Essentials Study[/b]"
		self.ids.user_button_label.text = "[b]Seu Perfil[/b]"
		self.ids.cronograma_button_label.text = "[b]Seu Cronograma[/b]"
		self.ids.rendimento_button_label.text = "[b]Seu Rendimento[/b]"
		self.ids.simulados_button_label.text = "[b]Seus Simulados[/b]"
		self.ids.stats_button_label.text = "[b]Suas Estatísticas[/b]"
		self.ids.timer_button_label.text = "[b]Seu Temporizador[/b]"
		self.ids.help_button_label.text = "[b]Ajuda/Dúvidas[/b]"
		self.ids.settings_button_label.text = "[b]Suas Configurações[/b]"

	def refresh_align(self,**kwargs):
		# ICON POSITION RESET
		self.ids.toggle_button_icon.size_hint = (1000,1)
		self.ids.user_button_icon.size_hint = (1000,1)
		self.ids.cronograma_button_icon.size_hint = (1000, 1)
		self.ids.rendimento_button_icon.size_hint = (1000, 1)
		self.ids.simulados_button_icon.size_hint = (1000, 1)
		self.ids.stats_button_icon.size_hint = (1000, 1)
		self.ids.timer_button_icon.size_hint = (1000, 1)
		self.ids.help_button_icon.size_hint = (1000, 1)
		self.ids.settings_button_icon.size_hint = (1000, 1)

		# LABELS RESET
		self.ids.toggle_button_label.text = ""
		self.ids.user_button_label.text = ""
		self.ids.cronograma_button_label.text = ""
		self.ids.rendimento_button_label.text = ""
		self.ids.simulados_button_label.text = ""
		self.ids.stats_button_label.text = ""
		self.ids.timer_button_label.text = ""
		self.ids.help_button_label.text = ""
		self.ids.settings_button_label.text = ""

	def change_width(self,**kwargs):
		self.value = 250

	def refresh_width(self,**kwargs):
		self.value = 50


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
				size_hint=[0.4, 0.2],
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
						#print('encontrei em', nome_materia)
						#print(self.data)
						self.data[nome_materia][1].remove(name)
						#print(self.data)
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
			#self.data = pickle.load((open("data_subjects_topics.p", "rb")))
			super().__init__(**kwargs)
			# self.background_normal = ''
			# self.background_color = [238 / 255, 242 / 255, 254 / 255, 1]  # blue colour
			self.dropdown_cls = SpinnerDropdown
			self.option_cls = SpinnerOptions
			#self.values = tuple(self.data.keys())
			self.color = [104 / 255, 111 / 255, 163 / 255, 1]
			#self.text = "Selecione uma matéria"
			self.bold = True
			self.dropdown_cls.max_height = self.height * 2 + 2 * 4







	value = NumericProperty(50)
	align = (1000, 1)

	def change_align(self, **kwargs):
		# ICON POSITION UPDATE
		self.ids.toggle_button_icon.size_hint = (0.4, 50)
		self.ids.user_button_icon.size_hint = (0.4, 50)
		self.ids.cronograma_button_icon.size_hint = (0.4, 50)
		self.ids.rendimento_button_icon.size_hint = (0.4, 50)
		self.ids.simulados_button_icon.size_hint = (0.4, 50)
		self.ids.stats_button_icon.size_hint = (0.4, 50)
		self.ids.timer_button_icon.size_hint = (0.4, 50)
		self.ids.help_button_icon.size_hint = (0.4, 50)
		self.ids.settings_button_icon.size_hint = (0.4, 50)

		# LABELS UPDATE
		self.ids.toggle_button_label.text = "[b]Essentials Study[/b]"
		self.ids.user_button_label.text = "[b]Seu Perfil[/b]"
		self.ids.cronograma_button_label.text = "[b]Seu Cronograma[/b]"
		self.ids.rendimento_button_label.text = "[b]Seu Rendimento[/b]"
		self.ids.simulados_button_label.text = "[b]Seus Simulados[/b]"
		self.ids.stats_button_label.text = "[b]Suas Estatísticas[/b]"
		self.ids.timer_button_label.text = "[b]Seu Temporizador[/b]"
		self.ids.help_button_label.text = "[b]Ajuda/Dúvidas[/b]"
		self.ids.settings_button_label.text = "[b]Suas Configurações[/b]"

	def refresh_align(self, **kwargs):
		# ICON POSITION RESET
		self.ids.toggle_button_icon.size_hint = (1000, 1)
		self.ids.user_button_icon.size_hint = (1000, 1)
		self.ids.cronograma_button_icon.size_hint = (1000, 1)
		self.ids.rendimento_button_icon.size_hint = (1000, 1)
		self.ids.simulados_button_icon.size_hint = (1000, 1)
		self.ids.stats_button_icon.size_hint = (1000, 1)
		self.ids.timer_button_icon.size_hint = (1000, 1)
		self.ids.help_button_icon.size_hint = (1000, 1)
		self.ids.settings_button_icon.size_hint = (1000, 1)

		# LABELS RESET
		self.ids.toggle_button_label.text = ""
		self.ids.user_button_label.text = ""
		self.ids.cronograma_button_label.text = ""
		self.ids.rendimento_button_label.text = ""
		self.ids.simulados_button_label.text = ""
		self.ids.stats_button_label.text = ""
		self.ids.timer_button_label.text = ""
		self.ids.help_button_label.text = ""
		self.ids.settings_button_label.text = ""

	def change_width(self, **kwargs):
		self.value = 250

	def refresh_width(self, **kwargs):
		self.value = 50

	def addTopico(self, root, *args):
		self.data = pickle.load((open("data_subjects_topics.p", "rb")))
		nome_topico_bruto = ' '.join(root.ids.name_topico.text.split()).lower().title()

		if root.ids.spinnerMaterias.text != "" and root.ids.spinnerMaterias.text != 'Selecione uma matéria' and root.ids.name_topico.text != "" and len(root.ids.name_topico.text) <= 20:
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
	value = NumericProperty(50)
	align = (1000, 1)

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

	def EstudadoFunction_Home(self, root):
		validation_tabel = '<kivymd.uix.spinner.spinner.MDSpinner'
		data_cronograma = pickle.load((open("data_timeline.p", "rb")))

		# IDENTIFICAR SPIN WIDGET
		if str(self.ids.cronograma22.children[-1])[0:37] == validation_tabel:
			pass

		# IDENTIFICAR TABELA E ROWS CHECK DIFERENTE DE LISTA VAZIA
		if str(self.ids.cronograma22.children[-1])[0:37] != validation_tabel and self.ids.cronograma22.children[-1].get_row_checks() != [] and len(self.ids.cronograma22.children[-1].get_row_checks()) > 0:

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

			options = list(root.ids.cronograma22.children[-1].get_row_checks())        # opções selecionadas para mudar status
			data_cronograma = colorData(organizerData(sortData(data_cronograma)))      # organizar, colorir e sort para o dado bruto
			estudadoList = rebuildDataStyle(options)								   # colocar as opções selecionadas no padrão do dado motificado acima

			data_cronograma = Estudado(data_cronograma, estudadoList)                  # aplicar a função estudado para as opções selecionadas em data

			# CRIAR O PADRÃO DE ESTILO NA LISTA
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

			data_cronograma = defaultStyle(data_cronograma)                           # retornar o data modificado para o padrão bruto de data
			pickle.dump(data_cronograma, open("data_timeline.p", "wb"))
			#self.ids.cronograma22.clear_widgets()

			def changeTime(label):
				return label.split(':')[0] + 'h' + label.split(':')[1] + 'min'

			def changeData(label):
				text = label.split('-')
				separator = '/'
				return separator.join([text[2], text[1], text[0]])

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

				self.estudado = count_Estudado(True)
				self.nao_estudado = count_Estudado(False)

			#data_new = pickle.load((open("data_timeline.p", "rb")))
			#self.data_new = pickle.load((open("data_timeline.p", "rb")))

			# NOVOS DADOS A PARTIR DO BOTAO DE FILTRAR ITEM
			try:
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

				DataSearched = SearchByData(data_cronograma, str(self.data_selecionada))

				if len(DataSearched) >= 0:
					def AutoSizeTableRowsNum(lista):
						lista = CronogramaTableStyle(colorData(organizerData(sortData(lista))))

						if len(lista) == 0:
							return createEmptyRow(createEmptyRow(lista))

						if len(lista) == 1:
							return createEmptyRow(lista)

						if len(lista) > 1:
							return lista

					data_DataByName = MDDataTable(
						background_color=get_color_from_hex("#eef2fe"),
						background_color_header=get_color_from_hex("#eef2fe"),
						background_color_selected_cell=get_color_from_hex("#f2f5fc"),
						background_color_cell=(0.9333, 0.9490, 0.9960, 1),
						size_hint=(1, 1),
						elevation=0,
						check=True,
						use_pagination=True,
						rows_num=5,
						column_data=[("[color=#686fa3]Data[/color]", dp(35)),
									 ("[color=#686fa3]Horário[/color]", dp(35)),
									 ("[color=#686fa3]Categoria[/color]", dp(35)),
									 ("[color=#686fa3]Matéria[/color]", dp(35)),
									 ("[color=#686fa3]Tópico[/color]", dp(35)),
									 ("[color=#686fa3]Status[/color]", dp(35))],
						row_data=AutoSizeTableRowsNum(DataSearched)
					)

					#self.ids.cronograma22.add_widget(data_DataByName)
					self.ids.cronograma22.children[0].update_row_data(self, AutoSizeTableRowsNum(DataSearched))


					def refreshChecks(dt):
						try:
							self.ids.cronograma22.children[0].DoubleClickRefreshChecks()

						except IndexError:
							pass

					Clock.schedule_once(refreshChecks, 1.10)


			# NOVOS DADOS A PARTIR DA PAGINA INICIAL
			except AttributeError:
				def AutoSizeTableRowsNum(lista):
					lista = today_only(CronogramaTableStyle(colorData(organizerData(sortData(lista)))))

					if len(lista) == 0:
						return createEmptyRow(createEmptyRow(lista))

					if len(lista) == 1:
						return createEmptyRow(lista)

					if len(lista) > 1:
						return lista

				data_new = pickle.load((open("data_timeline.p", "rb")))

				data_tables = MDDataTable(
					background_color_header=get_color_from_hex("#eef2fe"),
					background_color_selected_cell=get_color_from_hex("#f2f5fc"),
					background_color_cell=(0.9333, 0.9490, 0.9960, 1),
					size_hint=(1, 1),
					elevation=0,
					check=True,
					use_pagination=True,
					rows_num=5,
					column_data=[("[color=#686fa3]Data[/color]", dp(35)), ("[color=#686fa3]Horário[/color]", dp(35)),
								 ("[color=#686fa3]Categoria[/color]", dp(35)),
								 ("[color=#686fa3]Matéria[/color]", dp(35)),
								 ("[color=#686fa3]Tópico[/color]", dp(35)), ("[color=#686fa3]Status[/color]", dp(35))],
					row_data=AutoSizeTableRowsNum(data_new)

				)

				#self.ids.cronograma22.add_widget(data_tables)
				self.ids.cronograma22.children[0].update_row_data(self, AutoSizeTableRowsNum(data_new))

				def refreshChecks(dt):
					try:
						self.ids.cronograma22.children[0].DoubleClickRefreshChecks()

					except IndexError:
						pass

				Clock.schedule_once(refreshChecks, 1.10)

	def NaoEstudadoFunction_Home(self, root):
		validation_tabel = '<kivymd.uix.spinner.spinner.MDSpinner'
		data_cronograma = pickle.load((open("data_timeline.p", "rb")))

		# IDENTIFICAR SPIN WIDGET
		if str(self.ids.cronograma22.children[-1])[0:37] == validation_tabel:
			pass

		# IDENTIFICAR TABELA E ROWS CHECK DIFERENTE DE LISTA VAZIA
		if str(self.ids.cronograma22.children[-1])[0:37] != validation_tabel and self.ids.cronograma22.children[
			-1].get_row_checks() != [] and len(self.ids.cronograma22.children[-1].get_row_checks()) > 0:

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

			options = list(root.ids.cronograma22.children[-1].get_row_checks())  # opções selecionadas para mudar status
			data_cronograma = colorData(
				organizerData(sortData(data_cronograma)))  # organizar, colorir e sort para o dado bruto
			estudadoList = rebuildDataStyle(
				options)  # colocar as opções selecionadas no padrão do dado motificado acima

			data_cronograma = NaoEstudado(data_cronograma,
									   estudadoList)  # aplicar a função estudado para as opções selecionadas em data

			# CRIAR O PADRÃO DE ESTILO NA LISTA
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

						# DEFAULT PARA A DURAÇÃO
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

			data_cronograma = defaultStyle(data_cronograma)  # retornar o data modificado para o padrão bruto de data

			pickle.dump(data_cronograma, open("data_timeline.p", "wb"))

			#self.ids.cronograma22.clear_widgets()

			def changeTime(label):
				return label.split(':')[0] + 'h' + label.split(':')[1] + 'min'

			def changeData(label):
				text = label.split('-')
				separator = '/'
				return separator.join([text[2], text[1], text[0]])


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
				self.estudado = count_Estudado(True)
				self.nao_estudado = count_Estudado(False)



			# NOVOS DADOS A PARTIR DO BOTÃO DE PESQUISAR
			try:
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

				DataSearched = SearchByData(data_cronograma, str(self.data_selecionada))

				if len(DataSearched) >= 0:
					def AutoSizeTableRowsNum(lista):
						lista = CronogramaTableStyle(colorData(organizerData(sortData(lista))))

						if len(lista) == 0:
							return createEmptyRow(createEmptyRow(lista))

						if len(lista) == 1:
							return createEmptyRow(lista)

						if len(lista) > 1:
							return lista

					data_DataByName = MDDataTable(
						background_color=get_color_from_hex("#eef2fe"),
						background_color_header=get_color_from_hex("#eef2fe"),
						background_color_selected_cell=get_color_from_hex("#f2f5fc"),
						background_color_cell=(0.9333, 0.9490, 0.9960, 1),
						size_hint=(1, 1),
						elevation=0,
						check=True,
						use_pagination=True,
						rows_num=5,
						column_data=[("[color=#686fa3]Data[/color]", dp(35)),
									 ("[color=#686fa3]Horário[/color]", dp(35)),
									 ("[color=#686fa3]Categoria[/color]", dp(35)),
									 ("[color=#686fa3]Matéria[/color]", dp(35)),
									 ("[color=#686fa3]Tópico[/color]", dp(35)),
									 ("[color=#686fa3]Status[/color]", dp(35))],
						row_data=AutoSizeTableRowsNum(DataSearched)
					)

					self.ids.cronograma22.children[0].update_row_data(self, AutoSizeTableRowsNum(DataSearched))
					#self.ids.cronograma22.add_widget(data_DataByName)

					def refreshChecks(dt):
						try:
							self.ids.cronograma22.children[0].DoubleClickRefreshChecks()

						except IndexError:
							pass

					Clock.schedule_once(refreshChecks, 1)

			# NOVOS DADOS A PARTIR DA PAGINA INICIAL DO DIA ATUAL
			except AttributeError:
				def AutoSizeTableRowsNum(lista):
					lista = today_only(CronogramaTableStyle(colorData(organizerData(sortData(lista)))))

					if len(lista) == 0:
						return createEmptyRow(createEmptyRow(lista))

					if len(lista) == 1:
						return createEmptyRow(lista)

					if len(lista) > 1:
						return lista

				data_new = pickle.load((open("data_timeline.p", "rb")))

				data_tables = MDDataTable(
					background_color_header=get_color_from_hex("#eef2fe"),
					background_color_selected_cell=get_color_from_hex("#f2f5fc"),
					background_color_cell=(0.9333, 0.9490, 0.9960, 1),
					size_hint=(1, 1),
					elevation=0,
					check=True,
					use_pagination=True,
					rows_num=5,
					column_data=[("[color=#686fa3]Data[/color]", dp(35)), ("[color=#686fa3]Horário[/color]", dp(35)),
								 ("[color=#686fa3]Categoria[/color]", dp(35)),
								 ("[color=#686fa3]Matéria[/color]", dp(35)),
								 ("[color=#686fa3]Tópico[/color]", dp(35)), ("[color=#686fa3]Status[/color]", dp(35))],
					row_data=AutoSizeTableRowsNum(data_new)

				)

				self.ids.cronograma22.children[0].update_row_data(self, AutoSizeTableRowsNum(data_new))

				def refreshChecks(dt):
					try:
						self.ids.cronograma22.children[0].DoubleClickRefreshChecks()

					except IndexError:
						pass

				Clock.schedule_once(refreshChecks, 1.10)




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
		date_dialog.primary_color = get_color_from_hex("#ff5959")         # COR DO FUNDO DE TRABALHO (AZUL CLARO)
		date_dialog.accent_color = get_color_from_hex("#e5ebfb")          # COR DO MENU DO LADO ESQUEROD (VERMELHO)
		date_dialog.selector_color = get_color_from_hex("#686fa3")        # COR DO CIRCULO DE SELEÇÃO
		date_dialog.text_toolbar_color = get_color_from_hex("#ffffff")    # COR DO TEXTO NO MENU DO LADO ESQUERDO (VERMELHO)
		#date_dialog.input_field_background_color = (0.9569, 0.9647, 0.9922, 0.2)

		# COR DOS TEXTOS
		date_dialog.text_color = ("#686fa3")
		date_dialog.text_current_color = get_color_from_hex("#686fa3")
		date_dialog.text_button_color = (0.4078, 0.4353, 0.6392, .5)
		#date_dialog.input_field_text_color = (0.4078, 0.4353, 0.6392, .5)

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

		def changeData(label):
			text = label.split('-')
			separator = '/'
			return separator.join([text[2], text[1], text[0]])

		data_cronograma = pickle.load((open("data_timeline.p", "rb")))
		self.ids.cronograma22.clear_widgets()

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

		DataSearched = SearchByData(data_cronograma, str(self.data_selecionada))

		self.estudado_data = changeData(str(self.data_selecionada))
		self.nao_estudado_data = changeData(str(self.data_selecionada))
		self.estudado = count_Estudado(True, str(self.data_selecionada))
		self.nao_estudado = count_Estudado(False, str(self.data_selecionada))

		if len(DataSearched) >= 0:
			def AutoSizeTableRowsNum(lista):
				lista = CronogramaTableStyle(colorData(organizerData(sortData(lista))))

				if len(lista) == 0:
					print('lista vazia')
					print(lista)
					return createEmptyRow(createEmptyRow(lista))

				if len(lista) == 1:
					return createEmptyRow(lista)

				if len(lista) > 1:
					return lista

			data_DataByName = MDDataTable(
				background_color=get_color_from_hex("#eef2fe"),
				background_color_header=get_color_from_hex("#eef2fe"),
				background_color_selected_cell=get_color_from_hex("#f2f5fc"),
				background_color_cell=(0.9333, 0.9490, 0.9960, 1),
				size_hint=(1, 1),
				elevation=0,
				check=True,
				use_pagination=True,
				rows_num=5,
				column_data=[("[color=#686fa3]Data[/color]", dp(35)), ("[color=#686fa3]Horário[/color]", dp(35)),
							 ("[color=#686fa3]Categoria[/color]", dp(35)),
							 ("[color=#686fa3]Matéria[/color]", dp(35)),
							 ("[color=#686fa3]Tópico[/color]", dp(35)),
							 ("[color=#686fa3]Status[/color]", dp(35))],
				row_data=AutoSizeTableRowsNum(DataSearched)
			)

			self.ids.cronograma22.add_widget(data_DataByName)




	def filtrar_item(self, instance, value, date_range):
		def changeData(label):
			text = label.split('-')
			separator = '/'
			return separator.join([text[2], text[1], text[0]])

		self.dataFiltrada = []
		self.dataFiltrada.append(value)
		self.data_selecionada = str(self.dataFiltrada[0])
		#self.data_selecionada = changeData(self.data_selecionada)

		self.ids.cronograma22.clear_widgets()
		spin = MDSpinner(size_hint=(0.2, 0.2),
						 pos_hint={'center_x': 0.5, 'center_y': 0.5},
						 active=True,
						 line_width=dp(12),
						 color=[0.8980, 0.9216, 0.9843, 1])

		self.ids.cronograma22.add_widget(spin)

		def remover_spin(dt):
			self.ids.cronograma22.remove_widget(self.ids.cronograma22.children[-1])

		def adicionarNewTable(dt):
			self.tabela_dados_filtrados()

		def refreshChecks(dt):
			try:
				self.ids.cronograma22.children[0].DoubleClickRefreshChecks()

			except IndexError:
				pass


		Clock.schedule_once(remover_spin, 1.05)
		Clock.schedule_once(adicionarNewTable, 1.05)
		Clock.schedule_once(refreshChecks, 1.10)


	def on_cancel(self, instance, value):
		pass

	def change_align(self, **kwargs):
		# ICON POSITION UPDATE
		self.ids.toggle_button_icon.size_hint = (0.4, 50)
		self.ids.user_button_icon.size_hint = (0.4, 50)
		self.ids.cronograma_button_icon.size_hint = (0.4, 50)
		self.ids.rendimento_button_icon.size_hint = (0.4, 50)
		self.ids.simulados_button_icon.size_hint = (0.4, 50)
		self.ids.stats_button_icon.size_hint = (0.4, 50)
		self.ids.timer_button_icon.size_hint = (0.4, 50)
		self.ids.help_button_icon.size_hint = (0.4, 50)
		self.ids.settings_button_icon.size_hint = (0.4, 50)

		# LABELS UPDATE
		self.ids.toggle_button_label.text = "[b]Essentials Study[/b]"
		self.ids.user_button_label.text = "[b]Seu Perfil[/b]"
		self.ids.cronograma_button_label.text = "[b]Seu Cronograma[/b]"
		self.ids.rendimento_button_label.text = "[b]Seu Rendimento[/b]"
		self.ids.simulados_button_label.text = "[b]Seus Simulados[/b]"
		self.ids.stats_button_label.text = "[b]Suas Estatísticas[/b]"
		self.ids.timer_button_label.text = "[b]Seu Temporizador[/b]"
		self.ids.help_button_label.text = "[b]Ajuda/Dúvidas[/b]"
		self.ids.settings_button_label.text = "[b]Suas Configurações[/b]"

	def refresh_align(self, **kwargs):
		# ICON POSITION RESET
		self.ids.toggle_button_icon.size_hint = (1000, 1)
		self.ids.user_button_icon.size_hint = (1000, 1)
		self.ids.cronograma_button_icon.size_hint = (1000, 1)
		self.ids.rendimento_button_icon.size_hint = (1000, 1)
		self.ids.simulados_button_icon.size_hint = (1000, 1)
		self.ids.stats_button_icon.size_hint = (1000, 1)
		self.ids.timer_button_icon.size_hint = (1000, 1)
		self.ids.help_button_icon.size_hint = (1000, 1)
		self.ids.settings_button_icon.size_hint = (1000, 1)

		# LABELS RESET
		self.ids.toggle_button_label.text = ""
		self.ids.user_button_label.text = ""
		self.ids.cronograma_button_label.text = ""
		self.ids.rendimento_button_label.text = ""
		self.ids.simulados_button_label.text = ""
		self.ids.stats_button_label.text = ""
		self.ids.timer_button_label.text = ""
		self.ids.help_button_label.text = ""
		self.ids.settings_button_label.text = ""

	def change_width(self, **kwargs):
		self.value = 250

	def refresh_width(self, **kwargs):
		self.value = 50


	def on_enter(self, *args):

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
		today = changeData(str(today))

		try:
			self.estudado_data = today
			self.nao_estudado_data = today
			self.estudado = count_Estudado(True)
			self.nao_estudado = count_Estudado(False)
		except ValueError:
			pass


		def AutoSizeTableRowsNum(lista):
			lista = today_only(CronogramaTableStyle(colorData(organizerData(sortData(lista)))))

			if len(lista) == 0:
				return createEmptyRow(createEmptyRow(lista))

			if len(lista) == 1:
				return createEmptyRow(lista)

			if len(lista) > 1:
				return lista

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

		data_tables = MDDataTable(
			background_color_header=get_color_from_hex("#eef2fe"),
			background_color_selected_cell = get_color_from_hex("#f2f5fc"),
			background_color_cell = (0.9333, 0.9490, 0.9960,1),
			size_hint=(1, 1),
			elevation=0,
			check = True,
			use_pagination=True,
			rows_num=5,
			#rows_num = len(AutoSizeTableRowsNum(data_cronograma)),
			column_data=[("[color=#686fa3]Data[/color]", dp(35)), ("[color=#686fa3]Horário[/color]", dp(35)), ("[color=#686fa3]Categoria[/color]", dp(35)), ("[color=#686fa3]Matéria[/color]", dp(35)),
						 ("[color=#686fa3]Tópico[/color]", dp(35)), ("[color=#686fa3]Status[/color]", dp(35))],
			row_data= AutoSizeTableRowsNum(data_cronograma)

		)

		def adicionar_Tabela(dt):
			self.ids.cronograma22.add_widget(data_tables)
			self.ids.cronograma22.children[-1].pos_hint = {'center_x': .5,'center_y': .5}


		def remover_spin(dt):
			self.ids.cronograma22.remove_widget(self.ids.cronograma22.children[-1])

		def refreshChecks(dt):
			try:
				self.ids.cronograma22.children[0].DoubleClickRefreshChecks()

			except IndexError:
				pass

		Clock.schedule_once(adicionar_Tabela, 1.05)
		Clock.schedule_once(remover_spin, 1.05)
		Clock.schedule_once(refreshChecks, 1.07)


	def on_leave(self, *args):
		self.ids.cronograma22.clear_widgets()


	def on_pre_enter(self, *args):
		spin = MDSpinner(size_hint=(0.2, 0.2),
						 pos_hint={'center_x': 0.5, 'center_y': 0.5},
						 active=True,
						 line_width=dp(12),
						 color=[0.8980, 0.9216, 0.9843, 1])

		self.ids.cronograma22.add_widget(spin)

class Cronograma_CriarItem(Screen):
	dialog8 = None


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

	value = NumericProperty(50)
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
		date_dialog.primary_color = get_color_from_hex("#ff5959")         # COR DO FUNDO DE TRABALHO (AZUL CLARO)
		date_dialog.accent_color = get_color_from_hex("#e5ebfb")          # COR DO MENU DO LADO ESQUEROD (VERMELHO)
		date_dialog.selector_color = get_color_from_hex("#686fa3")        # COR DO CIRCULO DE SELEÇÃO
		date_dialog.text_toolbar_color = get_color_from_hex("#ffffff")    # COR DO TEXTO NO MENU DO LADO ESQUERDO (VERMELHO)
		#date_dialog.input_field_background_color = (0.9569, 0.9647, 0.9922, 0.2)

		# COR DOS TEXTOS
		date_dialog.text_color = ("#686fa3")
		date_dialog.text_current_color = get_color_from_hex("#686fa3")
		date_dialog.text_button_color = (0.4078, 0.4353, 0.6392, .5)
		#date_dialog.input_field_text_color = (0.4078, 0.4353, 0.6392, .5)

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
		time_dialog.primary_color = get_color_from_hex("#e5ebfb")  # COR DO FUNDO DE TRABALHO (AZUL CLARO)
		time_dialog.accent_color = get_color_from_hex("#eef2fe")  # COR DO RELOGIO
		time_dialog.selector_color = get_color_from_hex("#686fa3")  # COR DOS BOTOES DE HORA + COR DO BOTAO
		time_dialog.text_toolbar_color = get_color_from_hex("#686fa3")  # COR DOS TITULOS E BOTÕES SECUNDARIOS

		# COR DOS TEXTOS
		time_dialog.text_color = ("#686fa3")  # COR DAS LETRAS DAS HORAS DO PONTEIRO
		time_dialog.text_current_color = get_color_from_hex("#ffffff")  # COR DA HORA NO PONTEIRO SELECIONADO
		time_dialog.text_button_color = (0.4078, 0.4353, 0.6392, 1)  # COR DOS TEXTOS DOS BOTÕES CANCELAR E CONCLUIR

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


	def change_align(self, **kwargs):
			# ICON POSITION UPDATE
			self.ids.toggle_button_icon.size_hint = (0.4, 50)
			self.ids.user_button_icon.size_hint = (0.4, 50)
			self.ids.cronograma_button_icon.size_hint = (0.4, 50)
			self.ids.rendimento_button_icon.size_hint = (0.4, 50)
			self.ids.simulados_button_icon.size_hint = (0.4, 50)
			self.ids.stats_button_icon.size_hint = (0.4, 50)
			self.ids.timer_button_icon.size_hint = (0.4, 50)
			self.ids.help_button_icon.size_hint = (0.4, 50)
			self.ids.settings_button_icon.size_hint = (0.4, 50)

			# LABELS UPDATE
			self.ids.toggle_button_label.text = "[b]Essentials Study[/b]"
			self.ids.user_button_label.text = "[b]Seu Perfil[/b]"
			self.ids.cronograma_button_label.text = "[b]Seu Cronograma[/b]"
			self.ids.rendimento_button_label.text = "[b]Seu Rendimento[/b]"
			self.ids.simulados_button_label.text = "[b]Seus Simulados[/b]"
			self.ids.stats_button_label.text = "[b]Suas Estatísticas[/b]"
			self.ids.timer_button_label.text = "[b]Seu Temporizador[/b]"
			self.ids.help_button_label.text = "[b]Ajuda/Dúvidas[/b]"
			self.ids.settings_button_label.text = "[b]Suas Configurações[/b]"

	def refresh_align(self, **kwargs):
		# ICON POSITION RESET
		self.ids.toggle_button_icon.size_hint = (1000, 1)
		self.ids.user_button_icon.size_hint = (1000, 1)
		self.ids.cronograma_button_icon.size_hint = (1000, 1)
		self.ids.rendimento_button_icon.size_hint = (1000, 1)
		self.ids.simulados_button_icon.size_hint = (1000, 1)
		self.ids.stats_button_icon.size_hint = (1000, 1)
		self.ids.timer_button_icon.size_hint = (1000, 1)
		self.ids.help_button_icon.size_hint = (1000, 1)
		self.ids.settings_button_icon.size_hint = (1000, 1)

		# LABELS RESET
		self.ids.toggle_button_label.text = ""
		self.ids.user_button_label.text = ""
		self.ids.cronograma_button_label.text = ""
		self.ids.rendimento_button_label.text = ""
		self.ids.simulados_button_label.text = ""
		self.ids.stats_button_label.text = ""
		self.ids.timer_button_label.text = ""
		self.ids.help_button_label.text = ""
		self.ids.settings_button_label.text = ""

	def change_width(self, **kwargs):
		self.value = 250

	def refresh_width(self, **kwargs):
		self.value = 50

	def addToCronograma(self, root):
		try:
			#print(root.ids.duracao_horas.text + ' ' + root.ids.duracao_minutos.text)

			# CORRIGIR TEMPO DE DURAÇÃO

			if root.ids.spinnerCategorias.text != "Categorias" and root.ids.spinnerAllMaterias.text != "Matérias" and root.ids.spinnerTopicos.text != "Tópicos" and len(
				self.saveData) == 1 and len(self.saveTime) == 1 and root.ids.duracao_horas.text != "" and root.ids.duracao_minutos.text != "" and len(root.ids.duracao_horas.text) <=2 and len(root.ids.duracao_minutos.text) <= 2 and (root.ids.duracao_horas.text + ':' + root.ids.duracao_minutos.text) != "00:00":

				# CONDIÇÕES PARA ADICIONAR ZERO A ESQUERDA SE NECESSÁRIO
				if len(root.ids.duracao_horas.text) == 1:
					root.ids.duracao_horas.text = '0' + root.ids.duracao_horas.text

				if len(root.ids.duracao_horas.text) == 2:
					root.ids.duracao_horas.text  = root.ids.duracao_horas.text

				if len(root.ids.duracao_minutos.text) == 1:
					root.ids.duracao_minutos.text = '0' + root.ids.duracao_minutos.text

				if len(root.ids.duracao_horas.text) == 2:
					root.ids.duracao_minutos.text  = root.ids.duracao_minutos.text


				duration = root.ids.duracao_horas.text + ':' + root.ids.duracao_minutos.text + ':00'

				print(root.ids.spinnerCategorias.text)
				print(root.ids.spinnerAllMaterias.text)
				print(root.ids.spinnerTopicos.text)
				print('')
				print(self.saveData[0])
				print('')
				print(self.saveTime[0])
				print('')
				print(duration)

				self.data_cronograma = pickle.load((open("data_timeline.p", "rb")))

				self.data_cronograma.append((str(self.saveData[0]), str(self.saveTime[0]), root.ids.spinnerCategorias.text,
											 root.ids.spinnerAllMaterias.text, root.ids.spinnerTopicos.text, duration, ("alert-circle", [1, 0, 0, 1], "Não Estudado"), ' ', ' ', ' '))

				root.ids.duracao_horas.text = '00'
				root.ids.duracao_minutos.text = '00'
				root.show_item_confirmation()
				root.manager.current = 'Cronograma'

				# Refresh Data and Time List
				self.saveTime.clear()
				self.saveData.clear()

				pickle.dump(self.data_cronograma, open("data_timeline.p", "wb"))

		except AttributeError:  # CASO NÃO TIVER SELECIONADO DATA E TEMPO
			pass




	def on_leave(self, *args):
		self.ids.spinnerAllMaterias.values = ()
		self.ids.spinnerAllMaterias.text = "Matérias"
		self.ids.spinnerTopicos.text = 'Tópicos'
		self.ids.spinnerCategorias.text = 'Categorias'

	def on_enter(self, *args):
		self.data = pickle.load((open("data_subjects_topics.p", "rb")))
		self.ids.spinnerAllMaterias.values = tuple(self.data.keys())

		self.ids.spinnerAllMaterias.text = "Matérias"
		self.ids.spinnerTopicos.text = 'Tópicos'
		self.ids.spinnerCategorias.text = 'Categorias'


class Cronograma_RemoverItem(Screen):
	value = NumericProperty(50)
	align = (1000, 1)

	def search_by_string(self):
		data_cronograma = pickle.load((open("data_timeline.p", "rb")))

		DataByName = SearchBar(data_cronograma, str(self.ids.search_bar_name.text))

		if len(DataByName) != 0:

			def AutoSizeTableRowsNum(lista):
				if len(lista) == 0:
					return createEmptyRowRemoveCronograma(createEmptyRowRemoveCronograma(lista))

				if len(lista) == 1:
					return createEmptyRowRemoveCronograma(lista)

				if len(lista) > 1:
					return lista

			data_DataByName = MDDataTable(
				background_color=get_color_from_hex("#eef2fe"),
				background_color_header=get_color_from_hex("#eef2fe"),
				background_color_selected_cell=get_color_from_hex("#f2f5fc"),
				background_color_cell=(0.9333, 0.9490, 0.9960, 1),
				size_hint=(1, 1),
				elevation=0,
				check=True,
				use_pagination=True,
				rows_num=10,
				column_data=[("[color=#686fa3]Data[/color]", dp(35)), ("[color=#686fa3]Horário[/color]", dp(35)),
							 ("[color=#686fa3]Categoria[/color]", dp(35)), ("[color=#686fa3]Matéria[/color]", dp(35)),
							 ("[color=#686fa3]Tópico[/color]", dp(35)), ("[color=#686fa3]Duração[/color]", dp(35)),
							 ("[color=#686fa3]Status[/color]", dp(35))],
				row_data=AutoSizeTableRowsNum(DataByName)
			)

			self.ids.cronogramaAllItems.clear_widgets()
			self.ids.cronogramaAllItems.add_widget(data_DataByName)

			self.ids.cronogramaAllItems.children[0].DoubleClickRefreshChecks()


	def removeItemCronograma (self, root):
		#print(self.ids.cronogramaAllItems.children[-1])
		validation_tabel = '<kivymd.uix.spinner.spinner.MDSpinner'

		data_cronograma = pickle.load((open("data_timeline.p", "rb")))

		# IDENTIFICAR SPIN WIDGET
		if str(self.ids.cronogramaAllItems.children[-1])[0:37] == validation_tabel:
			pass

		# IDENTIFICAR TABELA E ROWS CHECK DIFERENTE DE LISTA VAZIA
		if str(self.ids.cronogramaAllItems.children[-1])[0:37] != validation_tabel and self.ids.cronogramaAllItems.children[-1].get_row_checks() != []:
			#print(self.ids.cronogramaAllItems.children[-1].get_row_checks())
			#data_cronograma = createEmptyRowRemoveCronograma(createEmptyRowRemoveCronograma(colorData(organizerData(sortData(data_cronograma)))))
			data_cronograma = colorData(organizerData(sortData(data_cronograma)))

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

			removeList = rebuildDataStyle(list(self.ids.cronogramaAllItems.children[-1].get_row_checks()))


			def list_diff(a, b):
				return [x for x in a if x not in b]


			data_cronograma = list_diff(data_cronograma, removeList)

			def defaultStyle(lista):
				step14 = []
				for i in range(len(lista)):
					step14.append([])

				# CONVERTER TUPLA PARA LISTA [()] - > [[]]
				for y in range(len(step14)):
					for x in range(len(lista[y])):
						if x < 6:
							step14[y].append(lista[y][x])

						if x == 6:
							step14[y].append(list(lista[y][x]))

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
							step14[x][0][15:25][-4:] + '-' + step14[x][0][15:25][-7:-5] + '-' + step14[x][0][15:25][-10:-8])

						# DEFAULT PARA O TEMPO
						step14[x][1] = str(step14[x][1][15:17] + ':' + step14[x][1][18:20] + ':00')

						# DEFAULT PARA CATEGORIA
						for y in range(2, 5):
							step14[x][y] = RegEx(step14[x][y])

						# DEFAULT PARA A DURAÇÃO
						step14[x][5] = str(step14[x][5][15:17] + ':' + step14[x][5][18:20] + ':00')

						# DEFAULT STATUS ESTUDADO - NÃO ESTUDADO
						try:
							if step14[x][6][2][15:27] == 'Não Estudado':
								step14[x][6][2] = 'Não Estudado'

							if step14[x][6][2][15:23] == 'Estudado':
								step14[x][6][2] = 'Estudado'
						except IndexError:
							pass

				#step14 = step14[:-2]

				for x in range(len(step14)):
					step14[x][-1] = tuple(step14[x][-1])
					step14[x] = tuple(step14[x])

				return step14

			data_cronograma = defaultStyle(data_cronograma)

			pickle.dump(data_cronograma, open("data_timeline.p", "wb"))

			self.ids.cronogramaAllItems.children[0].DoubleClickRefreshChecks()
			root.manager.current = 'Cronograma'

	def change_align(self, **kwargs):
		# ICON POSITION UPDATE
		self.ids.toggle_button_icon.size_hint = (0.4, 50)
		self.ids.user_button_icon.size_hint = (0.4, 50)
		self.ids.cronograma_button_icon.size_hint = (0.4, 50)
		self.ids.rendimento_button_icon.size_hint = (0.4, 50)
		self.ids.simulados_button_icon.size_hint = (0.4, 50)
		self.ids.stats_button_icon.size_hint = (0.4, 50)
		self.ids.timer_button_icon.size_hint = (0.4, 50)
		self.ids.help_button_icon.size_hint = (0.4, 50)
		self.ids.settings_button_icon.size_hint = (0.4, 50)

		# LABELS UPDATE
		self.ids.toggle_button_label.text = "[b]Essentials Study[/b]"
		self.ids.user_button_label.text = "[b]Seu Perfil[/b]"
		self.ids.cronograma_button_label.text = "[b]Seu Cronograma[/b]"
		self.ids.rendimento_button_label.text = "[b]Seu Rendimento[/b]"
		self.ids.simulados_button_label.text = "[b]Seus Simulados[/b]"
		self.ids.stats_button_label.text = "[b]Suas Estatísticas[/b]"
		self.ids.timer_button_label.text = "[b]Seu Temporizador[/b]"
		self.ids.help_button_label.text = "[b]Ajuda/Dúvidas[/b]"
		self.ids.settings_button_label.text = "[b]Suas Configurações[/b]"

	def refresh_align(self, **kwargs):
		# ICON POSITION RESET
		self.ids.toggle_button_icon.size_hint = (1000, 1)
		self.ids.user_button_icon.size_hint = (1000, 1)
		self.ids.cronograma_button_icon.size_hint = (1000, 1)
		self.ids.rendimento_button_icon.size_hint = (1000, 1)
		self.ids.simulados_button_icon.size_hint = (1000, 1)
		self.ids.stats_button_icon.size_hint = (1000, 1)
		self.ids.timer_button_icon.size_hint = (1000, 1)
		self.ids.help_button_icon.size_hint = (1000, 1)
		self.ids.settings_button_icon.size_hint = (1000, 1)

		# LABELS RESET
		self.ids.toggle_button_label.text = ""
		self.ids.user_button_label.text = ""
		self.ids.cronograma_button_label.text = ""
		self.ids.rendimento_button_label.text = ""
		self.ids.simulados_button_label.text = ""
		self.ids.stats_button_label.text = ""
		self.ids.timer_button_label.text = ""
		self.ids.help_button_label.text = ""
		self.ids.settings_button_label.text = ""

	def change_width(self, **kwargs):
		self.value = 250

	def refresh_width(self, **kwargs):
		self.value = 50

	def on_enter(self, *args):
		self.ids.search_bar_name.text = ''

		data_cronograma = pickle.load((open("data_timeline.p", "rb")))

		def AutoSizeTableRowsNum(lista):
			if len(lista) == 0:
				return createEmptyRowRemoveCronograma(createEmptyRowRemoveCronograma(colorData(organizerData(sortData(lista)))))

			if len(lista) == 1:
				return createEmptyRowRemoveCronograma(colorData(organizerData(sortData(lista))))

			if len(lista) > 1:
				return colorData(organizerData(sortData(lista)))

		data_tables2 = MDDataTable(
			background_color = get_color_from_hex("#eef2fe"),
			background_color_header=get_color_from_hex("#eef2fe"),
			background_color_selected_cell = get_color_from_hex("#f2f5fc"),
			background_color_cell = (0.9333, 0.9490, 0.9960,1),
			size_hint=(1, 1),
			elevation=0,
			check=True,
			use_pagination=True,
			rows_num=10,
			column_data=[("[color=#686fa3]Data[/color]", dp(35)), ("[color=#686fa3]Horário[/color]", dp(35)), ("[color=#686fa3]Categoria[/color]", dp(35)), ("[color=#686fa3]Matéria[/color]", dp(35)),
						 ("[color=#686fa3]Tópico[/color]", dp(35)),("[color=#686fa3]Duração[/color]", dp(35)), ("[color=#686fa3]Status[/color]", dp(35))],
			row_data= AutoSizeTableRowsNum(data_cronograma)
		)

		def adicionarTabela(dt):
			self.ids.cronogramaAllItems.add_widget(data_tables2)

		def removerSpin(dt):
			self.ids.cronogramaAllItems.remove_widget(self.ids.cronogramaAllItems.children[-1])

		def refreshChecks(dt):
			try:
				self.ids.cronogramaAllItems.children[0].DoubleClickRefreshChecks()

			except IndexError:
				pass

		Clock.schedule_once(adicionarTabela, 2)
		Clock.schedule_once(removerSpin, 2)
		Clock.schedule_once(refreshChecks, 2.1)


	def on_leave(self, *args):
		self.ids.cronogramaAllItems.clear_widgets()


	def on_pre_enter(self, *args):
		spin = MDSpinner(size_hint=(0.2, 0.2),
						 pos_hint={'center_x': 0.5, 'center_y': 0.5},
						 active=True,
						 line_width=dp(12),
						 color=[0.8980, 0.9216, 0.9843, 1])

		self.ids.cronogramaAllItems.add_widget(spin)

class Cronograma_AlterarStatus(Screen):
	value = NumericProperty(50)
	align = (1000, 1)

	def search_by_string(self):
		data_cronograma = pickle.load((open("data_timeline.p", "rb")))

		DataByName = SearchBar(data_cronograma, str(self.ids.search_bar_name.text))

		if len(DataByName) != 0:

			def AutoSizeTableRowsNum(lista):
				if len(lista) == 0:
					return createEmptyRowRemoveCronograma(createEmptyRowRemoveCronograma(lista))

				if len(lista) == 1:
					return createEmptyRowRemoveCronograma(lista)

				if len(lista) > 1:
					return lista

			data_DataByName = data_tables2 = MDDataTable(
			background_color = get_color_from_hex("#eef2fe"),
			background_color_header=get_color_from_hex("#eef2fe"),
			background_color_selected_cell = get_color_from_hex("#f2f5fc"),
			background_color_cell = (0.9333, 0.9490, 0.9960,1),
			size_hint=(1, 1),
			elevation=0,
			check=True,
			use_pagination=True,
			rows_num = 10,
			column_data=[("[color=#686fa3]Data[/color]", dp(35)), ("[color=#686fa3]Horário[/color]", dp(35)), ("[color=#686fa3]Categoria[/color]", dp(35)), ("[color=#686fa3]Matéria[/color]", dp(35)),
						 ("[color=#686fa3]Tópico[/color]", dp(35)),("[color=#686fa3]Duração[/color]", dp(35)), ("[color=#686fa3]Status[/color]", dp(35))],
			row_data= AutoSizeTableRowsNum(DataByName)
		)

			self.ids.cronogramaAllItems.clear_widgets()
			self.ids.cronogramaAllItems.add_widget(data_DataByName)

			self.ids.cronogramaAllItems.children[0].DoubleClickRefreshChecks()

	def EstudadoFunction(self, root):
		validation_tabel = '<kivymd.uix.spinner.spinner.MDSpinner'
		data_cronograma = pickle.load((open("data_timeline.p", "rb")))

		# IDENTIFICAR SPIN WIDGET
		if str(self.ids.cronogramaAllItems.children[-1])[0:37] == validation_tabel:
			pass


		# IDENTIFICAR TABELA E ROWS CHECK DIFERENTE DE LISTA VAZIA
		if str(self.ids.cronogramaAllItems.children[-1])[0:37] != validation_tabel and self.ids.cronogramaAllItems.children[-1].get_row_checks() != [] and len(self.ids.cronogramaAllItems.children[-1].get_row_checks()) > 0:
			#print('entrei funcao estudadofunction comprimento lista get_row_checks = ', len(self.ids.cronogramaAllItems.children[-1].get_row_checks()))

			print(list(self.ids.cronogramaAllItems.children[-1].get_row_checks()))
			def Estudado(data, select, color_hex='686fa3'):
				step22 = []
				step23 = []  # OPÇÕES PARA ALTERAR PARA ESTUDADO

				# ////////////////////////////////////////////
				# ORGANIZAR OS DADOS DE DATA
				for i in range(len(data)):
					step22.append([])

				# CONVERTER TUPLA PARA LISTA [()] - > [[]]
				for y in range(len(data)):
					for x in range(len(data[y])):
						if x == 6:
							step22[y].append(list(data[y][x]))

						else:
							step22[y].append(data[y][x])

				# ////////////////////////////////////////////
				# ORGANIZAR OS DADOS DE SELECT
				for i in range(len(select)):
					step23.append([])

				# CONVERTER TUPLA PARA LISTA [()] - > [[]]
				for y in range(len(select)):
					for x in range(len(select[y])):
						if x == 6:
							step23[y].append(list(select[y][x]))

						else:
							step23[y].append(select[y][x])

				def list_diff(a, b):
					return [x for x in a if x not in b]

				data_diff = list_diff(step22, step23)

				# COLOCAR ESTUDADO EM TODOS OS ITEMS DA LISTA SELECT
				for x in range(len(step23)):
					if step23[x][-1][2] == '[color=#{}]Estudado[/color]'.format(color_hex):
						pass

					else:
					#print(step23[x][-1])
						step23[x][-1][0] = 'checkbox-marked-circle'
						step23[x][-1][1] = [39 / 256, 174 / 256, 96 / 256, 1]
						step23[x][-1][2] = '[color=#{}]Estudado[/color]'.format(color_hex)
					#print(step23[x][-1])

				if len(data_diff) == 0:
					data_diff = step23

				elif len(data_diff) != 0:
					for item in range(len(step23)):
						data_diff.append(step23[item])

				# CONVERTER PARA TUPLA TODOS OS DADOS DE DATA_DIFF
				for x in range(len(data_diff)):
					data_diff[x][-1] = tuple(data_diff[x][-1])
					data_diff[x] = tuple(data_diff[x])

				return data_diff

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

			options = list(root.ids.cronogramaAllItems.children[-1].get_row_checks())
			data_cronograma = colorData(organizerData(sortData(data_cronograma)))
			estudadoList = rebuildDataStyle(options)
			data_Estudado = Estudado(data_cronograma, estudadoList)

			# CRIAR O PADRÃO DE ESTILO NA LISTA
			def defaultStyle(lista):
				step14 = []
				for i in range(len(lista)):
					step14.append([])

				# CONVERTER TUPLA PARA LISTA [()] - > [[]]
				for y in range(len(step14)):
					for x in range(len(lista[y])):
						if x < 6:
							step14[y].append(lista[y][x])

						if x == 6:
							step14[y].append(list(lista[y][x]))

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
							step14[x][0][15:25][-4:] + '-' + step14[x][0][15:25][-7:-5] + '-' + step14[x][0][15:25][-10:-8])

						# DEFAULT PARA O TEMPO
						step14[x][1] = str(step14[x][1][15:17] + ':' + step14[x][1][18:20] + ':00')

						# DEFAULT PARA CATEGORIA
						for y in range(2, 5):
							step14[x][y] = RegEx(step14[x][y])

						# DEFAULT PARA A DURAÇÃO
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
					step14[x][-1] = tuple(step14[x][-1])
					step14[x] = tuple(step14[x])

				return step14

			data_cronograma = defaultStyle(data_Estudado)
			pickle.dump(data_cronograma, open("data_timeline.p", "wb"))
			self.ids.cronogramaAllItems.children[0].DoubleClickRefreshChecks()

			def refreshScreen(dt):
				root.manager.current = 'Cronograma'

			Clock.schedule_once(refreshScreen, 0.2)

	def NaoEstudadoFunction(self, root):
		validation_tabel = '<kivymd.uix.spinner.spinner.MDSpinner'
		data_cronograma = pickle.load((open("data_timeline.p", "rb")))

		# IDENTIFICAR SPIN WIDGET
		if str(self.ids.cronogramaAllItems.children[-1])[0:37] == validation_tabel:
			pass


		# IDENTIFICAR TABELA E ROWS CHECK DIFERENTE DE LISTA VAZIA
		if str(self.ids.cronogramaAllItems.children[-1])[0:37] != validation_tabel and self.ids.cronogramaAllItems.children[-1].get_row_checks() != [] and len(self.ids.cronogramaAllItems.children[-1].get_row_checks()) > 0:
			def NaoEstudado(data, select, color_hex='686fa3'):
				step22 = []
				step23 = []  # OPÇÕES PARA ALTERAR PARA ESTUDADO

				# ////////////////////////////////////////////
				# ORGANIZAR OS DADOS DE DATA
				for i in range(len(data)):
					step22.append([])

				# CONVERTER TUPLA PARA LISTA [()] - > [[]]
				for y in range(len(data)):
					for x in range(len(data[y])):
						if x == 6:
							step22[y].append(list(data[y][x]))

						else:
							step22[y].append(data[y][x])

				# ////////////////////////////////////////////
				# ORGANIZAR OS DADOS DE SELECT
				for i in range(len(select)):
					step23.append([])

				# CONVERTER TUPLA PARA LISTA [()] - > [[]]
				for y in range(len(select)):
					for x in range(len(select[y])):
						if x == 6:
							step23[y].append(list(select[y][x]))

						else:
							step23[y].append(select[y][x])

				def list_diff(a, b):
					return [x for x in a if x not in b]

				data_diff = list_diff(step22, step23)

				# COLOCAR ESTUDADO EM TODOS OS ITEMS DA LISTA SELECT
				for x in range(len(step23)):
					if step23[x][-1][2] == '[color=#{}]Não Estudado[/color]'.format(color_hex):
						pass

					else:
						step23[x][-1][0] = 'alert-circle'
						step23[x][-1][1] = [1,0,0, 1]
						step23[x][-1][2] = '[color=#{}]Não Estudado[/color]'.format(color_hex)


				if len(data_diff) == 0:
					data_diff = step23

				elif len(data_diff) != 0:
					for item in range(len(step23)):
						data_diff.append(step23[item])

				# CONVERTER PARA TUPLA TODOS OS DADOS DE DATA_DIFF
				for x in range(len(data_diff)):
					data_diff[x][-1] = tuple(data_diff[x][-1])
					data_diff[x] = tuple(data_diff[x])

				return data_diff

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

			options = list(root.ids.cronogramaAllItems.children[-1].get_row_checks())
			data_cronograma = colorData(organizerData(sortData(data_cronograma)))
			estudadoList = rebuildDataStyle(options)
			data_Estudado = NaoEstudado(data_cronograma, estudadoList)

			# CRIAR O PADRÃO DE ESTILO NA LISTA
			def defaultStyle(lista):
				step14 = []
				for i in range(len(lista)):
					step14.append([])

				# CONVERTER TUPLA PARA LISTA [()] - > [[]]
				for y in range(len(step14)):
					for x in range(len(lista[y])):
						if x < 6:
							step14[y].append(lista[y][x])

						if x == 6:
							step14[y].append(list(lista[y][x]))

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
							step14[x][0][15:25][-4:] + '-' + step14[x][0][15:25][-7:-5] + '-' + step14[x][0][15:25][-10:-8])

						# DEFAULT PARA O TEMPO
						step14[x][1] = str(step14[x][1][15:17] + ':' + step14[x][1][18:20] + ':00')

						# DEFAULT PARA CATEGORIA
						for y in range(2, 5):
							step14[x][y] = RegEx(step14[x][y])

						# DEFAULT PARA A DURAÇÃO
						step14[x][5] = str(step14[x][5][15:17] + ':' + step14[x][5][18:20] + ':00')

						# DEFAULT STATUS ESTUDADO - NÃO ESTUDADO
						try:
							if step14[x][6][2][15:27] == 'Não Estudado':
								step14[x][6][2] = 'Não Estudado'

							if step14[x][6][2][15:23] == 'Estudado':
								step14[x][6][2] = 'Estudado'
						except IndexError:
							pass

				#step14 = step14[:-2]

				for x in range(len(step14)):
					step14[x][-1] = tuple(step14[x][-1])
					step14[x] = tuple(step14[x])

				return step14

			data_cronograma = defaultStyle(data_Estudado)
			pickle.dump(data_cronograma, open("data_timeline.p", "wb"))

			self.ids.cronogramaAllItems.children[0].DoubleClickRefreshChecks()


			def refreshScreen(dt):
				root.manager.current = 'Cronograma'

			Clock.schedule_once(refreshScreen, 0.2)

	def change_align(self, **kwargs):
		# ICON POSITION UPDATE
		self.ids.toggle_button_icon.size_hint = (0.4, 50)
		self.ids.user_button_icon.size_hint = (0.4, 50)
		self.ids.cronograma_button_icon.size_hint = (0.4, 50)
		self.ids.rendimento_button_icon.size_hint = (0.4, 50)
		self.ids.simulados_button_icon.size_hint = (0.4, 50)
		self.ids.stats_button_icon.size_hint = (0.4, 50)
		self.ids.timer_button_icon.size_hint = (0.4, 50)
		self.ids.help_button_icon.size_hint = (0.4, 50)
		self.ids.settings_button_icon.size_hint = (0.4, 50)

		# LABELS UPDATE
		self.ids.toggle_button_label.text = "[b]Essentials Study[/b]"
		self.ids.user_button_label.text = "[b]Seu Perfil[/b]"
		self.ids.cronograma_button_label.text = "[b]Seu Cronograma[/b]"
		self.ids.rendimento_button_label.text = "[b]Seu Rendimento[/b]"
		self.ids.simulados_button_label.text = "[b]Seus Simulados[/b]"
		self.ids.stats_button_label.text = "[b]Suas Estatísticas[/b]"
		self.ids.timer_button_label.text = "[b]Seu Temporizador[/b]"
		self.ids.help_button_label.text = "[b]Ajuda/Dúvidas[/b]"
		self.ids.settings_button_label.text = "[b]Suas Configurações[/b]"

	def refresh_align(self, **kwargs):
		# ICON POSITION RESET
		self.ids.toggle_button_icon.size_hint = (1000, 1)
		self.ids.user_button_icon.size_hint = (1000, 1)
		self.ids.cronograma_button_icon.size_hint = (1000, 1)
		self.ids.rendimento_button_icon.size_hint = (1000, 1)
		self.ids.simulados_button_icon.size_hint = (1000, 1)
		self.ids.stats_button_icon.size_hint = (1000, 1)
		self.ids.timer_button_icon.size_hint = (1000, 1)
		self.ids.help_button_icon.size_hint = (1000, 1)
		self.ids.settings_button_icon.size_hint = (1000, 1)

		# LABELS RESET
		self.ids.toggle_button_label.text = ""
		self.ids.user_button_label.text = ""
		self.ids.cronograma_button_label.text = ""
		self.ids.rendimento_button_label.text = ""
		self.ids.simulados_button_label.text = ""
		self.ids.stats_button_label.text = ""
		self.ids.timer_button_label.text = ""
		self.ids.help_button_label.text = ""
		self.ids.settings_button_label.text = ""

	def change_width(self, **kwargs):
		self.value = 250

	def refresh_width(self, **kwargs):
		self.value = 50

	def on_enter(self, *args):
		self.ids.search_bar_name.text = ''
		data_cronograma = pickle.load((open("data_timeline.p", "rb")))

		def AutoSizeTableRowsNum(lista):
			if len(lista) == 0:
				return createEmptyRowRemoveCronograma(createEmptyRowRemoveCronograma(colorData(organizerData(sortData(lista)))))

			if len(lista) == 1:
				return createEmptyRowRemoveCronograma(colorData(organizerData(sortData(lista))))

			if len(lista) > 1:
				return colorData(organizerData(sortData(lista)))

		data_tables2 = MDDataTable(
			background_color = get_color_from_hex("#eef2fe"),
			background_color_header=get_color_from_hex("#eef2fe"),
			background_color_selected_cell = get_color_from_hex("#f2f5fc"),
			background_color_cell = (0.9333, 0.9490, 0.9960,1),
			size_hint=(1, 1),
			elevation=0,
			check=True,
			use_pagination=True,
			rows_num = 10,
			column_data=[("[color=#686fa3]Data[/color]", dp(35)), ("[color=#686fa3]Horário[/color]", dp(35)), ("[color=#686fa3]Categoria[/color]", dp(35)), ("[color=#686fa3]Matéria[/color]", dp(35)),
						 ("[color=#686fa3]Tópico[/color]", dp(35)),("[color=#686fa3]Duração[/color]", dp(35)), ("[color=#686fa3]Status[/color]", dp(35))],
			row_data= AutoSizeTableRowsNum(data_cronograma)
		)


		def adicionarTabela(dt):
			self.ids.cronogramaAllItems.add_widget(data_tables2)
		def removerSpin(dt):
			self.ids.cronogramaAllItems.remove_widget(self.ids.cronogramaAllItems.children[-1])

		def refreshChecks(dt):
			try:
				self.ids.cronogramaAllItems.children[0].DoubleClickRefreshChecks()

			except IndexError:
				pass


		Clock.schedule_once(adicionarTabela, 2)
		Clock.schedule_once(removerSpin, 2)
		Clock.schedule_once(refreshChecks, 2.05)


	def on_leave(self, *args):
		self.ids.cronogramaAllItems.clear_widgets()

	def on_pre_enter(self, *args):
		spin = MDSpinner(size_hint=(0.2, 0.2),
						 pos_hint={'center_x': 0.5, 'center_y': 0.5},
						 active=True,
						 line_width=dp(12),
						 color=[0.8980, 0.9216, 0.9843, 1])

		self.ids.cronogramaAllItems.add_widget(spin)

class Rendimento(Screen):
	pass



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
	#cor_principal_icone_fundo = StringProperty('c7cfea')
	cor_fundo_area_de_trabalho = StringProperty('e6ebfb')
	cor_widgets_default = StringProperty('eef2fe')
	cor_widgets_hover = StringProperty('f4f7fe')

	cor_principal_icone_fundo = StringProperty('686fa3')

	cor_principal_texto_perfil = StringProperty('b7c1e0')
	cor_principal_icone_perfil = StringProperty('b7c1e0')

	cor_principal_texto_cronograma = StringProperty('b7c1e0')
	cor_principal_icone_cronograma = StringProperty('b7c1e0')

	cor_principal_texto_exercicios = StringProperty('b7c1e0')
	cor_principal_icone_exercicios = StringProperty('b7c1e0')

	cor_principal_texto_simulados = StringProperty('b7c1e0')
	cor_principal_icone_simulados = StringProperty('b7c1e0')

	cor_principal_texto_stats = StringProperty('b7c1e0')
	cor_principal_icone_stats = StringProperty('b7c1e0')

	cor_principal_texto_timer = StringProperty('b7c1e0')
	cor_principal_icone_timer = StringProperty('b7c1e0')

	cor_principal_texto_help = StringProperty('b7c1e0')
	cor_principal_icone_help = StringProperty('b7c1e0')

	cor_principal_texto_settings = StringProperty('b7c1e0')
	cor_principal_icone_settings = StringProperty('b7c1e0')

	cor_principal_texto_deslogar = StringProperty('b7c1e0')
	cor_principal_icone_deslogar = StringProperty('b7c1e0')







	def build(self):
		return Builder.load_file('grid.kv')



if __name__ == '__main__':
	#Window.size = (1280,720)
	#Window.fullscreen = True
	Window.maximize()
	grid().run()


