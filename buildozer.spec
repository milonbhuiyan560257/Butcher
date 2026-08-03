[app]

title = Voucher Scanner
package.name = voucherscanner
package.domain = org.milonbhuiyan
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,txt,csv
version = 1.1.0
requirements = python3,kivy,pillow,requests
orientation = portrait
fullscreen = 0
android.permissions = CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET
android.api = 34
android.minapi = 24
android.archs = arm64-v8a
android.accept_sdk_license = True
log_level = 2

[buildozer]

log_level = 2
warn_on_root = 1
