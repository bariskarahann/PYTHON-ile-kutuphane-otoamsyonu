USE [KütüphaneOtomasyonu]
GO
/****** Object:  Table [dbo].[kayıtlı_kişiler]    Script Date: 11.06.2023 21:36:46 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[kayıtlı_kişiler](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[kullanıcı_adı] [varchar](20) NULL,
	[şifre] [varchar](20) NULL,
	[üyelik_tipi] [varchar](10) NULL,
	[ad] [varchar](20) NULL,
	[soyad] [varchar](20) NULL,
	[tel_no] [varchar](20) NULL,
	[adres] [varchar](50) NULL,
	[eposta] [varchar](25) NULL,
	[üyelik_tarihi] [varchar](10) NULL,
	[doğum_tarihi] [varchar](10) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[kitap_geçmişi]    Script Date: 11.06.2023 21:36:46 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[kitap_geçmişi](
	[kitap_id] [int] NULL,
	[kullanıcı_id] [int] NULL,
	[ad] [varchar](20) NULL,
	[soyad] [varchar](20) NULL,
	[kitap_adı] [varchar](25) NULL,
	[alma_tarihi] [varchar](10) NULL,
	[teslim_tarihi] [varchar](10) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[kitaplar]    Script Date: 11.06.2023 21:36:46 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[kitaplar](
	[kitap_id] [int] IDENTITY(1,1) NOT NULL,
	[kitap_adı] [varchar](25) NULL,
	[yazar] [varchar](25) NULL,
	[basım_evi] [varchar](25) NULL,
	[basım_yılı] [varchar](5) NULL,
	[toplam_adet] [int] NULL,
	[mevcut_adet] [int] NULL
) ON [PRIMARY]
GO
