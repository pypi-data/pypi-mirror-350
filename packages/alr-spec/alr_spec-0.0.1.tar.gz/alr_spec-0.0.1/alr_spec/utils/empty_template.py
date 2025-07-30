import sys

file = """name=example
version=1.0.0
release=1
epoch=0
desc=Description
homepage=https://example.com
maintainer="Name Surname <email@example.com>"
# or 'all' for noarch
architectures=('amd64')
license=('custom:proprietary')
provides=()
conflicts=()
deps=()
build_deps=()
opt_deps=()
auto_prov=0
auto_req=0
replaces=()
sources=()
checksums=()
backup=()
scripts=(
  ['preinstall']='preinstall.sh'
  ['postinstall']='postinstall.sh'
  ['preremove']='preremove.sh'
  ['postremove']='postremove.sh'
  ['preupgrade']='preupgrade.sh'
  ['postupgrade']='postupgrade.sh'
  ['pretrans']='pretrans.sh'
  ['posttrans']='posttrans.sh'
)

prepare() {
    echo "PREPARE"
}
build() {
    echo "BUILD"
}
package() {
    echo "PACKAGE"
}
files() {
    echo ./usr/bin/example
}
"""


def create_from_empty_template(output_file):
    try:
        with open(output_file, "w") as f:
            f.write(file)
        print(f"Файл успешно записан в {output_file}.")
    except IOError as e:
        print(f"Ошибка при записи файла: {e}")
        sys.exit(1)
