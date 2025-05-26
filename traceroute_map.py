import os
import re
import requests
import folium

# اجرای tracert و گرفتن IPها
output = os.popen("tracert www.google.com").read()

# پیدا کردن IPها
ips = re.findall(r"\d+\.\d+\.\d+\.\d+", output)

print("IPهایی که از مسیر بسته‌ها به‌دست اومدن:")
print(ips)

# گرفتن مختصات برای هر IP
locations = []

for ip in ips:
    print(f"در حال بررسی IP: {ip}")
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
       
        # بررسی وضعیت درخواست و صحت داده‌های مختصات
        if res['status'] == 'success' and res['lat'] != 0 and res['lon'] != 0:
            latlng = [res['lat'], res['lon']]
            print(f"مکان برای {ip}: {latlng}")
            locations.append(latlng)
        else:
            print(f"مکان برای {ip} پیدا نشد یا مختصات معتبر نیست.")
    except Exception as e:
        print(f"خطا در پردازش {ip}: {e}")

# نمایش نقشه
if locations:
    print("در حال ساخت نقشه...")
    m = folium.Map(location=locations[0], zoom_start=4)
   
    for i in range(len(locations)):
        folium.Marker(locations[i], tooltip=f"Hop {i+1}").add_to(m)
        if i < len(locations) - 1:
            folium.PolyLine([locations[i], locations[i+1]], color="blue").add_to(m)

    m.save("map.html")
    print("نقشه با موفقیت ذخیره شد.")
else:
    print("هیچ مختصاتی برای نمایش وجود ندارد.")
