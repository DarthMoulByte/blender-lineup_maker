import bpy
import re
from os import path

from . import variables as V
from . import preferences as P

class NamingConvention(object):
    def __init__(self, name, convention):
        self.fullname = name
        self.name, self.ext = path.splitext(name)

        if self.ext:
            self.ext = self.ext.lower()
        if self.name:
            self.name = self.name.lower()

        self.convention = convention
        self._naming_convention = None

    @property
    def naming_convention(self):
        if self._naming_convention is None:
            self._naming_convention = self.slice()

        return self._naming_convention

    
    def slice(self):
        def assign_value(ckws, value, return_dict, word):
            if len(ckws):
                if value in ckws:
                    return_dict[word] = value
            else:
                return_dict[word] = value

        # person = {'first': 'Jean-Luc', 'last': 'Picard'}
        # string = '{p[first]} {p[last]}'.format(p=person)
        # <PROJECT>_<TEAM>_<CATEGORY>_<INCR>_<GENDER>
        naming_convention = {'name':[], 'fullname': self.fullname}

        if len(self.ext):
            naming_convention['ext'] = self.ext

        word_pattern = re.compile(r'[{0}]?([a-zA-Z0-9]+)[{0}]?'.format(V.LM_SEPARATORS), re.IGNORECASE)
        keyword_pattern = re.compile(r'[{0}]?<([a-zA-Z0-9]+)>[{0}]?'.format(V.LM_SEPARATORS), re.IGNORECASE)
        not_keyword_pattern = re.compile(r'(?<=[{0}])([a-zA-Z0-9]+)|([a-zA-Z0-9]+)(?=[{0}])'.format(V.LM_SEPARATORS), re.IGNORECASE)
        
        name_pattern = re.compile(r'[{0}]?([a-zA-Z0-9]+)[{0}]?'.format(V.LM_SEPARATORS))
        
        words = word_pattern.finditer(self.convention)
        keywords = keyword_pattern.finditer(self.convention)
        not_keyword = not_keyword_pattern.finditer(self.convention)
        names = name_pattern.finditer(self.name)

        name_grp = [n.group(1) for n in names]

        for i,word in enumerate(words):
            w = word.group(1).lower()
            for ckw,ckws in V.LM_NAMING_CONVENTION_KEYWORDS.items():
                if w == ckw: # word is a keyword
                    if w in V.LM_NAMING_CONVENTION_KEYWORDS_MESH.keys():
                        if w not in self.get_other_ckws(V.LM_NAMING_CONVENTION_KEYWORDS_MESH, w):
                            assign_value(ckws, name_grp[i], naming_convention, w)
                    elif w in V.LM_NAMING_CONVENTION_KEYWORDS_TEXTURE.keys():
                        if w not in self.get_other_ckws(V.LM_NAMING_CONVENTION_KEYWORDS_TEXTURE, w):
                            assign_value(ckws, name_grp[i], naming_convention, w)
                else:
                    naming_convention[w] = w

            naming_convention['name'].append(name_grp[i])

        return naming_convention

    def pop(self, item):
        new_naming = self.naming_convention
        if item in new_naming['name']:
            new_naming['name'].pop()
        
        if item in new_naming:
            new_naming.pop()
        
        item_pattern = re.compile(r'[{0}]?({1})[{0}]?'.format(V.LM_SEPARATORS, item), re.IGNORECASE)
        if len(item_pattern.finditer(new_naming['fullname'])):
            new_naming['fullname'] = item_pattern.sub(r'\0')

        self.naming_convention = new_naming

    def get_other_ckws(self, ckw_dict, current_key):
        other_ckws = []
        for ckw, ckws in ckw_dict.items():
            if ckw != current_key:
                other_ckws = other_ckws + ckws

        return other_ckws