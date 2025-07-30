This project is a branch of <a target="_blank" rel="noopener" href="https://pypi.org/project/parsel/">parsel</a> on <a href="https://www.qpython.org">QPython</a>.

Parsel is a BSD-licensed Python_ library to extract data from HTML_, JSON_, and
XML_ documents.

It supports:

-   CSS_ and XPath_ expressions for HTML and XML documents

-   JMESPath_ expressions for JSON documents

-   `Regular expressions`_

Find the Parsel online documentation at https://parsel.readthedocs.org.

Example (`open online demo`_):

```python

    >>> from parsel import Selector
    >>> text = """
            <html>
                <body>
                    <h1>Hello, Parsel!</h1>
                    <ul>
                        <li><a href="http://example.com">Link 1</a></li>
                        <li><a href="http://scrapy.org">Link 2</a></li>
                    </ul>
                    <script type="application/json">{"a": ["b", "c"]}</script>
                </body>
            </html>"""
    >>> selector = Selector(text=text)
    >>> selector.css('h1::text').get()
    'Hello, Parsel!'
    >>> selector.xpath('//h1/text()').re(r'\w+')
    ['Hello', 'Parsel']
    >>> for li in selector.css('ul > li'):
    ...     print(li.xpath('.//@href').get())
    http://example.com
    http://scrapy.org
    >>> selector.css('script::text').jmespath("a").get()
    'b'
    >>> selector.css('script::text').jmespath("a").getall()
    ['b', 'c']
```
