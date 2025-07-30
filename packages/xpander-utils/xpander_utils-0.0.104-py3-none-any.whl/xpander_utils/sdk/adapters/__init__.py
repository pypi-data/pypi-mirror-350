import importlib

if importlib.util.find_spec("smolagents") is not None:
    from .smolagents import SmolAgentsAdapter

if importlib.util.find_spec("llamaindex") is not None:
    from .llamaindex import LlamaIndexAdapter

if importlib.util.find_spec("chainlit") is not None:
    from .chainlit import ChainlitAdapter, ChainlitXpanderDataLayer
