# Open Innovation MLOps Client API

Welcome to the Open Innovation MLOps Client API documentation! This guide offers detailed instructions on how to install, set up, and use the client library.

## Deployment

To publish the package on Pypi run the manual step `deploy_on_pypi` on the pipeline.

The credentials for the upload are in the variables
- `PYPI_USERNAME`
- `PYPI_PASSWORD`

Set on the [CI/CD Variables page](https://gitlab.com/openinnovationai/platform/mlops/librairies/tracking-client/-/settings/ci_cd).

## Release process

To release a new package version:
- Bump the version in `setup.py`
- Commit and push the changes
- Trigger the pipeline steps `publish_on_gitlab` and `publish_on_pypi`

## Documentation

Public documentation is in the file [README.public.md](README.public.md).

## Manual build

To build the package run `python setup.py sdist bdist_wheel`.