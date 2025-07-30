====================
datastreamservicelib
====================

AsyncIO eventloop helpers and Abstract Base Classes for making services that use ZMQ nice, easy and DRY

Usage
-----

Use the CookieCutter template at https://gitlab.com/advian-oss/python-datastreamserviceapp_template

You can also take a look at src/datastreamservicelib/console.py for some very simple test examples.

Docker
------

For more controlled deployments and to get rid of "works on my computer" -syndrome, we always
make sure our software works under docker.

It's also a quick way to get started with a standard development environment.

SSH agent forwarding
^^^^^^^^^^^^^^^^^^^^

We need buildkit_::

    export DOCKER_BUILDKIT=1

.. _buildkit: https://docs.docker.com/develop/develop-images/build_enhancements/

And also the exact way for forwarding agent to running instance is different on OSX::

    export DOCKER_SSHAGENT="-v /run/host-services/ssh-auth.sock:/run/host-services/ssh-auth.sock -e SSH_AUTH_SOCK=/run/host-services/ssh-auth.sock"

and Linux::

    export DOCKER_SSHAGENT="-v $SSH_AUTH_SOCK:$SSH_AUTH_SOCK -e SSH_AUTH_SOCK"

Creating a development container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Build image, create container and start it::

    docker build --ssh default --target devel_shell -t datastreamservicelib:devel_shell .
    docker create --name datastreamservicelib_devel -v `pwd`":/app" -it -v /tmp:/tmp `echo $DOCKER_SSHAGENT` datastreamservicelib:devel_shell
    docker start -i datastreamservicelib_devel

pre-commit considerations
^^^^^^^^^^^^^^^^^^^^^^^^^

If working in Docker instead of native env you need to run the pre-commit checks in docker too::

    docker exec -i datastreamservicelib_devel /bin/bash -c "pre-commit install"
    docker exec -i datastreamservicelib_devel /bin/bash -c "pre-commit run --all-files"

You need to have the container running, see above. Or alternatively use the docker run syntax but using
the running container is faster::

    docker run -it --rm -v `pwd`":/app" datastreamservicelib:devel_shell -c "pre-commit run --all-files"

Test suite
^^^^^^^^^^

You can use the devel shell to run py.test when doing development, for CI use
the "tox" target in the Dockerfile::

    docker build --ssh default --target tox -t datastreamservicelib:tox .
    docker run -it --rm -v `pwd`":/app" `echo $DOCKER_SSHAGENT` datastreamservicelib:tox

Production docker
^^^^^^^^^^^^^^^^^

There's a "production" target as well for quick running of testsubscriber and testpublisher

    docker build --ssh default --target production -t datastreamservicelib:latest .
    docker run --rm -it -v /tmp:/tmp datastreamservicelib:latest testpublisher -s ipc:///tmp/test_pub.sock -t foo
    docker run --rm -it -v /tmp:/tmp datastreamservicelib:latest testsubscriber -s ipc:///tmp/test_pub.sock -t foo

Note that on non-linux platforms the IPC sockets may not as expected between host and container over volume mounts.


Local Development
-----------------

TLDR:

- Create and activate a Python 3.9 virtualenv (assuming virtualenvwrapper)::

    mkvirtualenv -p `which python3.9` my_virtualenv

- change to a branch::

    git checkout -b my_branch

- install Poetry: https://python-poetry.org/docs/#installation
- Install project deps and pre-commit hooks::

    poetry install
    pre-commit install
    pre-commit run --all-files

- Ready to go, try the following::

    testpublisher --help
    testsubscriber --help

Use Python 3.9 for development since it's the lowest supported version so you don't accidentally
use features only available in higher versions and then have to re-do everything when CI tests fail
on 3.9.

Remember to activate your virtualenv whenever working on the repo, this is needed
because pylint and mypy pre-commit hooks use the "system" python for now (because reasons).

Running "pre-commit run --all-files" and "py.test -v" regularly during development and
especially before committing will save you some headache.
