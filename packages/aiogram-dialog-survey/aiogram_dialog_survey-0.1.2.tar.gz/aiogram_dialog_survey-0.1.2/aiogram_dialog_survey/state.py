from typing import List, Type

from aiogram.fsm.state import State, StatesGroup

from aiogram_dialog_survey.interface import QuestionDict


class StateGroupFactory(StatesGroup):
	first_state_name = "start"
	last_state_name = "end"

	@classmethod
	def create_state_group(
			cls, group_name: str, state_names: List[str], use_wrapper: bool
	) -> Type[StatesGroup]:
		"""
		Динамически создает класс StatesGroup с заданными состояниями.

		:param group_name: Имя класса StatesGroup.
		:param state_names: Список имен состояний.
		:param use_wrapper: Использовать окна обертку.
		:return: Класс, унаследованный от StatesGroup.
		"""
		if use_wrapper:
			state_names.insert(0, cls.first_state_name)
			state_names.append(cls.last_state_name)

		# Создаем атрибуты класса (состояния) из списка строк
		attrs = {name: State() for name in state_names}

		# Создаем сам класс с помощью type()
		state_group = type(group_name, (StatesGroup,), attrs)

		return state_group  # type: ignore


class StateGroupManager(StateGroupFactory):
	def __init__(self, name: str, questions: list[QuestionDict], use_wrapper: bool):
		self._state_group = self.create_state_group(
			name.title(),
			[question["name"] for question in questions],
			use_wrapper=use_wrapper
		)

	def get_first_state(self) -> State:
		state_attributes = {
			name: value
			for name, value in vars(self._state_group).items()
			if isinstance(value, State)
		}
		first_state_name = next(iter(state_attributes))
		return state_attributes[first_state_name]
