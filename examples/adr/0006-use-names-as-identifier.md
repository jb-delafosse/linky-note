# Use names as identifier

* Type: [ADR](adr.md)
* Status: [Accepted](accepted.md)
* Deciders: [John](john.md) [Richard](richard.md) [Sophia](sophia.md)
* Date: 2020-02-01
* Categorie: [Names](names.md)

## Context and Problem Statement

An option is listed at "Considered Options" and repeated at "Pros and Cons of the Options". Finally, the chosen option is stated at "Decision Outcome".

## Decision Drivers

* Easy to read
* Easy to write
* Avoid copy and paste errors

## Considered Options

* Repeat all option names if they occur
* Assign an identifier to an option, e.g., `[A] Use gradle as build tool`

## Decision Outcome

Chosen option: "Assign an identifier to an option", because 1) there is no markdown standard for identifiers, 2) the document is harder to read if there are multiple options.


## Linked References

* [Use dashes in filenames](0005-use-dashes-in-filenames.md)
  * Status: [Deprecated](deprecated.md) superseded by [ADR-0006](0006-use-names-as-identifier.md)
