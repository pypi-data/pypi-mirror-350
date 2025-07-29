# pytoolsz

一组常用的Python工具，主要用于处理自己常用的工作问题。
（说白了就是个工具集的罗列，减少一些重复劳动。）

目前已有的小工具：

1. `saveExcel` 数据表保存方法
2. `compress` 压缩包处理
3. `utob` YouTube常用数据处理方法
4. `frame` 数据框DataFrame快捷方法
5. `pretools` 四舍五入与日期处理
6. `ppTrans` PPT转换与PPT拼接长图
7. `graphs` 绘图工具（子弹图、颜色映射、中国地图可视化|热力图） 

目前完成了部分便捷小工具。预测工具和更多绘图工具还在构建中。

现在已经可以直接使用pip安装了：

```bash
pip install pytoolsz
```

**其他说明**

国家代码转换的说明：

1.  ISO2 (ISO 3166-1 alpha-2) - including UK/EL for Britain/Greece (but always convert to GB/GR)
2.  ISO3 (ISO 3166-1 alpha-3)
3.  ISO - numeric (ISO 3166-1 numeric)
4.  UN numeric code (M.49 - follows to a large extend ISO-numeric)
5.  A standard or short name
6.  The "official" name
7.  Continent: 6 continent classification with Africa, Antarctica, Asia, Europe, America, Oceania
8.  [Continent_7 classification](https://ourworldindata.org/world-region-map-definitions) - 7 continent classification spliting North/South America
9.  UN region
10. [EXIOBASE 1](http://exiobase.eu/) classification (2 and 3 letters)
11. [EXIOBASE 2](http://exiobase.eu/) classification (2 and 3 letters)
12. [EXIOBASE 3](https://zenodo.org/doi/10.5281/zenodo.3583070) classification (2 and 3 letters)
13. [WIOD](http://www.wiod.org/home) classification
14. [Eora](http://www.worldmrio.com/)
15. [OECD](http://www.oecd.org/about/membersandpartners/list-oecd-member-countries.htm)
    membership (per year)
16. [MESSAGE](http://www.iiasa.ac.at/web/home/research/researchPrograms/Energy/MESSAGE-model-regions.en.html)
    11-region classification
17. [IMAGE](https://models.pbl.nl/image/index.php/Welcome_to_IMAGE_3.0_Documentation)
18. [REMIND](https://www.pik-potsdam.de/en/institute/departments/transformation-pathways/models/remind)
19. [UN](http://www.un.org/en/members/) membership (per year)
20. [EU](https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:EU_enlargements)
    membership (including EU12, EU15, EU25, EU27, EU27_2007, EU28)
21. [EEA](https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:European_Economic_Area_(EEA))
    membership
22. [Schengen](https://en.wikipedia.org/wiki/Schengen_Area) region
23. [Cecilia](https://cecilia2050.eu/system/files/De%20Koning%20et%20al.%20%282014%29_Scenarios%20for%202050_0.pdf)
    2050 classification
24. [APEC](https://en.wikipedia.org/wiki/Asia-Pacific_Economic_Cooperation)
25. [BRIC](https://en.wikipedia.org/wiki/BRIC)
26. [BASIC](https://en.wikipedia.org/wiki/BASIC_countries)
27. [CIS](https://en.wikipedia.org/wiki/Commonwealth_of_Independent_States)
    (as by 2019, excl. Turkmenistan)
28. [G7](https://en.wikipedia.org/wiki/Group_of_Seven)
29. [G20](https://en.wikipedia.org/wiki/G20) (listing all EU member
    states as individual members)
30. [FAOcode](http://www.fao.org/faostat/en/#definitions) (numeric)
31. [GBDcode](http://ghdx.healthdata.org/) (numeric - Global Burden of
    Disease country codes)
32. [IEA](https://www.iea.org/countries) (World Energy Balances 2021)
33. [DACcode](https://www.oecd.org/dac/financing-sustainable-development/development-finance-standards/dacandcrscodelists.htm)
    (numeric - OECD Development Assistance Committee)
33. [ccTLD](https://en.wikipedia.org/wiki/Country_code_top-level_domain) - country code top-level domains
34. [GWcode](https://www.tandfonline.com/doi/abs/10.1080/03050629908434958) - Gledisch & Ward numerical codes as published in https://www.andybeger.com/states/articles/statelists.html
35. CC41 - common classification for MRIOs (list of countries found in all public MRIOs)
36. [IOC](https://en.wikipedia.org/wiki/List_of_IOC_country_codes) - International Olympic Committee (IOC) country codes