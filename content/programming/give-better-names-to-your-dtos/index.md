---
title: Give better names to your DTOs
date: 2016-02-11
tags:
- java
- dto
summary: Ideas of meaningful names for your DTOs.
aliases:
- /give-better-names-to-your-dtos/
---

The [Java Language Specification][1] states the following regarding the [name convention for classes][2]:


> Names of class types should be descriptive nouns or noun phrases, not overly long, in mixed case with the first letter of each word capitalized.
>
> <!-- language: lang-java -->
>
> ```java
> ClassLoader
> SecurityManager
> Thread
> Dictionary
> BufferedInputStream
> ```

Having said that, your [**D**ata **T**ransfer **O**bject][3] class names should follow the convention mentioned above.

---

Suffixing a class name with **DTO** or **Dto** won't tell much about the class itself besides indicating it carries data without any behaviour. So, instead of just calling your objects DTO, it might be worth considering more meaningful names, which convey better semantics for the classes.

Here are a few name suggestions you could use:

- <code>SomeSortOf**Command**</code>
- <code>SomeSortOf**Configuration**</code>
- <code>SomeSortOf**Credentials**</code>
- <code>SomeSortOf**Details**</code>
- <code>SomeSortOf**Element**</code>
- <code>SomeSortOf**Event**</code>
- <code>SomeSortOf**Filter**</code>
- <code>SomeSortOf**Header**</code>
- <code>SomeSortOf**Input**</code>
- <code>SomeSortOf**Instruction**</code>
- <code>SomeSortOf**Item**</code>
- <code>SomeSortOf**Message**</code>
- <code>SomeSortOf**Metadata**</code>
- <code>SomeSortOf**Operation**</code>
- <code>SomeSortOf**Output**</code>
- <code>SomeSortOf**Payload**</code>
- <code>SomeSortOf**Projection**</code>
- <code>SomeSortOf**Properties**</code>
- <code>SomeSortOf**QueryParameter**</code>
- <code>SomeSortOf**QueryResult**</code>
- <code>SomeSortOf**Representation**</code>
- <code>SomeSortOf**Request**</code>
- <code>SomeSortOf**Resource**</code>
- <code>SomeSortOf**Response**</code>
- <code>SomeSortOf**Result**</code>
- <code>SomeSortOf**Row**</code>
- <code>SomeSortOf**Settings**</code>
- <code>SomeSortOf**Specification**</code>
- <code>SomeSortOf**Status**</code>
- <code>SomeSortOf**Summary**</code>

---

**Note 1:** Whether acronyms or all capitalized words should be handled as words or not, I guess it's up to you. Check the [Java API][4] and you will find some stumbles like [`ZipInputStream`][5] / [`GZIPInputStream`][6]. Both classes are in the [same package][7] and the name convention is not consistent. [`HttpURLConnection`][8] doesn't show any consistency with acronyms either.

**Note 2:** Some names listed above were borrowed from this [article][9] written by [Richard Dingwall][10] (the original article seems to be no longer available, so [here's a cached copy][11] from Web Archive).


  [1]: https://docs.oracle.com/javase/specs/index.html
  [2]: https://docs.oracle.com/javase/specs/jls/se9/html/jls-6.html#jls-6
  [3]: https://en.wikipedia.org/wiki/Data_transfer_object
  [4]: https://docs.oracle.com/javase/9/docs/api/allclasses-frame.html
  [5]: https://docs.oracle.com/javase/9/docs/api/java/util/zip/ZipInputStream.html
  [6]: https://docs.oracle.com/javase/9/docs/api/java/util/zip/GZIPInputStream.html
  [7]: https://docs.oracle.com/javase/9/docs/api/java/util/zip/package-summary.html
  [8]: https://docs.oracle.com/javase/9/docs/api/java/net/HttpURLConnection.html
  [9]: http://rdingwall.com/2010/04/17/try-not-to-call-your-objects-dtos/
  [10]: https://stackoverflow.com/users/91551/richard-dingwall
  [11]: https://web.archive.org/web/20170614081139/http://rdingwall.com/2010/04/17/try-not-to-call-your-objects-dtos/
