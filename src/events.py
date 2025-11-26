event_handlers = {}

def subscribe(event_type, handler_fn):
    if event_type not in event_handlers:
        event_handlers[event_type] = []
    event_handlers[event_type].append(handler_fn)

def publish(event_type, payload):
    handlers = event_handlers.get(event_type, [])
    for handler in handlers:
        handler(payload)
