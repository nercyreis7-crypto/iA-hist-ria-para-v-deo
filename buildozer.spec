[app]

# Título do seu app
title = DirectorAI
package.name = directorai
package.domain = org.director.ai

# Arquivos fonte
source.dir = .
source.include_exts = py,png,jpg,kv,json,txt

version = 1.0

# REQUISITOS CORRIGIDOS (A IA do Google precisa destas dependências)
requirements = python3,kivy,google-generativeai,grpcio,setuptools,openssl,idna,certifi

# Orientação e tela
orientation = portrait
fullscreen = 0

# PERMISSÕES OBRIGATÓRIAS (Para a IA funcionar)
android.permissions = INTERNET,WAKE_LOCK

# Configurações de API (Mantidas conforme o seu original)
android.api = 34
android.minapi = 26
android.sdk = 34
android.ndk = 25b
android.accept_sdk_license = True
android.wakelock = True
android.archs = arm64-v8a,armeabi-v7a

# Logs e configurações técnicas
log_level = 2
warn_on_root = 0

[buildozer]
log_level = 2
warn_on_root = 0




