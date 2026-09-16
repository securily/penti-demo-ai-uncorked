# GOAL — the books must match the cash

Harbor Books closed December rent.
The register and the cash must tell the same story.

If they do not match, the books are wrong.

One slice per loop.

```dod
DOD-01 | unchecked | cmd | see-budget | books | books/budget.csv | The register
DOD-02 | unchecked | cmd | see-spent | books | books/receipt.txt | The cash
DOD-03 | unchecked | cmd | write-left | books | books/leftover.csv | The books match
```
