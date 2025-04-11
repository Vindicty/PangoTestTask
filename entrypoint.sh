#!/bin/bash
set -e

echo "➡️  Запуск эмулятора..."
nohup emulator -avd test -no-audio -no-window -gpu swiftshader_indirect -no-boot-anim -no-snapshot -no-metrics > /app/emulator.log 2>&1 &

echo "⏳ Ожидание запуска эмулятора..."
adb wait-for-device
BOOT_COMPLETED=""
until [[ "$BOOT_COMPLETED" == "1" ]]; do
  BOOT_COMPLETED=$(adb shell getprop sys.boot_completed 2>/dev/null | tr -d '\r')
  sleep 1
done
echo "✅ Эмулятор загружен"

echo "🚀 Запуск Appium..."
nohup appium --address 0.0.0.0 --port 4723 --base-path /wd/hub > /app/appium.log 2>&1 &

echo "⏳ Ожидание старта Appium..."
until curl --silent http://127.0.0.1:4723/wd/hub/status || curl --silent http://0.0.0.0:4723/wd/hub/status; do
    sleep 1
done
echo "✅ Appium работает"

echo "📄 Последние 20 строк лога Appium:"
tail -n 20 /app/appium.log || true

echo "🧪 Запуск тестов..."
pytest automation_framework/tests --html=automation_framework/tests/logs/report.html || true

exec "$@"
