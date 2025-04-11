#!/bin/bash
set -e

echo "➡️  Запуск эмулятора..."
nohup emulator -avd test -no-audio -no-window -gpu swiftshader_indirect -no-boot-anim &

echo "⏳ Ожидание запуска эмулятора..."
adb wait-for-device
BOOT_COMPLETED=""
until [[ "$BOOT_COMPLETED" == "1" ]]; do
  BOOT_COMPLETED=$(adb shell getprop sys.boot_completed 2>/dev/null | tr -d '\r')
  sleep 1
done
echo "✅ Эмулятор загружен"

echo "🚀 Запуск Appium..."
nohup appium --base-path /wd/hub > /app/appium.log 2>&1 &

echo "⏳ Ожидание старта Appium..."
until curl --output /dev/null --silent --head --fail http://127.0.0.1:4723/wd/hub; do
    sleep 1
done
echo "✅ Appium работает"

echo "🧪 Запуск тестов..."
pytest automation_framework/tests --html=automation_framework/tests/logs/report.html

exec "$@"
