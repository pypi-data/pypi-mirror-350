Changes
=======

4.1 (2025-05-27)
----------------

- Add support for Python 3.12, 3.13.

- Drop support for Python 3.7, 3.8.


4.0 (2023-07-11)
----------------

- Drop support for Python 2.7, 3.5, 3.6.

- Add support for Python 3.9, 3.10, 3.11.

- Adapt code to ``zope.site >= 4.4`` thus requiring at least that version.
  (`#7 <https://github.com/zopefoundation/grokcore.site/pull/7>`_)

3.1 (2020-09-02)
----------------

- Fix DeprecationWarnings.

- Drop support for Python 3.4 and add support for 3.7 and 3.8.

3.0.3 (2018-01-12)
------------------

- Rearrange tests such that Travis CI can pick up all functional tests too.

3.0.2 (2018-01-11)
------------------

- Do not import `getSite` from `zope.site.hooks` anymore but from
  `zope.component.hooks`.

3.0.1 (2018-01-10)
------------------

- Fix dependencies by removing ZODB3.

3.0.0 (2018-01-05)
------------------

- Python 3 compatibility.

1.8 (2016-09-21)
----------------

- When removing a site make sure reference are removed from the parent
  site.

1.7.1 (2016-01-29)
------------------

- Update tests.

1.7 (2015-06-11)
----------------

- Add a new directive ``install_on`` that is usable on a site. This
  directive let you customize when (namely the event) to install the
  configured local sites.

- Rename ``ApplicationInitializedEvent`` to ``ApplicationAddedEvent``.

- When the ``IApplicationAddedEvent`` is triggered the new application
  will be current Zope local site. The site is restored after the
  event.

1.6.1 (2012-05-02)
------------------

- Exposed ApplicationInitializedEvent and IApplicationInitializedEvent.

- Added the missing import for the exposed IApplication interface.

1.6 (2012-05-01)
----------------

- Moved the directive `site` from Grok to this package.

- Moved the component `Application` and all the related utilities from Grok
  to this package.

1.5 (2011-01-03)
----------------

- Moved IApplication and getApplication from the Grok package into
  this one.

1.4 (2010-11-01)
----------------

- Upped versions requirements for martian and grokcore.component.

1.3 (2010-10-18)
----------------

- Made package comply to repository policy.

- Update functional tests to only use zope.app.appsetup instead
  of zope.app.testing.

- Update functional tests not to require zope.app.zcmlfiles
  anymore.

1.2 (2009-12-20)
----------------

* Migrated imports from zope.app.component to zope.site.

1.1 (2009-09-18)
----------------

* Updated dependencies (added missing ones and added separate test
  dependencies).

* A local utility now implements IAttributeAnnotatable.

* Update code documentation from Grok itself.

* Use 1.0b2 versions.cfg in Grok's release info instead of a local
  copy; a local copy for all grokcore packages is just too hard to
  maintain.


1.0.1 (2009-06-30)
------------------

* Reupload to pypi with a correct version of Python which doesn't have
  a distutils bug.

1.0 (2009-06-29)
----------------

* Created ``grokcore.site`` by factoring local site based components,
  grokkers and directives out of Grok.
