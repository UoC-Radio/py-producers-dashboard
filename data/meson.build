# Compiling the resources
VCS_TAG = ''
if get_option('profile') != 'default'
  git = find_program('git', required : false)
  if git.found()
    VCS_TAG = run_command('git', 'rev-parse', '--short', 'HEAD').stdout().strip()
  endif
  if VCS_TAG == ''
    VCS_TAG = '-devel'
  else
    VCS_TAG = '-@0@'.format(VCS_TAG)
  endif
endif
about_dialog_conf = configuration_data()
about_dialog_conf.set('PACKAGE_VERSION', '@0@@1@'.format(meson.project_version(), VCS_TAG))
about_dialog_conf.set('PACKAGE_URL', PACKAGE_URL)
about_dialog_conf.set('PROGRAM_NAME', 'Dashboard' + NAME_SUFFIX)
about_dialog_conf.set('APPID', APPLICATION_ID)

gnome.compile_resources(
  PROJECT_RDNN_NAME,
  PROJECT_RDNN_NAME + '.gresource.xml',
  gresource_bundle: true,
  source_dir: '.',
  install_dir: PKGDATA_DIR,
  install: true,
  dependencies: configure_file(
    input: 'AboutDialog.ui.in',
    output: 'AboutDialog.ui',
    configuration: about_dialog_conf
  )
)

# Installing the schema file
install_data(
  PROJECT_RDNN_NAME + '.gschema.xml',
  install_dir: 'share/glib-2.0/schemas'
)

