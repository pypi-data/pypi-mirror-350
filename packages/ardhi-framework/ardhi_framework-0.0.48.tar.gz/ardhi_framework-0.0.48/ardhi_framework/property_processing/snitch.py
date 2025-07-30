"""Send signals and notifications to owners, directors, POAs and all parties involved in a parcel of parcel activity
Just snitch for actions by owners if any;
With tips
"""

def snitch_func(func):
	
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    
    return wrapper

