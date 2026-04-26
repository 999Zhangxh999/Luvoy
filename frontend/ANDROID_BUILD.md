# 律途 Luvoy - Android APK 打包指南

## 📋 前置要求

1. **Java JDK 17+** - Android开发必需
   - 下载地址: https://adoptium.net/
   
2. **Android Studio** (可选但推荐)
   - 下载地址: https://developer.android.com/studio
   - 或者只安装 Android SDK Command-line Tools

3. **环境变量配置**
   ```
   JAVA_HOME = C:\Program Files\Eclipse Adoptium\jdk-17.x.x
   ANDROID_HOME = C:\Users\<用户名>\AppData\Local\Android\Sdk
   ```

## 🚀 快速打包

### 方式一：命令行打包（推荐）

1. **打包Debug版APK**（无需签名，用于测试）
   ```bash
   cd frontend
   npm run build:apk
   ```
   
   APK位置: `frontend/android/app/build/outputs/apk/debug/app-debug.apk`

2. **打包Release版APK**（需要签名）
   ```bash
   npm run build:apk:release
   ```

### 方式二：Android Studio打包

1. 打开Android Studio
2. 运行以下命令在Android Studio中打开项目：
   ```bash
   npm run cap:android
   ```
3. 等待Gradle同步完成
4. 菜单 Build → Build Bundle(s) / APK(s) → Build APK(s)
5. APK生成在 `android/app/build/outputs/apk/`

## 📱 安装测试

1. **USB安装**
   - 手机开启USB调试
   - 连接电脑
   - 运行: `adb install app-debug.apk`

2. **直接安装**
   - 将APK传输到手机
   - 手机设置允许安装未知来源应用
   - 点击APK安装

## 🔐 发布签名（正式发布必需）

1. **生成签名密钥**
   ```bash
   keytool -genkey -v -keystore luvoy-release.keystore -alias luvoy -keyalg RSA -keysize 2048 -validity 10000
   ```

2. **配置签名信息**
   
   编辑 `android/app/build.gradle`:
   ```gradle
   android {
       signingConfigs {
           release {
               storeFile file("luvoy-release.keystore")
               storePassword "你的密码"
               keyAlias "luvoy"
               keyPassword "你的密码"
           }
       }
       buildTypes {
           release {
               signingConfig signingConfigs.release
           }
       }
   }
   ```

## 📦 输出文件

- **Debug APK**: `android/app/build/outputs/apk/debug/app-debug.apk`
- **Release APK**: `android/app/build/outputs/apk/release/app-release.apk`

## 🔧 常见问题

### Gradle下载慢
编辑 `android/gradle/wrapper/gradle-wrapper.properties`，使用国内镜像：
```
distributionUrl=https://mirrors.cloud.tencent.com/gradle/gradle-8.x-all.zip
```

### SDK版本问题
编辑 `android/app/build.gradle` 调整:
```gradle
android {
    compileSdk 35
    defaultConfig {
        minSdk 22
        targetSdk 35
    }
}
```

### 打包体积过大
项目已启用代码分割，APK大小约 8-15MB 是正常的

## 📞 技术支持

如遇问题，请检查：
1. Java版本是否正确 (`java -version`)
2. ANDROID_HOME环境变量是否配置
3. Gradle是否能正常下载依赖

---
**律途 · Luvoy** - Life's Unique Voyage
