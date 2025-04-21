# ---- مرحله run ----
FROM eclipse-temurin:17-jdk

# دایرکتوری کاری داخل کانتینر
WORKDIR /app

# کپی فایل jar ساخته‌شده از مرحله package
COPY target/*.jar app.jar

# پورت برنامه (در صورت نیاز)
EXPOSE 8080

# دستور اجرای برنامه
ENTRYPOINT ["java", "-jar", "app.jar"]

