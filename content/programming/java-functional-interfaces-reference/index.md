---
title: Java functional interfaces reference
date: 2022-07-15
tags:
- java
summary:  This post is a quick reference on the built-in functional interfaces available in the Java API.
aliases: 
- /2022/07/15/java-functional-interfaces-reference/
featured: true
---

This post is a quick reference on the built-in functional interfaces available in the Java API.

A [functional interface][functional-interface] is an interface that has **exactly one abstract method**. It may also contain `default` and `static` methods which do have an implementation. Functional interfaces will most likely be annotated with [`@FunctionalInterface`][FunctionalInterface], indicating that the annotated interface in intented to be a functional interface, as defined above.

Functional interfaces were introduced in Java 8, are associated with [lambda expressions][lambda-expressions], and are extensively used in the [`Stream` API][java.util.stream]. So you certainly want to be familiar with the main [built-in functional interfaces][java.util.function], along with what they take as input and produce as output:

<!--
| Functional interface                            |            Input | → | Output      |
|:------------------------------------------------|-----------------:|:-:|:------------|
| [`Consumer<T>`][Consumer]                       |              `T` | → |             |
| [`Supplier<T>`][Supplier]                       |                  | → | `T`         |
| [`Function<T,R>`][Function]                     |              `T` | → | `R`         |
| [`Predicate<T>`][Predicate]                     |              `T` | → | `boolean`   |
-->

| Functional interface                            | Functional method                                 |            Input | → | Output      |
|:------------------------------------------------|:--------------------------------------------------|-----------------:|:-:|:------------|
| [`Consumer<T>`][Consumer]                       | `void accept(T t)`                                |              `T` | → |             |
| [`Supplier<T>`][Supplier]                       | `T get()`                                         |                  | → | `T`         |
| [`Function<T,R>`][Function]                     | `R apply(T t)`                                    |              `T` | → | `R`         |
| [`Predicate<T>`][Predicate]                     | `boolean test(T t)`                               |              `T` | → | `boolean`   |

For variations on the input arguments and results, the following tables will come handy:

{{< table-of-contents >}}

## Consumers

A **consumer** represents an operation that accepts a single input argument and returns no result.

<!--
| Functional interface                            |            Input | → | Output      |
|:------------------------------------------------|-----------------:|:-:|:------------|
| [`Consumer<T>`][Consumer]                       |              `T` | → |             |
| [`BiConsumer<T,U>`][BiConsumer]                 |           `T, U` | → |             |
| [`DoubleConsumer`][DoubleConsumer]              |         `double` | → |             |
| [`IntConsumer`][IntConsumer]                    |            `int` | → |             |
| [`LongConsumer`][LongConsumer]                  |           `long` | → |             |
| [`ObjDoubleConsumer<T>`][ObjDoubleConsumer]     |      `T, double` | → |             |
| [`ObjIntConsumer<T>`][ObjIntConsumer]           |         `T, int` | → |             |
| [`ObjLongConsumer<T>`][ObjLongConsumer]         |        `T, long` | → |             |
-->

| Functional interface                            | Functional method                                 |            Input | → | Output      |
|:------------------------------------------------|:--------------------------------------------------|-----------------:|:-:|:------------|
| [`Consumer<T>`][Consumer]                       | `void accept(T t)`                                |              `T` | → |             |
| [`BiConsumer<T,U>`][BiConsumer]                 | `void accept(T t, U u)`                           |           `T, U` | → |             |
| [`DoubleConsumer`][DoubleConsumer]              | `void accept(double value)`                       |         `double` | → |             |
| [`IntConsumer`][IntConsumer]                    | `void accept(int value)`                          |            `int` | → |             |
| [`LongConsumer`][LongConsumer]                  | `void accept(long value)`                         |           `long` | → |             |
| [`ObjDoubleConsumer<T>`][ObjDoubleConsumer]     | `void accept(T t, double value)`                  |      `T, double` | → |             |
| [`ObjIntConsumer<T>`][ObjIntConsumer]           | `void accept(T t, int value)`                     |         `T, int` | → |             |
| [`ObjLongConsumer<T>`][ObjLongConsumer]         | `void accept(T t, long value)`                    |        `T, long` | → |             |


## Suppliers

A **supplier** represents an operation that accepts no arguments and returns a result.

<!--
| Functional interface                            |            Input | → | Output      |
|:------------------------------------------------|-----------------:|:-:|:------------|
| [`Supplier<T>`][Supplier]                       |                  | → | `T`         |
| [`BooleanSupplier`][BooleanSupplier]            |                  | → | `boolean`   |
| [`DoubleSupplier`][DoubleSupplier]              |                  | → | `double`    |
| [`IntSupplier`][IntSupplier]                    |                  | → | `int`       |
| [`LongSupplier`][LongSupplier]                  |                  | → | `long`      |
-->

| Functional interface                            | Functional method                                 |            Input | → | Output      |
|:------------------------------------------------|:--------------------------------------------------|-----------------:|:-:|:------------|
| [`Supplier<T>`][Supplier]                       | `T get()`                                         |                  | → | `T`         |
| [`BooleanSupplier`][BooleanSupplier]            | `boolean getAsBoolean()`                          |                  | → | `boolean`   |
| [`DoubleSupplier`][DoubleSupplier]              | `double getAsDouble()`                            |                  | → | `double`    |
| [`IntSupplier`][IntSupplier]                    | `int getAsInt()`                                  |                  | → | `int`       |
| [`LongSupplier`][LongSupplier]                  | `long getAsLong()`                                |                  | → | `long`      |


## Functions

A **function** represents an operation that accepts argument(s) and produces a result.
For operations meant to return `boolean` results, have a look at the predicates in the next section.

<!--
| Functional interface                            |            Input | → | Output      |
|:------------------------------------------------|-----------------:|:-:|:------------|
| [`Function<T,R>`][Function]                     |              `T` | → | `R`         |
| [`DoubleFunction<R>`][DoubleFunction]           |         `double` | → | `R`         |
| [`IntFunction<R>`][IntFunction]                 |            `int` | → | `R`         |
| [`LongFunction<R>`][LongFunction]               |           `long` | → | `R`         |
| [`ToDoubleFunction<T>`][ToDoubleFunction]       |              `T` | → | `double`    |
| [`ToIntFunction<T>`][ToIntFunction]             |              `T` | → | `int`       |
| [`ToLongFunction<T>`][ToLongFunction]           |              `T` | → | `long`      |
| [`DoubleToIntFunction`][DoubleToIntFunction]    |         `double` | → | `int`       |
| [`DoubleToLongFunction`][DoubleToLongFunction]  |         `double` | → | `long`      |
| [`IntToDoubleFunction`][IntToDoubleFunction]    |            `int` | → | `double`    |
| [`IntToLongFunction`][IntToLongFunction]        |            `int` | → | `long`      |
| [`LongToDoubleFunction`][LongToDoubleFunction]  |           `long` | → | `double`    |
| [`LongToIntFunction`][LongToIntFunction]        |           `long` | → | `int`       |
| [`UnaryOperator<T>`][UnaryOperator]             |              `T` | → | `T`         |
| [`DoubleUnaryOperator`][DoubleUnaryOperator]    |         `double` | → | `double`    |
| [`IntUnaryOperator`][IntUnaryOperator]          |            `int` | → | `int`       |
| [`LongUnaryOperator`][LongUnaryOperator]        |           `long` | → | `long`      |
| [`BiFunction<T,U,R>`][BiFunction]               |           `T, U` | → | `R`         |
| [`BinaryOperator<T>`][BinaryOperator]           |           `T, T` | → | `T`         |
| [`ToDoubleBiFunction<T,U>`][ToDoubleBiFunction] |           `T, U` | → | `double`    |
| [`ToIntBiFunction<T,U>`][ToIntBiFunction]       |           `T, U` | → | `int`       |
| [`ToLongBiFunction<T,U>`][ToLongBiFunction]     |           `T, U` | → | `long`      |
| [`DoubleBinaryOperator`][DoubleBinaryOperator]  | `double, double` | → | `double`    |
| [`IntBinaryOperator`][IntBinaryOperator]        |       `int, int` | → | `int`       |
| [`LongBinaryOperator`][LongBinaryOperator]      |     `long, long` | → | `long`      |
-->

| Functional interface                            | Functional method                                 |            Input | → | Output      |
|:------------------------------------------------|:--------------------------------------------------|-----------------:|:-:|:------------|
| [`Function<T,R>`][Function]                     | `R apply(T t)`                                    |              `T` | → | `R`         |
| [`DoubleFunction<R>`][DoubleFunction]           | `R apply(double value)`                           |         `double` | → | `R`         |
| [`IntFunction<R>`][IntFunction]                 | `R apply(int value)`                              |            `int` | → | `R`         |
| [`LongFunction<R>`][LongFunction]               | `R apply(long value)`                             |           `long` | → | `R`         |
| [`ToDoubleFunction<T>`][ToDoubleFunction]       | `double applyAsDouble(T value)`                   |              `T` | → | `double`    |
| [`ToIntFunction<T>`][ToIntFunction]             | `int applyAsInt(T value)`                         |              `T` | → | `int`       |
| [`ToLongFunction<T>`][ToLongFunction]           | `long applyAsLong(T value)`                       |              `T` | → | `long`      |
| [`DoubleToIntFunction`][DoubleToIntFunction]    | `int applyAsInt(double value)`                    |         `double` | → | `int`       |
| [`DoubleToLongFunction`][DoubleToLongFunction]  | `long applyAsLong(double value)`                  |         `double` | → | `long`      |
| [`IntToDoubleFunction`][IntToDoubleFunction]    | `double applyAsDouble(int value)`                 |            `int` | → | `double`    |
| [`IntToLongFunction`][IntToLongFunction]        | `long applyAsLong(int value)`                     |            `int` | → | `long`      |
| [`LongToDoubleFunction`][LongToDoubleFunction]  | `double applyAsDouble(long value)`                |           `long` | → | `double`    |
| [`LongToIntFunction`][LongToIntFunction]        | `int applyAsInt(long value)`                      |           `long` | → | `int`       |
| [`UnaryOperator<T>`][UnaryOperator]             | `T apply(T t)`                                    |              `T` | → | `T`         |
| [`DoubleUnaryOperator`][DoubleUnaryOperator]    | `double applyAsDouble(double operand)`            |         `double` | → | `double`    |
| [`IntUnaryOperator`][IntUnaryOperator]          | `int applyAsInt(int operand)`                     |            `int` | → | `int`       |
| [`LongUnaryOperator`][LongUnaryOperator]        | `long applyAsLong(long operand)`                  |           `long` | → | `long`      |
| [`BiFunction<T,U,R>`][BiFunction]               | `R apply(T t, U u)`                               |           `T, U` | → | `R`         |
| [`BinaryOperator<T>`][BinaryOperator]           | `T apply(T t1, T t2)`                             |           `T, T` | → | `T`         |
| [`ToDoubleBiFunction<T,U>`][ToDoubleBiFunction] | `double applyAsDouble(T t, U u)`                  |           `T, U` | → | `double`    |
| [`ToIntBiFunction<T,U>`][ToIntBiFunction]       | `int applyAsInt(T t, U u)`                        |           `T, U` | → | `int`       |
| [`ToLongBiFunction<T,U>`][ToLongBiFunction]     | `long applyAsLong(T t, U u)`                      |           `T, U` | → | `long`      |
| [`DoubleBinaryOperator`][DoubleBinaryOperator]  | `double applyAsDouble(double left, double right)` | `double, double` | → | `double`    |
| [`IntBinaryOperator`][IntBinaryOperator]        | `int applyAsInt(int left, int right)`             |       `int, int` | → | `int`       |
| [`LongBinaryOperator`][LongBinaryOperator]      | `long applyAsLong(long left, long right)`         |     `long, long` | → | `long`      |


## Predicates

A **predicate** (or boolean-valued function) represents an operation that accepts argument(s) and returns a `boolean` result. 

<!--
| Functional interface                            |            Input | → | Output      |
|:------------------------------------------------|-----------------:|:-:|:------------|
| [`Predicate<T>`][Predicate]                     |              `T` | → | `boolean`   |
| [`BiPredicate<T,U>`][BiPredicate]               |           `T, U` | → | `boolean`   |
| [`DoublePredicate`][DoublePredicate]            |         `double` | → | `boolean`   |
| [`IntPredicate`][IntPredicate]                  |            `int` | → | `boolean`   |
| [`LongPredicate`][LongPredicate]                |           `long` | → | `boolean`   |
-->

| Functional interface                            | Functional method                                 |            Input | → | Output      |
|:------------------------------------------------|:--------------------------------------------------|-----------------:|:-:|:------------|
| [`Predicate<T>`][Predicate]                     | `boolean test(T t)`                               |              `T` | → | `boolean`   |
| [`BiPredicate<T,U>`][BiPredicate]               | `boolean test(T t, U u)`                          |           `T, U` | → | `boolean`   |
| [`DoublePredicate`][DoublePredicate]            | `boolean test(double value)`                      |         `double` | → | `boolean`   |
| [`IntPredicate`][IntPredicate]                  | `boolean test(int value)`                         |            `int` | → | `boolean`   |
| [`LongPredicate`][LongPredicate]                | `boolean test(long value)`                        |           `long` | → | `boolean`   |


## Runnable

[`Runnable`][Runnable] was introduced back in JDK 1.0, and it's indeed a functional interface, as it defines exactly one abstract method which doesn't take any arguments neither returns a value:

<!--
| Functional interface                            |            Input | → | Output      |
|:------------------------------------------------|-----------------:|:-:|:------------|
| [`Runnable`][Runnable]                          |                  | → |             |
-->

| Functional interface                            | Functional method                                 |            Input | → | Output      |
|:------------------------------------------------|:--------------------------------------------------|-----------------:|:-:|:------------|
| [`Runnable`][Runnable]                          | `void run()`                                      |                  | → |             |



[functional-interface]: https://docs.oracle.com/javase/specs/jls/se17/html/jls-9.html#jls-9.8
[lambda-expressions]:   https://docs.oracle.com/javase/tutorial/java/javaOO/lambdaexpressions.html
[java.util.stream]:     https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/package-summary.html
[java.util.function]:   https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/package-summary.html
[FunctionalInterface]:  https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/FunctionalInterface.html
[Runnable]:             https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Runnable.html
[Consumer]:             https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/Consumer.html
[Supplier]:             https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/Supplier.html
[Function]:             https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/Function.html
[Predicate]:            https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/Predicate.html
[BiConsumer]:           https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/BiConsumer.html
[DoubleConsumer]:       https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/DoubleConsumer.html
[IntConsumer]:          https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/IntConsumer.html
[LongConsumer]:         https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/LongConsumer.html
[ObjDoubleConsumer]:    https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/ObjDoubleConsumer.html
[ObjIntConsumer]:       https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/ObjIntConsumer.html
[ObjLongConsumer]:      https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/ObjLongConsumer.html
[BooleanSupplier]:      https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/ObjLongConsumer.html
[DoubleSupplier]:       https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/DoubleSupplier.html
[IntSupplier]:          https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/IntSupplier.html
[LongSupplier]:         https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/LongSupplier.html
[DoubleFunction]:       https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/DoubleFunction.html
[IntFunction]:          https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/LongFunction.html
[LongFunction]:         https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/ToDoubleFunction.html
[ToDoubleFunction]:     https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/ToDoubleFunction.html
[ToIntFunction]:        https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/ToIntFunction.html
[ToLongFunction]:       https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/ToLongFunction.html
[DoubleToIntFunction]:  https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/DoubleToIntFunction.html
[DoubleToLongFunction]: https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/DoubleToLongFunction.html
[IntToDoubleFunction]:  https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/IntToDoubleFunction.html
[IntToLongFunction]:    https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/IntToLongFunction.html
[LongToDoubleFunction]: https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/LongToDoubleFunction.html
[LongToIntFunction]:    https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/LongToIntFunction.html
[UnaryOperator]:        https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/UnaryOperator.html
[DoubleUnaryOperator]:  https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/DoubleUnaryOperator.html
[IntUnaryOperator]:     https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/IntUnaryOperator.html
[LongUnaryOperator]:    https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/LongUnaryOperator.html
[BiFunction]:           https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/BiFunction.html
[BinaryOperator]:       https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/BinaryOperator.html
[ToDoubleBiFunction]:   https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/ToDoubleBiFunction.html
[ToIntBiFunction]:      https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/ToIntBiFunction.html
[ToLongBiFunction]:     https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/ToLongBiFunction.html
[DoubleBinaryOperator]: https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/DoubleBinaryOperator.html
[IntBinaryOperator]:    https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/IntBinaryOperator.html
[LongBinaryOperator]:   https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/LongBinaryOperator.html
[BiPredicate]:          https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/BiPredicate.html
[DoublePredicate]:      https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/DoublePredicate.html
[IntPredicate]:         https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/IntPredicate.html
[LongPredicate]:        https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/LongPredicate.html
