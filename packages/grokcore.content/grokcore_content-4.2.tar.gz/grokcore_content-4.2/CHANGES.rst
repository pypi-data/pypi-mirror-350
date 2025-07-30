Changes
=======

4.2 (2025-05-27)
----------------

- Add support for Python 3.12, 3.13.

- Drop support for Python 3.7, 3.8.


4.1 (2023-08-28)
----------------

- Drop support for deprecated ``python setup.py test``.


4.0 (2023-08-28)
----------------

- Add support for Python 3.7, 3.8, 3.9, 3.10, 3.11.

- Drop support for Python 2.7, 3.4, 3.5, 3.6.


3.0.2 (2018-01-12)
------------------

- Rearrange tests such that Travis CI can pick up all functional tests too.

3.0.1 (2018-01-10)
------------------

- Fix dependencies by removing ZODB3.

3.0.0 (2018-01-04)
------------------

- Use ``zope.interface.implementer`` decorator instead of
  ``zope.interface.implements`` with classes to support Python 3.

- Express support for Python 2.7, 3.4 and 3.5 and 3.6,

- Use tox for test orchestration.

1.3.1 (2016-01-29)
------------------

- Update tests.

1.3 (2015-09-30)
----------------

- Fix updateOrder that would create a new PersistentList object in the
  database each time the order is updated.

1.2 (2015-04-01)
----------------

- Introduce ObjectEditedEvent which is meant to used when the
  attribute of an object are edited. This makes possible to easily
  distinguish it from generic and container modification operations.

- Fix a bug where the OrderedContainer could get corrupted in case
  updateOrder() would have been called with a list containing multiple
  occurrences of a existing key in the mapping.

1.1 (2010-11-01)
----------------

- Use newer grokcore.component.

- Made package comply to zope.org repository policy.

1.0 (2010-02-06)
----------------

- Created ``grokcore.content`` in January 2010 by factoring basic
  component base classes out of Grok.
