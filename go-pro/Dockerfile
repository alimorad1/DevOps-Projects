# استفاده از یک تصویر پایه برای Go
FROM golang:1.20 as builder

# تنظیم دایرکتوری کاری
WORKDIR /app

# کپی کردن فایل‌های پروژه
COPY . .

# نصب وابستگی‌ها و ساخت فایل اجرایی
RUN go mod tidy
RUN go build -o myapp main.go

# تصویر نهایی که فقط فایل اجرایی را شامل می‌شود
FROM alpine:latest

WORKDIR /root/

COPY --from=builder /app/myapp .

CMD ["./myapp"]

