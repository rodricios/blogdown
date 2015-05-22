Solving the Data Extraction Problem in 10 lines
===

#####By Rodrigo Palacios, follow me on [twitter](https://twitter.com/rodricios), and [github](https://github.com/rodricios)

*[Libextract](https://github.com/datalib/libextract) - extract data from the web (a Python implementation of this work)*.

---

<img class="pure-img" src="https://i.imgur.com/Xfb8zYE.jpg?2" alt="Data extraction at it's root" title="Maybe here, no, here? No... man, they said I'd find Ja Rule's albums here..."></img>


In the grand scheme of things, extracting data from the web is a small step in a 
much larger objective. But in the micro, *data extraction* appears to us as a problem
that has no real definitive solution, a sort of *dirty job* - how often is the task
relegated as that of "scraping" the web?

Just think about how many times you've ran into this type of web-scraping tutorial: 
download HTML, parse HTML, open dev tools, flip back-and-forth between browser and 
console, debug your [XPath](http://en.wikipedia.org/wiki/XPath) expressions, etc. 

On the other hand, data extraction via web-scraping has seemlessly, and sometimes elegantly,
found its way into larger projects ([Apache Nutch](http://nutch.apache.org/) includes [Tika](http://tika.apache.org/), 
[Scrapy](http://scrapy.org/) has hybrid crawl-n-scrape architecture). Needless to
say, they're designed to give you - the developer, the data scientist, the hacker, the
one with time to spare - a lot of control... to a fault. But at least they provide XPath
 tutorials ([\[1\]](http://tika.apache.org/1.8/examples.html#Fetching_just_certain_bits_of_the_XHTML) 
[\[2\]](http://doc.scrapy.org/en/0.24/intro/tutorial.html?highlight=data%20extraction#extracting-items)).

In this post, I present an informal solution to the data extraction problem. It's 
short, it's sweet, and it leaves much room for improvement. Enjoy :) 

## *The algorithm*

In not-so-plain words:

> Given a tree, return a list of all subtrees - sorted by the number
of children relative to the root node in the subtree.

In Python: 

```python
	from requests import get
	from collections import Counter
	from lxml import html
	
	reddit_request = get('http://www.reddit.com/')
	#wiki_request = get('http://en.wikipedia.org/wiki/Information_extraction')

	parsed_doc = html.fromstring(reddit_request.content)
	
	# In SQL-like terms: select all parents in <body>
	parent_elements = parsed_doc.xpath('//body//*/..')
	
	parents_with_children_counts = []
	
	for parent in parent_elements:
	    children_counts = Counter([child.tag for child in parent.iterchildren()])
	    parents_with_children_counts.append((parent, children_counts))

	# This line, one could say, is what wraps this data-extraction 
	# algorithm up as a maximization/optimization algorithm
	parents_with_children_counts.sort(# x[1].most_common(1)[0][1] gets the frequency value
                                      key=lambda x: x[1].most_common(1)[0][1], 
                                      reverse=True)
```

## *The Problem*

According to [wikipedia](http://en.wikipedia.org/wiki/Data_extraction): 

> **Data extraction** is the act or process of retrieving data out of 
(usually unstructured or poorly structured) data sources ... Typical 
unstructured data sources include web pages ...

The problem I'm attempting to tackle is that of extracting data from 
websites. 

## *What sort of "data" are we extracting?*

Websites are structured by HTML (sure, the styling is also partially 
responsible for the *visual* structure, but as you'll see later on, 
we don't *have* to take style sheets into account). It's in the 
structured HTML where you'll find "unstructured data".

Before I continue, I'll give a bit of background as to why the heck 
I'm even tackling this problem. 

About 4 months ago, I debuted [eatiht](https://github.com/rodricios/eatiht) 
(a text-extracting library; the predecessor to this algorithm) on [reddit](http://www.reddit.com/r/compsci/comments/2ppyot/just_made_what_i_consider_my_first_algorithm_it/).
I can only say positive things about doing so. For one, it's landed me an
opportunity to coauthor a paper with [Tim Weninger](http://www3.nd.edu/~tweninge/). 

It was Tim who introduced me to the *structured [tabular] data extraction*
problem. He illustrated the scenario of trying to extract ``<table>``'s and 
table-like structures from a website like [reddit](http://www.reddit.com). 
Here's what he says about that:

> The first [candidate] is the list of subreddits across the top of 
the page ... The second is the list of reddit posts with link, time, 
username, and a bunch of other things. The front page of reddit is 
nothing more than a stylized set of multi-attribute lists or tables. 

## *A wild problem appears!*

Let's get a better picture of what Tim is saying:

<figure markdown="1"> 
	<img class="pure-img" src="https://i.imgur.com/OsA7Iiyl.png" alt="reddit tables" title=""></img> 
	<figcaption markdown="1"> 
		Websites are like a series of tables...
	</figcaption> 
</figure>

What's highlighted in red is what is meant by *structured* or *tabular data*. 

Since we're dealing with HTML, let's have a look at the underlying markup: 

<figure markdown="1"> 
	<img class="pure-img" src="https://i.imgur.com/d3cFlB8l.png" alt="subreddits" title=""></img> 
	<figcaption markdown="1"> 
		subreddits - there's a lot of ``li``'s 
	</figcaption> 
</figure>


<figure markdown="1"> 	
	<img class="pure-img" src="https://i.imgur.com/78rNdf4l.png" alt="top posts" title=""></img> 
	<figcaption markdown="1"> 
		top posts - there's a lot of ``div``'s 
	</figcaption>
</figure>

Looking at the above pictures, one thing should be clear: although
``<table>``'s are the epitome of **tabular data**, there are no 
``<table>``'s in the above HTML. But despite the lack of tables, it 
should also be clear that there is tabular data on the front page of Reddit.

So what do? 

## Deconstruction

Clearly define what the problem is: 

*__Data__ (in the context of HTML) are collections of HTML elements. 
Visually, data is presented as rows or columns (usually). Structurally, 
data is presented as a collection (__parent element__) of __children 
elements__.*

Some of you guys and gals may be thinking, "This definition is ambiguous. 
We're practically talking about every element in an HTML tree."

Yup.

But now throw the phrase *frequently occuring* into the definition:

*Structurally, data is presented as a collection (parent element)
of __frequently occurring__ children elements.*

To reiterate clearly (hopefully):

1. We're looking for the *parents* of elements of any tag.

2. We're looking for repetitive elements, or rather the *counts* of 
repetitive elements

In the case of reddit.com, we'd like to create some solution that will 
retrieve at least two collections: the ``<ul>`` containing those 
``<li>``'s; the parent ``<div>`` containing those inner ``<div>``'s. 

Having said all that, let's take out my prototyping weapon of choice, 
Python, and get to it. 

## Solution

First, let's just get our HTML into a Python-friendly object.

```python
	from requests import get
	
	reddit_request = get('http://www.reddit.com/')
	# >>> reddit_request.content[:50]
	# '<!doctype html><html xmlns="http://www.w3.org/1999'
```

Now let's process the HTML string through a library ([lxml](http://lxml.de/lxmlhtml.html)) that will take 
that string and create an DOM-traversable, [XPath](http://en.wikipedia.org/wiki/XPath)-queryable object.

```python
	from lxml import html
	
	parsed_doc = html.fromstring(reddit_request.content)
```

From here, we can start doing things like querying for different 
types of nodes (HTML elements). But we're not looking for a specific 
*type* of node - where by *type* I mean [*tag*](http://www.w3schools.com/tags/ref_byfunc.asp). 

*We're looking for the __parents__ of elements of any tag.*

```python
	# In SQL-like terms: select all parents in body
	parent_elements = parsed_doc.xpath('//body//*/..')
	
	# >>> parent_elements[:5]
	# [<Element body at 0x5a69958>,
	#  <Element div at 0x5a699a8>,
	#  <Element div at 0x5c37a98>,
	#  <Element div at 0x5c37ae8>,
	#  <Element div at 0x5c379a8>]
```

And *we're looking for repetitive elements, or rather the __counts__ of 
repetitive elements*

```python
	from collections import Counter
	
	parents_with_children_counts = []
	
	for parent in parent_elements:
	    children_counts = Counter([child.tag for child in parent.iterchildren()])
	    parents_with_children_counts.append((parent, children_counts))
		
	# >>> parents_with_children_counts[:5]
	# [(<Element body at 0x5a69958>, Counter({'script': 4, 'div': 4, 'a': 1, 'p': 1})),
	#  (<Element div at 0x5a699a8>, Counter({'div': 3, 'a': 1})),
	#  (<Element div at 0x5c37a98>, Counter({'div': 1})),
	#  (<Element div at 0x5c37ae8>, Counter({'div': 3, 'a': 1})),
	#  (<Element div at 0x5c379a8>, Counter({'span': 1}))]
```

Finally, let's sort our list of parent-child counter pairs by the *frequency* 
of the most common element in each *child counter*.

```python 
	# This line, one could say, is what wraps this data-extraction 
	# algorithm as a maximization/optimization algorithm
	parents_with_children_counts.sort(# x[1].most_common(1)[0][1] gets the frequency value
                                      key=lambda x: x[1].most_common(1)[0][1], 
                                      reverse=True)

	# >>> parents_with_children_counts[:5]
	# [(<Element div at 0x5f4ae08>, Counter({'a': 51})),
	#  (<Element div at 0x5f64048>, Counter({'div': 51})),
	#  (<Element ul at 0x5f5f048>, Counter({'li': 48})),
	#  (<Element div at 0x5f613b8>, Counter({'div': 23})),
	#  (<Element ul at 0x5f60048>, Counter({'li': 8}))]								  
```

## Results

Let's print out the text content from each of the retrived (extracted) 
elements' children:

```python
	>>> [elem.text_content() for elem in parents_with_children_counts[0][0].iterchildren()]
	announcements
	Art
	AskReddit
	...
	worldnews
	WritingPrompts
	edit subscriptions
```

So where's that coming from?

<figure markdown="1"> 
	<img class="pure-img" src="https://i.imgur.com/s7W7R4Bl.png" alt="Hidden list of subreddits" title=""></img> 
	<figcaption markdown="1"> 
		Here's where. It's the *MY SUBREDDITS* button.
	</figcaption>
</figure>

Let's print out the text content of the second and third retrieved elements:

```python
	for child in parents_with_children_counts[1][0]:
		print(child.text_content())
	
	# 1732273237324Dad Instincts (share.gifyoutube.com)submitted 4 hours ago by redditfresher to /r/funny2351 commentssharecancelloading...
	#
	# 2342634273428Transparency is important to us, and today, we take another step forward. (self.announcements)submitted 4 hours ago * by weffey[A] to /r/announcements2424 commentssharecancelloading...
	#
	# 3456345644565My heart belongs to my cat (i.imgur.com)submitted 6 hours ago by ShahzaibElahi1 to /r/aww290 commentssharecancelloading...
	#
	# 4441444154416My buddy was camping near the highway in Haines, Alaska when a curious fox took an interest in him... (m.imgur.com)submitted 6 hours ago by iamkokonutz to /r/pics212 commentssharecancelloading...var cache = expando_cache(); cache["t3_35ufuc_cache"] = " &lt;iframe src=&quot;//www.redditmedia.com/mediaembed/35ufuc&quot; id=&quot;media-embed-35ufuc-1ds&quot; class=&quot;media-embed&quot; width=&quot;560&quot; height=&quot;560&quot; border=&quot;0&quot; frameBorder=&quot;0&quot; scrolling=&quot;no&quot; allowfullscreen&gt;&lt;/iframe&gt; ";
	...
	for child in parents_with_children_counts[2][0]:
    	print(child.text_content())
	
	# gadgets
	# -sports
	# -gaming
	# -pics
	# -worldnews
	...
```

*note: the results are different from the above image because I'm a slow writer.*

Suffice to say that Tim's tabular data was extracted. But can this algorithm 
extract other forms of data?

After running the algorithm on a [wikipedia page](http://en.wikipedia.org/wiki/Information_extraction), 
our top result is:

> Information extraction (IE) is the task of automatically extracting 
structured information from unstructured and/or semi-structured 
machine-readable documents. In most of the cases this activity concerns 
processing human language texts by means of natural language processing 
(NLP). Recent activities in multimedia document processing like automatic 
annotation and content extraction out of images/audio/video could be seen 
as information extraction. ...

The algorithm yielded the div containing the main article of the wiki 
page as its top result.

## Final Thoughts

So far, we've been able to extract what we came to extract: tabular data 
and article text.

This algorithm is able to exploit the fact that data exists on the same 
depth, DOM-wise - whether it is the ``<p>``'s that make up the main article, 
or the ``<li>``'s under a list.

**This algorithm doesn't clean, convert, or format the extracted data.** This in itself 
is another problem. Not in any way less interesting :)

Anyways, I'm done working on extraction problems.

## "Must have been thought of before"

There's a lot of research that has been done in this area. But there's 
one very important piece of work that should be mentioned before the rest:

[*Fact or fiction: content classification for digital libraries* (2001) 
- Aidan Finn, Nicholas Kushmerik, Barry Smyth](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.21.3834&rep=rep1&type=pdf)

This 14 year old paper was not in my line of sight when I first wrote 
this algorithm (around the time Tim had presented the tabular-data-extraction
problem to me, which was 4 months ago). 

Okay, technically it was in my periphery. Someone had linked the article
in a comment on my [reddit post](http://www.reddit.com/r/compsci/comments/2ppyot/just_made_what_i_consider_my_first_algorithm_it/cmz1m4h).

Here's the thing, my lexicon at the time was so limited that I couldn't even 
acknowledge/respond to Yacoby's question about whether or not I 
"considered using a simple maximisation algorithm?" 

I should have responded with, *eatiht is a maximization algorithm*; instead, 
and I remember this clearly, I was describing the algorithm up to the point 
of what's known as the [argmax](http://en.wikipedia.org/wiki/Arg_max) 
calculation (for whatever reason, I couldn't put 2 and 2 together). 

Anyways, logically what should and would have followed after that
is a big moment of *Ohhhhh... It's been done before, and here it is:*

> The [text extraction] problem can now be viewed as an optimization 
problem. We must identify points i and j such that we maximize the 
number of tag tokens below i and above j, while simultaneously maximizing 
the number of text tokens between i and j. The text is only extracted 
between i and j. - *from pg. 3 of __Fact or fiction__*

I waited until I started gathering resources for this post; I read Yacoby's 
suggestion once again; I looked for and found the paper; I ``ctrl-F``'ed;
I typed "maxim". I had that moment like I describe above. 

All I can say about repeating 14 year old work is that [rediscovery of work](http://en.wikipedia.org/wiki/Gregor_Mendel#Rediscovery_of_Mendel.27s_work) happens.
According to an uncle of mine, wavelet theory has that "work rediscovery" element 
in its history.

Anyways, is this particular algorithm a straight-up rework of *Fact or fiction*? 
In my opinion, no. Is the previous (eatiht) algorithm I worked on a rework 
of *Fact or fiction*? I'd say I "rediscovered" it. 

The authors of *Fact or fiction* are describing an "optimization" algorithm 
that can extract text. 

They were very close to describing the more general algorithm that 
I describe in this post, and that I have yet to pin a name to. Any ideas?

If anyone knows of a similar solution, please let me know in the comments! 

Now onto the realm of startups. 

---

## Closed-source solutions

There's a fair bit of options: 

* [import.io](https://import.io/) 

* [embed.ly](http://embed.ly/)

* [diffbot.com](https://www.diffbot.com/)

All of these solutions essentially run on top of extraction algorithms.
Import.io is probably the one I'd recommend for broke college students - 
their service is free. It's when a user-soon-to-be-client's 
demands increase that import.io's profit model kicks in. Smart. 

Embedly made a clever move in finding a niche market and exploiting it. 
They make it easy for, say, *The New York Times* to make links to other
articles on their site - a pretty little "card" is created that contains
a snippet from an article, and optionally an image. For developers, they
provide services to create embeds, extract text, etc. 

Diffbot seems to be the one playing it safe, providing services for 
multiple types of extractions jobs (article text, product pages (\*cough\*
tabular data \*cough\*). One differentiating factor that diffbot has is 
its crawling engine. 

Want to see how each one fares against this algorithm?

*__Note: the following is not, by any reasonable standard, a "benchmark".__ 
My apologies if the lack of sophistication offends anyone.*

---

### Wikipedia

*target: [AOL's wikipage](http://en.wikipedia.org/wiki/AOL)*

I'll provide permalinks to each service's request so that you can see the
results first hand. 

#### Diffbot

<figure markdown="1"> 
	<img class="pure-img" src="https://i.imgur.com/MzV1brol.png" alt="AOL wiki - diffbot" title=""></img> 
	<figcaption markdown="1"> 
		[Test it out.](http://www.diffbot.com/testdrive/?api=article&url=http%3A%2F%2Fen.wikipedia.org%2Fwiki%2FAOL) Ey! They extracted the text!
	</figcaption>
</figure>

#### import.io

<figure markdown="1"> 
	<img class="pure-img" src="https://i.imgur.com/TqHjIxNl.png" alt="AOL wiki - import.io" title=""></img> 
	<figcaption markdown="1"> 
		[Test it out.](https://magic.import.io/?site=http:%2F%2Fen.wikipedia.org%2Fwiki%2FAOL)
		They managed to extract the references at the bottom of the article - but no article.
	</figcaption>
</figure>

#### embed.ly

<figure markdown="1"> 
	<img class="pure-img" src="https://i.imgur.com/7sXC0p6l.png" alt="AOL wiki - embed.ly" title=""></img> 
	<figcaption markdown="1"> 
		[Test it out.](http://embed.ly/docs/explore/extract?url=http%3A%2F%2Fen.wikipedia.org%2Fwiki%2FAOL)
		They provide some pretty useful databites, but not the main content :(
	</figcaption>
</figure>

#### libextract

[Libextract](https://github.com/datalib/libextract) is the name of the library
that implements this algorithm. To demonstrate the results, I render the
unstyled HTML of the extracted elements. Or in other words, it's going
to look ugly.

Best result: 

<figure markdown="1"> 
	<img class="pure-img" src="https://i.imgur.com/sQ5WbCZl.png" alt="AOL wiki - libextract" title=""></img> 
	<figcaption markdown="1"> 
		No style is the new style. Here we've extract the references.
	</figcaption>
</figure>

Second best result:

<figure markdown="1"> 
	<img class="pure-img" src="https://i.imgur.com/PTHYH2rl.png" alt="AOL wiki - libextract" title=""></img> 
	<figcaption markdown="1"> 
		Here you can see we've extacted the main body of the wiki page. 
		It's clear how awesome it would be to have post-processing, data-cleaning
		steps. Maybe for the next release?
	</figcaption>
</figure>

---

### Reddit

*target: [r/aww](http://www.reddit.com/r/aww)*


#### import.io
<figure markdown="1"> 
	<img class="pure-img" src="https://i.imgur.com/f6Qzi6Ll.png" alt="r/aww - import.io" title=""></img> 
	<figcaption markdown="1">  
		[Test it out.](https://magic.import.io/?site=http:%2F%2Fwww.reddit.com%2Fr%2Faww)
		Import.io clearly has the upper hand. They elegantly clean the data into a tabular format.
	</figcaption>
</figure>

#### Diffbot

<figure markdown="1"> 
	<img class="pure-img" src="https://i.imgur.com/4b3FBojl.png" alt="r/aww - diffbot" title=""></img> 
	<figcaption markdown="1"> 
		Diffbot results are similar to import.io's, minus the fancy styling.
	</figcaption>
</figure>

#### embed.ly

<figure markdown="1"> 
	<img class="pure-img" src="https://i.imgur.com/G3tpLnIl.png" alt="r/aww - embed.ly" title=""></img> 
	<figcaption markdown="1"> 
		[Test it out.](http://embed.ly/docs/explore/extract?url=http%3A%2F%2Fwww.reddit.com%2Fr%2Faww)
		Embed.ly extracts the images fine, but nothing close to tabular data.
	</figcaption>
</figure>

#### libextract

Second best result: 

<figure markdown="1"> 
	<img class="pure-img" src="https://i.imgur.com/vLxPJiyl.png" alt="r/aww - libextract" title=""></img> 
	<figcaption markdown="1"> 
		Like Diffbot and import.io's but absolutely no styling. 
		I never said it would look pretty.
	</figcaption>
</figure>

The top result is the top bar subreddits. No point in showing that. 

---

### NYTimes

*target: [NYTimes - Dead birds](http://www.nytimes.com/2015/05/15/business/bird-flu-outbreak-chicken-farmers.html)*

#### embed.ly

<figure markdown="1"> 
	<img class="pure-img" src="https://i.imgur.com/BV4C6Cyl.png" alt="nytimes - embed.ly" title=""></img> 
	<figcaption markdown="1"> 
		[Test it out.](http://embed.ly/docs/explore/extract?url=http%3A%2F%2Fwww.nytimes.com%2F2015%2F05%2F15%2Fbusiness%2Fbird-flu-outbreak-chicken-farmers.html)
		Embed.ly wins this one (at least in terms of presentation), as its "cards" are something not seen in other the other extractors.
	</figcaption>
</figure>

#### Diffbot

<figure markdown="1"> 
	<img class="pure-img" src="https://i.imgur.com/uPMKocyl.png" alt="nytimes - diffbot" title=""></img> 
	<figcaption markdown="1"> 
		[Test it out.](http://www.diffbot.com/testdrive/?api=article&url=http%3A%2F%2Fwww.nytimes.com%2F2015%2F05%2F15%2Fbusiness%2Fbird-flu-outbreak-chicken-farmers.html%3Fgwh%3DCEA82EAED8027FA1CE80B287AD63C3D0%26gwt%3Dpay) Diffbot handles this one well. 
	</figcaption>
</figure>

#### import.io
<figure markdown="1"> 
	<img class="pure-img" src="https://i.imgur.com/2hFNLeKl.png" alt="nytimes - import.io" title=""></img> 
	<figcaption markdown="1"> 
		[Test it out.](https://magic.import.io/?site=http:%2F%2Fwww.nytimes.com%2F2015%2F05%2F15%2Fbusiness%2Fbird-flu-outbreak-chicken-farmers.html)
		Import.io is like, *meh, just another website for me*.
	</figcaption>
</figure>

#### libextract


<figure markdown="1"> 
	<img class="pure-img" src="https://i.imgur.com/FsWpOJ5l.png" alt="nytimes - libextract" title=""></img> 
	<figcaption markdown="1"> 
		That's it, data cleaning (and styling) is libextract's next feature.
	</figcaption>
</figure>

---

## More related work

Most work in tabular data extraction focuses mainly on HTML ``<table>`` 
extraction and processing. For instance, some tables have columns of 
only numerical values. A proper "processing" step would make note of 
that column's datatype (and possibly coerce the datatype in code).

[*Mining Tables from Large Scale HTML Texts* (2000) - Hsin-Hsi Chen, Shih-Chung Tsai and Jin-He Tsai*](http://www.aclweb.org/anthology/C00-1025)

A well-cited approach to deducing a ``<table>``'s schema - or what some 
call "extracting table schema".

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

Not to bash on the merits of the above research, but none of those 
solutions are easily available for the rest of us. 



<script type="text/javascript">
var addthis_share = addthis_share || {}
addthis_share = {
	passthrough : {
		twitter: {
			via: "rodricios",
			text: "Solving #data extraction in #Python"
		}
	}
}

</script>
<!-- Go to www.addthis.com/dashboard to customize your tools -->
<script type="text/javascript" src="//s7.addthis.com/js/300/addthis_widget.js#pubid=ra-55562a0c27b23012" async="async"></script>



<div id="disqus_thread"></div>
<script type="text/javascript">
    /* * * CONFIGURATION VARIABLES * * */
    var disqus_shortname = 'rodricios';
    
    /* * * DON'T EDIT BELOW THIS LINE * * */
    (function() {
        var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
        dsq.src = '//' + disqus_shortname + '.disqus.com/embed.js';
        (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
    })();
</script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript" rel="nofollow">comments powered by Disqus.</a></noscript>

<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-59748564-2', 'auto');
  ga('send', 'pageview');
</script>
