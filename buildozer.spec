[app]
title = DirectorIA
package.name = directorai
package.domain = org.director.ai
source.dir = .
source.include_exts = py,png,jpg,kv,json,txt
version = 1.0

# Adicionei 'requests' aqui, que é o que seu main.py usa
requirements = python3,kivy,requests,idna,certifi

orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 34
android.minapi = 26
android.sdk = 34
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a,armeabi-v7a

log_level = 2
warn_on_root = 0

[buildozer]
log_level = 2
warn_on_root = 0





