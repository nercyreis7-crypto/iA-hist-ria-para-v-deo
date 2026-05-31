
[app]
title = DirectorIA
package.name = directoria
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 0.1

requirements = python3,kivy,requests,idna,certifi,urllib3

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.grant_permissions = 1

orientation = portrait
fullscreen = 0
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

android.build_tools_version = 34.0.0

[buildozer]
log_level = 2
warn_on_root = 0
bin_dir = .
