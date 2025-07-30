AC_INIT

AC_CHECK_PROGS([MAKE], [make], [no])
AS_IF([test "$MAKE" == "no"], 
      [AC_MSG_NOTICE([without GNU Make, you have to inspect 'Makefile' and deduce build targets yourself.])])

AC_CHECK_PROGS([M4], [m4], [no])
AS_IF([test "$M4" == "no"], 
      [AC_MSG_NOTICE([without GNU M4, you will be unable to generate bitbucket-pipelines.yml.])])

AC_CHECK_PROGS([GIT], [git], [no])
AS_IF([test "$GIT" == "no"], 
      [AC_MSG_ERROR([install Git, before continuing.])])

AC_CHECK_PROGS([PYTHON3], [python3], [no])
AS_IF([test "$PYTHON3" == "no"],
      [AC_MSG_ERROR([install Python 3, before continuing.])])

AC_CHECK_PROGS([PIPENV], [pipenv], [no])
AS_IF([test "$PIPENV" == "no"],
      [AC_MSG_ERROR([install pipenv (pip) package, before continuing.

Alternatively bootstrap a venv:

    python3 -m venv --system-site-packages .venv
    .venv/bin/python3 -m pip install pipenv

Then execute this script through pipenv:

    .venv/bin/python -m pipenv run sh ./configure
])])

# required in Makefile to ensure proper path resolution during preprocessing
# realpath is not available on macOS
AC_CHECK_PROGS([REALPATH], [realpath], [no])
AS_IF([test "$REALPATH" == "no"], 
      [AC_MSG_ERROR([set a persistent alias for 'realpath', before continuing, e.g.

alias='python3 -c "import pathlib,sys;print(pathlib.Path(sys.argv[[1]]).resolve())"'"
])])

AC_MSG_CHECKING([for TWINE_PASSWORD])
if test -z "$TWINE_PASSWORD"; then
    AC_MSG_RESULT([no])
    AC_MSG_WARN([
TWINE_PASSWORD must be set to an API token of a PyPI account.
])
else
    AC_MSG_RESULT([yes])
fi

AC_MSG_CHECKING([for BITBUCKET_ACCESS_TOKEN])
if test -z "$BITBUCKET_ACCESS_TOKEN"; then
    AC_MSG_RESULT([no])
    AC_MSG_WARN([BITBUCKET_ACCESS_TOKEN not set])
else
    AC_MSG_RESULT([yes])
fi


sh -ex << 'EOF'
uname
git --version
python3 --version
python3 -m pip --version
python3 -m pipenv --version
EOF

AC_MSG_NOTICE([initializing pipenv...])
sh -exc 'python3 -m pipenv install -d -v --skip-lock'

AC_OUTPUT
