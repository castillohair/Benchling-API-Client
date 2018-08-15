"""
Benchling API Client

"""

import requests

# Versions should comply with PEP440.  For a discussion on single-sourcing
# the version across setup.py and the project code, see
# https://packaging.python.org/en/latest/single_source_version.html
__version__ = '0.2.0'

# URL of the API
API_URL = "https://benchling.com/api/v2/"

# API Key for login
LOGIN_KEY = 'not a real key!'

def _request_get(url, **kwargs):
    """
    """
    # Send a get request
    r = requests.get(url, auth=(LOGIN_KEY, ''), params=kwargs)
    # Check if response is formatted as JSON
    try:
        rj = r.json()
    except:
        raise Exception("API request not in JSON format. Check if the API URL "
            "is correct.")
    # If the status code indicates an error, raise and show the error message
    # returned.
    # See https://docs.benchling.com/docs/errors
    if r.status_code >= 400:
        raise Exception(rj['error']['message'])

    # Everything good, return formatted response
    return rj

class Resource(object):
    """
    Class that represents a generic benchling resource.

    Notes
    -----
    See https://docs.benchling.com/reference

    """
    # List of parameters in the resource
    parameters = []
    # Resource parameter types. Only specify for parameters that are resources.
    parameter_types = {}
    # API endpoint. For example, folder resources are queried at the URL
    # "[API_URL]/folders", therefore the endpoint is "folders". Use None if the
    # resource doesn't have an endpoint.
    endpoint = None
    # "list_key" is the key under which the results of a "list" request are
    # contained. This is not necessarily equal to the endpoint. For example,
    # the endpoint for the DNA Sequence resource is "dna-sequences", but the
    # key that contains the results of a "List DNA Sequences" request is
    # "dnaSequences".
    # If not specified, assume that it is the same as the endpoint.
    list_key = None

    def __init__(self, id=None, d=None):
        """
        """
        if (self.endpoint is not None) and (id is not None):
            # Load by ID if there is an endpoint specified and the "id" argument
            # has been specified.
            self._load_by_id(id)
        elif d is not None:
            # Populate parameters from dictionary "d" if specified
            self._populate_from_dict(d)
        else:
            # Initialize all parameters as None
            for parameter in self.parameters:
                setattr(self, parameter, None)

    def __eq__(self, other):
        """
        """
        # Test whether parameters match
        if self.parameters != other.parameters:
            return False

        # Test whether parameter values are identical
        for p in self.parameters:
            if getattr(self, p)!=getattr(other, p):
                return False

        # Parameter and parameter contents are the same.
        return True

    def _load_by_id(self, id):
        """
        """
        # Raise error if endpoint is not specified
        if self.endpoint is None:
            raise TypeError("no endpoint specified for this resource")
        # Request resource from API and populate this object
        d = _request_get(API_URL + '{}/{}'.format(self.endpoint, id))
        self._populate_from_dict(d)

    @classmethod
    def list(cls,
             pageSize=50,
             nextToken=None,
             **kwargs):
        """
        """
        # Raise error if endpoint is not specified
        if cls.endpoint is None:
            raise TypeError("no endpoint specified for this resource")

        # Obtain list key
        if cls.list_key is not None:
            list_key = cls.list_key
        else:
            list_key = cls.endpoint

        # Submit request
        d = _request_get(API_URL + cls.endpoint,
                         pageSize=pageSize,
                         nextToken=nextToken,
                         **kwargs)

        # Construct list of resource objects
        resource_list = []
        for resource_dict in d[list_key]:
            resource_list.append(cls(d=resource_dict))

        if d['nextToken']:
            nextToken = d['nextToken']
        else:
            nextToken = None

        return resource_list, nextToken

    @classmethod
    def list_all(cls, **kwargs):
        """
        """
        # Raise error if endpoint is not specified
        if cls.endpoint is None:
            raise TypeError("no endpoint specified for this resource")

        # Obtain list key
        if cls.list_key is not None:
            list_key = cls.list_key
        else:
            list_key = cls.endpoint

        # Initialize list of resource objects to return
        resource_list = []

        # Iterate
        nextToken = None
        while(True):
            # Submit request with maximum page size
            request_dict = _request_get(API_URL + cls.endpoint,
                                        pageSize=100,
                                        nextToken=nextToken,
                                        **kwargs)

            # Add to list of resource objects
            for resource_dict in request_dict[list_key]:
                resource_list.append(cls(d=resource_dict))

            # If nextToken is not present, return. Otherwise, save.
            if request_dict['nextToken']:
                nextToken = request_dict['nextToken']
            else:
                break

        return resource_list

    def _populate_from_dict(self, d):
        """
        """
        for parameter in self.parameters:
            # Check if parameter is a special resource type
            if parameter in self.parameter_types:
                parameter_type = self.parameter_types[parameter]
                # Assign None if parameter value is None or not specified
                # If the parameter value is a list, every element should be an
                # instance of the resource type class.
                # Otherwise, assign a single class instance.
                if (parameter not in d) or (d[parameter] is None):
                    setattr(self, parameter, None)
                elif type(d[parameter]) is list:
                    parameter_list = []
                    for single_parameter_dict in d[parameter]:
                        parameter_object = parameter_type(
                            d=single_parameter_dict)
                        parameter_list.append(parameter_object)
                    setattr(self, parameter, parameter_list) 
                else:
                    parameter_object = parameter_type(d=d[parameter])
                    setattr(self, parameter, parameter_object)                    
            else:
                # Assign value from dictionary. If parameter not in dictionary.
                # "get()" will return None.
                setattr(self, parameter, d.get(parameter))

class Annotation(Resource):
    """
    Class that represents an annotation resource.

    Notes
    -----
    See https://docs.benchling.com/reference#section-annotation-resource
    for information on this resource.

    """
    parameters = ['color',
                  'start',
                  'end',
                  'name',
                  'strand',
                  'type']

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

class Primer(Resource):
    """
    Class that represents a primer resource.

    Notes
    -----
    See https://docs.benchling.com/reference#section-primer-resource
    for information on this resource.

    """
    parameters = ["bases",
                  "bindPosition",
                  "color",
                  "end",
                  "name",
                  "overhangLength",
                  "start",
                  "strand"]

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
        if self.bindPosition is not None:
            s += "Binding position: {}\n".format(bindPosition)

        return s

class Translation(Resource):
    """
    Class that represents a translation resource.

    Notes
    -----
    See https://docs.benchling.com/reference#section-translation-resource
    for information on this resource.

    """
    parameters = ["start",
                  "end",
                  "strand",
                  "aminoAcids",
                  "regions"]

    def __str__(self):
        """
        """
        s = ""
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

class ArchiveRecord(Resource):
    """
    Class that represents an ArchiveRecord resource.

    Notes
    -----
    See https://docs.benchling.com/reference#archiverecord-resource
    for information on this resource.

    """
    parameters = ["reason"]

    def __str__(self):
        """
        """
        s = ""
        s += str(self.reason)

        return s

class UserSummary(Resource):
    """
    Class that represents an UserSummary resource.

    Notes
    -----
    See https://docs.benchling.com/reference#usersummary-resource
    for information on this resource.

    """
    parameters = ["handle", "id", "name"]

    def __str__(self):
        """
        """
        s = ""
        s += "Name: {}\n".format(self.name)
        s += "Id: {}\n".format(self.id)
        s += "Handle: {}\n".format(self.handle)

        return s

class TeamSummary(Resource):
    """
    Class that represents an TeamSummary resource.

    Notes
    -----
    See https://docs.benchling.com/reference#teamsummary-resource
    for information on this resource.

    """
    parameters = ["handle", "id", "name"]

    def __str__(self):
        """
        """
        s = ""
        s += "Name: {}\n".format(self.name)
        s += "Id: {}\n".format(self.id)
        s += "Handle: {}\n".format(self.handle)

        return s

class OrganizationSummary(Resource):
    """
    Class that represents an OrganizationSummary resource.

    Notes
    -----
    See https://docs.benchling.com/reference#organizationsummary-resource
    for information on this resource.

    """
    parameters = ["handle", "id", "name"]

    def __str__(self):
        """
        """
        s = ""
        s += "Name: {}\n".format(self.name)
        s += "Id: {}\n".format(self.id)
        s += "Handle: {}\n".format(self.handle)

        return s

class Folder(Resource):
    """
    Class that represents a Folder resource.

    Notes
    -----
    See https://docs.benchling.com/reference#folder-resource
    for information on this resource.

    """
    parameters = ["archiveRecord",
                  "id",
                  "name",
                  "parentFolderId",
                  "projectId"]
    parameter_types = {"archiveRecord": ArchiveRecord}
    endpoint = 'folders'

    def __str__(self):
        """
        """
        s = ""
        s += "Name: {}\n".format(self.name)
        s += "ID: {}\n".format(self.id)
        s += "Parent's ID: {}\n".format(self.parentFolderId)
        s += "Project ID: {}\n".format(self.projectId)
        if self.archiveRecord is not None:
            s += "Archived: {}\n".format(self.archiveRecord)

        return s

class Project(Resource):
    """
    Class that represents a Project resource.

    Notes
    -----
    See https://docs.benchling.com/reference#project-resource
    for information on this resource.

    """
    parameters = ["archiveRecord",
                  "id",
                  "name",
                  "owner"]
    parameter_types = {"archiveRecord": ArchiveRecord,
                       "owner": UserSummary}
    endpoint = 'projects'

    def __init__(self, id=None, d=None):
        """
        """
        if id is not None:
            self._load_by_id(id)
        elif d is not None:
            self._populate_from_dict(d)

    def __str__(self):
        """
        """
        s = ""
        s += "Name: {}\n".format(self.name)
        s += "ID: {}\n".format(self.id)
        s += "Owner: {} (ID: {})\n".format(self.owner.name, self.owner.id)
        if self.archiveRecord is not None:
            s += "Archived: {}\n".format(self.archiveRecord)

        return s

class DNASequence(Resource):
    """
    Class that represents a DNA Sequence resource.

    Notes
    -----
    See https://docs.benchling.com/reference#sequences
    for information on this resource.

    """
    parameters = ["id",
                  "aliases",
                  "annotations",
                  "archiveRecord",
                  "bases",
                  "createdAt",
                  "creator",
                  "customFields",
                  "entityRegistryId",
                  "fields",
                  "folderId",
                  "isCircular",
                  "length",
                  "modifiedAt",
                  "name",
                  "primers",
                  "registryId",
                  "schema",
                  "schema.id",
                  "schema.name",
                  "translations",
                  "webURL"]
    parameter_types = {"annotations": Annotation,
                       "archiveRecord": ArchiveRecord,
                       "creator": UserSummary,
                       "primers": Primer,
                       "translations": Translation}
    endpoint = 'dna-sequences'
    list_key = 'dnaSequences'

    def __str__(self):
        """
        """
        s = ""
        s += "Name: {}\n".format(self.name)
        s += "Id: {}\n".format(self.id)
        if self.creator is not None:
            s += "Created by: {} (ID: {})\n".format(self.creator.name,
                                                    self.creator.id)
        if self.folderId is not None:
            s += "Folder ID: {}\n".format(self.folderId)
        if self.isCircular is not None:
            s += "Sequence type: {}\n".format("circular"
                                              if self.isCircular
                                              else "linear")
        if self.length is not None:
            s += "Length: {}\n".format(self.length)
        if self.annotations is not None:
            s += "Number of annotations: {}\n".format(len(self.annotations))
        if self.primers is not None:
            s += "Number of primers attached: {}\n".format(len(self.primers))
        if self.translations is not None:
            s += "Number of translated sequences: {}\n".format(
                len(self.translations))

        return s

    @classmethod
    def load_all(cls):
        """
        """
        r = connect_get(API_URL + 'sequences/')

        seq_list = []
        for seq_dict in r.json()['sequences']:
            seq_list.append(cls(d=seq_dict))

        return seq_list

