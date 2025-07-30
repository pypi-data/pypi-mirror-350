<img align="center" height="70" src="https://i.imgur.com/kYSTmrt.png">

# `parsomics-core`

A tool for parsing omics data into a relational database.

##  Background

The development of the `parsomics` project (which now includes
[parsomics-core](https://gitlab.com/parsomics/parsomics-core),
[parsomics-api-server](https://gitlab.com/parsomics/parsomics-api-server),
[parsomics-plugin-interpro](https://gitlab.com/parsomics/parsomics-plugin-interpro),
etc) was driven by the needs of prokaryote metagenomics research, though aims
to be adaptable to other studies within bioinformatics. It was created at the
[Brazilian Biorenewables National Laboratory (LNBR)](https://lnbr.cnpem.br/)
within the [Brazilian Center for Research in Energy](https://cnpem.br/) and
Materials (CNPEM).

## Supported file formats and tools

- FASTA
- GFF
- dRep
- GTDB-Tk
- Interpro
- run_dbCAN

## Database schema

The `parsomics` database is structured as in the Entity-Relationship Diagram below:

![Entity-Relationship diagram of the parsomics database](https://i.imgur.com/lGfkn3l.png)

You can check out a scalable PDF version of this diagram at [assets/schema.pdf](assets/schema.pdf).

## License

This work is licensed under the terms of the GPL-3.0.

## Copyright

© 2025 Brazilian Center for Research in Energy and Materials (CNPEM).
