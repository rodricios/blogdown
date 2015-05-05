Autocomplete and a Compression Algorithm
===

![middle-out](http://i.imgur.com/khrCYbT.jpg)
<figcaption>Photo:Isabella Vosmikova/HBO</figcaption>

*Note to the readers: feel free to skip this part, as it's unrelated
to the rest of this post.* This is a post that I've been wanting to
do in a long while now. About two months ago, I released a Python 
package [autocomplete](https://github.com/rodricios/autocomplete) 
on [reddit](http://www.reddit.com/r/Python/comments/2wjute/hi_two_months_ago_i_showed_you_guys_a_project/). 
If you visit GitHub repo, you'll find an illustration of [Markov 
chains](http://en.wikipedia.org/wiki/Markov_chain)
(the theoretical structure that is used for this autocomplete 
implementation) in the form of a letter to my younger siblings. 

But like many of my peers, I'm prone to and finally succumbed to the 
urge of overengineering; instead of just installing WordPress on my 
EC2 instance, I decided to automate blog-posting to my github.io page. 
Worth the effort? I can't say just yet.

*Second note to the readers:* I'm going to try to stick to a rather 
dry, but rhythmic way of explaining things. For every concept I bring 
up, I'm going to provide links to skip to or over sections that are either 
full of nomenclature or full of gross oversimplifications.  


---

Autocomplete
---

Everyone has an "autocomplete" program running in their brain. What 
do I mean? Tell yourself a sentence. Notice the order of the words are spoken. 

If your sentence started with "The", you *probably* didn't follow it with "and". 

###Markov chains

[*Skip to references*](#markov-chain-references)

A simple [Markov chain](#) was used to create [autocomplete](https://github.com/rodricios/autocomplete). 

In plain words, here's what autocomplete is: 

 1. a Python dict where...
   * each key is a word (let's call this the *previous word*), and... 
   * each *previous word* points to another dict; each dict acts as a frequency distribution where...
        * each key is a word that followed the *previous word*, and... 
	    * the value is this inner key's (word) *conditional frequency*

Here's how that structure would look like in Python: 

```python
autocomplete = {
	'the': {
		'same': 996, 
		'first': 652, 
		'most': 573,
		...
		'flexion': 1,
		'McCarthys':1
	},
	'tired': {
		'of': 11, 
		'and': 6, 
		'that': 2,
		...
	},
	...
}
```

With the above model, once you've typed "the", you'll be provided the top N 
words ordered by frequency (or what I called *conditional frequency* - a property
not so different from *[conditional probabilities](http://en.wikipedia.org/wiki/Conditional_probability)*).

The top 3 suggestions given by our model, for words after "the" are: *same, first, most*. 

Using the same 

<a name="markov-chain-references"></a>
###Markov chain references

What are these [Markov chains](http://en.wikipedia.org/wiki/Markov_chain) anyway? 
Here's what wikipedia has to say:

> [Markov chains] must possess a property that is usually characterized as "memoryless": 
the probability distribution of the next state depends only on the current 
state and not on the sequence of events that preceded it. 

What about the book [Peter Norvig](http://norvig.com) considers to be a 
[fantastic return on investment](http://www.amazon.com/review/R3GSYXSKRU8V17)? 


> We can model English with what are known as n-gram models, or Markov chains[...]
> We assume that the probability of the next word depends only on the previous 
> k words in the input. This gives a kth order Murkov approximation:
>
> P( X<sub>n</sub> = x<sub>n</sub> | X<sub>n-1</sub> = x<sub>n-1</sub>,..., X<sub>1</sub> = x<sub>1</sub> ) = P( X<sub>n</sub> = x<sub>n</sub> | X<sub>n-1</sub> = x<sub>n-1</sub>,. . . ,X<sub>n-k</sub> = x<sub>n-k</sub> )
>
> If we are working on a character basis, for example, we are trying to guess what the next character in a text will be given the preceding k characters. 
>
> *taken from pg. 77 in Foundations of Statistical Natural Language Processing, Manning & Schütze*

If you have the time to read through those sources, by all means do so. 

There are some things to point out between above implementation description and these last few references:

Frequency distributions are unnormalized probability distributions:
where frequencies can have values ranging from 0 to infinity (non-negative integers), 
probabilities have values ranging from 0 to 1. 

Autocomplete was implemented using frequency distributions; to provide completion suggestions, 
we return the top N most frequent words following the *previous word*. 

###The code



```
# "preparation" step
# for every word in corpus, normalize ('The' -> 'the'), insert to list
WORDS = re_split(large_collection_english_text)

# first model -> P(word)
# Counter constructor will take a list of elements and create a frequency distribution (histogram)
WORDS_MODEL = collections.Counter(WORDS)

# another preperation step
# [a,b,c,d] -> [[a,b], [b,c], [c,d]]
WORD_TUPLES = list(chunks(WORDS, 2))

# second model -> P(next word | prev. word) 
# I interpret "..| prev. word)" as saying "dictionary key 
# leading to seperate and smaller (than WORDS_MODEL) freq. dist. 
WORD_TUPLES_MODEL = {first:collections.Counter() for first, second in WORD_TUPLES}

for prev_word, next_word in WORD_TUPLES:
    # this is called the "conditioning" step where we assert
    # that the probability space of all possible "next_word"'s
    # is "conditioned" under the event that "prev_word" has occurred
    WORD_TUPLES_MODEL[prev_word].update([next_word])
```