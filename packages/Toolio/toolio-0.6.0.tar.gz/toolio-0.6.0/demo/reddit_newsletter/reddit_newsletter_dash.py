import os
import json
# import asyncio
import ssl

import aiohttp
import asyncpraw
import dash
import dash_core_components as dcc
import dash_html_components as html
from ogbujipt.llm_wrapper import openai_chat_api # , prompt_to_chat

# from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# from toolio.tool import tool
from toolio.llm_helper import model_manager
from toolio.common import response_text


# Need this crap to avoid self-signed cert errors (really annoying, BTW!)
ssl_ctx = ssl.create_default_context(cafile=os.environ.get('CERT_FILE'))

os.environ['TOKENIZERS_PARALLELISM'] = 'false'  # Shut up Tokenizers lib warning

# Need this crap to avoid self-signed cert errors (really annoying, BTW!)
ssl_ctx = ssl.create_default_context(cafile=os.environ.get('CERT_FILE'))

# Requires OPENAI_API_KEY in environment
llm_api = openai_chat_api(model='gpt-4o-mini')

MLX_MODEL_PATH = 'mlx-community/Mistral-Nemo-Instruct-2407-4bit'

USER_AGENT = 'Python:Arkestra Agent:v0.1.0 (by u/CodeGriot'

MAX_SUBREDDITS = 3

AGENT_1_SCHEMA = '''\
{
  "type": "object",
  "description": "Respond with a \\"question\\" response, or \\"ready\\" BUT NEVER BOTH.",
  "anyOf": [
    {"required" : ["question"]},
    {"required" : ["ready"]}
  ],
  "properties": {
    "question": {
      "description": "Initial or follow-up question to the user. DO NOT USE IF YOU ALSO USE ready.",
      "type": "string"
    },
    "ready": {
      "description": "Use this when you have a decent amount of info from the user. Contains a summarized bullet list of to user's desired topics, in a way that's easy to look up by tags in a public forum. DO NOT USE IF YOU ALSO USE question.",
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  }
}
''' #  noqa E501

AGENT_2_SCHEMA = '{"type": "array", "items": { "type": "string" } }'

AGENT_3_UPROMPT = '''\
Here is a list of the top ten hottest post titles in a selection of subreddits: 

=== BEGIN POST TITLES
{titles}
=== END POST TITLES

The source subreddits are: {subreddits}

Based on this, please provide a nicely-written newletter summary of the interesting topics of the day across these
forums. Try to make it more than just a random list of topics, and more a readable take on the latest points of intrest.
'''

toolio_mm = model_manager(MLX_MODEL_PATH)

# System prompt will be used to direct the LLM's tool-calling
agent_1_sysprompt = '''\
You are a newsletter ghost-writer who interviews a user asking for a topic of interest, with a couple
of follow-up questions to narrow down the discussion. The user will start the process by saying they want to
create a newsletter post. Your responses are always in JSON, either using the
`question` object key to ask the user an inital or follow-up question, or when you think you have
a reasonable amount of information, and after no more than a few turns, you will respond using
the `ready` object key, with a list of topics in a form that can be looked up as simple topic tags.
Here is the schema for you to use: {json_schema}
'''
userprompt_1 = 'Hi! I\'d like to create a newsletter post'

agent_2_sysprompt = '''\
You are a helpful assistant who specializes in finding online forums relevant
to a user's informational needs. You always respond with a simple list of forums
to check, relevant to a given list of topics.
'''

agent_2_uprompt = '''\
Given the following list of topics:

### BEGIN TOPICS
{topics}
### END TOPICS

Select which of the following subreddits might be useful for research.

### BEGIN SUBREDDITS
{subreddits}
### END SUBREDDITS

Respond using the following schema: {{json_schema}}
'''


with open('subreddits.json') as fp:
    AVAILABLE_SUBREDDITS = json.load(fp)

async def get_reddit_posts(subreddits):
    """
    Fetches hot posts from specified subreddits using asyncpraw
    
    Args:
        subreddits (list): List of subreddit names without the /r/ prefix
        
    Returns:
        list: List of submission objects from the subreddits
    """
    async with aiohttp.ClientSession() as session:
        reddit = asyncpraw.Reddit(
            client_id=os.environ.get('REDDIT_CLIENT_ID'),
            client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
            user_agent=USER_AGENT,
            requestor_kwargs={'session': session},
        )
        
        posts = []
        for subreddit in subreddits:
            subreddit_api = await reddit.subreddit(subreddit, fetch=True)
            async for submission in subreddit_api.hot(limit=20):
                if submission.stickied:  # Skip pinned posts
                    continue
                posts.append(submission)
                
        return posts

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Reddit Newsletter"),
    html.Div(id='available-subreddits-store', style={'display': 'none'}, 
             children=json.dumps(AVAILABLE_SUBREDDITS)),
    
    # Interview section
    html.Div([
        html.H2("Interview"),
        # Store for conversation history
        dcc.Store(id='conversation-history', data=[]),
        # Display previous QA turns
        html.Div(id='conversation-display'),
        # Current question and input
        html.Div(id='current-question'),
        dcc.Input(id='user-answer', type='text', style={'width': '100%', 'marginTop': '10px'}),
        html.Button('Submit Answer', id='submit-answer', n_clicks=0),
        # Start over button
        html.Button('Start Over', id='start-over', n_clicks=0),
    ], style={'marginBottom': '20px'}),
    
    # Newsletter output section
    html.Div(id='newsletter-output'),
    
    # Debug output
    html.Div(id='debug-output', style={'whiteSpace': 'pre-wrap', 'marginTop': '20px'})
])

@app.callback(
    [Output('conversation-history', 'data'),
     Output('current-question', 'children'),
     Output('conversation-display', 'children'),
     Output('user-answer', 'value')],
    [Input('submit-answer', 'n_clicks'),
     Input('start-over', 'n_clicks')],
    [State('conversation-history', 'data'),
     State('user-answer', 'value')],
    prevent_initial_call=True
)
async def handle_interview(submit_clicks, start_over_clicks, history, user_answer):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
        
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == 'start-over':
        # Reset everything and start fresh
        msgs = [
            {'role': 'system', 'content': agent_1_sysprompt},
            {'role': 'user', 'content': 'Hi! I\'d like to create a newsletter post'}
        ]
        resp = await response_text(toolio_mm.complete(msgs, json_schema=AGENT_1_SCHEMA, max_tokens=2048))
        resp_data = json.loads(resp)
        
        new_history = [{
            'question': 'Hi! I\'d like to create a newsletter post',
            'answer': resp_data.get('question', '')
        }]
        return new_history, resp_data.get('question', ''), None, ''
        
    elif trigger_id == 'submit-answer' and user_answer:
        # Continue conversation
        msgs = [
            {'role': 'system', 'content': agent_1_sysprompt}
        ]
        
        # Reconstruct conversation for context
        for turn in history:
            msgs.append({'role': 'user', 'content': turn['question']})
            msgs.append({'role': 'assistant', 'content': turn['answer']})
        
        # Add latest user answer
        msgs.append({'role': 'user', 'content': user_answer})
        
        # Get next question or ready signal
        resp = await response_text(toolio_mm.complete(msgs, json_schema=AGENT_1_SCHEMA, max_tokens=2048))
        resp_data = json.loads(resp)
        
        # Update history
        new_history = history + [{
            'question': user_answer,
            'answer': resp_data.get('question', '')
        }]
        
        # Create conversation display
        conversation_display = html.Div([
            html.Div([
                html.Div(f"You: {turn['question']}", style={'fontWeight': 'bold'}),
                html.Div(f"Agent: {turn['answer']}", style={'marginLeft': '20px', 'marginBottom': '10px'})
            ]) for turn in new_history
        ])
        
        # If we got 'ready' instead of a question, trigger newsletter generation
        if resp_data.get('ready'):
            return new_history, "Thanks! Generating your newsletter...", conversation_display, ''
            
        return new_history, resp_data.get('question', ''), conversation_display, ''
    
    raise PreventUpdate

@app.callback(
    [Output('newsletter-output', 'children'),
     Output('debug-output', 'children')],
    [Input('conversation-history', 'data')],
    [State('available-subreddits-store', 'children')]
)
async def generate_newsletter(history, available_subreddits_json):
    if not history:
        raise PreventUpdate
        
    # Check last response for 'ready' signal
    msgs = [
        {'role': 'system', 'content': agent_1_sysprompt}
    ]
    for turn in history:
        msgs.append({'role': 'user', 'content': turn['question']})
        msgs.append({'role': 'assistant', 'content': turn['answer']})
    
    resp = await response_text(toolio_mm.complete(msgs, json_schema=AGENT_1_SCHEMA, max_tokens=2048))
    resp_data = json.loads(resp)
    
    if not resp_data.get('ready'):
        raise PreventUpdate
        
    topics = resp_data['ready']
    debug_output = [f"Topics identified: {topics}"]
    
    # Get subreddit recommendations from Agent 2
    all_available_subreddits = json.loads(available_subreddits_json)
    msgs = [
        {'role': 'system', 'content': agent_2_sysprompt},
        {'role': 'user', 'content': agent_2_uprompt.format(
            topics='\n* '.join(topics), 
            subreddits=all_available_subreddits)}
    ]
    resp = await response_text(toolio_mm.complete(msgs, json_schema=AGENT_2_SCHEMA, max_tokens=2048))
    selected_subreddits = json.loads(resp)[:MAX_SUBREDDITS]
    selected_subreddits = [s.replace('/r/', '') for s in selected_subreddits]
    
    debug_output.append(f"Selected subreddits: {selected_subreddits}")
    
    # Get posts and generate newsletter
    posts = await get_reddit_posts(selected_subreddits)
    titles = [post.title for post in posts]
    titles_text = '\n*  '.join(titles).strip()
    
    uprompt = AGENT_3_UPROMPT.format(
        subreddits=selected_subreddits,
        titles=titles_text
    )
    msgs = [{'role': 'user', 'content': uprompt}]
    newsletter = await response_text(toolio_mm.complete(msgs, max_tokens=8096))
    
    return html.Div([
        html.H2("Reddit Newsletter Summary"),
        html.H3(f"Based on topics: {', '.join(topics)}"),
        html.H3(f"Selected subreddits: {', '.join(selected_subreddits)}"),
        html.Pre(newsletter)
    ]), "\n".join(debug_output)

if __name__ == '__main__':
    app.run_server(debug=True)
