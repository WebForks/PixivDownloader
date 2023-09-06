# PixivDownloader

This Pixiv Downloader is a Python-based command-line utility designed for downloading Pixiv artworks, illustrations, and more based on user-defined criteria. You can use it to fetch images for a specific artwork, tags, and various other sorting options. The utility also supports cookies for authentication and debugging for better development and troubleshooting.

---

## Getting Started

### Dependencies

- Python 3.x
- install requirements.txt

### Installing

- Have python installed
- pip install -r requirements.txt

### Executing program

- Modify config.ini (optional)

```
python cli.py {url} --config.ini {path if not in current dir}
```

---

### Capabilities:

- Download images, manga, and ugoira (animated images) from Pixiv
- Supports single and multiple image downloads
- Filter by tags, sorting order, and various other criteria
- Create GIFs for ugoira artworks
- Command-line arguments and optional config file for easier use

### Examples:

download image to current directory

```
https://www.pixiv.net/en/artworks/4531683
```

download image to another directory

```
https://www.pixiv.net/en/artworks/4531683 --file_location ./test
```

### FAQ

```
1. Priority from first to last for file location/tags/sort order/etc...
   - config.ini (if using --config tag)
   - --arguments
   - link used
```

#### Notes

Pixiv Scraper for links and tags. Work In Progress

ARTWORK

illustType
0 = illustration
1 = manga
2 = ugoira

xRestrict
0 = SFW/All Ages
1 = NSFW/R-18

---

SEARCH

https://www.pixiv.net/ajax/search/artworks/{tags}?word={tags}
sort - &order= newest - date_d,
oldest - date,
popular with all - popular_d,
popular (male) - popular_male_d
popular (female) - popular_female_d

&mode=all

page - &p= mininum - 1
maximum - 5000 (with premium)

targets tags - &s_mode= s_tag_full = perfect match,
s_tag = partial match,
s_tc = title,caption

targets manga/illustrations/ugoria/ - type= all = Illustrations, Manga, Ugoria(animation),
illust_and_ugoira = Illustrations, Ugoria(animation),
illust = Illustrations,
manga = Manga,
ugoira = Ugoria(animation)

AI generated work - &ai_type= 0 = display, 1 = hide

Filters Resolutions - (No metion) = All resolutions
&wlt=3000&hlt=3000 = More than 3000px x 3000px
&wlt=1000&wgt=2999&hlt=1000&hgt=2999 = 1,000px × 1,000px ~ 2,999px × 2,999px
&wgt=999&hgt=999 = Less than 999px x 999px

Filters Ratios - (No metion) = All ratios
&ratio= 0.5 = Horizontal
-0.5 = Vertical
0 = Square

Period - (No Mention) = All Periods
&scd= {year}-{month}-{day}
scd = starting
ecd = ending
?scd=2023-08-22&ecd=2023-08-29

Bookmarks - (No Mention) = All Bookmarks
&blt= 10000 = 10000+
&blt=5000&bgt=9999 = 5000 - 9999
&blt=1000&bgt=4999 = 1000 - 4999

&lang=en&version=f32089e9d176912e655d9eda2c1b816e46a82d4b

picture 1 - 3 and thumbnail
https://i.pximg.net/img-master/img/2021/03/21/02/45/56/{id}_p0_master1200.jpg
https://i.pximg.net/img-master/img/2021/03/21/02/45/56/{id}_p1_master1200.jpg
https://i.pximg.net/img-master/img/2021/03/21/02/45/56/{id}_p2_master1200.jpg
https://i.pximg.net/c/250x250_80_a2/custom-thumb/img/2021/03/21/02/45/56/{id}_p0_custom1200.jpg

"urls":{"mini":"https://i.pximg.net/c/48x48/img-master/img/2016/03/21/01/19/37/55908541_p0_square1200.jpg",
"thumb":"https://i.pximg.net/c/250x250_80_a2/img-master/img/2016/03/21/01/19/37/55908541_p0_square1200.jpg",
"small":"https://i.pximg.net/c/540x540_70/img-master/img/2016/03/21/01/19/37/55908541_p0_master1200.jpg",
"regular":"https://i.pximg.net/img-master/img/2016/03/21/01/19/37/55908541_p0_master1200.jpg",
"original":"https://i.pximg.net/img-original/img/2016/03/21/01/19/37/55908541_p0.jpg"}
