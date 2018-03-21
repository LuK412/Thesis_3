from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Welcome(Page):
	pass


class Instructions1(Page):
	pass


class Instructions2(Page):
	pass


class Control_1(Page):
	form_model = "player"
	form_fields = ["question_1", "question_2", "question_3", "question_4", "question_5"]


class Control_2(Page):
	form_model = "player"
	form_fields = ["question_1", "question_2", "question_3", "question_4", "question_5"]

	def error_message(self, values):
		if values["question_1"] == 0 or values["question_2"] == 1 or values["question_3"] == 0 or values["question_4"] == 1 or values["question_5"] == 0:
			return "Bitte korrigieren Sie falsch beantwortete Fragen."


class CategoryPick(Page):
	form_model = "player"
	form_fields = ["category"]


class CategoryWaitPage(WaitPage):
	wait_for_all_groups = True

	def after_all_players_arrive(self):
		self.subsession.set_groups()
		# weil wait_for_all_groups gesetzt ist, wird die Funktion nur einmal aufgerufen,
		# folglich muss ich dann noch eine Ebene über die Gruppe hinaus auf die Subsession
		# in der aufgerufenen Funktion auf der Subsession-Ebene wird dann durch alle Gruppen gegangen
		# und da dann jeweils durch jeden Spieler um die Category zu kommunizieren.
		self.subsession.communicate_categories()


class Agent(Page):
	form_model = "player"
	form_fields = ["decision_for_principal"]


class WaitPage1(WaitPage):
	def after_all_players_arrive(self):
		self.group.after_investments()


class Results_Principals(Page):	
	def is_displayed(self):
		return self.player.role() == "Principal"

	form_model = "player"
	form_fields = ["message"]


class WaitForPrincipals(WaitPage):
	def after_all_players_arrive(self):
		self.group.after_results_principals()


class Results_Agents(Page):
	def is_displayed(self):
		return self.player.role() == "Agent"


class Questionnaire(Page):
	form_model = "player"
	form_fields = ["age", "gender", "studies", "nonstudent", "financial_advice", "income"]

	# This works now, but is not in compliance with the oTree manual.. I guess we found a bug.
	# returns an error message if a participant...
	def error_message(self, values):
		# ... indicates field of studies and ticks the box "non-student".
		if values["studies"]:
			if values["nonstudent"]:
				return "Bitte geben Sie entweder ein Studienfach an oder wählen Sie \"Kein Student\""
		# ... states no field of studies and and does not tick the box.
		else:
		#elif "studies" not in values:
			if not values["nonstudent"]:
				return "Sie haben kein Studienfach angegeben. Wenn Sie kein Student sind, treffen Sie bitte eine entsprechende Auswahl."

class Last_Page(Page):
	pass



page_sequence = [
# 	Welcome,
#	Instructions1,
# 	Instructions2,
	Control_1,
	Control_2,
	CategoryPick,
	CategoryWaitPage,
	Agent,
	WaitPage1,
	Results_Principals,
	WaitForPrincipals,
	Results_Agents,
	Questionnaire,
	Last_Page
]
