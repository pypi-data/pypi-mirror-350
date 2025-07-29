# Change log

## 0.5.0
* Add our own custom `litellm` practice with custom endpoint (`openai` standard)

## 0.4.1
* Add `streamlit` support
* Now you can use `ai_cap_utils.streamlit.run_streamlit_chat_ui` function and run `streamlit run ...` command to run chat UI

## 0.4.0
* Add support for passing google credentials as a dict or JSON format
* Add rebuild graph capability in the `BaseAgent`
* Add shared memory capability for multi agents
* Refactor credentials handling in agents classes
* Refactor agent base code, expose only the necessary interfaces
* Change parameters name

## 0.3.0
* Change to `ai-cap-utils`

## 0.2.1
* Update to `do-cap-utils`

## 0.2.0
* Make system prompt mandatory for `BaseAgent`
* Add `agent_name`, if not provided, generate a random one
* Add `BaseChatInterface` that supplies the base methods, i.t., `chat_interact()`, `run_batch` and `chat_each_message()`
* Add multiple agents support
* Use `BaseMultiAgentLLMRouter` class to route different intents to different agents (**not yet support shared memory**)

## 0.1.0
* First dev version
* Provide `BaseAgent`