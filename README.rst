zest.zodbupdate
===============

zodbupdate rename dictionary and dexterity patch for Plone 6 projects.

See `post on community.plone.org <https://community.plone.org/t/zodbverify-porting-plone-with-zopedb-to-python3/8806/13>`_.
And the `Plone ZODB Python 3 migration docs <https://5.docs.plone.org/manage/upgrading/version_specific_migration/upgrade_zodb_to_python3.html>`_.


Compatibility
-------------

This is for Plone 6.0 or higher and Python 3.9 and higher.
All Plone imports should be optional, so you could try this in a plain Zope project as well, but most of the renames are for Plone.

For Plone 5.2, please use ``zest.zodbupdate`` version 1.x, and see its `README.rst`.
It includes explanations for using this as part of migrating your Plone 5.2 database from Python 2.7 to Python 3.


Quick usage
-----------

With a ``pip`` based project::

    pip install zodbverify zodbupdate zest.zodbupdate

If you use ``zc.buildout``, you can add these in a simplified ``buildout.cfg`` like this, and then run ``bin/buildout``::

    [buildout]
    parts =
        instance
        zodbupdate

    [instance]
    recipe = plone.recipe.zope2instance
    eggs =
        Plone
        zodbverify

    [zodbupdate]
    recipe = zc.recipe.egg
    scripts = zodbupdate
    eggs =
        zodbupdate
        zest.zodbupdate
        ${instance:eggs}

After installation with pip or Buildout, you can run the ``zodbupdate`` tool.
It needs the location of your file storage::

    bin/zodbupdate -f var/filestorage/Data.fs

You can also pass a configuration file.
See the `zodbupdate readme <https://github.com/zopefoundation/zodbupdate/tree/master?tab=readme-ov-file#non-filestorage-configurations>`_.


Use case and process
--------------------

You use this in combination with the `zodbverify <https://github.com/plone/zodbverify>`_ and `zodbupdate <https://github.com/zopefoundation/zodbupdate>`_ tools.
When you first run ``bin/zodbverify`` or ``bin/instance zodbverify``, you may see warnings and exceptions.
It may warn about problems that ``zodbupdate`` will fix.
So the idea is now:

1. Pack your database, with zero days of changes.

2. Run ``bin/instance zodbverify``.
   If this gives no errors, you are done.

3. Run ``bin/zodbupdate --pack -f var/filestorage/Data.fs``
   This applies all explicit and implicit renames.
   With the ``--pack`` option, it also packs your database afterwards.

4. Run ``bin/instance zodbverify``.
   If this gives no errors, you are done.
   If this still gives errors, you may need to define more rules and apply them with zodbupdate.

When this works fine on a copy of your production database,
you could choose to safe some downtime and only do step 3 on your production database.
But please check this process again on a copy of your database.


Rename rules
------------

zodbverify may give warnings and exceptions like these::

    Warning: Missing factory for Products.ResourceRegistries.interfaces.settings IResourceRegistriesSettings
    Warning: Missing factory for App.interfaces IPersistentExtra
    Warning: Missing factory for App.interfaces IUndoSupport
    ...
    Found X records that could not be loaded.
    Exceptions and how often they happened:
    ImportError: No module named ResourceRegistries.interfaces.settings: 8
    AttributeError: 'module' object has no attribute 'IPersistentExtra': 4508

For each, you need to check if it can be safely replaced by something else,
or if this points to a real problem: maybe a previously installed add-on is missing.

In this case, these interfaces seem no longer needed.
Easiest is to replace them with a basic Interface.
Maybe there are better ways to clean these up, but so far so good.

You fix these with renames in an entrypoint using zodbupdate.
See https://github.com/zopefoundation/zodbupdate#pre-defined-rename-rules
The current package defines such an entrypoint.

Here is the rename dictionary from the `master branch <https://github.com/zestsoftware/zest.zodbupdate/blob/master/src/zest/zodbupdate/renames.py>`_
and here from the `1.x branch <https://github.com/zestsoftware/zest.zodbupdate/blob/1.x/src/zest/zodbupdate/renames.py>`_.
The warnings and exceptions mentioned above are handled on the 1.x branch.
Each version of this package may have different contents.


Dynamic dexterity schemas
-------------------------

A special case that ``bin/zodbupdate`` and ``bin/zodbverify`` may bump into, is::

    AttributeError: Cannot find dynamic object factory for module plone.dexterity.schema.generated: 58
    Warning: Missing factory for plone.dexterity.schema.generated Plone_0_Image
    Warning: Missing factory for plone.dexterity.schema.generated Plone_0_Document
    Warning: Missing factory for plone.dexterity.schema.generated Site2_0_News_1_Item
    Warning: Missing factory for plone.dexterity.schema.generated Site3_0_Document

This is because no zcml is loaded by these scripts.
So this utility from ``plone.dexterity/configure.zcml`` is not registered::

    <utility
        factory=".schema.SchemaModuleFactory"
        name="plone.dexterity.schema.generated"
        />

This utility implements ``plone.alterego.interfaces.IDynamicObjectFactory``.
This is responsible for generating schemas on the fly.
So we register this utility in Python code.

Note that in normal use (``bin/instance``) this would result in a double registration,
but the second one is simply ignored by zope.interface, because it is the same.

Also, when you have zodbverify in the instance eggs and you call ``bin/instance zodbverify``,
you will not get this error, because then zcml is loaded, and no special handling is needed.


Package structure
-----------------

- This package only has an ``__init__.py`` file and a ``renames.py`` file.
- The ``renames.py`` file has the rename dictionary that is pointed to by the entrypoint in our ``setup.cfg``.
- It is only loaded when running ``bin/zodbupdate``, because this is the only code that looks for the entrypoint.
- As a side effect, when the entrypoint is loaded we also register the dexterity utility when available.
  This code is executed simply because it also is in the ``__init__.py`` file.
