[app]

# (str) Title of your application
title = Voucher Scanner

# (str) Package name
package.name = voucherscanner

# (str) Package domain (needed for android/ios packaging)
package.domain = org.milonbhuiyan

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,json,txt,xlsx

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# python3,kivy,pillow,openpyxl,pytesseract — tesseract needs special recipe for Android
requirements = python3,kivy,pillow,openpyxl,pytesseract

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (str) Presplash of the application
presplash.filename = assets/logo.png

# (str) Icon of the application
icon.filename = assets/icon.png

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET

# (int) Target Android API
android.api = 34

# (int) Minimum API required
android.minapi = 24

# (int) Android SDK version to use
#android.sdk = 34

# (str) Android NDK version to use
#android.ndk = 25b

# (list) Android ABIs
android.archs = arm64-v8a, armeabi-v7a

# (bool) Accept Android SDK license
android.accept_sdk_license = True

# (str) Android entry point
#android.entrypoint = org.kivy.android.PythonActivity

# (list) Pattern to whitelist for the whole project
#android.whitelist =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
# android.skip_update = False

# (str) The format used to package the app for release mode (aab or apk or aar).
# android.release_artifact = aab

# (str) The format used to package the app for debug mode (apk or aar).
# android.debug_artifact = apk

# (int) Loglevel
log_level = 2

# (int) Buildozer log level (0 = error only, 1 = info, 2 = debug)
# buildozer.loglevel = 1

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
