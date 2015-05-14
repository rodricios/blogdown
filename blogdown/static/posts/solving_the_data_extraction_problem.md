Solving the Data Extraction Problem
===

#####By Rodrigo Palacios, follow me on [twitter](https://twitter.com/rodricios), and [github](https://github.com/rodricios)

A Python implementation of this work can be found on [GitHub](https://github.com/datalib/libextract).

---

Yes, the clickbait title was unashamedely intentional. No, I'm not formally
solving anything (my apologies to all the formal-proof-loving people
I've mislead into my post). Yes, there's an algorithm.

## *The algorithm*

In not-so-plain words:

> Given a tree, return a list of all subtrees - sorted by the number of children relative to the root node in the subtree.

In Python: 

```python
	from requests import get
	from collections import Counter
	from lxml import html
	
	reddit_request = get('http://www.reddit.com/')
	#wiki_request = get('http://en.wikipedia.org/wiki/Information_extraction')

	parsed_doc = html.fromstring(reddit_request.content)
	
	# In SQL-like terms: select all parents
	parent_elements = parsed_doc.xpath('//*/..')
	
	parents_with_children_counts = []
	
	for parent in parent_elements:
	    children_counts = Counter([child.tag for child in parent.iterchildren()])
	    parents_with_children_counts.append((parent, children_counts))

	# This line, one could say, is what wraps this data-extraction 
	# algorithm up as a maximization/optimization algorithm
	parents_with_children_counts.sort(# x[1].most_common(1) gets the most frequent element
                                      # x[1].most_common(1)[0][1] gets the frequency value
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

The correct answer, I'd argue, is: *the sort of data that's produced by 
the source of that data*. But let's get specific. 

Websites are structured by HTML (sure, the styling is also partially 
responsible for the *visual* structure, but as you'll see later on, 
we don't *have* to take style sheets into account).

Before I continue, I'll give a bit of background as to why the heck 
I'm even tackling this problem. 

About 4 months ago, I debuted [eatiht](https://github.com/rodricios/eatiht) 
(a text-extracting library; the predecessor to this algorithm) on [reddit](http://www.reddit.com/r/compsci/comments/2ppyot/just_made_what_i_consider_my_first_algorithm_it/).
I can only say positiive things about doing so. For one, it's landed me an opportunity
to coauthor a paper with [Tim Weninger](http://www3.nd.edu/~tweninge/). 

It was Tim who introduced me to the *structured [tabular] data extraction* problem. 
He illustrated the scenario of trying to extract ``<table>``'s and table-like 
structures from a website.

### *A wild problem appears!*

Let's take [reddit](http://www.reddit.com):

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
	<figcaption>
		subreddits - there's a lot of ``li``'s 
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
HTML. But despite the lack of tables, it should be clear that there is tabular data on the 
front page of Reddit.

So what do? 

## Deconstruction

Clearly define what the problem is: 

*__Data__ (in the context of HTML) are collections of HTML elements. 
Visually, data is presented as rows or columns. Structurally, data 
is presented as a collection (__parent element__) of (__children__) elements.*

Some of you guys/gals may have asked *Aren't we practically talking about every
element in an HTML tree?*

Yup.

But now throw the phrase *frequently occuring* into the definition:

*Structurally, data is presented as a collection (__parent element__)
of __frequently occurring__ (__children__) elements.*

To reiterate clearly (hopefully):

1. We're looking for the *parents* of any elements of any tag.

2. We're looking for repetitive elements, or rather the *counts* of repetitive elements

In the case of reddit.com, we'd like to create some solution that will retrieve at least two collections:
the ``<ul>`` containing those ``<li>``'s; the parent ``<div>`` containing those inner ``<div>``'s. 

There's a catch: we can't directly target those HTML elements.

Having said all that, let's take out my prototyping weapon of choice, Python, and get to it. 

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

*We're looking for the __parents__ of any elements of any tag.*

```python
	# In SQL-like terms: select all parents
	parent_elements = parsed_doc.xpath('//*/..')
	
	# >>> parent_elements
	# [<Element html at 0x5a69818>,
	# <Element head at 0x5f4abd8>,
	# <Element body at 0x5f4ac28>,
	# <Element div at 0x5f4ac78>,
	# <Element div at 0x5f4acc8>,
	# <Element div at 0x5f4ad18>,
	# ..]
```

*We're looking for repetitive elements, or rather the __counts__ of repetitive elements*

```python
	from collections import Counter
	
	parents_with_children_counts = []
	
	for parent in parent_elements:
	    children_counts = Counter([child.tag for child in parent.iterchildren()])
	    parents_with_children_counts.append((parent, children_counts))
		
	# >>> parents_with_children_counts[:5]
	# [(<Element html at 0x5a69818>, Counter({'head': 1, 'body': 1})),
	# (<Element head at 0x5f4abd8>, Counter({'script': 7, ..., 'title': 1, 'style': 1})),
	# (<Element body at 0x5f4ac28>, Counter({'script': 4, 'div': 4, 'a': 1, 'p': 1})),
	# (<Element div at 0x5f4ac78>, Counter({'div': 3, 'a': 1})),
	# (<Element div at 0x5f4acc8>, Counter({'div': 1}))]
```

Finally, let's sort our list of parent, child counter by the *frequency* of the most common 
element in each *child counter*.

```python 
	# This line, one could say, is what wraps this data-extraction 
	# algorithm as a maximization/optimization algorithm
	parents_with_children_counts = sorted(parents_with_children_counts, 
	                                      # x[1] is the Counter object
	                                      # x[1].most_common(1) gets the most frequent element
	                                      # x[1].most_common(1)[0][1] gets the frequency value
	                                      key=lambda x: x[1].most_common(1)[0][1], 
	                                      reverse=True)
										  
	# >>> parents_with_children_counts[:5]
	# [(<Element div at 0x5f4ae08>, Counter({'a': 51})),
	# (<Element div at 0x5f64048>, Counter({'div': 51})),
	# (<Element ul at 0x5f5f048>, Counter({'li': 48})),
	# (<Element div at 0x5f613b8>, Counter({'div': 23})),
	# (<Element ul at 0x5f60048>, Counter({'li': 8}))]								  
```

### Results

Let's print out the text content from each of the retrived (extracted) elements' children:

```python
	>>> for child in parents_with_children_counts[0][0]:
    >>> 	print(child.text_content())
	announcements
	Art
	AskReddit
	...
	worldnews
	WritingPrompts
	edit subscriptions
```

So where's that coming from?

<figure>
	![Hidden list of subreddits](http://i.imgur.com/s7W7R4Bl.png)
	<figcaption> 
		Here's where. It's the *MY SUBREDDITS* button.
	</figcaption>
</figure>

Let's get the text content of the second and third retrieved elements:

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

After running the above steps on a [wikipedia page](http://en.wikipedia.org/wiki/Information_extraction), our top result is:

> Information extraction (IE) is the task of automatically extracting structured information from unstructured and/or semi-structured machine-readable documents. In most of the cases this activity concerns processing human language texts by means of natural language processing (NLP). Recent activities in multimedia document processing like automatic annotation and content extraction out of images/audio/video could be seen as information extraction. ...

In case anyone is wondering, the top result yielded the div containing the main article of the wiki page.

## Final Thoughts

So far, we've been able to extract what we came to extract: tabular data and article text.

To clarify, this algorithm extracts HTML elements that likely lead us to tabular data and article text. 

If people want to philosophize on reasons why this algorithm extracts
not only tabular data but also article text, then please do so! 

Undoubtedly, people will say *paragraph elements (``<p>``) are usually all 
declared in the same level (ie. they are all siblings) of any given HTML document.

This algorithm doesn't convert or format the extracted data. This in itself is another problem. Not
in any way less interesting :)

Anyways, I'm done working on extraction problems. I'd like to start working on something 
that can feed me. Did I mention that I'm hireable? Maybe I should start a company...

## Related work

There's a lot of research that has been done in this area. But there's one very
important piece of work that should be mentioned before the rest:

[*Fact or fiction: content classification for digital libraries* (2001) - Aidan Finn, Nicholas Kushmerik, Barry Smyth](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.21.3834&rep=rep1&type=pdf)

This 14 year old paper was not in my line of sight when I first wrote 
this algorithm (around the time Tim had presented the tabular-data-extraction
problem to me, which was 4 months ago). 

Okay, technically it was in my line of sight. Someone had linked the article
in a comment on my [eatiht post on reddit](http://www.reddit.com/r/compsci/comments/2ppyot/just_made_what_i_consider_my_first_algorithm_it/cmz1m4h).

Here's the thing, my lexicon at the time was so limited that I couldn't even 
acknowledge/respond to Yacoby's question about whether or not I 
"considered using a simple maximisation algorithm?" 

I should have responded with, *eatiht is a maximization algorithm*; instead, and I remember
this clearly, I was describing the algorithm up to the point of what's known 
as the [argmax](http://en.wikipedia.org/wiki/Arg_max) step (for whatever
reason, I couldn't put 2 and 2 together). 

Anyways, logically what should and would have followed after that
is a big moment of *Ohhhhh... It's been done before, and here it is:*

> The [information extraction] problem can now be viewed as an 
optimization problem. We must identify points i and j such that
we maximize the number of tag tokens below i and above j, while 
simultaneously maximizing the number of text tokens between i 
and j. The text is only extracted between i and j. 

I waited until I started gathering resources for this post; I read Yacoby's 
suggestion once again; I actually opened looked up the paper; I pressed ``ctrl-F``;
I typed "maxim". I had that moment like I had described above. 

All I can say about repeating 14 year old work is that [rediscovery of work](http://en.wikipedia.org/wiki/Gregor_Mendel#Rediscovery_of_Mendel.27s_work) happens.
According to an uncle of mine, who also happens to be a mathematician, 
history surrounding wavelet theory has that "work rediscovery" element 
in it. 

Anyways, is this algorithm a straight-up rework of *Fact or
fiction*? In my opinion, no. Is the previous (eatiht) algorithm I worked on
a rework/rediscovery of *Fact or fiction*? I'd say yes. 

The authors of *Fact or fiction* are describing the solution to
an "optimization" algorithm that can extract text. 

They were very close to describing the more general algorithm that 
I describe in this post, and that I have yet to pin a name to. Any ideas?

#### More related work

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

Not to bash on the merits of the above research, none of those 
solutions are easily available for the rest of us. 