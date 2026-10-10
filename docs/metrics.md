# Metric definitions

## Exact match

A prediction gets a score of 1.0 only when its string value exactly equals the reference answer.

## Normalized exact match

This metric strips whitespace and punctuation and compares lower-cased strings so trivial formatting differences do not produce false negatives.

## Token F1

Token F1 measures overlap between prediction tokens and reference tokens. It is useful for short free-form outputs, but it is not a factual correctness guarantee.

## Schema compliance

When a case includes an expected output schema, the metric checks required fields and basic types. It is helpful for structured generation but does not replace semantic correctness.
