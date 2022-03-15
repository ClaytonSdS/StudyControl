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



from kivymd.uix.pickers import MDTimePicker, MDDatePicker
from kivymd.uix.spinner import MDSpinner
from kivy.clock import Clock

from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.gridlayout import MDGridLayout

from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView

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

def changeStatusColor(lista_tuple, color_percent=[1,0,0,1], color_hex='686fa3'):
    step5 = []
    for i in range(len(lista_tuple)):
        step5.append([])

    # CONVERTER TUPLA PARA LISTA [()] - > [[]]
    for y in range(len(step5)):
      step5[y].append(lista_tuple[y])

    step5[1][0] = color_percent
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

	# TIRAR A COLUNA DE DURAÇÃO
	for x in range(len(step7)):
		step7[x].remove(step7[x][-2])

	# CONVERTER PARA TUPLAR [[]] -> [()]
	for j in range(len(step7)):
		step7[j] = tuple(step7[j])

	return step7


def DataGreaterThanToday(lista):
  from datetime import date
  today = str(date.today())

  def changeData (label):
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

    if step8[h][0][15:25] >= today:
      step9.append(step8[h])

    if str(step8[h][0][15:25]) < today:
      pass

  # CONVERTER PARA TUPLAR [[]] -> [()]
  for j in range(len(step9)):
    step9[j] = tuple(step9[j])

  return step9


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

	class cronogramaFundo (MDBoxLayout):
		def __init__(self, **kwargs):
			self.data_cronograma = pickle.load((open("data_timeline.p", "rb")))
			super().__init__(**kwargs)
			data_tables = MDDataTable(
				size_hint=(0.9, 0.6),
				use_pagination=True,
				column_data=[
					("No.", dp(30)),
					("Column 1", dp(30)),
					("Column 2", dp(30)),
					("Column 3", dp(30)),
					("Column 4", dp(30)),
					("Column 5", dp(30)),
				],
				row_data=[
					(f"{i + 1}", "1", "2", "3", "4", "5") for i in range(50)
				],
			)
			self.add_widget(data_tables)



	class cronogramaDataTable(MDDataTable):
		def __init__(self, **kwargs):
			self.data_cronograma = pickle.load((open("data_timeline.p", "rb")))
			super().__init__(**kwargs)
			self.column_data = [("Data"), ("Horário"), ("Categoria"), ("Matéria"), ("Tópico"), ("Duração"), ("Status")]
			self.row_data = self.data_cronograma
			#self.size_hint = (0.9, 0.6)

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
		data_cronograma = pickle.load((open("data_timeline.p", "rb")))



		data_tables = MDDataTable(
			background_color = get_color_from_hex("#eef2fe"),
			background_color_header=get_color_from_hex("#eef2fe"),
			background_color_selected_cell = get_color_from_hex("#f2f5fc"),
			background_color_cell = (0.9333, 0.9490, 0.9960,1),
			size_hint=(1, 1),
			use_pagination=True,
			column_data=[("[color=#686fa3]Data[/color]", dp(35)), ("[color=#686fa3]Horário[/color]", dp(35)), ("[color=#686fa3]Categoria[/color]", dp(35)), ("[color=#686fa3]Matéria[/color]", dp(35)),
						 ("[color=#686fa3]Tópico[/color]", dp(35)), ("[color=#686fa3]Status[/color]", dp(35))],
			row_data= createEmptyRow(DataGreaterThanToday(CronogramaTableStyle(colorData(organizerData(sortData(data_cronograma))))))
		)


		spin = MDSpinner(size_hint= (0.2, 0.2),
						 pos_hint= {'center_x': 0.5, 'center_y': 0.5},
						 active= True,
						 line_width = dp(12),
						 color = [0.8980,0.9216,0.9843,1])


		self.ids.cronograma22.add_widget(data_tables)

		# CronogramaTableStyle(createEmptyRow(colorData(organizerData(sortData(data_cronograma)))))


	def on_leave(self, *args):
		self.ids.cronograma22.clear_widgets()



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
		date_dialog = MDDatePicker()
		date_dialog.bind(on_save=self.on_saveData, on_cancel=self.on_cancel)


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

		date_dialog.open()

	def show_time_picker(self):
		'''Open time picker dialog.'''

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
				print(self.saveData[0])
				print(self.saveTime[0])
				print(duration)

				self.data_cronograma = pickle.load((open("data_timeline.p", "rb")))

				self.data_cronograma.append((str(self.saveData[0]), str(self.saveTime[0]), root.ids.spinnerCategorias.text,
											 root.ids.spinnerAllMaterias.text, root.ids.spinnerTopicos.text, duration, ("alert-circle", [1, 0, 0, 1], "Não Estudado")))

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
	def build(self):
		return Builder.load_file('grid.kv')



if __name__ == '__main__':
	#Window.size = (1024, 768)
	#Window.fullscreen = True
	Window.maximize()
	grid().run()


