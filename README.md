# Generate-IR-Functions

**cite** contains an implementation to generate IR functions as described in our ECIR 2014 [paper](http://ama.liglab.fr/Khronos/Docs/ECIR2014.pdf). If you find this code useful in your research, please consider citing:

    @inproceedings{Goswami:2014,
        author = {Goswami, Parantapa and Moura, Simon and Gaussier, Eric and Amini, Massih-Reza and Maes, Francis},
        title = {Exploring the Space of IR Functions},
        booktitle = {Proceedings of the 36th European Conference on IR Research on Advances in Information Retrieval - Volume 8416},
        series = {ECIR 2014},
        year = {2014},
        isbn = {978-3-319-06027-9},
        location = {Amsterdam, The Netherlands},
        pages = {372--384},
        numpages = {13},
        url = {http://dx.doi.org/10.1007/978-3-319-06028-6_31},
        doi = {10.1007/978-3-319-06028-6_31},
        acmid = {2963525},
        publisher = {Springer-Verlag New York, Inc.},
        address = {New York, NY, USA},
        keywords = {Automatic Discovery, Function Generation, IR Theory},
    }

### Usage

    python2.7 Generate_IR_Functions.py

You will be asked for 3 integers:

1. `Enter max depth :` Maximum number of symbols per function. E.g. `sqrt(x)-log(y)` contains 5 symbols : `sqrt, x, -, log and y`.
2. `Keep functions >= N :` Write only functions that have more than N symbols
3. `Save every N valid results : ` Save the last N valid functions discovered.

### Dependencies
* [sympy](http://www.sympy.org/fr/index.html)
