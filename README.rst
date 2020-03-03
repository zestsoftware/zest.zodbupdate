zest.zodbupdate
===============

zodbupdate rename dictionary and dexterity patch for Plone 5.2 projects.

See `post on community.plone.org <https://community.plone.org/t/zodbverify-porting-plone-with-zopedb-to-python3/8806/13>`_.
And the `Plone ZODB Python 3 migration docs <https://docs.plone.org/manage/upgrading/version_specific_migration/upgrade_zodb_to_python3.html>`_.


Quick usage
-----------

In a simplified ``buildout.cfg``::

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
    eggs =
        zodbupdate
        zest.zodbupdate
        ${instance:eggs}

Run ``bin/buildout`` and then ``bin/zodbupdate -f var/filestorage/Data.fs``.


Use case and process
--------------------

You want to migrate your Plone 5.2 database from Python 2.7 to Python 3.
You use the zodbverify and zodbupdate tools for this.
When you first run ``bin/zodbverify`` or ``bin/instance zodbverify``, you may see warnings and exceptions.
It may warn about problems that zodbupdate will fix.
So the idea is now:

1. First with Python 2.7, run ``bin/zodbupdate -f var/filestorage/Data.fs``
   So *no* python3 convert stuff!
   This will detect and apply several explicit and implicit rename rules.

2. Then run ``bin/instance zodbverify``.
   If this still gives warnings or exceptions,
   you may need to define more rules and apply them with zodbupdate.

3. When all is well, on Python 3 run::

     bin/zodbupdate --convert-py3 --file=var/filestorage/Data.fs --encoding utf8

4. For good measure, on Python 3 run ``bin/instance zodbverify``.

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

Here is the rename dictionary from the `master branch <https://github.com/zestsoftware/zest.zodbupdate/blob/master/src/zest/zodbupdate/renames.py>`_.
The warnings and exceptions mentioned above are handled here.
Each version of this package may have different contents.

Note that I have seen several warnings that are not handled but that seem innocent.
I choose to ignore them.
These are some warnings because of a missing ``webdav`` (removed in Zope 4.0, reintroduced in 4.3)::

    Warning: Missing factory for webdav.interfaces IDAVResource
    Warning: Missing factory for webdav.interfaces IFTPAccess
    Warning: Missing factory for webdav.interfaces IDAVCollection


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

- This package only has an ``__init__.py`` file.
- It has the rename dictionary pointed to by the entrypoint in our ``setup.cfg``.
- It is only loaded when running ``bin/zodbupdate``, because this is the only code that looks for the entrypoint.
- As a side effect, when the entrypoint is loaded we also register the dexterity utility when available.
  This code is executed simply because it also is in the ``__init__.py`` file.
