---
title: Asserting exceptions in JUnit
date: 2019-06-23 10:10:00 Z
tags:
- java
- junit
- test
layout: post
author: Cassio Mazzochi Molin
excerpt: This post explores some techniques for asserting exceptions in Java with JUnit.
image: "/images/posts/2019-06-23-asserting-exceptions-in-junit/cover.jpg"
image_source: https://unsplash.com/photos/8lItGdbjB6o
redirect_from:
  - /asserting-exceptions-in-junit/
---



This post explores some techniques for asserting exceptions in Java with JUnit.

<!--more-->



##### Table of contents 
{:.no_toc}

* TOC 
{:toc} 



## Using `try`-`catch` with `fail()`

In this approach, the code which is excepted to throw an exception is wrapped in a `try`-`catch` block.

Then the [`fail()`][org.junit.Assert.fail] method is called _immediately_ after the code that should throw the exception, so that if the exception is not thrown, the test fails. Then assertions can be performed on the exception that has been caught:

```java
import org.junit.Test;

import static org.hamcrest.CoreMatchers.instanceOf;
import static org.hamcrest.CoreMatchers.is;
import static org.junit.Assert.assertThat;
import static org.junit.Assert.fail;

public class UsingTryCatchWithFail {

    private Foo foo = new Foo();

    @Test
    public void doStuff_shouldThrowException() {

        try {

            // This method is expected to throw a FooException
            foo.doStuff();
            
            // If the exception is not thrown, the test will fail
            fail("Expected exception has not been thrown");

        } catch (FooException e) {

            assertThat(e.getMessage(), is("An exception has occurred"));
            assertThat(e.getCause(), instanceOf(IllegalStateException.class));
        }
    }
}
```



## Using `@Test` with `expected`

In this approach, the [`@Test`][org.junit.Test] annotation is used to indicate the [`expected`][org.junit.Test.expected] exception to be thrown in the test:

```java
import org.junit.Test;

public class UsingTestWithExpected {

    private Foo foo = new Foo();

    @Test(expected = FooException.class)
    public void doStuff_shouldThrowException() {

        foo.doStuff();
    }
}
```

While it's a simple approach, it lacks the ability of asserting both the message and the cause of the exception that has been thrown. As good exception messages are valuable, assertions on messages should be taken into account.

Also, depending on how the test is written, this approach should be discouraged: As the exception expectation is placed _around the whole test method_, this might not actually test what is itended to be tested, leading to _false positives results_, as shown below:

```java
@Test(expected = FooException.class)
public void prepareToDoStuff_shouldSucceed_doStuff_shouldThrowException() {

    // This method may throw a FooException, which may lead to a false positive result
    foo.prepareToDoStuff();

    // This is the method that is supposed to throw the actual FooException being asserted
    foo.doStuff();
}
```



## Using `@Rule` with `ExpectedException`

This approach uses the [`ExpectedException`][org.junit.rules.ExpectedException] rule to assert an exception and also gives the ability of making assertions on both the message and the cause of the exeption:

```java
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.ExpectedException;

import static org.hamcrest.core.IsInstanceOf.instanceOf;

public class UsingRuleWithExpectedException {

    private Foo foo = new Foo();

    @Rule
    public final ExpectedException thrown = ExpectedException.none();

    @Test
    public void doStuff_shouldThrowException() {

        thrown.expect(FooException.class);
        thrown.expectMessage("An exception has occurred");
        thrown.expectCause(instanceOf(IllegalStateException.class));

        foo.doStuff();
    }
}
```

While this approach attempts to fix the caveats of [`@Test`][org.junit.Test] with [`expected`][org.junit.Test.expected] to assert the exception message and cause, it also has issues when it comes to false positives:

```java
@Test
public void prepareToDoStuff_shouldSucceed_doStuff_shouldThrowException() {

    thrown.expect(FooException.class);
    thrown.expectMessage("An exception has occurred");
    thrown.expectCause(instanceOf(IllegalStateException.class));

    // This method may throw a FooException, which may lead to a false positive result
    foo.prepareToDoStuff();

    // This is the method that is supposed to throw the actual FooException being asserted
    foo.doStuff();
}
```

Finally, if the test follows [Behaviour-driven Development][wikipedia.bdd] (BDD), you'll find that [`ExpectedException`][org.junit.rules.ExpectedException] doesn't use such writing style.



## Using `assertThrows` from JUnit 5

JUnit 5 aims to solve some problems of JUnit 4 and also takes advantage of Java 8 features, such as lambdas.

When it comes to exceptions, the [`@Test`][org.junit.jupiter.api.Test] annotation no longer can be used for indicate the expected exception. As described above, this approach may lead to false positives and doesn't allow asserting on the exception itself. 

As replacement, JUnit 5 introduced the [`assertThrows()`][org.junit.jupiter.api.Assertions.assertThrows] method: It asserts that the execution of the supplied executable throws an exception of the expected type and returns the exception instance, so assertions can be performed on it. 

The test will fail if no exception is thrown, or if an exception of a different type is thrown.

```java
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.hamcrest.CoreMatchers.instanceOf;
import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

public class UsingAssertThrowsFromJUnit5 {

    private Foo foo = new Foo();

    @Test
    @DisplayName("doStuff method should throw exception")
    public void doStuff_shouldThrowException() {

        Throwable thrown = assertThrows(FooException.class, () -> foo.doStuff());

        assertThat(thrown.getMessage(), is("An exception has occurred"));
        assertThat(thrown.getCause(), instanceOf(IllegalStateException.class));
    }
}
```



## Using AssertJ

[AssertJ][assertj] provides a rich API for _fluent assertions_ in Java. It aims to improve the test code readability and make the maintenance of tests easier by providing strongly-typed assertions and intuitive failure messages.

If your tests use at least Java 8, then you can use AssertJ 3.x and leverage on lambdas for asserting exceptions:

```java
import org.junit.Test;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatExceptionOfType;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.assertj.core.api.Assertions.catchThrowable;

public class UsingAssertJWithJava8 {

    private Foo foo = new Foo();

    @Test
    public void doStuff_shouldThrowException_1() {

        assertThatExceptionOfType(FooException.class)
                .isThrownBy(() -> foo.doStuff())
                .withMessage("An exception has occurred")
                .withCauseExactlyInstanceOf(IllegalStateException.class);
    }

    @Test
    public void doStuff_shouldThrowException_2() {

        assertThatThrownBy(() -> foo.doStuff())
                .isInstanceOf(FooException.class)
                .hasMessage("An exception has occurred")
                .hasCauseExactlyInstanceOf(IllegalStateException.class);
    }

    @Test
    public void doStuff_shouldThrowException_3() {

        Throwable thrown = catchThrowable(() -> foo.doStuff());

        assertThat(thrown)
                .isInstanceOf(Exception.class)
                .hasMessage("An exception has occurred")
                .hasCauseExactlyInstanceOf(IllegalStateException.class);
    }

    @Test
    public void doStuff_shouldThrowException_4() {

        FooException thrown = catchThrowableOfType(() -> foo.doStuff(), FooException.class);

        assertThat(thrown)
                .hasMessage("An exception has occurred")
                .hasCauseExactlyInstanceOf(IllegalStateException.class);
    }
}
```

If your tests use Java 7, then you can use the `try`-`catch` with [`fail()`][org.junit.Assert.fail] approach with AssertJ 2.x and perform fluent assertions on the exception that has been thrown:

```java
import org.junit.Test;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.failBecauseExceptionWasNotThrown;
import static org.junit.Assert.fail;

public class UsingAssertJWithJava7 {

    private Foo foo = new Foo();

    @Test
    public void doStuff_shouldThrowException_1() {

        try {

            foo.doStuff();
            fail("Expected exception has not been thrown");

        } catch (FooException e) {

            assertThat(e)
                    .hasMessage("An exception has occurred")
                    .hasCauseExactlyInstanceOf(IllegalStateException.class);
        }
    }

    @Test
    public void doStuff_shouldThrowException_2() {

        try {

            foo.doStuff();
            failBecauseExceptionWasNotThrown(FooException.class);

        } catch (FooException e) {

            assertThat(e)
                    .hasMessage("An exception has occurred")
                    .hasCauseExactlyInstanceOf(IllegalStateException.class);
        }
    }
}
```



## Bottom line and my thoughts

After evaluating the approaches for asserting exceptions described above, I would avoid both [`@Test`][org.junit.Test] with [`expected`][org.junit.Test.expected] and [`@Rule`][org.junit.Rule] with [`ExpectedException`][org.junit.rules.ExpectedException] approaches, as they may lead to _false positive results_.

For Java 7, simply stick to the `try`-`catch` with [`fail()`][org.junit.Assert.fail] approach, even if the test look a bit clumsy.

If you are using at least Java 8 (which I really hope you are), then you can leverage the power of lambdas for assertions. And I strongly encourage you to consider using AssertJ, as it provides a fluent API and the assertions are very close to plain English, which boosts the readability of your tests.



  [assertj]: https://assertj.github.io/doc/
  [wikipedia.bdd]: https://en.wikipedia.org/wiki/Behavior-driven_development

  [org.junit.Assert.fail]: https://junit.org/junit4/javadoc/4.12/org/junit/Assert.html#fail()

  [org.junit.Test]: https://junit.org/junit4/javadoc/4.12/org/junit/Test.html
  [org.junit.Test.expected]: https://junit.org/junit4/javadoc/4.12/org/junit/Test.html#expected()

  [org.junit.Rule]: https://junit.org/junit4/javadoc/4.12/org/junit/Rule.html

  [org.junit.rules.ExpectedException]: https://junit.org/junit4/javadoc/4.12/org/junit/rules/ExpectedException.html

  [org.junit.jupiter.api.Assertions.assertThrows]: https://junit.org/junit5/docs/5.3.0/api/org/junit/jupiter/api/Assertions.html#assertThrows(java.lang.Class,org.junit.jupiter.api.function.Executable)
  [org.junit.jupiter.api.Test]: https://junit.org/junit5/docs/current/api/org/junit/jupiter/api/Test.html

  [org.assertj.core.api.Assertions]: https://static.javadoc.io/org.assertj/assertj-core/3.12.2/org/assertj/core/api/Assertions.html
