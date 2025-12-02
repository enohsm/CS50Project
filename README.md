# VISA & GREENCARD MANAGEMENT SYSTEM

A web-based management system for visa appointment requests, green card insurance processes, and user passport/vehicle data. Includes admin and employee interfaces with role-based access control.

## Table of Contents
- [ENGLISH](#english)
- [Instructions](#instructions)
- [Setup](#setup)
- [Usage](#usage)
- [Notes](#notes)
- [License](#license)

---

## İçerik Tablosu
- [TÜRKÇE](#türkçe)
- [Yönergeler](#yönergeler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Notlar](#notlar)
- [Lisans](#lisans)

###### ENGLISH ######

### INSTRUCTIONS

#### Setup

1. First, to ensure the project works correctly on your computer, open the terminal in the working directory and run:
    ```bash
    pip install -r requirements.txt

    Your terminal must be located in the same directory as the files.
    ```
2. For the mail-sending system to work, you must configure the mail settings inside "app.py" and "/routes/dashboard_routes.py". (You can search for "setmailsetting" using CTRL+F. Mailtrap was used for testing.)

#### Usage

1. To run the application, navigate your terminal to the project directory and enter this code:
    ```bash
    python app.py
    ```
2. Open your web browser and go to:
    ```bash
    127.0.0.1:8080
    ```
3. You can see news and announcements at the homepage.
4. On the page that opens, create an account using the sign-up section in the upper right corner.
5. Then log in.
6. Using the quick-access menu on the left side, you can access "My Passports", "My Vehicles", and "My Requests".
7. My Passports section:
    - Enter the My Passports section.
    - Your existing passports will be displayed on the page.
    - Passport viewing, adding, editing (cannot be edited after approval), and deleting operations are carried out in this area.
    - Users can register only the passports that belong to them. Passport information is matched with the details provided during registration.
    - If there is an active visa appointment request associated with your passport, it cannot be edited or deleted.
8. My Vehicles section:
    - Enter the My Vehicles section.
    - Your existing vehicles will be displayed on the page.
    - Vehicle adding, editing, deleting, and license document viewing operations are carried out in this area.
    - If there is an active green card insurance request associated with your vehicle, it cannot be edited or deleted.
9. My Requests section:
    - Enter the My Requests section.
    - On the page that opens, your last 5 visa appointment requests and last 5 green card insurance requests will be displayed.
    - If you wish, you can create a new visa appointment request or a new green card insurance request from this page.
    - To view all your visa appointment requests and manage them, click the "Show More" button under the "Visa Requests" table:
    - On the page that opens, all your visa appointment requests will be displayed.
    - From here, you can check the status of your visa requests, edit those that have not yet been processed, or cancel them.
    - To view all your green card insurance requests and manage them, click the "Show More" button under the "Green Card Insurance Requests" table:
    - On the page that opens, all your green card insurance requests will be displayed.
    - From here, you can check the status of your requests, edit unprocessed requests, or cancel them.
10. To experience the employee and admin interface, log in using the information below:

| Role     | Username | Password | ID No       |
| -------- | -------- | -------- | ----------- |
| Admin    | admin    | admin    | 00000000000 |
| Employee | employee | employee | 11111111111 |

11. According to your access level, the Employee Interface and Admin Interface sections will be added to the left-side menu. (By logging in as an administrator, you can experience both at the same time.)
12. When you enter the admin interface:
    - you will see a "User Roles" button. When you click the button, you can adjust user permissions by searching for the username on the page that appears. (You can view all users by typing "all".)
    - and you will see a "Posts" button. When you click the button, you can display posts and modify or cancel them.
13. The employee interface is divided into three parts: "All Requests", "Visa Operations", and "Green Card Operations":
    - In the "All Requests" area, you can view all user requests by clicking the "All Visa Requests" or "All Green Card Requests" buttons.
    - In the "Visa Operations" area, you can perform the following:
        - Enter the "Passports Pending Approval" section to review passport images and approve or reject passports if the information matches.
        - Enter the "Visa Requests Awaiting Approval" section to review pending visa requests, mark payment status as "Paid", finalize the appointment date, or cancel the request.
        - Enter the "Approved Visa Requests" section to update the request as "Applicated" by entering the application reference number.
        - Enter the "Visa Application Tracking" section to track the application by reference number and then update it as "Completed".
    - In the "Green Card Operations" area, you can perform the following:
        - Enter the "Pending Green Card Requests" section.
        - On the page that opens, you will see all pending and in-process insurance requests.
        - You can process pending requests on this page using the mail order method or cancel them.
        - You can mark in-process requests as "Prepared".
14. By clicking the "Change Password" button in the "My Profile" section, you can access the password change page and update your password.


#### Notes

1. Although all validations are implemented in database operations, due to potential race conditions, all processes are handled using try-except.
2. The route blueprint code structure was written in the order: main → profile → request → dashboard → admin_db (with exceptions for later additions). Reviewing them in this order is recommended.
3. AI was only used to find the necessary functions and to learn how to use them, their behavior, and return values. In code blocks written with AI assistance, this is indicated in the comments.
4. Since I will publish this project on platforms like LinkedIn and want developers in my country to understand it clearly, comments are written in both English and Turkish.
5. Blueprint imports are done inside "imports.py".
6. A .gitignore file was used during development for the protection of sensitive data.
7. Helper functions were created in "xaharfuncs.py".
8. Since the project was designed for educational purposes, the SECRET_KEY was generated randomly. Users are responsible for any risks if used in production environments.
9. Phone number, identity number, passport number, and date formats are configured according to Türkiye’s standards:
    Examples:
        - Phone Number: 05555555555 (11 digits)
        - Identity Number: 00000000000 (11 digits)
        - Passport Number: U00000000 (1 letter and 8 digits, 9 characters total)
        - Vehicle Plate: 01AA0101 (2 digits, 1–3 letters, and 1–4 digits)

#### License
This project was created for educational purposes and does not include a production license.



###### TÜRKÇE ######

### YÖNERGELER

#### Kurulum

1. Öncelikle projenin bilgisayarınızda doğru bir şekilde çalışması için çalışma dizininde terminalinizi açıp şunu yazınız:
    ```bash
    pip install -r requirements.txt

    Your terminal must be located in the same directory as the files.
    ```
2. Mail gönderme sisteminin çalışabilmesi için "app.py" içerisindeki mail ayarlarını ve "/routes/dashboard_routes.py" içerisindeki mail ayarlarını yapmalısınız. (CTRL+F ile "setmailsetting" olarak aratabilirsiniz. Test için mailtrap kullanılmıştır.)

#### Kullanım

1. Uygulamayı çalıştırmak için terminalinizi proje dizinine getirip şu kodu yazmanız yeterli olacaktır:
    ```bash
    python app.py
    ```
2. İnternet tarayıcınızı açıp şu adrese gidiniz:
    ```bash
    127.0.0.1:8080
    ```
3. Açılan sayfada sağ üst kısımdaki üye ol alanından üyelik oluşturunuz.
4. Ardından giriş yapınız.
5. Sol taraftaki hızlı erişim menüsünü kullanarak "Pasaportlarım", "Araçlarım", "Taleplerim" kısımlarına ulaşabilirsiniz.
6. Pasaportlarım kısmı:
    - Pasaportlarım kısmına giriniz.
    - Açılan sayfada mevcut pasaportlarınız görüntülenecek.
    - Pasaport görüntüleme, ekleme, düzenleme (pasaport onaylandıktan sonra düzenlenemez) ve silme gibi işlemler bu alanda yapılmaktadır.
    - Kullanıcılar yalnızca kendilerine ait olan pasaportları sisteme kayıt edebilirler. Pasaport bilgileri, kayıt olurken girilen bilgilerle eşleştirilmektedir.
    - Eğer pasaportunuz adına aktif bir vize randevu talebi mevcut ise düzenleme ve silme işlemleri yapılamaz.
7. Araçlarım kısmı:
    - Araçlarım kısmına giriniz.
    - Açılan sayfada mevcut olan araçlarınız görüntülenecek.
    - Araç ekleme, düzenleme, silme ve ruhsat görüntüleme işlemleri bu alanda yapılmaktadır.
    - Eğer aracınız adına aktif bir yeşil sigorta talebi mevcut ise düzenleme ve silme işlemleri yapılamaz.
8. Taleplerim kısmı:
    - Taleplerim kısmına giriniz.
    - Açılan sayfada son 5 vize randevusu talebiniz ve son 5 yeşil sigorta talebiniz görüntülenecek.
    - Dilerseniz bu sayfa yeni bir vize randevu talebi ya da yeşil sigorta talebi oluşturabilirsiniz.
    - Tüm vize randevu taleplerinizi görüntülemek ve taleplerinizle ilgili işlem yapmak için "Vize Talepleri" tablosunun altındaki "Daha Fazla Göster" butonuna tıklayabilirsiniz:
        - Açılan sayfada tüm vize randevusu talepleriniz görüntülenecektir.
        - Buradan vize taleplerinizin durumunu kontrol edebilir, henüz işleme girmemiş olan vize taleplerinizi düzenleyebilir ya da iptal edebilirsiniz.
    - Tüm yeşil sigorta taleplerinizi görüntülemek ve taleplerinizle ilgili işlem yapmak için "Yeşil Sigorta Talepleri" tablosunun altındaki "Daha Fazla Göster" butonuna tıklayabilirsiniz:
        - Açılan sayfada tüm yeşil sigorta talepleriniz görüntülenecektir.
        - Buradan yeşil sigorta taleplerinizin durumunu kontrol edebilir, henüz işleme girmemiş olan vize taleplerinizi düzenleyebilir ya da iptal edebilirsiniz.
9. Çalışan ve yönetici arayüzünü deneyimleyebilmek için aşağıdaki bilgiler ile giriş yapınız:

| Role     | Username | Password | ID No       |
| -------- | -------- | -------- | ----------- |
| Admin    | admin    | admin    | 00000000000 |
| Employee | employee | employee | 11111111111 |

10. Giriş yaptığınız yetkiye göre sol taraftaki menüye "Çalışan Arayüzü" ve "Yönetici Arayüzü" kısımları eklenecektir. (Yönetici olarak giriş yaparak her ikisini aynı anda deneyimleyebilirsiniz.)
11. Yönetici arayüzüne girdiğinizde "Kullanıcı Rolleri" butonunu göreceksiniz. Butona tıkladığınızda karşınıza gelen sayfada kullanıcı adı ile kullanıcı arayarak yetkilerini ayarlayabilirsiniz. ("all" yazarak tüm kullanıcıları görüntüleyebilirsiniz.)
12. Çalışan arayüzü "Tüm Talepler", "Vize İşlemleri" ve "Yeşil Sigorta İşlemleri" olarak üçe ayrılmıştır:
    - "Tüm Talepler" alanında "Tüm Vize Talepleri" ya da "Tüm Yeşil Sigorta Talepleri" tuşlarına basarak kullanıcılara ait tüm talepleri görüntüleyebilirsiniz.
    - "Vize İşlemleri" alanında şu işlemleri yapabilirsiniz:
        - "Onay Bekleyen Pasaportlar" kısmına girip pasaport görüntülerini inceleyerek girilen bilgilerin eşleşmesi durumunda pasaportları onaylayabilir ya da iptal edebilirsiniz.
        - "Bekleyen Vize Talepleri" kısmına girip randevu bekleyen vize taleplerini inceleyebilir, ödeme durumunu "Ödendi" olarak ayarlayıp ardından tarih kesinleştirebilir ya da talebi iptal edebilirsiniz.
        - "Onaylanmış Vize Talepleri" kısmına girip başvuru referans numarası girerek talebi "Başvuru Yapıldı" olarak güncelleyebilirsiniz.
        - "Vize Başvuru Takibi" kısmına girip başvuruyu referans numarası ile takip edebilir, ardından "Tamamlandı" olarak güncelleyebilirsiniz.
    - "Yeşil Sigorta İşlemleri" alanında şu işlemleri yapabilirsiniz:
        - "Bekleyen Yeşil Sigorta Talepleri" kısmına giriniz.
        - Açılan sayfada işlem bekleyen ve işlemde olan tüm sigorta taleplerini görüntüleyeceksiniz.
        - İşlem bekleyen talepleri bu sayfada "mail order" yöntemiyle işleme koyabilir ya da iptal edebilirsiniz.
        - İşlemde olan talepleri "Hazırlandı" olarak işaretleyebilirsiniz.
13. "My Profile" kısmındaki "Şifreyi Değiştir" butonuna tıklayarak şifre değiştirme sayfasına ulaşabilir ve şifrenizi değiştirebilirsiniz.


#### Notlar

1. Veritabanı işlemlerinde tüm kontroller sağlanmış olsa da, "race conditions" sebebiyle tüm işlemler try-except yöntemiyle sağlanmıştır.
2. Rota blueprint kodlarının yazımı, main -> profile -> request -> dashboard -> admin_db sırasıyla yapılmıştır (sonradan eklenen kodlar istisnadır), incelemeyi bu sırayla yapmanız tavsiye edilir.
3. Yapay zeka sadece ihtiyaç olunan fonksiyonlar bulunurken ve bu fonksiyonun kullanımı, işlevi ve ne dönürdüğü gibi bilgilerin öğrenilmesi için kullanılmıştır. Yapay zeka desteğiyle yazılan kod bloklarında durum yorum olarak belirtilmiştir.
4. Projemi LinkedIn gibi kanallarımda yayınlayacağımdan dolayı ve yaşadığım ülkedeki yazılım geliştiricilerinin de doğru anlayabilmesi adına yorum satırlarını hem İngilizce hem de Türkçe yazdım.
5. Rota blueprintlerinin importları "imports.py" içerisinde yapılmıştır.
6. Hassas verilerin korunması adına proje üzerinde çalışılırken ".gitignore" kullanılmıştır.
7. Yardımcı fonksiyonlar "xaharfuncs.py" içerisinde oluşturulmuştur.
8. Proje eğitim amaçlı tasarlandığı için SECRET_KEY random bir şekilde oluşturulmuştur, üretim amaçlu kullanımlarda oluşacak risklerden kullanıcı sorumludur.
9. Telefon numarası, kimlik numarası, pasaport numarası, tarih veriler için formatlar Türkiye'ye göre ayarlanmıştır:
    Örnekler:
        - Telefon Numarası: 05555555555 (11 hane)
        - Kimlik Numarası: 00000000000 (11 hane)
        - Pasaport Numarası: U00000000 (1 harf ve 8 rakam, toplam 9 hane)
        - Araç Plakası: 01AA0101 (2 rakam, 1-3 harf ve 1-4 rakam)

#### Lisans
Bu proje eğitim amaçlı oluşturulduğundan üretim lisansı bulunmamaktadır.