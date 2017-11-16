---
layout:  post
title:   Give better names to your DTOs
author:  Cássio Mazzochi Molin
date:    2016-02-11 14:14:09Z
excerpt: Some ideas of meaningful names for your DTOs.
tags:    [java, dto]
image:   /images/give-better-names-to-your-dtos.jpg
---

The [Java Language Specification][1] states the following regarding the [name convention for classes][2]:

> Names of class types should be descriptive nouns or noun phrases, not overly long, in mixed case with the first letter of each word capitalized.
>
> <!-- language: lang-java -->
>
>     ClassLoader
>     SecurityManager
>     Thread
>     Dictionary
>     BufferedInputStream
>
> [...]

Your [**D**ata **T**ransfer **O**bject][3] class names should follow the convention mentioned above.

---

Suffixing a class name with **DTO** or **Dto** is not really meaningful and doesn't tell much about the class itself. Try to give names that describe the purpose of your classes. Here are a few name suggestions you could use:

- _SomeSortOf_**Command**
- _SomeSortOf_**Configuration**
- _SomeSortOf_**Credentials**
- _SomeSortOf_**Details**
- _SomeSortOf_**Element**
- _SomeSortOf_**Event**
- _SomeSortOf_**Header**
- _SomeSortOf_**Instruction**
- _SomeSortOf_**Item**
- _SomeSortOf_**Message**
- _SomeSortOf_**Metadata**
- _SomeSortOf_**Operation**
- _SomeSortOf_**QueryParameter**
- _SomeSortOf_**QueryResult**
- _SomeSortOf_**Representation**
- _SomeSortOf_**Request**
- _SomeSortOf_**Response**
- _SomeSortOf_**Result**
- _SomeSortOf_**Row**
- _SomeSortOf_**Settings**
- _SomeSortOf_**Specification**
- _SomeSortOf_**Status**
- _SomeSortOf_**Summary**
- _SomeSortOf_**View**

---

<sup>**Note 1:** Whether acronyms will be handled as words or not, I guess it's up to you. Check the [Java API][4] and you will find some stumbles like [`ZipInputStream`][5] / [`GZIPInputStream`][6]. Both classes are in the [same package][7] and the name convention is not consistent. [`HttpURLConnection`][8] doesn't show any consistency with acronyms either.</sup>

<sup>**Note 2:** Some names listed above were borrowed from this [article][9] written by [Richard Dingwall][10].</sup>


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