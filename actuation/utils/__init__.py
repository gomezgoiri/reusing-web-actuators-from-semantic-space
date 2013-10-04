import re

def append_slash_if_absent( file_path ):
    return file_path if file_path.endswith( "/" ) else file_path + "/"

def _construct_sparql_select( prefixes, variabs, where ):
    if len(variabs)==0:
        raise Exception("The SPARQL SELECT must contain at least a variable.")
    
    ret = ""
    for name, value in prefixes.iteritems():
        ret += "prefix %s: <%s>\n" % (name, value) 
    
    ret += "\nselect "
    for v in variabs:
        ret += "?%s, " % v
    ret = ret[:-2] # remove last ", "
    ret += "\nwhere {\n"
    ret += where
    ret += "}"
    return ret

def _parse_prefixes( n3ql_query ):
    ptt_pref = re.compile( "^\s*@prefix\s+(?P<prefix>[\w-]*)\s*:\s*<(?P<url>.*)>\s*.", re.MULTILINE | re.IGNORECASE )
    
    prefixes = {}
    for name, value in ptt_pref.findall( n3ql_query ):
        prefixes[name] = value
    return prefixes

def _extract_uncommented_premise( n3ql_query ):
    ptt_premise = re.compile( "^\s*{(?P<premise>.+)}\s*=>\s*{.+}", re.MULTILINE | re.DOTALL )
    commented_premise = ptt_premise.search( n3ql_query ).group("premise")
    
    premise = ""
    for l in commented_premise.split("\n"):
        pos = l.find( "#" )
        new_line = l if pos == -1 else l[:pos]
        if new_line.strip()!="": #only adds lines with content
            premise += new_line + "\n"
    return premise

def _parse_variable_names( text ):
    variabs = set()
    ptt_vars = re.compile( "\s*[?](\w+)\s+" )
    for var_name in ptt_vars.findall( text ):
        variabs.add( var_name )
    return variabs

def n3ql_to_sparql( n3ql_query ):
    """
    Overly simplified conversion from N3QL to SPARQL select.
    
    N3QL pattern:
    
    @prefix p: <http://blablah> .
    ...
    {
        [sth] # this resembles to the WHERE 
    } => {
        [sth2] # this resembles to a SPARQL CONSTRUCT
    }
    
    
    It transforms to a SPARQL with the following shape:
    
    PREFIX p: <http://blablah>
    
    SELECT ?var1, ?var2 # this variables are extracted from [sth]
    WHERE {
        [sth]
    }
    """
    prefixes = _parse_prefixes( n3ql_query )
    premise = _extract_uncommented_premise( n3ql_query )
    variabs = _parse_variable_names( premise )
    return _construct_sparql_select(prefixes, variabs, premise)