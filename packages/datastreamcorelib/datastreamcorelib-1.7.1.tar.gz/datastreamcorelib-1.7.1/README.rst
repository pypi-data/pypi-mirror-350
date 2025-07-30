=================
datastreamcorelib
=================

Core helpers and Abstract Base Classes for making use of ZMQ nice, easy and DRY.

You should probably look at https://gitlab.com/advian-oss/python-datastreamservicelib and
https://gitlab.com/advian-oss/python-datastreamserviceapp_template unless you're working
on an adapter for yet unsupported eventloop.

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

    docker build --ssh default --target devel_shell -t datastreamcorelib:devel_shell .
    docker create --name datastreamcorelib_devel -v `pwd`":/app" -it -v /tmp:/tmp `echo $DOCKER_SSHAGENT` datastreamcorelib:devel_shell
    docker start -i datastreamcorelib_devel

pre-commit considerations
^^^^^^^^^^^^^^^^^^^^^^^^^

If working in Docker instead of native env you need to run the pre-commit checks in docker too::

    docker exec -i datastreamcorelib_devel /bin/bash -c "pre-commit install --install-hooks"
    docker exec -i datastreamcorelib_devel /bin/bash -c "pre-commit run --all-files"

You need to have the container running, see above. Or alternatively use the docker run syntax but using
the running container is faster::

    docker run -it --rm -v `pwd`":/app" datastreamcorelib:devel_shell -c "pre-commit run --all-files"

Test suite
^^^^^^^^^^

You can use the devel shell to run py.test when doing development, for CI use
the "tox" target in the Dockerfile::

    docker build --ssh default --target tox -t datastreamcorelib:tox .
    docker run -it --rm -v `pwd`":/app" `echo $DOCKER_SSHAGENT` datastreamcorelib:tox

Production docker
^^^^^^^^^^^^^^^^^

There's a "production" target since it's our standard pattern, however this library does not yet
expose any CLI tools so the production target is kinda useless.

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
    pre-commit install --install-hooks
    pre-commit run --all-files

- Ready to go.

Use Python 3.9 for development since it's the lowest supported version so you don't accidentally
use features only available in higher versions and then have to re-do everything when CI tests fail
on 3.9.

Remember to activate your virtualenv whenever working on the repo, this is needed
because pylint and mypy pre-commit hooks use the "system" python for now (because reasons).

Running "pre-commit run --all-files" and "py.test -v" regularly during development and
especially before committing will save you some headache.
