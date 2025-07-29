# Fandango, functional tools for Tango Control System

Fandango ("functional" programming for Tango) is a Python library for 
developing functional and multithreaded control applications and scripts.
It is mostly (but not only) used in the scope of Tango Control System and 
PANIC Alarm System projects.

Fandango is available at:

- github: https://gitlab.com/tango-controls/fandango/
- pypi: https://pypi.python.org/pypi/fandango

```python
  pip install fandango
```

## Description

Fandango was developed to simplify the configuration of big control systems; implementing the behavior of Jive (configuration) and/or Astor (deployment) tools in methods that could be called from scripts using regexp and wildcards.

It has been later extended with methods commonly used in some of our python API's (archiving, CCDB, alarms, vacca) or generic devices (composers, simulators, facades).

Fandango python modules provides functional methods, classes and utilities to develop high-level device servers and APIs for Tango control system.

Fandango is published using the same licenses than other TANGO projects; the license will be kept up to date in the [LICENSE](<https://github.com/tango-controls/fandango/blob/documentation/LICENSE>) file.

For more comprehensive documentation:

- http://pythonhosted.org/fandango/

Checkout for more updated recipes at:

- https://github.com/tango-controls/fandango/blob/documentation/doc/recipes

## Windows

FANDANGO IS TESTED ON LINUX ONLY, WINDOWS/MAC MAY NOT BE FULLY SUPPORTED IN MASTER BRANCH

## Authors

Fandango library was originally written by Sergi Rubio Manrique for the ALBA Synchrotron. Later authors will be acknowledged in the [AUTHORS](https://github.com/tango-controls/fandango/blob/documentation/AUTHORS) file.

## Features

This library provides submodules with utilities for PyTango device servers and applications written in python:

<table>
<tr>
	<th>Module</th>
	<th>Description</th>
</tr>
<tr>
	<td>fandango.functional</td>
	<td>functional programming, data format conversions, caseless regular expressions</td>
</tr>
<tr>
	<td>fandango.tango</td>
	<td>tango api helper methods, search/modify using regular expressions</td>
</tr>
<tr>
	<td>fandango.dynamic</td>
	<td>dynamic attributes, online python code evaluation</td>
</tr>
<tr>
	<td>fandango.server</td>
	<td>Astor-like python API</td>
</tr>
<tr>
	<td>fandango.device</td>
	<td>some templates for Tango device servers.</td>
</tr>
<tr>
	<td>fandango.interface</td>
	<td>device server inheritance</td>
</tr>
<tr>
	<td>fandango.db</td>
	<td>MySQL access</td>
</tr>
<tr>
	<td>fandango.dicts fandango.arrays</td>
	<td>advanced containers, sorted/caseless list/dictionaries, .csv parsing</td>
</tr>
<tr>
	<td>fandango.log</td>
	<td>Logging</td>
</tr>
<tr>
	<td>fandango.objects</td>
	<td>object templates, singletones, structs</td>
</tr>
<tr>
	<td>fandango.threads</td>
	<td>serialized hardware access, multiprocessing</td>
</tr>
<tr>
	<td>fandango.linos</td>
	<td>some linux tricks</td>
</tr>
<tr>
	<td>fandango.web</td>
	<td>html parsing</td>
</tr>
<tr>
	<td>fandango.qt</td>
	<td>some custom Qt classes, including worker-like threads.</td>
</tr>
</table>

## Main Classes

- DynamicDS/DynamicAttributes
- ServersDict
- TangoEval
- ThreadDict/SingletoneWorker
- TangoInterfaces(FullTangoInheritance) 

 
## Where it is used

Several PyTango APIs and device servers use Fandango modules:

- PyTangoArchiving
- PyPLC
- SplitterBoxDS
- PyStateComposer
- PySignalSimulator
- PyAlarm
- CSVReader
 
## Requirements

- The functional, object submodules doesn't have any dependency
- It requires PyTango to use tango, device, dynamic and callback submodules
- Some submodules have its own dependencies (Qt,MySQL), so they are always imported within try,except clauses. 

## Downloading

Fandango module is available from github (>=T9) and sourceforge (<=T9):

```sh
git clone https://github.com/tango-controls/fandango
```
```sh
svn checkout https://tango-cs.svn.sourceforge.net/svnroot/tango-cs/share/fandango/trunk fandango.src
```

## Warranty

See [WARRANTY](https://github.com/tango-controls/fandango/blob/documentation/WARRANTY) file.

## Developers and Contributors

### GitLab pipeline

GitLab pipeline is configured with `.gitlab-ci.yml` to run automatic tests on new commits.
Here's the description of the pipeline configuration:

```yml
# Full reference on gitlab pipeline configuration:
# https://docs.gitlab.com/ee/ci/yaml/

# Keyword values defined here will apply to all jobs
default:
  interruptible: true

# Stages used often are: build, test, deploy
# Stages will be running in the defined order
# One stage can have multiple jobs
# All jobs contained in one stage will run in parallel
stages:
  - test

# A job definition
# Jobs with names starting with dot are only templates
# Templates will not be executed and have to be extended
.prepare_tests:
  # Each job is executed inside a docker container
  image: continuumio/miniconda3:latest
  # Define variables used in this job
  variables:
    CPPTANGO_VERSION: '9.3.4'
    PYTANGO_VERSION: '9.3.3'
  # This job will run ONLY on those branches
  only:
    - master
    - develop
    - /^feature/.*/
  # This job will be executed in test stage
  stage: test
  # Before the "main" script of the job is executed, this will run
  before_script:
    - conda init bash
    - source /root/.bashrc
    - conda create --prefix ./envs/fandango -y python=$PYTHON_VERSION
    - conda activate ./envs/fandango
    - conda install --yes -c tango-controls cpptango=$CPPTANGO_VERSION
    - conda install --yes -c tango-controls pytango=$PYTANGO_VERSION
    - conda install --yes future
    - conda install --yes -c conda-forge pytest pytest-freezegun pytz
  # Script doing the main work of the job
  script:
    - pip install -e .
    - python setup.py generate_tests
    - pytest --color=yes -v "./ci/tests/test_functional.py" ./ci/tests/test_functional_auto.py ./ci/tests/test_objects_manual.py

# Job definition
python27:
  # This job inherits all keywords from extended job
  # So the script that will be run is defined in extended job
  extends: .prepare_tests
  # Some variables specific only to this job
  # Other variables will not be overwriten
  variables:
    PYTHON_VERSION: '2.7'

python36:
  extends: .prepare_tests
  variables:
    PYTHON_VERSION: '3.6'
  # Define on which branches we don't want to run this job
  except:
    - feature/pre-futurize
    - /^feature/.*-py2/
```

## Workflow

<em>Preliminary Documentation Sketch</em>

<table>
<tr><th>Authors</th></tr>
<tr><td>Celary Mateusz</td></tr>
<tr><td>Rubio Sergio</td></tr>
</table>

Case:
- We need to define workflow allowing deploying new features/fixes to master branch
- Workflow have to consider python2 and python3 code compatibility
- It have to be possible to work on new features/fixes at the same time developing tests for old features

Qestions:

Q: How often new features/fixes have to be pushed to master?
A: Usually 1 per month. Sometimes 1 a week if necessary

### Branching strategy

Main points:
- If we write new features, make it python3 compatible right away
- It's too complicated to write first on python2 branch, then merge to python3, then to master
- Pipeline will be configured with one `.gitlab-ci.yml` so on branch master it can pass with python2 tests only
- Different docker images used to run tests for python2 and python3 on pipelines
- Use conda to switch between python2 and python3 and run `pytest` separately

Branches:
- `master` - Will always and only have latest official release. Each merge will trigger new package. Next major release == fandango 15 == porting to python3. If there is a really important bugfix needed we just backport as described on diagram.
- `v14` - Current branch `develop` will be renamed `v14` and it will be used for applying backports. 
- `v15` - Treat this branch will be de-facto new `develop` branch for py2+py3 fandango version. We runed `futurize` on this code, so the code here should be python3 compatible. We develop all tests here and use conda to switch between python2 and python3 to test. There is slight possibility to have in mind that `futurize` script could break something even for python2 - discussion in "problems". Python2 compatibility will be limited to newer systems (Debian 9 and newer).
- `vXX` - next major releases develop
- `features/some-feature` - new features should be developed on separate branches branched from `v15`. Eg. `features/new_ci_config`. Code need to be developed for new major release in mind, compatible with both python2 and python3. It's best to add tests along with new features to prevent mess. Once ready, should be merged to `v15`.
- `backports/v14_feature_name` - for backporting branched from `v14`
- `hotfix/issue-number` - for bugfixes, branched from v15, merged to v15, then cherry-picked to master
- `features/tests-py2` - This branch will not be used anymore.

Example branching diagram:

![branching](./doc/img/branching.drawio.png)
<center><em>Branching strategy for Fandango</em></center>

Problems:
- Small possibility that `futurize` script broke something for python2. The only possibility is make sure 100% before new major release it's working with python2 and python3 BUT it would be something we ned to do anyway if we want to have fully python3 compatible package

Deployment:
- It's possible to have `pip` and `conda` packages published with setup GitLab pipeline for fandango

Drawio template from [here](https://gist.githubusercontent.com/bryanbraun/8c93e154a93a08794291df1fcdce6918/raw/bf563eb36c3623bb9e7e1faae349c5da802f9fed/template-data.xml).

## Autogenerated tests

For simple functions and methods, it's possible to autogenerate the tests in form of:
```python
...
assert f(x1, x2, x3) == result
```

All autogenerated tests are in `tests` directory and have `_auto_gen` suffix.

To define the tests to be autogenerated, add them to the `tests` dictionary in `tests/definitions.py` file.

### Defining tests

The general syntax for defining tests for autogeneration i like below.

```
tests = {
    'fandango.module.<function.|class.submethod|class::static_method>': { #fully qualified name of the method or function to be tested
        'case1': { #individual test suffix (see example below)
            'docs': "explain the test case",
            'params': ( #the same test will be run for each tuple in params
                # args - arguments to pass to the method/function
                # kwargs - named arguments to pass to the method/function
                # init_args - arguments to pass to instance/class __init__ when being tested
                # init_args - named arguments to pass to instance/class __init__ when being tested
                # result - result for each test params (have to be the same type of what function that is tested returns)
                (args, kwargs, init_args, init_kwargs, result),
                (args, kwargs, init_args, init_kwargs, result),
                ...
            },
        '': { #if this is empty string, we dont use suffix for test name (see example)
                ...
            }
        }
}
```

#### Examples

This definition
```   
tests = {
        'fandango.functional.floor': {
            '': {
                'docs': 'This is my test docs'
                'params': (
                    ((2.3,), {}, 2),
                    ((), {"x": 2.3, "unit": 1.1}, 2.2),
                )
            }
        }
}
```

will generate test named test_floor_auto_gen inside file /test/test_functional.py .
This test will be ran two times, once with args (2.3,) asserting result 2,
second time with kwargs {"x": 2.3, "unit": 1.1} asserting result 2.2.
The test itself will be documented with 'This is my test docs'.

The following definition:

```
tests = {
        'fandango.functional.floor': {
        'suffix': {
            'docs': 'This is my test documentation'
            'params': (
                ((2.3,), {}, 2),
                ((), {"x": 2.3, "unit": 1.1}, 2.2),
            )
        }
}
```

will give the same, except the name of the test will be test_floor_suffix.

#### Skipping tests

You can also define function that you want to skip in testing.

```
skip_tests = [ 'module.function' ] # methods/classes to not test
```

### Generating the tests

Gitlab CI/CD pipeline automatically generates the tests from their definitions.
However, you can do it yourself by running:

```python3 setup.py generate_tests```

in the project root directory.
