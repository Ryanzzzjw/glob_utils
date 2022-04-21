from glob_utils.args.check_type import isint, isstring


MAX_LOG_MSG_LENGTH= 80

################################################################################
# Messages/Strings transformation mostly for logging purpose
################################################################################

def highlight_msg(msg:str, symbol:str='#')->str:
    """Add a continious line of symbol before and after a message to highlight it
    MAX_LOG_MSG_LENGTH= 80
    eg.:
    ############################################################################
    msg
    ############################################################################

    Args:
        msg (str): msg to highlight
        symbol (str, optional): symbol for highlighting. Defaults to '#'.

    Returns:
        str: highlighted message (at least 3 lines)
    """    
    isstring(msg, raise_error=True)
    isstring(symbol, raise_error=True)

    sym= symbol*MAX_LOG_MSG_LENGTH
    sym = trunc_msg(sym, MAX_LOG_MSG_LENGTH) # in case that sym is not a single char
    return f'\n{sym}\n{msg}\n{sym}'    

def trunc_msg(msg:str, max_length:int=MAX_LOG_MSG_LENGTH, trunc_end:bool=True)->str:
    """Truncate a msg to a max_length

    Args:
        msg (str): message to truncate
        max_length (int, optional): [description]. Defaults to MAX_LOG_MSG_LENGTH.
        trunc_end (bool, optional): if set to `True` the end of the message is truncated. Defaults to `True`.

    Returns:
        [str]: truncated message
    """    
    isstring(msg, raise_error=True)
    isint(max_length, raise_error=True)
    
    if len(msg)< max_length: 
        return msg
    return msg[:max_length] if trunc_end else msg[-max_length:]