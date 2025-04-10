FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    curl wget unzip git openjdk-11-jdk \
    python3 python3-pip \
    nodejs npm \
    libgl1-mesa-dev \
    qemu-kvm \
    && apt-get clean

# Установка Appium
RUN npm install -g appium

# Установка Android SDK
ENV ANDROID_HOME /opt/android-sdk
ENV PATH ${PATH}:${ANDROID_HOME}/cmdline-tools/tools/bin:${ANDROID_HOME}/platform-tools:${ANDROID_HOME}/emulator:${ANDROID_HOME}/tools

RUN mkdir -p ${ANDROID_HOME}/cmdline-tools \
    && curl -o sdk.zip https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip \
    && unzip sdk.zip -d ${ANDROID_HOME}/cmdline-tools \
    && mv ${ANDROID_HOME}/cmdline-tools/cmdline-tools ${ANDROID_HOME}/cmdline-tools/tools \
    && yes | sdkmanager --licenses \
    && sdkmanager "platform-tools" "platforms;android-30" "build-tools;30.0.3" "system-images;android-30;google_apis;x86" "emulator"

# Создание AVD
RUN echo "no" | avdmanager create avd -n test -k "system-images;android-30;google_apis;x86"

# Запуск Appium по умолчанию
CMD ["appium"]
