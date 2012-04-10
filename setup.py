from distutils.core import setup
setup(
  name='django_autologin',
  version='0.1',
  packages=['django_autologin', 'django_autologin.templatetags'],
  install_requires=['django>=1.0'],
  description='Token generator and processor to provide automatic login links for users'
)
