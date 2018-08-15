===================================
Python Client for the Benchling API
===================================

This package allows you to directly access the `Benchling API v2 <https://docs.benchling.com/docs>`_ from Python. Currently, only reading resources related to DNA sequences is supported.

Installation
============

Clone or download the package, and run the following from a terminal:

.. code::

    python setup.py install

Usage
=====

First, you will need to request an API key from Benchling. You can do that either via email or using the chat function in the Benchling UI.


.. code:: python

    # Import package
    import benchlingclient
    # You need to specify your key!
    benchlingclient.LOGIN_KEY = 'write_your_key_here!'
    
    # Get all the folders to which you have read access
    # Warning: may take a while
    folder_list = benchlingclient.Folder.list_all()

    print("\n{} folders found.".format(len(folder_list)))
    for folder in folder_list:
        print("")
        print("Folder name: {}".format(folder.name))
        print("Folder ID: {}".format(folder.id))
        print("ID of parent folder: {}".format(folder.parentFolderId))
        print("ID of parent project: {}".format(folder.projectId))

    # Get all the projects to which you have read access
    # Warning: may take a while
    project_list = benchlingclient.Project.list_all()

    print("\n{} projects found.".format(len(project_list)))
    for project in project_list:
        print("")
        print("Project name: {}".format(project.name))
        print("Project ID: {}".format(project.id))
        print("Owner: {} (ID: {})".format(project.owner.name, project.owner.id))

    # Search for DNA sequences with a specified name
    # Warning: may take a while
    seq_list = benchlingclient.DNASequence.list_all(name="pBR322")

    print("\n{} sequences found.".format(len(seq_list)))
    # Print details about the sequence
    for seq in seq_list:
        print("")
        print("Sequence name: {}".format(seq.name))
        print("Sequence ID: {}".format(seq.id))
        print("Sequence creator: {} (ID: {})".format(seq.creator.name,
                                                     seq.creator.id))
        # Some other interesting attributes are: `.annotations`, `.primers`,
        # and `.bases`.

    # Load a sequence using its id
    seq = benchlingclient.DNASequence(id='seq_me1auXTF')
    print("")
    print(seq)

Future work
===========

This API client is still in early alpha, and supports a limited subset of the API's functionality. Suggestions or bug reports are welcome in the "Issues" section of the github repo.