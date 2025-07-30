# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_alembic',
 'pytest_alembic.plugin',
 'pytest_alembic.tests',
 'pytest_alembic.tests.experimental']

package_data = \
{'': ['*']}

install_requires = \
['alembic', 'pytest>=7.0', 'sqlalchemy']

entry_points = \
{'pytest11': ['pytest_alembic = pytest_alembic.plugin']}

setup_kwargs = {
    'name': 'pytest-alembic',
    'version': '0.12.1',
    'description': 'A pytest plugin for verifying alembic migrations.',
    'long_description': '![Github Actions Build](https://github.com/schireson/pytest-alembic/actions/workflows/build.yml/badge.svg)\n[![codecov](https://codecov.io/gh/schireson/pytest-alembic/branch/master/graph/badge.svg)](https://codecov.io/gh/schireson/pytest-alembic)\n[![Documentation Status](https://readthedocs.org/projects/pytest-alembic/badge/?version=latest)](https://pytest-alembic.readthedocs.io/en/latest/?badge=latest)\n\nSee the full documentation [here](https://pytest-alembic.readthedocs.io/en/latest/).\n\n## Introduction\n\nA pytest plugin to test alembic migrations (with default tests) and\nwhich enables you to write tests specific to your migrations.\n\n```bash\n$ pip install pytest-alembic\n$ pytest --test-alembic\n\n...\n::pytest_alembic/tests/model_definitions_match_ddl <- . PASSED           [ 25%]\n::pytest_alembic/tests/single_head_revision <- . PASSED                  [ 50%]\n::pytest_alembic/tests/up_down_consistency <- . PASSED                   [ 75%]\n::pytest_alembic/tests/upgrade <- . PASSED                               [100%]\n\n============================== 4 passed in 2.32s ===============================\n```\n\n## The pitch\n\nHave you ever merged a change to your models and you forgot to generate\na migration?\n\nHave you ever written a migration only to realize that it fails when\nthere’s data in the table?\n\nHave you ever written a **perfect** migration only to merge it and later\nfind out that someone else merged also merged a migration and your CD is\nnow broken!?\n\n`pytest-alembic` is meant to (with a little help) solve all these\nproblems and more. Note, due to a few different factors, there **may**\nbe some [minimal required\nsetup](http://pytest-alembic.readthedocs.io/en/latest/setup.html);\nhowever most of it is boilerplate akin to the setup required for alembic\nitself.\n\n### Built-in Tests\n\n- **test_single_head_revision**\n\n  Assert that there only exists one head revision.\n\n  We’re not sure what realistic scenario involves a diverging history to\n  be desirable. We have only seen it be the result of uncaught merge\n  conflicts resulting in a diverged history, which lazily breaks during\n  deployment.\n\n- **test_upgrade**\n\n  Assert that the revision history can be run through from base to head.\n\n- **test_model_definitions_match_ddl**\n\n  Assert that the state of the migrations matches the state of the\n  models describing the DDL.\n\n  In general, the set of migrations in the history should coalesce into\n  DDL which is described by the current set of models. Therefore, a call\n  to `revision --autogenerate` should always generate an empty migration\n  (e.g.\xa0find no difference between your database (i.e.\xa0migrations\n  history) and your models).\n\n- **test_up_down_consistency**\n\n  Assert that all downgrades succeed.\n\n  While downgrading may not be lossless operation data-wise, there’s a\n  theory of database migrations that says that the revisions in\n  existence for a database should be able to go from an entirely blank\n  schema to the finished product, and back again.\n\n- [Experimental\n  tests](http://pytest-alembic.readthedocs.io/en/latest/experimental_tests.html)\n\n  - all_models_register_on_metadata\n\n    Assert that all defined models are imported statically.\n\n    Prevents scenarios in which the minimal import of your models in your `env.py`\n    does not import all extant models, leading alembic to not autogenerate all\n    your models, or (worse!) suggest the deletion of tables which should still exist.\n\n  - downgrade_leaves_no_trace\n\n    Assert that there is no difference between the state of the database pre/post downgrade.\n\n    In essence this is a much more strict version of `test_up_down_consistency`,\n    where the state of a MetaData before and after a downgrade are identical as\n    far as alembic (autogenerate) is concerned.\n\n  These tests will need to be enabled manually because their semantics or API are\n  not yet guaranteed to stay the same. See the linked docs for more details!\n\nLet us know if you have any ideas for more built-in tests which would be\ngenerally useful for most alembic histories!\n\n### Custom Tests\n\nFor more information, see the docs for [custom\ntests](http://pytest-alembic.readthedocs.io/en/latest/custom_tests.html)\n(example below) or [custom static\ndata](http://pytest-alembic.readthedocs.io/en/latest/custom_data.html)\n(to be inserted automatically before a given revision).\n\nSometimes when writing a particularly gnarly data migration, it helps to\nbe able to practice a little timely TDD, since there’s always the\npotential you’ll trash your actual production data.\n\nWith `pytest-alembic`, you can write tests directly, in the same way\nthat you would normally, through the use of the `alembic_runner`\nfixture.\n\n```python\ndef test_gnarly_migration_xyz123(alembic_engine, alembic_runner):\n    # Migrate up to, but not including this new migration\n    alembic_runner.migrate_up_before(\'xyz123\')\n\n    # Perform some very specific data setup, because this migration is sooooo complex.\n    # ...\n    alembic_engine.execute(table.insert(id=1, name=\'foo\'))\n\n    alembic_runner.migrate_up_one()\n```\n\n`alembic_runner` has a number of methods designed to make it convenient\nto change the state of your database up, down, and all around.\n\n## Installing\n\n```bash\npip install "pytest-alembic"\n```\n',
    'author': 'Dan Cardin',
    'author_email': 'ddcardin@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/schireson/pytest-alembic',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4',
}


setup(**setup_kwargs)
