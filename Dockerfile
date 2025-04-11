FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV ANDROID_HOME=/opt/android-sdk
ENV PATH=$PATH:$ANDROID_HOME/cmdline-tools/tools/bin:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$ANDROID_HOME/tools

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    curl wget unzip git default-jdk \
    libgl1-mesa-dev qemu-kvm \
    libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 libxi6 \
    libx11-6 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxrandr2 libxss1 libxtst6 libasound2 \
    && apt-get clean

# Удаление старых Node.js, установка 18
RUN apt-get remove -y nodejs npm || true
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Установка Appium
RUN npm install -g appium

# Установка Python-зависимостей
COPY requirements.txt /app/
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r /app/requirements.txt

# Установка Android SDK и AVD
RUN mkdir -p ${ANDROID_HOME}/cmdline-tools && \
    curl -o sdk.zip https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip && \
    unzip sdk.zip -d ${ANDROID_HOME}/cmdline-tools && \
    mv ${ANDROID_HOME}/cmdline-tools/cmdline-tools ${ANDROID_HOME}/cmdline-tools/tools && \
    yes | sdkmanager --licenses && \
    sdkmanager \
      "platform-tools" \
      "emulator" \
      "platforms;android-30" \
      "build-tools;30.0.3" \
      "system-images;android-30;google_apis;x86"

RUN echo "no" | avdmanager create avd -n test -k "system-images;android-30;google_apis;x86"

# Копирование проекта
COPY . /app
WORKDIR /app

# Копирование entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
