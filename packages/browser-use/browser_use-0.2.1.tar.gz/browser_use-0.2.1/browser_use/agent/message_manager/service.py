from __future__ import annotations

import logging
import re
import textwrap

from langchain_core.messages import (
	AIMessage,
	BaseMessage,
	HumanMessage,
	SystemMessage,
	ToolMessage,
)
from pydantic import BaseModel

from browser_use.agent.message_manager.views import MessageMetadata
from browser_use.agent.prompts import AgentMessagePrompt
from browser_use.agent.views import ActionResult, AgentOutput, AgentStepInfo, MessageManagerState
from browser_use.browser.views import BrowserStateSummary
from browser_use.utils import time_execution_sync

logger = logging.getLogger(__name__)


class MessageManagerSettings(BaseModel):
	max_input_tokens: int = 128000
	estimated_characters_per_token: int = 3
	image_tokens: int = 800
	include_attributes: list[str] = []
	message_context: str | None = None
	# Support both old format {key: value} and new format {domain: {key: value}}
	sensitive_data: dict[str, str | dict[str, str]] | None = None
	available_file_paths: list[str] | None = None


class MessageManager:
	def __init__(
		self,
		task: str,
		system_message: SystemMessage,
		settings: MessageManagerSettings = MessageManagerSettings(),
		state: MessageManagerState = MessageManagerState(),
	):
		self.task = task
		self.settings = settings
		self.state = state
		self.system_prompt = system_message

		# Only initialize messages if state is empty
		if len(self.state.history.messages) == 0:
			self._init_messages()

	def _init_messages(self) -> None:
		"""Initialize the message history with system message, context, task, and other initial messages"""
		self._add_message_with_tokens(self.system_prompt, message_type='init')

		if self.settings.message_context:
			context_message = HumanMessage(content='Context for the task' + self.settings.message_context)
			self._add_message_with_tokens(context_message, message_type='init')

		task_message = HumanMessage(
			content=f'Your ultimate task is: """{self.task}""". If you achieved your ultimate task, stop everything and use the done action in the next step to complete the task. If not, continue as usual.'
		)
		self._add_message_with_tokens(task_message, message_type='init')

		if self.settings.sensitive_data:
			info = f'Here are placeholders for sensitive data: {list(self.settings.sensitive_data.keys())}'
			info += '\nTo use them, write <secret>the placeholder name</secret>'
			info_message = HumanMessage(content=info)
			self._add_message_with_tokens(info_message, message_type='init')

		placeholder_message = HumanMessage(content='Example output:')
		self._add_message_with_tokens(placeholder_message, message_type='init')

		example_tool_call = AIMessage(
			content='',
			tool_calls=[
				{
					'name': 'AgentOutput',
					'args': {
						'current_state': {
							'evaluation_previous_goal': """
							Success - I successfully clicked on the 'Apple' link from the Google Search results page, 
							which directed me to the 'Apple' company homepage. This is a good start toward finding 
							the best place to buy a new iPhone as the Apple website often list iPhones for sale.
						""".strip(),
							'memory': """
							I searched for 'iPhone retailers' on Google. From the Google Search results page, 
							I used the 'click_element_by_index' tool to click on element at index [45] labeled 'Best Buy' but calling 
							the tool did not direct me to a new page. I then used the 'click_element_by_index' tool to click 
							on element at index [82] labeled 'Apple' which redirected me to the 'Apple' company homepage. 
							Currently at step 3/15.
						""".strip(),
							'next_goal': """
							Looking at reported structure of the current page, I can see the item '[127]<h3 iPhone/>' 
							in the content. I think this button will lead to more information and potentially prices 
							for iPhones. I'll click on the link at index [127] using the 'click_element_by_index' 
							tool and hope to see prices on the next page.
						""".strip(),
						},
						'action': [{'click_element_by_index': {'index': 127}}],
					},
					'id': str(self.state.tool_id),
					'type': 'tool_call',
				},
			],
		)
		self._add_message_with_tokens(example_tool_call, message_type='init')
		self.add_tool_message(content='Browser started', message_type='init')

		placeholder_message = HumanMessage(content='[Your task history memory starts here]')
		self._add_message_with_tokens(placeholder_message)

		if self.settings.available_file_paths:
			filepaths_msg = HumanMessage(content=f'Here are file paths you can use: {self.settings.available_file_paths}')
			self._add_message_with_tokens(filepaths_msg, message_type='init')

	def add_new_task(self, new_task: str) -> None:
		content = f'Your new ultimate task is: """{new_task}""". Take the previous context into account and finish your new ultimate task. '
		msg = HumanMessage(content=content)
		self._add_message_with_tokens(msg)
		self.task = new_task

	@time_execution_sync('--add_state_message')
	def add_state_message(
		self,
		browser_state_summary: BrowserStateSummary,
		result: list[ActionResult] | None = None,
		step_info: AgentStepInfo | None = None,
		use_vision=True,
	) -> None:
		"""Add browser state as human message"""

		# if keep in memory, add to directly to history and add state without result
		if result:
			for r in result:
				if r.include_in_memory:
					if r.extracted_content:
						msg = HumanMessage(content='Action result: ' + str(r.extracted_content))
						self._add_message_with_tokens(msg)
					if r.error:
						# if endswith \n, remove it
						if r.error.endswith('\n'):
							r.error = r.error[:-1]
						# get only last line of error
						last_line = r.error.split('\n')[-1]
						msg = HumanMessage(content='Action error: ' + last_line)
						self._add_message_with_tokens(msg)
					result = None  # if result in history, we dont want to add it again

		# otherwise add state message and result to next message (which will not stay in memory)
		assert browser_state_summary
		state_message = AgentMessagePrompt(
			browser_state_summary=browser_state_summary,
			result=result,
			include_attributes=self.settings.include_attributes,
			step_info=step_info,
		).get_user_message(use_vision)
		self._add_message_with_tokens(state_message)

	def add_model_output(self, model_output: AgentOutput) -> None:
		"""Add model output as AI message"""
		tool_calls = [
			{
				'name': 'AgentOutput',
				'args': model_output.model_dump(mode='json', exclude_unset=True),
				'id': str(self.state.tool_id),
				'type': 'tool_call',
			}
		]

		msg = AIMessage(
			content='',
			tool_calls=tool_calls,
		)

		self._add_message_with_tokens(msg)
		# empty tool response
		self.add_tool_message(content='')

	def add_plan(self, plan: str | None, position: int | None = None) -> None:
		if plan:
			msg = AIMessage(content=plan)
			self._add_message_with_tokens(msg, position)

	def _get_message_emoji(self, message_type: str) -> str:
		"""Get emoji for a message type"""
		emoji_map = {
			'HumanMessage': '💬',
			'AIMessage': '🧠',
			'ToolMessage': '🔨',
		}
		return emoji_map.get(message_type, '🎮')

	def _clean_whitespace(self, text: str) -> str:
		"""Replace all repeated whitespace with single space and strip"""
		return re.sub(r'\s+', ' ', text).strip()

	def _truncate_text(self, text: str, max_length: int) -> str:
		"""Truncate text to max_length and add ellipsis if needed"""
		if len(text) <= max_length:
			return text
		return text[:max_length] + '...'

	def _extract_text_from_list_content(self, content: list) -> str:
		"""Extract text from list content structure"""
		text_content = ''
		for item in content:
			if isinstance(item, dict) and 'text' in item:
				text_content += item['text']
		return text_content

	def _format_agent_output_content(self, tool_call: dict) -> str:
		"""Format AgentOutput tool call into readable content"""
		args = tool_call.get('args', {})
		action_info = ''

		# Get action name
		if 'action' in args and args['action']:
			first_action = args['action'][0] if isinstance(args['action'], list) and args['action'] else args['action']
			if isinstance(first_action, dict):
				action_name = next(iter(first_action.keys())) if first_action else 'unknown'
				action_info = f'{action_name}()'

		# Get goal
		goal_info = ''
		if 'current_state' in args and isinstance(args['current_state'], dict):
			next_goal = args['current_state'].get('next_goal', '').strip()
			if next_goal:
				goal_info = f': {self._truncate_text(next_goal, 40)}'

		# Combine action and goal info
		if action_info and goal_info:
			return f'{action_info}{goal_info}'
		elif action_info:
			return action_info
		elif goal_info:
			return goal_info[2:]  # Remove ': ' prefix for goal-only
		else:
			return 'AgentOutput'

	def _generate_history_log(self) -> str:
		"""Generate a formatted log string of message history for debugging / printing to terminal"""
		total_input_tokens = 0
		message_lines = []

		for i, m in enumerate(self.state.history.messages):
			total_input_tokens += m.metadata.tokens
			is_last_message = i == len(self.state.history.messages) - 1

			# Get emoji based on message type
			message_type = m.message.__class__.__name__
			emoji = self._get_message_emoji(message_type)

			# Extract content based on message structure
			if is_last_message and message_type == 'HumanMessage' and isinstance(m.message.content, list):
				# Special handling for last message with list content
				text_content = self._extract_text_from_list_content(m.message.content)
				text_content = self._clean_whitespace(text_content)

				# Look for current state section
				if '[Current state starts here]' in text_content:
					start_idx = text_content.find('[Current state starts here]')
					content = self._truncate_text(text_content[start_idx:], 150)
				else:
					content = self._truncate_text(text_content, 150)
			else:
				# Standard content extraction
				content = self._clean_whitespace(str(m.message.content)[:80])

				# Shorten "Action result:" to "Result:" for display
				if content.startswith('Action result:'):
					content = 'Result:' + content[14:]

				# Handle AIMessages with tool calls
				if hasattr(m.message, 'tool_calls') and m.message.tool_calls and not content:
					tool_call = m.message.tool_calls[0]
					tool_name = tool_call.get('name', 'unknown')

					if tool_name == 'AgentOutput':
						content = self._format_agent_output_content(tool_call)
					else:
						content = f'[TOOL: {tool_name}]'
				elif len(str(m.message.content)) > 80:
					content += '...'

			# Format the message line
			left_part = f'          {emoji}[{m.metadata.tokens}]'

			# For last message, allow multiple lines if needed
			if is_last_message and '\n' not in content:
				wrapped = textwrap.wrap(content, width=80, subsequent_indent=' ' * 20)
				if len(wrapped) > 2:
					wrapped = wrapped[:2]
					wrapped[-1] = self._truncate_text(wrapped[-1], 77)
				message_lines.append(f'{left_part.ljust(16)}: {wrapped[0]}')
				message_lines.extend(wrapped[1:])
			else:
				message_lines.append(f'{left_part.ljust(16)}: {content}')

		# Build final log message
		return (
			f'📜 LLM Message history ({len(self.state.history.messages)} messages, {total_input_tokens} tokens):\n'
			+ '\n'.join(message_lines)
		)

	@time_execution_sync('--get_messages')
	def get_messages(self) -> list[BaseMessage]:
		"""Get current message list, potentially trimmed to max tokens"""
		msg = [m.message for m in self.state.history.messages]

		# Log message history for debugging
		logger.debug(self._generate_history_log())

		return msg

	def _add_message_with_tokens(
		self, message: BaseMessage, position: int | None = None, message_type: str | None = None
	) -> None:
		"""Add message with token count metadata
		position: None for last, -1 for second last, etc.
		"""

		# filter out sensitive data from the message
		if self.settings.sensitive_data:
			message = self._filter_sensitive_data(message)

		token_count = self._count_tokens(message)
		metadata = MessageMetadata(tokens=token_count, message_type=message_type)
		self.state.history.add_message(message, metadata, position)

	@time_execution_sync('--filter_sensitive_data')
	def _filter_sensitive_data(self, message: BaseMessage) -> BaseMessage:
		"""Filter out sensitive data from the message"""

		def replace_sensitive(value: str) -> str:
			if not self.settings.sensitive_data:
				return value

			# Collect all sensitive values, immediately converting old format to new format
			sensitive_values: dict[str, str] = {}

			# Process all sensitive data entries
			for key_or_domain, content in self.settings.sensitive_data.items():
				if isinstance(content, dict):
					# Already in new format: {domain: {key: value}}
					for key, val in content.items():
						if val:  # Skip empty values
							sensitive_values[key] = val
				elif content:  # Old format: {key: value} - convert to new format internally
					# We treat this as if it was {'http*://*': {key_or_domain: content}}
					sensitive_values[key_or_domain] = content

			# If there are no valid sensitive data entries, just return the original value
			if not sensitive_values:
				logger.warning('No valid entries found in sensitive_data dictionary')
				return value

			# Replace all valid sensitive data values with their placeholder tags
			for key, val in sensitive_values.items():
				value = value.replace(val, f'<secret>{key}</secret>')

			return value

		if isinstance(message.content, str):
			message.content = replace_sensitive(message.content)
		elif isinstance(message.content, list):
			for i, item in enumerate(message.content):
				if isinstance(item, dict) and 'text' in item:
					item['text'] = replace_sensitive(item['text'])
					message.content[i] = item
		return message

	def _count_tokens(self, message: BaseMessage) -> int:
		"""Count tokens in a message using the model's tokenizer"""
		tokens = 0
		if isinstance(message.content, list):
			for item in message.content:
				if 'image_url' in item:
					tokens += self.settings.image_tokens
				elif isinstance(item, dict) and 'text' in item:
					tokens += self._count_text_tokens(item['text'])
		else:
			msg = message.content
			if hasattr(message, 'tool_calls'):
				msg += str(message.tool_calls)  # type: ignore
			tokens += self._count_text_tokens(msg)
		return tokens

	def _count_text_tokens(self, text: str) -> int:
		"""Count tokens in a text string"""
		tokens = len(text) // self.settings.estimated_characters_per_token  # Rough estimate if no tokenizer available
		return tokens

	def cut_messages(self):
		"""Get current message list, potentially trimmed to max tokens"""
		diff = self.state.history.current_tokens - self.settings.max_input_tokens
		if diff <= 0:
			return None

		msg = self.state.history.messages[-1]

		# if list with image remove image
		if isinstance(msg.message.content, list):
			text = ''
			for item in msg.message.content:
				if 'image_url' in item:
					msg.message.content.remove(item)
					diff -= self.settings.image_tokens
					msg.metadata.tokens -= self.settings.image_tokens
					self.state.history.current_tokens -= self.settings.image_tokens
					logger.debug(
						f'Removed image with {self.settings.image_tokens} tokens - total tokens now: {self.state.history.current_tokens}/{self.settings.max_input_tokens}'
					)
				elif 'text' in item and isinstance(item, dict):
					text += item['text']
			msg.message.content = text
			self.state.history.messages[-1] = msg

		if diff <= 0:
			return None

		# if still over, remove text from state message proportionally to the number of tokens needed with buffer
		# Calculate the proportion of content to remove
		proportion_to_remove = diff / msg.metadata.tokens
		if proportion_to_remove > 0.99:
			raise ValueError(
				f'Max token limit reached - history is too long - reduce the system prompt or task. '
				f'proportion_to_remove: {proportion_to_remove}'
			)
		logger.debug(
			f'Removing {proportion_to_remove * 100:.2f}% of the last message  {proportion_to_remove * msg.metadata.tokens:.2f} / {msg.metadata.tokens:.2f} tokens)'
		)

		content = msg.message.content
		characters_to_remove = int(len(content) * proportion_to_remove)
		content = content[:-characters_to_remove]

		# remove tokens and old long message
		self.state.history.remove_last_state_message()

		# new message with updated content
		msg = HumanMessage(content=content)
		self._add_message_with_tokens(msg)

		last_msg = self.state.history.messages[-1]

		logger.debug(
			f'Added message with {last_msg.metadata.tokens} tokens - total tokens now: {self.state.history.current_tokens}/{self.settings.max_input_tokens} - total messages: {len(self.state.history.messages)}'
		)

	def _remove_last_state_message(self) -> None:
		"""Remove last state message from history"""
		self.state.history.remove_last_state_message()

	def add_tool_message(self, content: str, message_type: str | None = None) -> None:
		"""Add tool message to history"""
		msg = ToolMessage(content=content, tool_call_id=str(self.state.tool_id))
		self.state.tool_id += 1
		self._add_message_with_tokens(msg, message_type=message_type)
