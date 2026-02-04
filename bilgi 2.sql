USE bilgi_platform;

CREATE TABLE canlinin_bilgileri(
    id INT IDENTITY(1,1) PRIMARY KEY,
    baslik NVARCHAR(255) UNIQUE NOT NULL,
    giris_ozeti NVARCHAR(MAX),
    genel_ozet NVARCHAR(MAX),
    tam_metin NVARCHAR(MAX),
    url NVARCHAR(500),
    kategori NVARCHAR(50) DEFAULT 'Diger',
    kayit_tarihi DATETIME DEFAULT GETDATE()
);

--create database bilgi_platform
/*
use bilgi_platform
CREATE TABLE canli_bilgileri (
    id INT IDENTITY(1,1) PRIMARY KEY,
    baslik NVARCHAR(255) UNIQUE,   
    giris_ozeti NVARCHAR(MAX),       
    genel_ozet NVARCHAR(MAX),        
    tam_metin NVARCHAR(MAX),         
    url NVARCHAR(500),              
    kayit_tarihi DATETIME DEFAULT GETDATE()
);


ALTER TABLE canli_bilgileri
ADD kategori NVARCHAR(50) DEFAULT 'Diger';
*/