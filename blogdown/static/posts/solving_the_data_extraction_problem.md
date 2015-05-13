Solving the Data Extraction Problem
===

Yes, the clickbait title was unashamedely intentional. No, I'm not formally
solving anything (my apologies to all the formal-proof-loving people
I've mislead into my post). Yes, there's an algorithm:

    Given a tree, return a list of all subtrees - sorted by the number of 
	children relative to the root node in the subtree.

##*The Problem*

According to [wikipedia](http://en.wikipedia.org/wiki/Data_extraction): 

> **Data extraction** is the act or process of retrieving data out of 
(usually unstructured or poorly structured) data sources ... Typical 
unstructured data sources include web pages ...

The problem I'm attempting to tackle is that of extracting data from 
websites. 

##*What sort of "data" are we extracting?*

The correct answer, I'd argue, is: *the sort of data that's produced by 
the source of that data*. But let's get specific. 

Websites are structured by HTML (sure, the styling is also partially 
responsible for the *visual* structure, but as you'll see later on, 
we don't *have* to take style sheets into account).

*What data can we get from __webpages__?*

Instead of writing down some cryptic but arguably true answer, I'll give
a bit of background as to why the heck I'm even tackling this problem
(don't worry, feel free to skip the next few paragraphs - I define
"data" as *__article text and tabular data__*).

About 4 months ago, I debuted [eatiht](https://github.com/rodricios/eatiht) 
(a text extracting library; the predecessor to this algorithm) on [reddit](http://www.reddit.com/r/compsci/comments/2ppyot/just_made_what_i_consider_my_first_algorithm_it/).
I can only say positiive things about doing so. For one, it's landed me an opportunity
to coauthor a paper with [Tim Weninger](http://www3.nd.edu/~tweninge/). 

It was Tim who introduced me to the *structured [tabular] data extraction* problem. 
He illustrated the scenario of trying to extract ``<table>``'s and table-like 
structures from a website.
 
For example, let's take [reddit](http://www.reddit.com):

<figure> 
	![reddit tables](http://i.imgur.com/OsA7Iiyh.png) 
	<figcaption> 
		Highlighted in red are examples of tabular data (a.k.a. *structured data, lists*) 
	</figcaption> 
</figure>

What's highlighted in red is what I'm referring to as *structured* or *tabular data*. 

Since we're dealing with HTML, let's have a look at the underlying markup: 
<figure> 
	![subreddits](http://i.imgur.com/d3cFlB8l.png) 
	<figcaption>subreddits - there's a lot of ``li``'s 
	</figcaption> 
</figure>


<figure>
	![top posts](http://i.imgur.com/78rNdf4l.png)
	<figcaption>
		top posts - there's a lot of ``div``'s 
	</figcaption>
</figure>

Looking at the above pictures, one thing should be clear: although ``<table>``'s 
are the epitome of **tabular data**, there are no ``<table>``'s in the above 
HTML. 

So what do? 

###Deconstruction

Simple. Clearly define what the problem is: 

*__Data__ (in the context of HTML) are collections of HTML elements. 
Visually, data is presented as rows or columns. Structurally, data 
is presented as a collection (__parent element__) of (__children__) elements.*

Many of you will say, *so then aren't we practically talking about every
element in the an HTML tree?*

Yup. 

But now through in the phrase *frequently occuring*:

*__Data__ (in the context of HTML) are collections of __frequently occurring__ HTML elements. 
Visually, data is presented as rows or columns. Structurally, data 
is presented as a collection (__parent element__) of __frequently occurring__ (__children__) elements.*

In the case of reddit.com, we'd like to create some solution that will retrieve at least two collections:
the ``<ul>`` containing those ``<li>``'s; the parent ``<div>`` containing those inner ``<div>``'s. There's
a catch: we can't directly target those HTML elements. 

Well, taking out my prototyping weapon of choice, Python, let's get to it. 

###Solution

First, let's just get our HTML into a Python-friendly object.

``python
from requests import get

reddit_request = get('http://www.reddit.com/')
# reddit_request.content[:100]
# '<!doctype html><html xmlns="http://www.w3.org/1999'
``

Now let's process the HTML string through a library ([lxml](http://lxml.de/lxmlhtml.html)) that will take 
that string and create an [XPath](http://en.wikipedia.org/wiki/XPath)-queryable object.

``python
from lxml import html

parsed_doc = html.fromstring(reddit_request.content)
`` 

From here, we can start doing things like querying for specific types of nodes (HTML elements): 



###Related work

There's a lot of research that has been done in this area: 

[*WebTables: Exploring the Power of Tables on the Web* (2008) - Michael J. Cafarella, Alon Halevy, Zhe Daisy Wang, Eugene Wu Yang Zhang](http://yz.mit.edu/papers/webtables-vldb08.pdf)

This work is more of a search engine than a simple n-step algorithm. Here's how the authors described their work: 

> We describe the WebTables system to explore two fundamental 
questions about this collection of databases. First, what are 
effective techniques for searching for structured data at 
search-engine scales? Second, what additional power can be 
derived by analyzing such a huge corpus?

[*HyLiEn: A Hybrid Approach to General List Extraction on the Web* (2011) - Fabio Fumarola, Tim Weninger, Rick Barber, Donato Malerba, Jiawei Han](http://web.engr.illinois.edu/~hanj/pdf/www11_ffumarola.pdf)

This project's solution is a tad bit closer to the solution that I'm providing. 
Their algorithm takes renders the webpage, thus employing their "visual-structural method".

[*Bootstrapping Information Extraction from Semi-structured Web Pages* (2008) - Andrew Carlson and Charles Schafer](http://www.cs.cmu.edu/~acarlson/papers/carlson-ecml08.pdf)

Supervised learning approach to extracting "structured records from semistructured web pages". 
Here they describe some examples:  

> ... semi-structured web page domains include books for sale,
properties for rent, or job offers.

Not to bash on the merits of their research, none of those 
solutions are easily available for the rest of us.  

