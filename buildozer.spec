[app]

# (str) Title of your application
title = DirectorIA

# (str) Package name
package.name = directoria

# (str) Package domain (needed for android/ios packaging)
package.domain = org.directoria

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,jpeg,gif,kv,json,ttf

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy,requests
requirements = python3,kivy,requests,urllib3,certifi,idna,charset-normalizer

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientations
# Valid options are: landscape, portrait, portrait-reverse or landscape-reverse
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

#
# Android specific
#

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Android Activity
# use that parameter together with android.entrypoint to set custom Java class instead of PythonActivity
#android.activity_class_name = org.kivy.android.PythonActivity

# (str) Extra xml to write directly inside the <manifest> element of AndroidManifest.xml
# use that parameter to provide a filename from where to load your custom XML code
#android.extra_manifest_xml = ./src/android/extra_manifest.xml

# (str) Full name including package path of the Java class that implements Python Service
# use that parameter to set custom Java class instead of PythonService
#android.service_class_name = org.kivy.android.PythonService

# (str) Android app theme, default is ok for Kivy-based app
# android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) Pattern to whitelist for the whole project
#android.whitelist =

# (str) Path to a custom whitelist file
#android.whitelist_src =

# (str) Path to a custom blacklist file
#android.blacklist_src =

# (list) Android additional libraries to copy
#android.add_libs_armeabi = libs/android/armeabi/*.so
#android.add_libs_armeabi_v7a = libs/android/armeabi-v7a/*.so
#android.add_libs_arm64_v8a = libs/android/arm64-v8a/*.so
#android.add_libs_x86 = libs/android/x86/*.so
#android.add_libs_x86_64 = libs/android/x86_64/*.so

# (bool) decides whether to use p4a or gradlew for building
# Default is p4a
#android.enable_androidx = True

# (bool) whether to skip the Java compilation
#android.skip_update = False

# (bool) If True, then skip trying to update the Android sdk
#android.skip_update = False

# (bool) If True, then skip trying to update the Android ndk
#android.skip_update = False

# (bool) If True, then automatically accept SDK license
#agreed_android_sdk_licenses = False

# (bool) If True, then compile the app for arm64-v8a only
#android.arch = arm64-v8a

# (list) Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Androidx (Jetpack) library support
android.enable_androidx = True

# (str) The build tools version to use.
#android.build_tools_version = '33.0.2'

# (str) The Android gradle plugin version.
#android.gradle_version = '7.4.2'

# (str) Path to build tool constraints
#android.gradle_dependencies = 

# (str) The path to the keystore file
#android.keystore =

# (str) The alias of the key in the keystore
#android.keyalias =

# (str) The password of the keystore
#android.keystore_password =

# (str) The password of the key in the keystore
#android.keyalias_password =

# (bool) Choose whether to use aapt2 or aapt
#android.use_aapt2 = True

# (str) Name of the sqlite database (deprecated)
#android.database =

# (str) A comma-separated list of sqlite tables (deprecated)
#android.tables =

# (str) The path to a .keystore file for signing
#android.keystore =

# (str) The name of the key to use for signing
#android.keyalias =

# (str) Password for the keystore
#android.keystore_password =

# (str) Password for the key
#android.keyalias_password =

# (str) The path to an added jar file
#android.add_jars =

# (str) The path to an added aar file
#android.add_aars =

# (str) The path to the res folder
#android.res =

# (str) The path to the libs folder
#android.libs =

# (str) The path to the assets folder
#android.assets =

# (str) The path to the src folder
#android.src =

# (str) The path to the java folder
#android.java =

# (str) The path to the jni folder
#android.jni =

# (str) The path to the python-for-android folder
#android.p4a_dir =

# (str) The branch of python-for-android to use
#android.p4a_branch = master

# (str) The path to the SDK
#android.sdk_path =

# (str) The path to the NDK
#android.ndk_path =

#
# Python for android (p4a) specific
#

# (str) python-for-android URL to use for download
#p4a.url =

# (str) python-for-android fork to use in case if p4a.url is not specified, defaults to upstream (kivy)
#p4a.fork = kivy

# (str) python-for-android branch to use, defaults to master
#p4a.branch = master

# (str) python-for-android specific commit to use, defaults to HEAD, must be within p4a.branch
#p4a.commit = HEAD

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
#p4a.source_dir =

# (str) The directory in which to place the p4a build directory
#p4a.build_dir = ./.buildozer/android/platform/build

# (str) The directory in which to place the p4a distribution directory
#p4a.dist_dir = ./.buildozer/android/app

# (str) The directory in which to place the p4a build-requirements directory
#p4a.local_recipes =

# (str) Filename to the hook for p4a
#p4a.hook =

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (int) port number to specify an explicit port for the p4a build
#p4a.port =

# Control passing the --use-setup-py vs --ignore-setup-py to p4a
# In the past, this was always --use-setup-py, but this has been
# deprecated. Set this to False to use --ignore-setup-py.
p4a.setup_py = false


#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_dir = ../kivy-ios
# Alternately, specify the URL and branch of a git checkout:
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

# Another platform dependency: ios-deploy
# Uncomment to use a custom checkout
#ios.ios_deploy_dir = ../ios_deploy
# Or specify URL and branch
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0

# (bool) Whether or not to sign the IPA
ios.codesign.allowed = false

# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: buildozer ios list_identities
#ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) The development team to use for signing the debug version
#ios.codesign.development_team.debug = <hexstring>

# (str) Name of the certificate to use for signing the release version
#ios.codesign.release = %(ios.codesign.debug)s

# (str) The development team to use for signing the release version
#ios.codesign.development_team.release = <hexstring>

# (str) URL pointing to .ipa file to be installed
# This option should be defined along with `display_image_url` and `full_size_image_url` options.
#ios.manifest.app_url =

# (str) URL pointing to an icon (57x57px) to be displayed during download
# This option should be defined along with `app_url` and `full_size_image_url` options.
#ios.manifest.display_image_url =

# (str) URL pointing to an icon (512x512px) to be displayed during download
# This option should be defined along with `app_url` and `display_image_url` options.
#ios.manifest.full_size_image_url =


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin

#    -----------------------------------------------------------------------------
#    List as sections
#
#    You can define all the "list" as [section:key].
#    Each line will be considered as an option.
#    This is useful for options that need to be passed to the build command.
#    -----------------------------------------------------------------------------

#
# Command line section
#

# (list) Source files to include (let empty to include all the files)
#source.include_exts = py,png,jpg,kv,atlas

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
# Do not prefix with './'
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (bool) Whether Android artifact should be exported as a bundle
#android.bundle.enable_uncompressed_native_libs = False

# (bool) enables Androidx (Jetpack) library support
#android.enable_androidx = True

#    -----------------------------------------------------------------------------
#    Profiles
#
#    You can extend configuration options by adding a [profile:xxx] section.
#    They will be applied when using --profile xxx as an argument.
#    -----------------------------------------------------------------------------

#    -----------------------------------------------------------------------------
#    (str) The release channel to use when building the APK/AAB
#    -----------------------------------------------------------------------------
#    Valid values are: stable, beta, dev, canary
#    Default is stable
#release_channel = stable
