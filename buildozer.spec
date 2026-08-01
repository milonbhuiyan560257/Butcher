[app]

title = Voucher Scanner

package.name = voucherscanner
package.domain = org.milonbhuiyan

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,json,txt

version = 1.0

requirements = python3,kivy,pillow,openpyxl

orientation = portrait

fullscreen = 0

icon.filename = assets/icon.png

presplash.filename = assets/logo.png

android.permissions = CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.api = 34
android.minapi = 24

android.archs = arm64-v8a

android.accept_sdk_license = True

log_level = 2

[buildozer]

warn_on_root = 1
