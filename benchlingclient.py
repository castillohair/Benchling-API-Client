"""
Benchling API Client

"""

import requests

# Versions should comply with PEP440.  For a discussion on single-sourcing
# the version across setup.py and the project code, see
# https://packaging.python.org/en/latest/single_source_version.html
__version__ = '0.1.2'

# URL for API requests
API_URL = "https://benchling.com/api/v1/"

# API Key for login
LOGIN_KEY = 'not a real key!'

def _raise_if_error(r):
    """
    """
    if r.status_code == 400:
        raise Exception("The request was invalid, either due to bad syntax \
            or invalid parameters.")
    elif r.status_code == 401:
        raise Exception("Authentication failed - your API key is likely \
            incorrect.")
    elif r.status_code == 403:
        raise Exception("You do not have access to the resource or method.")
    elif r.status_code == 404:
        raise Exception("The resource requested does not exist.")
    elif r.status_code == 500:
        raise Exception("Internal Server Error.")

def connect_get(url, **kwargs):
    """
    """
    # Send a get request
    r = requests.get(url, auth=(LOGIN_KEY, ''))
    # Raise exception if error code:
    _raise_if_error(r)

    # Everything good, return
    return r

def search(query, queryType='text', limit=50, offset=0):
    """
    """
    # Construct parameter dictionary
    params = {'query': query,
              'queryType': queryType,
              'limit': limit,
              'offset': offset,
              }

    # Send request
    r = requests.post(API_URL + 'search',
                      auth=(LOGIN_KEY, ''),
                      json=params)
    # Raise exception if error code:
    _raise_if_error(r)

    # Generate list of sequences
    seq_list = []
    for seq_dict in r.json()['results']:
        seq_list.append(Sequence(d=seq_dict))

    return seq_list

class Folder(object):
    """
    """
    def __init__(self, **kwargs):
        """
        """
        if 'id' in kwargs:
            self._load_by_id(kwargs['id'])
        elif 'd' in kwargs:
            self._populate_from_dict(kwargs['d'])

    def __str__(self):
        """
        """
        s = ""
        s += "Name: {}\n".format(self.name)
        s += "Id: {}\n".format(self.id)
        if self.sequences is not None:
            s += "Number of sequences: {}\n".format(len(self.sequences))

        return s

    def _load_by_id(self, id):
        """
        """
        r = connect_get(API_URL + 'folders/{}'.format(id))
        self._populate_from_dict(r.json())

    def _populate_from_dict(self, d):
        """
        """
        # Simple properties
        self.id = d.get('id')
        self.name = d.get('name')
        self.description = d.get('description')
        self.owner = d.get('owner')
        self.type = d.get('type')
        self.count = d.get('count')
        self.created_at = d.get('created_at')
        self.modified_at = d.get('modified_at')

        # Class properties
        if 'permissions' in d:
            self.permissions = Permissions(d=d['permissions'])
        else:
            self.permissions = None

        if 'sequences' in d:
            self.sequences = [Sequence(d=di) for di in d['sequences']]
        else:
            self.sequences = None

    @classmethod
    def load_all(cls):
        """
        """
        r = connect_get(API_URL + 'folders')

        folder_list = []
        for folder_dict in r.json()['folders']:
            folder_list.append(cls(d=folder_dict))

        return folder_list

class Sequence(object):
    """
    """
    def __init__(self, **kwargs):
        """
        """
        if 'id' in kwargs:
            self._load_by_id(kwargs['id'])
        elif 'd' in kwargs:
            self._populate_from_dict(kwargs['d'])

    def __str__(self):
        """
        """
        s = ""
        s += "Name: {}\n".format(self.name)
        s += "Id: {}\n".format(self.id)
        if self.creator is not None:
            s += "Created by: {}\n".format(self.creator.name)
        if self.folder is not None:
            s += "In folder: {}\n".format(self.folder.name)
        if self.circular is not None:
            s += "Sequence type: {}\n".format("circular"
                                              if self.circular
                                              else "linear")
        if self.length is not None:
            s += "Length: {}\n".format(self.length)
        if self.annotations is not None:
            s += "Number of annotations: {}\n".format(len(self.annotations))
        if self.primers is not None:
            s += "Number of primers attached: {}\n".format(len(self.primers))

        return s

    def _load_by_id(self, id):
        """
        """
        r = connect_get(API_URL + 'sequences/{}'.format(id))
        self._populate_from_dict(r.json())

    def _populate_from_dict(self, d):
        """
        """
        # Simple properties
        self.aliases = d.get('aliases')
        self.createdAt = d.get('createdAt')
        self.modifiedAt = d.get('modifiedAt')
        self.name = d.get('name')
        self.id = d.get('id')
        self.editURL = d.get('editURL')
        self.tagSchema = d.get('tagSchema')
        self.circular = d.get('circular')
        self.length = d.get('length')
        self.description = d.get('description')
        self.bases = d.get('bases')
        self.color = d.get('color')

        # Class properties
        if 'creator' in d:
            self.creator = Entity(d=d['creator'])
        else:
            self.creator = None

        if 'folder' in d:
            self.folder = Folder(d=d['folder'])
        else:
            self.folder = None

        if 'tags' in d:
            self.tags = [Tag(d=di) for di in d['tags']]
        else:
            self.tags = None

        if 'annotations' in d:
            self.annotations = [Annotation(d=di) for di in d['annotations']]
        else:
            self.annotations = None

        if 'primers' in d:
            self.primers = [Primer(d=di) for di in d['primers']]
        else:
            self.primers = None

        if 'notes' in d:
            self.notes = [Note(d=di) for di in d['notes']]
        else:
            self.notes = None

    @classmethod
    def load_all(cls):
        """
        """
        r = connect_get(API_URL + 'sequences/')

        seq_list = []
        for seq_dict in r.json()['sequences']:
            seq_list.append(cls(d=seq_dict))

        return seq_list

    def load(self):
        """
        """
        r = connect_get(API_URL + 'sequences/{}'.\
            format(self.id))

        self._populate_from_dict(r.json())

class Entity(object):
    """
    """
    def __init__(self, **kwargs):
        """
        """
        if 'id' in kwargs:
            self._load_by_id(kwargs['id'])
        elif 'd' in kwargs:
            self._populate_from_dict(kwargs['d'])

    def __str__(self):
        """
        """
        s = ""
        s += "Name: {}\n".format(self.name)
        s += "Id: {}\n".format(self.id)
        if self.type is not None:
            s += "Type: {}\n".format(self.type)

        return s

    def _load_by_id(self, id):
        """
        """
        r = connect_get(API_URL + 'entities/{}'.format(id))
        self._populate_from_dict(r.json())

    def _populate_from_dict(self, d):
        """
        """
        self.id = d.get('id')
        self.avatarUrl = d.get('avatarUrl')
        self.handle = d.get('handle')
        self.name = d.get('name')
        self.type = d.get('type')
        self.website = d.get('website')
        self.location = d.get('location')
        self.joined_on = d.get('joined_on')

    @classmethod
    def load_me(cls):
        """
        """
        r = connect_get(API_URL + 'entities/me')
        return cls(d=r.json())

class Annotation(object):
    """
    """
    def __init__(self, **kwargs):
        """
        """
        if 'd' in kwargs:
            self._populate_from_dict(kwargs['d'])

    def __str__(self):
        """
        """
        s = ""
        s += "Name: {}\n".format(self.name)
        if self.type is not None:
            s += "Type: {}\n".format(self.type)
        if self.strand is not None:
            if self.strand == 1:
                strand_text = "Forward"
            elif self.strand == -1:
                strand_text = "Reverse"
            else:
                strand_text = "None"
            s += "Strand: {}\n".format(strand_text)
        if (self.start is not None) and (self.end is not None):
            s += "Location: {}..{}\n".format(self.start, self.end)

        return s

    def _populate_from_dict(self, d):
        """
        """
        self.name = d.get('name')
        self.strand = d.get('strand')
        self.color = d.get('color')
        self.type = d.get('type')
        self.start = d.get('start')
        self.end = d.get('end')

class Note(object):
    """
    """
    def __init__(self, **kwargs):
        """
        """
        if 'd' in kwargs:
            self._populate_from_dict(kwargs['d'])

    def __str__(self):
        """
        """
        s = ""
        if self.creator is not None:
            s += "Created by: {}\n".format(self.creator)
        if self.text is not None:
            s += "Text:\n{}\n".format(self.text)

        return s

    def _populate_from_dict(self, d):
        """
        """
        self.text = d.get('text')
        self.created_at = d.get('created_at')
        self.creator = d.get('creator')

class Permissions(object):
    """
    """
    def __init__(self, **kwargs):
        """
        """
        if 'd' in kwargs:
            self._populate_from_dict(kwargs['d'])

    def __str__(self):
        """
        """
        s = ""
        if self.admin is not None:
            s += "Admin? {}\n".format("Yes" if self.admin else "No")
        if self.owner is not None:
            s += "Owner? {}\n".format("Yes" if self.owner else "No")
        if self.readable is not None:
            s += "Can read? {}\n".format("Yes" if self.readable else "No")
        if self.writable is not None:
            s += "Can write? {}\n".format("Yes" if self.writable else "No")
        if self.appendable is not None:
            s += "Can append? {}\n".format("Yes" if self.appendable else "No")

        return s

    def _populate_from_dict(self, d):
        """
        """
        self.admin = d.get('admin')
        self.owner = d.get('owner')
        self.readable = d.get('readable')
        self.writable = d.get('writable')
        self.appendable = d.get('appendable')

class Primer(object):
    """
    """
    def __init__(self, **kwargs):
        """
        """
        if 'd' in kwargs:
            self._populate_from_dict(kwargs['d'])

    def __str__(self):
        """
        """
        s = ""
        s += "Name: {}\n".format(self.name)
        if self.strand is not None:
            if self.strand == 1:
                strand_text = "Forward"
            elif self.strand == -1:
                strand_text = "Reverse"
            else:
                strand_text = "None"
            s += "Strand: {}\n".format(strand_text)
        if self.bind_position is not None:
            s += "Binding position: {}\n".format(bind_position)

        return s

    def _populate_from_dict(self, d):
        """
        """
        self.name = d.get('name')
        self.bases = d.get('bases')
        self.color = d.get('color')
        self.start = d.get('start')
        self.end = d.get('end')
        self.overhang_length = d.get('overhang_length')
        self.strand = d.get('strand')
        self.created_at = d.get('created_at')
        self.bind_position = d.get('bind_position')

class Tag(object):
    """
    """
    def __init__(self, **kwargs):
        """
        """
        if 'd' in kwargs:
            self._populate_from_dict(kwargs['d'])

    def _populate_from_dict(self, d):
        """
        """
        self.name = d.get('name')
        self.value = d.get('value')
        self.url = d.get('url')
        self.reference = d.get('reference')
