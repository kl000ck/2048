#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_root"

APPIMAGETOOL="${APPIMAGETOOL:-appimagetool}"
if ! command -v "$APPIMAGETOOL" >/dev/null 2>&1; then
    echo "Не найден appimagetool. Укажите его так:" >&2
    echo "    APPIMAGETOOL=/путь/к/appimagetool $0" >&2
    exit 1
fi

if [ ! -x dist/2048-linux-x86_64 ]; then
    echo "Сначала соберите dist/2048-linux-x86_64 с помощью PyInstaller." >&2
    exit 1
fi

appdir="build/2048.AppDir"
rm -rf "$appdir"
mkdir -p \
    "$appdir/usr/bin" \
    "$appdir/usr/share/applications" \
    "$appdir/usr/share/icons/hicolor/512x512/apps"

install -m 755 dist/2048-linux-x86_64 "$appdir/usr/bin/2048"
install -m 644 assets/2048.png "$appdir/2048.png"
ln -sf 2048.png "$appdir/.DirIcon"
install -m 644 assets/2048.png \
    "$appdir/usr/share/icons/hicolor/512x512/apps/2048.png"
install -m 644 packaging/2048.desktop "$appdir/2048.desktop"
install -m 644 packaging/2048.desktop \
    "$appdir/usr/share/applications/2048.desktop"
install -m 755 packaging/AppRun "$appdir/AppRun"

ARCH="${ARCH:-x86_64}" "$APPIMAGETOOL" "$appdir" dist/2048-x86_64.AppImage
