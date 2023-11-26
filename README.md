# dnf_repo - Ansible Role

An Ansible role for managing YUM / DNF repository configuration files (.repo).

Some repositories are predefined in this role repository
for easy installation.

## Usage

```yaml
# in your playbook
...
roles:
- role: dnf_repo
  vars:
    dnf_repos: ["epel"]
    dnf_repos_proxy: "http://192.168.0.1:3128"
```

## supported OSs

| Distribution | Major Version |
| ------------ | ------------- |
| RedHat (EL)  | 9, 8          |

## Pre-defined repositories

| Name     | Site       |
| -------- | ---------- |
| `epel`   | https://docs.fedoraproject.org/en-US/epel/ |
| `elrepo` | https://elrepo.org/tiki/HomePage |

## variables

### `dnf_repos` - repository names to install


These repositories are installed with this role.

The default is `[]` (empty list, nothing to install).

The repository to install must be specified as
an item in `dnf_repos_settings`
or `dnf_repos_settings_presets[].settings`.


```yaml
dnf_repos: ["epel", "elrepo"]
```

### `dnf_repos_proxy` - a proxy url to set .repo files

A proxy URL for accessing repositories via YUM / DNF.

This itself has no effect on the settings,
but some repository settings that are defined in this role,
are refer to this variable as the proxy setting.

### `dnf_repos_settings` - user defined repository settings

User-defined repository settings.
Settings for NOT predefined repositories are set in this variable.

The format of the settings must follow this example.

```yaml
dnf_repos_settings:
# This sample "epel" is predefined.
# You should not redefine in `dnf_repos_settings`
- name: epel
  rpm_url: https://dl.fedoraproject.org/pub/epel/epel-release-latest-{{ ansible_distribution_major_version }}.noarch.rpm
  gpg_key_url: "https://dl.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-{{ ansible_distribution_major_version }}"
  repofiles:
    - "/etc/yum.repos.d/epel.repo"
    - "/etc/yum.repos.d/epel-testing.repo"
    - "/etc/yum.repos.d/epel-cisco-openh264.repo"
  proxy: "{{ dnf_repos_proxy }}"
  validate_certs: true
  override: {}
  patches:
  - file: ["/etc/yum.repos.d/epel-testing.repo"]
    section: ["epel-testing"]
    settings:
      baseurl: http://download.fedoraproject.org/pub/epel/testing/{{ ansible_distribution_major_version }}/$basearch
      metalink: ~

```

| key           | Required? | description  |
| ------------- | --------- | ------------ |
| `name`        | Required  | A name of the repository. |
| `rpm_url`     | Required  | A URL of a RPM package |
| `gpg_key_url` | Optional  | A URL of a GPG key |
| `repofiles`   | Required  | .repo file paths to be installed. `proxy` settings are appended on these files. |
| `proxy`       | Optional  | A proxy URL to access this repository. To use shared config, set `"proxy: {{dnf_repos_proxy}}"` |
| `validate_certs` | Optional | Whether to verify the repository's certificates. |
| `override`    | Optional  | Force overrided settings (obsoluted). |
| `patches`    | Optional   | Override settings for specific sections in repo files. |
