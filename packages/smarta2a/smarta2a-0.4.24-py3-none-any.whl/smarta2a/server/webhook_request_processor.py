# Library imports
from typing import Callable, Any, Optional
import copy
from uuid import uuid4

# Local imports
from smarta2a.server.state_manager import StateManager
from smarta2a.utils.types import WebhookRequest, WebhookResponse, StateData, Message, TaskState
from smarta2a.utils.task_builder import TaskBuilder
from smarta2a.client.a2a_client import A2AClient

class WebhookRequestProcessor:
    def __init__(self, webhook_fn: Callable[[WebhookRequest], Any], state_manager: Optional[StateManager] = None):
        self.webhook_fn = webhook_fn
        self.state_manager = state_manager
        self.task_builder = TaskBuilder(default_status=TaskState.COMPLETED)
        self.a2a_aclient = A2AClient()

    async def process_request(self, request: WebhookRequest) -> WebhookResponse:
        if self.state_manager:
            state_data = await self.state_manager.get_and_update_state_from_webhook(request.id, request.result)
            return await self._webhook_handler(request, state_data)
        else:
            return await self._webhook_handler(request)
    

    async def _webhook_handler(self, request: WebhookRequest, state_data: Optional[StateData] = None) -> WebhookResponse:
        print("--- _webhook_handler ---")
        print(request)
        print("--- end of _webhook_handler ---")
        print("--- state_data ---")
        print(state_data)
        print("--- end of state_data ---")
        try:
            # Extract parameters from request
            task_id = request.id
            task = request.result

            if state_data:
                session_id = task.sessionId if task and task.sessionId else state_data.task.sessionId
                task_history = task.history if task and task.history is not None else state_data.task.history.copy() if state_data.task.history else []
                context_history = state_data.context_history.copy()
                metadata = task.metadata if task and task.metadata is not None else state_data.task.metadata.copy() if state_data.task.metadata else {}
                # Deep copy of push_notification_config
                push_notification_config = copy.deepcopy(state_data.push_notification_config) if state_data.push_notification_config else None
            else:
                # No state_data so just assign based on task from the request
                session_id = task.sessionId if task and task.sessionId else str(uuid4())
                task_history = task.history if task and task.history else []
                context_history = []
                metadata = task.metadata if task and task.metadata else {}
                push_notification_config = None
            
            # Call webhook handler
            if state_data:
                # Call webhook_fn with state_data
                raw_result = await self.webhook_fn(request, state_data)
            else:
                # Call webhook_fn with request
                raw_result = await self.webhook_fn(request)
            
            # Handle direct WebhookResponse returns
            if isinstance(raw_result, WebhookResponse):
                return raw_result
            
            # Process webhook_response in a way that is similar to handle_send_task
            # Build task with updated history
            updated_task = self.task_builder.build(
                content=raw_result,
                task_id=task_id,
                session_id=session_id,
                metadata=metadata,
                history=task_history
            )
            
            # Process messages through strategy (similar to handle_send_task)
            messages = []
            if updated_task.artifacts:
                agent_parts = [p for a in updated_task.artifacts for p in a.parts]
                agent_message = Message(
                    role="agent",
                    parts=agent_parts,
                    metadata=updated_task.metadata
                )
                messages.append(agent_message)
            
            # Update Task history with a simple append
            task_history.extend(messages)
            
            if state_data:
                # Update context history with a strategy
                history_strategy = self.state_manager.get_history_strategy()
                context_history = history_strategy.update_history(
                    existing_history=context_history,
                    new_messages=messages
                )
            
            # Update task with final state
            updated_task.history = task_history
            
            # State store update (if enabled)
            if state_data:
                await self.state_manager.update_state(
                    state_data=StateData(
                        task_id=task_id,
                        task=updated_task,
                        context_history=context_history,
                        push_notification_config=push_notification_config,
                    )
                )
            print("--- push_notification_config ---")
            print(push_notification_config)
            print("--- end of push_notification_config ---")
            # If push_notification_config is set send the task to the push notification url
            if push_notification_config:
                try:
                    await self.a2a_aclient.send_to_webhook(webhook_url=push_notification_config.url,id=task_id,task=updated_task.model_dump())
                except Exception as e:
                    pass
            
            # Return the updated task
            return WebhookResponse(
                id=request.id,
                result=updated_task
            )
            
        except Exception as e:
            # Handle exceptions
            return WebhookResponse(
                id=request.id,
                error=str(e)
            )