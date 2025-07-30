import cloudscraper


scraper = cloudscraper.create_scraper(interpreter='nodejs')

base_url = "httpx://picazor.com"
url_page_1 = "https://picazor.com/api/files/teemori/sfiles?page=1"
page1 = scraper.get(url_page_1)
[d["path"] for d in page1.json()]

"""
['/uploads/may25/sa3/teemori/fansly/bhqpk/teemori-fansly-6h0ds-9.jpg',
 '/uploads/may25/sa3/teemori/fansly/bhqpk/teemori-fansly-enl0f-8.jpg',
 '/uploads/may25/sa3/teemori/fansly/bhqpk/teemori-fansly-29ysw-7.jpg',
 '/uploads/may25/sa3/teemori/fansly/bhqpk/teemori-fansly-sytkf-6.jpg',
 '/uploads/may25/sa3/teemori/fansly/bhqpk/teemori-fansly-zcrer-5.jpg',
 '/uploads/may25/sa3/teemori/fansly/bhqpk/teemori-fansly-bsk8b-4.jpg',
 '/uploads/may25/sa3/teemori/fansly/bhqpk/teemori-fansly-7bbyk-3.jpg',
 '/uploads/may25/sa3/teemori/fansly/bhqpk/teemori-fansly-ju2nw-2.jpg',
 '/uploads/may25/sa3/teemori/fansly/bhqpk/teemori-fansly-93vp3-1.jpg',
 '/uploads/may25/sa3/teemori/fansly/klnil/teemori-fansly-lmryl-4.jpg',
 '/uploads/may25/sa3/teemori/fansly/klnil/teemori-fansly-fbl5a-3.jpg',
 '/uploads/may25/sa3/teemori/fansly/klnil/teemori-fansly-8fkzt-2.jpg']

full image URL will be: f{base_url}{path_from_list_above}

To grab
https://picazor.com/en/maria-bolona
https://picazor.com/en/kiakuromi
https://picazor.com/en/amber-chan
https://picazor.com/en/cami
https://picazor.com/en/joj-838 (with videos)


Huges
https://picazor.com/en/lady-melamori
https://picazor.com/en/potatogodzilla-3
https://picazor.com/en/vixenp
https://picazor.com/en/saizneko
https://picazor.com/en/hannapunzell

"""
