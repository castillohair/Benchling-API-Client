===================================
Python Client for the Benchling API
===================================

This package allows you to directly access the `Benchling API <https://api.benchling.com/docs/>`_ from Python. Currently, only reading from your Benchling library is supported.

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
    
    # Search for a sequence
    seq_list = benchlingclient.search('pSC101')
    for seq in seq_list:
        # Benchling's search function only gives basic information about a sequence.
        # The following loads the remaining information
        seq.load()
        # Print details about the sequence
        print ""
        print seq.id
        print seq.name
        print seq.description
        print seq.creator
        # Some other interesting attributes are: `.annotations`, `.primers`, and `.bases`.

    # Get all the folders to which you have read access
    # Warning: may take a while
    folder_list = benchlingclient.Folder.load_all()
    for folder in folder_list:
        print ""
        print folder.id
        print folder.name
        # `.sequences` contains the list of sequences in that folder. Other interesting
        # attributes are `.owner`, `.created_at`, and `.modified_at`.

    # Load a sequence using its id
    seq = benchlingclient.Sequence(id='Id_of_your_sequence')
    print seq

Future work
===========

This API client is still in early alpha, and supports a limited subset of the API's functionality. Suggestions or bug reports are welcome in the "Issues" section of the github repo.