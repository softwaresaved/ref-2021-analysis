# Environment statements (text)

Converted from [environment statements](environment_statements) using the [pdftotext(1)](https://manpages.debian.org/bookworm/poppler-utils/pdftotext.1.en.html) tool from poppler-utils

Script used to convert the PDFs; first change to the folder containing the PDFs

```shell
#!/bin/sh

for i in *.pdf; do
  pdftotext -layout "$i"
done
```

Then the `*.txt` files are copied into this folder.

Package used to convert to text is
[poppler-utils 22.12.0](https://packages.debian.org/bookworm/poppler-utils).
The conversion was done on a Debian bookworm system on a x86_64 architecture.

The script is not dockerised but can be done based on the `debian:bookworm-slim`
image if required.
