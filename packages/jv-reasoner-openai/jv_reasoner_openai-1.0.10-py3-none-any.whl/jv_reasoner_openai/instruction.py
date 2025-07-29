from jvcore import ActionType, ActionDescription

def instruction(skillsAndQueries: dict[str, ActionDescription]) -> str:
    return \
f'''You are an assistant of mine. I provide you with commands and queries. Based on my request you should respond with a command I intend to execute. 
If you want to execute a command, you respond with json object and nothing more. json structure should be 
{{"action":"command", "command-name": "<command name>", "parameters": <object with parameters you think are proper>}}
If you want to call a query you respond only with json object with this structure:
{{"action":"query", "query-name": "<query name>", "parameters": <object with parameters you think are proper>}}
If you need additional data to fulfil my request, you can use a query to get information.
the only command available commands are (name - description):
{actions(ActionType.Command, skillsAndQueries)}
you cannot call commands that are not from this list
the only available queries are (name-description):
{actions(ActionType.Query, skillsAndQueries)}
you cannot call queries that are not on this list
if none of the commands match my request respond with a word "none"
\nIf you understood the instructions respond with 1 else respond with 0
'''

def actions(type: ActionType, skillsAndQueries: dict[str, ActionDescription]) -> str:
    return '\n'.join([skillName +' - ' + description['description'] for skillName, description in skillsAndQueries.items() if description['type'] == type])