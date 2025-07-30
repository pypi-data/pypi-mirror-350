# Ardhi Framework
Ardhi Framework is a framework built for those who want rigid land systems on top of Django. 

### Main features:
- Rigid security framework and libraries that control requests and responses
- Data screening and masking of sensitive information per the role of the user
- Secured land records through hashed models and secured fields
- Cryptography on trial
- Full logging of indelible records for land transactions
- Land files and secured parcel history records
- All user activity, preconfigured and without ability to override

## Requirements
- Django (version>=4.0)
- Django Rest Framework (version >= 2.1)
- Python (version >= 3.9)

These versions are <strong>highly</strong> regulated from the framework itself. And you will rarely need to install them seperately.
If you have your django project already initialized, confirm the compatible Ardhi version to use before installation.

## Installation
Install using ```pip``` to install all required packages.
```shell
pip install ardhi-framework
```
Add ```'ardhi_framework'``` to your ```INSTALLED_APPS``` setting.

```shell
INSTALLED_APPS = [
...
'ardhi_framework',
]
```

## Quickstart
Check out tutorial to easily start off with our framework





