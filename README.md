<p align="center">
  <img width="100" src="https://i.imgur.com/4gUaVKW.png">
  <br>
<h1 align="center">Version managment package</h1>
</p>

<p align="center">
  <br>
  <img width="800" src="https://i.imgur.com/dwmhs3v.png">
  <br>
</p>

**Contents**

- [General Information](#general-information)
  - [What it does?](#what-it-does)
  - [Key features](#key-features)
- [Installation Guide](#installation-guide)
- [Usage](#usage)
  - [Prerequisitions](#prerequisitions)
  - [Start Stamping](#start-stamping)
  - [Release Candidates](#release-candidates)
  - [Show](#show)
  - [Goto](#goto)
- [Advanced Features](#advanced-features)
  - [Root Apps](#root-apps)
  - [Configuration](#configuration)


## General Information
A simple package for auto increasing version numbers of any application agnostic to language or architecture.

`vmn` is compliant with `Semver` (https://semver.org) semantics

### What it does?
`vmn` is a CLI tool for handling project versioning needs.

`vmn` can also be used like a Python library.

Go ahead and read `vmn`'s docs :)

### Key features

- [x] Stamping of versions of type: **`major`. `minor`.`patch`** , e.g.,` 1.6.0` [`Semver` compliant]
- [x] Stamping of versions of type: `major`. `minor`.`patch`**-`prerelease`** , e.g.,` 1.6.0-rc23` [`Semver` compliant]
- [x] Stamping of versions of type: `major`. `minor`.`patch`.**`hotfix`** , e.g.,` 1.6.7.4` [`Semver` extension]
- [x] Bringing back the repository / repositories state to the state they were when the project was stamped (see [`goto`](https://github.com/final-israel/vmn#goto) section)
- [x] Stamping of micro-services-like project topologies (see [`Root apps`](https://github.com/haimhm/vmn/blob/master/README.md#root-apps) section)
- [x] Stamping of a project depending on multiple git repositories (see [`Configuration: deps`](https://github.com/haimhm/vmn/blob/master/README.md#configuration) section)
- [x] Version auto-embedding into supported backends (`npm`, `cargo`) during the `vmn stamp` phase (see [`Version auto-embedding`](https://github.com/haimhm/vmn/blob/master/README.md#version-auto-embedding) section)
- [ ] `WIP` Addition of `buildmetadata` for an existing version, e.g.,` 1.6.0-rc23+build01.Info` [`Semver` compliant]
- [ ] `WIP` Addition of `releasenotes` for an existing version [`Semver` extension]
- [ ] `WIP` Support "root apps" that are located in different repositories

## Installation Guide
```sh
pip3 install vmn
```

## Usage
### Help support
`vmn` and all its subactions suppurts `--help` so use it when needed for forther explations

### Prerequisitions
```sh
# Change Directory Into Your Git Repository
cd to/your/repository

# Needed Only Once Per Repository.
vmn init
```
### Init App
Needed Only Once Per App-Name (Multiple App-Name can be exist under one Repository)
```
vmn init-app [-h] [-v VERSION] [--dry-run] <App-Name>                        
```
|     Argument Name                    | Mendatory / Optional  | Description                                                  |
| :----------------------------------: | --------------------- | ------------------------------------------------------------ |
|     `<App-Name>`                     | Mendatory | The application's name to initialize version tracking for |
|     `-h, --help`                     | Optional  | show this help message and exit                            |
|     `-v VERSION, --version VERSION`  | Optional  | The version to init from. Must be specified in the raw version format: {major}.{minor}.{patch}   |


#### exmple for usages
```
vmn init-app test-vmn
# The starting version is 0.0.0

## Example for starting other app in the same repository from version 1.6.8
vmn init-app -v 1.6.8 other-test
```

### Stamp
```
vmn stamp [-h] [-r] [--pr PR] [--pull] [--dont-check-vmn-version] [--orv ORV] [--ov OV] [--dry-run] [-e EXTRA_COMMIT_MESSAGE] name

positional arguments:
  name                  The application's name

optional arguments:
  -h, --help            show this help message and exit
  -r , --release-mode   major / minor / patch / hotfix
  --pr PR, --prerelease PR
                        Prerelease version. Can be anything really until you decide to release the version
  --pull
  --dont-check-vmn-version
  --orv ORV, --override-root-version ORV
                        Override current root version with any integer of your choice
  --ov OV, --override-version OV
                        Override current version with any version in the format: ^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:\.(?P<hotfix>0|[1-9]\d*))?$
  --dry-run
  -e EXTRA_COMMIT_MESSAGE, --extra-commit-message EXTRA_COMMIT_MESSAGE
                        add more information to the commit message.example: adding --extra-commit-message '[ci-skip]' will add the string '[ci-skip]' to the commit message
```


#### exmple for usages
```sh
# To Increace The Version To Version 0.0.1
vmn stamp -r patch <app-name>

# To Increace The Version To Version 1.7.0
vmn stamp -r minor <App-Name2>
```
##### Note:
`init-app` and `stamp` both support `--dry-run` flag

### Release Candidates

`vmn` supports `Semver`'s `prerelease` notion of version stamping, enabling you to release non-mature versions and only then release the final version.

```sh
# will start from 1.6.8
vmn init-app -v 1.6.8 <app-name>

# will stamp 2.0.0-alpha1
vmn stamp -r major --pr alpha <app-name>

# will stamp 2.0.0-alpha2
vmn stamp --pr alpha <app-name>

# will stamp 2.0.0-mybeta1
vmn stamp --pr mybeta <app-name>

# Run release when you ready - will stamp 2.0.0 (from the same commit)
vmn release -v 2.0.0-mybeta1 <app-name>
```
### Show

Use `vmn show` for displaying version information of previous `vmn stamp` commands

```sh
vmn show <app-name>
vmn show --verbose <app-name>
vmn show -v 1.0.1 <app-name>
```

### Goto 

Similar to `git checkout` but also supports checking out all configured dependencies. This way you can easily go back to the **exact** state of you entire code for a specific version even when multiple git repositories are involved. 

```sh
vmn goto -v 1.0.1 <app-name>
```

## Why `vmn` is agnostic to application language?
It is the application's responsibility to actually set the version number at build time. The version string can be retrieved from
```sh
vmn show <app-name>
```
and be embedded via a custom script to the application's code during its build phase. `vmn` supports auto-embedding the version string during the `vmn stamp` phase for popular backends (see **`Version auto-embedding`** section above).

### Version auto-embedding

| Backend | Description |
| :-: | :-: |
| ![alt text](https://user-images.githubusercontent.com/5350434/136626161-2a7bdc4a-5d42-4012-ae42-b460ddf7ea88.png) | Will embed Semver version string to your `package.json` file during the `vmn stamp` command |
| ![alt text](https://user-images.githubusercontent.com/5350434/136626484-0a8e4890-42f1-4437-b306-28f190d095ee.png) | Will embed Semver version string to your `Cargo.toml` file during the `vmn stamp` command |

## Advanced Features
### Root Apps

`vmn` supports stamping of something called a "root app" which can be useful for managing version of multiple services that are logically located under the same solution. 

##### For example:

```sh
vmn init-app my_root_app/service1
vmn stamp -r patch my_root_app/service1
```

```sh
vmn init-app my_root_app/service2
vmn stamp -r patch my_root_app/service2
```

```sh
vmn init-app my_root_app/service3
vmn stamp -r patch my_root_app/service3
```

Next we'll be able to use `vmn show` to display everything we need:

`vmn show --verbose my_root_app/service3`

```yml
vmn_info:
  description_message_version: '1'
  vmn_version: <the version of vmn itself that has stamped the application>
stamping:
  msg: 'my_root_app/service3: update to version 0.0.1'
  app:
    name: my_root_app/service3
    _version: 0.0.1
    release_mode: patch
    prerelease: release
    previous_version: 0.0.0
    stamped_on_branch: master
    changesets:
      .:
        hash: 8bbeb8a4d3ba8499423665ba94687b551309ea64
        remote: <remote url>
        vcs_type: git
    info: {}
  root_app:
    name: my_root_app
    version: 5
    latest_service: my_root_app/service3
    services:
      my_root_app/service1: 0.0.1
      my_root_app/service2: 0.0.1
      my_root_app/service3: 0.0.1
    external_services: {}
```

`vmn show my_root_app/service3` will output `0.0.1`

`vmn show --root my_root_app` will output `5`

### Configuration
`vmn` auto generates a `conf.yml` file that can be modified later by the user. 

An example of a possible `conf.yml` file:

```yaml
# Autogenerated by vmn. You can edit this configuration file
conf:
  template: '[{major}][.{minor}]'
  deps:
    ../:
      <repo dir name>:
        vcs_type: git
  extra_info: false
  create_verinfo_files: false
  hide_zero_hotfix: true
  version_backends: 
    npm:
      path: "relative_path/to/Cargo.toml"
```



|         Field          | Description                                                  | Example                                                      |
| :--------------------: | ------------------------------------------------------------ | ------------------------------------------------------------ |
|       `template`       | The template configuration string can be customized and will be applied on the "raw" vmn version.<br/>`vmn` will display the version based on the `template`. | `vmn show my_root_app/service3` will output `0.0` <br/>however running:<br/>`vmn show --raw my_root_app/service3` will output `0.0.1` |
|         `deps`         | In `deps` you can specify other repositories as your dependencies and `vmn` will consider them when stamping and performing `goto`. | See example `conf.yml` file above                            |
|      `extra_info`      | Setting this to `true` will make `vmn` output usefull data about the host on which `vmn` has stamped the version.<br/>**`Note`** This feature is not very popular and may be remove / altered in the future. | See example `conf.yml` file above                            |
| `create_verinfo_files` | Tells `vmn` to create file for each stamped version. `vmn show --from-file` will work with these files instead of working with `git tags`. | See example `conf.yml` file above                            |
|   `hide_zero_hotfix`   | Tells `vmn` to hide the fourth version octa when it is equal to zero. This way you will never see the fourth octa unless you will specifically stamp with `vmn stamp -r hotfix`. `True` by default. | See example `conf.yml` file above                            |
|   `version_backends`   | Tells `vmn` to auto-embed the version string into one of the supported backends' files during the `vmn stamp` command. For instance, `vmn` will auto-embed the version string into `package.json` file if configured for `npm` projects. | See example `conf.yml` file above                            |



[![codecov](https://codecov.io/gh/final-israel/vmn/branch/master/graph/badge.svg)](https://codecov.io/gh/final-israel/vmn)
