
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

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy,requests,urllib3,certifi,idna,charset-normalizer

# (str) Supported orientations
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

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use.
android.ndk_api = 21

# (list) Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Androidx (Jetpack) library support
android.enable_androidx = True

# ✅ LINHA ADICIONADA PARA ACEITAR LICENÇAS AUTOMATICAMENTE
android.accept_sdk_license = True

#
# Python for android (p4a) specific
#

# Control passing the --use-setup-py vs --ignore-setup-py to p4a
p4a.setup_py = false

#
# iOS specific
#

ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0
ios.codesign.allowed = false

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0
