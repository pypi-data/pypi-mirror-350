from typing import List, Optional, Type

from aiogram_dialog import Dialog, Window
from aiogram_dialog.dialog import OnDialogEvent, OnResultEvent
from aiogram_dialog.widgets.kbd import (
	Back,
	Cancel,
	Row, Button,
)
from aiogram_dialog.widgets.text import Const

from aiogram_dialog_survey.handler import WindowHandler
from aiogram_dialog_survey.interface import IWindowHandler, QuestionDict
from aiogram_dialog_survey.state import StateGroupManager
from aiogram_dialog_survey.widgets import WidgetManager
from aiogram_dialog_survey.window import WrapperWindows


class SurveyFactory(WrapperWindows, StateGroupManager, WidgetManager):
	# TODO: Нужно предусмотреть возможность суб анкет. То есть может появиться ветвление, которое ведет в суб анкету
	def __init__(self, name: str, questions: list[QuestionDict], handler: Type[IWindowHandler] = WindowHandler, is_subdialog: bool = True ):
		super().__init__(name=name, questions=questions, use_wrapper=not is_subdialog)
		self.is_subdialog = is_subdialog
		self._handler = handler
		self.questions = questions
	
	def _get_static_buttons(self, order: int) -> list[Button]:
		buttons = [Cancel(Const("Отменить заполнение"))]
		if self.is_subdialog and order == 0:
			buttons.append(Cancel(Const("Назад")))
		else:
			buttons.append(Back(Const("Назад")))
		
		return buttons
	
	def _create_windows(self) -> List[Window]:
		windows = list()
		questionnaire_length = len(self.questions)
		
		for order, question in enumerate(self.questions):
			handler = self._handler(question_name=question["name"])
			sequence_question_label = Const("") if self.is_subdialog else Const(f"Вопрос {order + 1}/{questionnaire_length}")
			widget = self.get_widget(question["question_type"])
			static_buttons = self._get_static_buttons(order)
			
			window = Window(
				sequence_question_label,
				Const(f"{question['text']}"),
				widget(question, handler).create(),
				Row(
					*static_buttons
				),
				self.get_skip_button(question, handler),
				state=getattr(self._state_group, question["name"]),
			)
			
			windows.append(window)

		return windows
	
	def to_dialog(
		self,
		on_start: Optional[OnDialogEvent] = None,
		on_close: Optional[OnDialogEvent] = None,
		on_process_result: Optional[OnResultEvent] = None,
	) -> Dialog:
		if self.is_subdialog:
			windows = self._create_windows()
		else:
			windows = self.wrap_windows(self._create_windows(), self._state_group)
			
		return Dialog(
			*windows,
			on_start=on_start,
			on_close=on_close,
			on_process_result=on_process_result,
		)