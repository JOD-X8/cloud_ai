import os
import json

from groq import Groq

from tools import (
    open_browser,
    browser_open,
    browser_search,
    browser_play,
    calculate,
    get_time
)


# ==========================================
# GROQ
# ==========================================

client = Groq(
    api_key=os.environ["GROQ_API_KEY"]
)


# ==========================================
# TOOL FUNCTIONS
# ==========================================

tool_functions = {
    "open_browser": open_browser,
    "browser_open": browser_open,
    "browser_search": browser_search,
    "browser_play": browser_play,
    "calculate": calculate,
    "get_time": get_time
}


# ==========================================
# TOOL DEFINITIONS FOR THE LLM
# ==========================================

tools = [

    # --------------------------------------
    # OPEN BROWSER
    # --------------------------------------

    {
        "type": "function",
        "function": {
            "name": "open_browser",
            "description": "Open a URL in an installed browser.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The complete URL to open."
                    },
                    "browser": {
                        "type": "string",
                        "enum": ["chrome", "edge", "brave"],
                        "description": (
                            "Browser to use. Omit to automatically "
                            "select an installed browser."
                        )
                    }
                },
                "required": ["url"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "browser_open",
            "description": "Open a URL using the controlled Chrome browser session.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to open."
                    }
                },
                "required": ["url"]
            }
        }
    },

    # --------------------------------------
    # BROWSER SEARCH
    # --------------------------------------

    {
        "type": "function",
        "function": {
            "name": "browser_search",
            "description": (
                "Search YouTube for a query using the "
                "controlled Chrome browser."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "What to search for on YouTube."
                        )
                    }
                },
                "required": ["query"]
            }
        }
    },

    # --------------------------------------
    # BROWSER PLAY
    # --------------------------------------

    {
        "type": "function",
        "function": {
            "name": "browser_play",
            "description": (
                "Play the currently open YouTube video "
                "in the controlled Chrome browser."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    # --------------------------------------
    # CALCULATOR
    # --------------------------------------

    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": (
                            "Arithmetic expression such as "
                            "25 * 16 or (100 + 50) / 3."
                        )
                    }
                },
                "required": ["expression"]
            }
        }
    },

    # --------------------------------------
    # TIME
    # --------------------------------------

    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Get the current time for a timezone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": (
                            "IANA timezone such as Asia/Kolkata "
                            "or America/New_York."
                        )
                    }
                },
                "required": []
            }
        }
    }

    

    

]


# ==========================================
# SYSTEM PROMPT
# ==========================================

SYSTEM_PROMPT = """
You are Jarvis, an elite and helpful AI assistant.

You are running the model openai/gpt-oss-20b through Groq.

Always respond in English unless the user explicitly asks
you to use another language.

Do not claim to be GPT-4, GPT-5, ChatGPT, or another model.

Do not invent technical specifications about yourself.

Use tools when they are appropriate.

Only say that you performed an action after the tool
has actually returned a successful result.

For browsers:
- If the user explicitly says Chrome, use Chrome.
- If the user explicitly says Edge, use Edge.
- If the user explicitly says Brave, use Brave.
- If the user simply says browser, use open_browser without
  specifying a browser so Python can detect one.

For casual conversation:
- Respond naturally and conversationally.
- Keep simple questions concise.
- Do not unnecessarily explain internal tools, tool calls,
  Python functions, APIs, or implementation details.
- Only explain how a tool works when the user explicitly asks
  about the tool or implementation.
"""


# ==========================================
# CONVERSATION HISTORY
# ==========================================

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


# Maximum number of user/assistant exchanges we remember.
# Tool messages are kept with their related exchange.

MAX_HISTORY = 10


def trim_history():

    global messages

    system_message = messages[0]
    conversation = messages[1:]

    # Find every user message.
    user_indices = [
        index
        for index, message in enumerate(conversation)
        if message.get("role") == "user"
    ]

    # Nothing to trim yet.
    if len(user_indices) <= MAX_HISTORY:
        return

    # Keep only the latest MAX_HISTORY user turns.
    start_index = user_indices[-MAX_HISTORY]

    conversation = conversation[start_index:]

    messages = [
        system_message
    ] + conversation


# ==========================================
# TOKEN TRACKING
# ==========================================

session_input_tokens = 0
session_output_tokens = 0
session_total_tokens = 0


def show_tokens(usage):

    global session_input_tokens
    global session_output_tokens
    global session_total_tokens

    if usage:

        session_input_tokens += usage.prompt_tokens
        session_output_tokens += usage.completion_tokens
        session_total_tokens += usage.total_tokens

        print(
            f"[TOKENS] "
            f"Request: {usage.total_tokens} | "
            f"Session: {session_total_tokens}"
        )


# ==========================================
# JARVIS
# ==========================================

print(
    "\n⚡ Jarvis is online. "
    "Type 'exit' to quit.\n"
)


while True:

    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        break


    # --------------------------------------
    # Add user message
    # --------------------------------------

    messages.append({
        "role": "user",
        "content": user_input
    })


    # --------------------------------------
    # Prevent unlimited history
    # --------------------------------------

    trim_history()


    try:

        # Maximum number of tool rounds
        # for a single user request.
        tool_rounds = 0


        # ==================================
        # AGENT LOOP
        # ==================================

        while True:

            # ==================================
            # LLM CALL
            # ==================================

            completion = client.chat.completions.create(

                model="openai/gpt-oss-20b",

                messages=messages,

                tools=tools,

                tool_choice="auto",

                parallel_tool_calls=False,

                temperature=0.5,

                reasoning_effort="low",

                max_completion_tokens=2048
            )


            show_tokens(completion.usage)


            assistant_message = (
                completion.choices[0].message
            )


            # ==================================
            # NORMAL RESPONSE
            # ==================================

            if not assistant_message.tool_calls:

                response = assistant_message.content

                print(
                    f"\nJarvis: {response}\n"
                )

                messages.append({
                    "role": "assistant",
                    "content": response
                })

                break


            # ==================================
            # TOOL CALL
            # ==================================

            tool_rounds += 1

            if tool_rounds > 5:

                print(
                    "\n[AGENT] Maximum tool rounds reached.\n"
                )

                break


            # --------------------------------------
            # IMPORTANT:
            # Groq returns ChatCompletionMessage,
            # not a normal dict.
            #
            # Convert it before putting it into
            # our messages list.
            # --------------------------------------

            messages.append(
                assistant_message.model_dump(
                    exclude_none=True
                )
            )


            # --------------------------------------
            # Execute requested tools
            # --------------------------------------

            for tool_call in assistant_message.tool_calls:

                tool_name = tool_call.function.name

                print(
                    f"\n[LLM] Requested tool: {tool_name}"
                )


                # ----------------------------------
                # Parse arguments
                # ----------------------------------

                try:

                    arguments = json.loads(
                        tool_call.function.arguments
                    )

                except json.JSONDecodeError:

                    arguments = {}

                    print(
                        "[TOOL] Invalid JSON arguments."
                    )


                print(
                    f"[TOOL] Arguments: {arguments}"
                )


                # ----------------------------------
                # Find Python function
                # ----------------------------------

                function = tool_functions.get(
                    tool_name
                )


                if function is None:

                    result = (
                        f"Tool '{tool_name}' does not exist."
                    )

                else:

                    try:

                        result = function(
                            **arguments
                        )

                    except Exception as e:

                        result = (
                            f"Tool failed: {str(e)}"
                        )


                # Make sure tool result is a string.
                result = str(result)


                print(
                    f"[TOOL] Result: {result}"
                )


                # ==================================
                # SEND TOOL RESULT TO LLM
                # ==================================

                messages.append({

                    "role": "tool",

                    "tool_call_id": tool_call.id,

                    "content": result

                })


            # --------------------------------------
            # The loop now runs another LLM call.
            #
            # The model can either:
            #
            # 1. Give a final answer
            # 2. Request another tool
            #
            # --------------------------------------


    except Exception as e:

        print(
            f"\n[ERROR] {e}\n"
        )


# ==========================================
# SESSION TOTAL
# ==========================================

print("\n==============================")
print("      JARVIS SESSION STATS")
print("==============================")
print(f"Input tokens : {session_input_tokens}")
print(f"Output tokens: {session_output_tokens}")
print(f"Total tokens : {session_total_tokens}")
print("==============================\n")