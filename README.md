# Web-Crawler
I need to list the urls of all pages, list outgoing links, list broken links, list urls of graphic (gif, jpg, jpeg, png) files, display the content of  &lt;TITLE> tag, implement exact duplicate detection.
(1) Implement stemming: 
I need to use the Porter Stemmer Algorithm to traverse each term. 
(2) Output term-document frequency: 
I need to save the words from each page and output a term-document frequency matrix 
(3) List the 20 most common words 
I choose to list the stemmed 20 most common words 
(4) Obey robots.txt 
I need to make sure that the URLs I crawl should obey the robots.txt.  
(5)  Implement exact duplication 
Firstly, I need to filter the same URLs. Then I need to filter the different URLs which contain the same content.

Software used:
(1)Python
(2)pywin32
(3)pip
(4)lxml
(5)Scrapy
