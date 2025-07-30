# Make the main entrypoints into the package available at the top level of the package
from .main import OpenAI, AsyncOpenAI, DEV_MODE

# Make the materialization functions available at the top level of the package, if
# we're in dev mode
if DEV_MODE:
    from .main import materialize

# Remove DEV_MODE from the namespace
del DEV_MODE

# Add a function to check remaining credits
def check_remaining_credits(api_key : str) -> dict:
    '''
    Make a request from the proxy server for remaining credits
    '''
    import requests
    out = requests.get('https://llm-proxy.guetta.com/key/info', headers={'x-litellm-api-key' : f'Bearer {api_key}'}).json()

    return {'max_budget' : out['max_budget'],
            'spent_so_far' : out['spend'],
            'remaining_budget' : out['max_budget'] - out['spend']}