TAS_PAGE = {'url': 'http://thealternateside.org/', 'layout': [
    {   'method': 'find',
        'element': 'div',
        'identifier': {'class': 'view-top-albums'}
    },
    {
        'method': 'find',
        'element': 'div',
        'identifier': {'class': "field-content"}
    },
    {
        'method': 'find_all',
        'element': 'p',
        'identifier': None
    }
]}

SOMA_FM_BAGEL_PAGE = {'url': 'http://somafm.com/charts/bagel/', 'layout': [
    {
        'method': 'find',
        'element': 'div',
        'identifier': {'id': 'content'}
    },
    {
        'method': 'find',
        'element': 'pre',
        'identifier': None
    }
]}

SOMA_FM_UNDERGROUND_80s = {'url': 'http://somafm.com/charts/u80s/', 'layout': [
    {
        'method': 'find',
        'element': 'div',
        'identifier': {'id': 'content'}
    },
    {
        'method': 'find',
        'element': 'pre',
        'identifier': None
    }
]}

SOMA_FM_INDIE_POP_ROCKS = {'url': 'http://somafm.com/charts/indiepop/', 'layout': [
    {
        'method': 'find',
        'element': 'div',
        'identifier': {'id': 'content'}
    },
    {
        'method': 'find',
        'element': 'pre',
        'identifier': None
    }
]}

SOMA_FM_LUSH = {'url': 'http://somafm.com/charts/lush/', 'layout': [
    {
        'method': 'find',
        'element': 'div',
        'identifier': {'id': 'content'}
    },
    {
        'method': 'find',
        'element': 'pre',
        'identifier': None
    }
]}

SOMA_FM_POPTRON = {'url': 'http://somafm.com/charts/poptron/', 'layout': [
    {
        'method': 'find',
        'element': 'div',
        'identifier': {'id': 'content'}
    },
    {
        'method': 'find',
        'element': 'pre',
        'identifier': None
    }
]}