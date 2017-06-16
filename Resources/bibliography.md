# Bibliography

Our data is extremely "spatial" in nature, with the spatial component being primary, and other data being of less interest.  I have not currently
found much work in this direction.


## Synthetic data in mainstream statistics

There appears to be increasing interest in using "synthetic data" in "traditional" statistical databases, to allow interesting statistical research, while
not releasing confidential (e.g. census-level) data.  Much of this work seems to be motivated by traditional
[Imputation](https://en.wikipedia.org/wiki/Imputation_(statistics)) work (for adding missing values).

1. Ron Jarmin, Thomas Louis, Javier Miranda, "Expanding the Role of Synthetic Data at the U.S. Census Bureau".  [DOI: 10.3233/SJI-140813](http://content.iospress.com/articles/statistical-journal-of-the-iaos/sji00813). See http://digitalcommons.ilr.cornell.edu/ldi/14/
   - Looking at how synthetic data is being trialled with the US Census data.  Not terribly useful from the perspective of how to _generate_ such synthetic data.
2. Harrison Quicka, Scott H. Holanb, Christopher K. Wikleb, Jerome P. Reiterc, "Bayesian marked point process modeling for generating fully synthetic public use data with point-referenced geography"  [DOI: 10.1016/j.spasta.2015.07.008](https://doi.org/10.1016/j.spasta.2015.07.008).  See also https://arxiv.org/abs/1407.7795
   - Uses a [Bayesian hierarchical model](https://en.wikipedia.org/wiki/Bayesian_network)
     to generate synthetic data which has a spatial component-- they simulate categorical attributes at the first level,
     then use a marked point process for the spatial locations, and then simulate continuous data.  At each level, a prior is given, and then the real data
     is used to generate a posterior distribution which is used to generate the synthetic data.  There is an interesting discussion on how such synthetic
     data can still carry enough information for "attackers" to deduce (with high probability) private values, and how to assess this risk.
3. Abowd J.M., Lane J. (2004) "New Approaches to Confidentiality Protection: Synthetic Data, Remote Access and Research Data Centers." In: Domingo-Ferrer J., Torra V. (eds) Privacy in Statistical Databases. PSD 2004. Lecture Notes in Computer Science, vol 3050. Springer, Berlin, Heidelberg.  [DOI: 10.1007/978-3-540-25955-8_22](http://link.springer.com/chapter/10.1007/978-3-540-25955-8_22)  See also https://courses.cit.cornell.edu/jma7/abowd-lane-barcelona-2004.pdf
   - Describes ideas around the infrastructure needed to support data centres, with (partially) synthetic data being used to allow researchers to develop techniques, before those techniques are run securely on the real data (for example).


# Crime related links

## Offender movement patterns

1. Wiles, Costello, "The road to nowhere: The evidence for travelling criminals."  Home Office Research Study 207.
  [Briefing paper](http://www.popcenter.org/tools/offender_interviews/PDFs/WilesCostello.pdf)
  [Full paper](http://library.college.police.uk/docs/hors/hors207.pdf)

2. Analysis by Andrew Brumwell on offender movement.  I haven't been able to find a formal publication.  See however
   - Page 43 of [Become a Problem
Solving Crime Analyst](http://www.popcenter.org/library/reading/PDFs/55stepsUK.pdf)
   - [Slides from talk by Andrew Brumwell](http://www.intelligenceanalysis.net/NAWG%20-%20West%20Midlands.pdf)

3. A "pioneering study": [Crimes in Minneapolis - Proposals for prevention](https://www.ncjrs.gov/App/Publications/abstract.aspx?ID=41627).  Doesn't appear to be online or in the library.


## Victim patterns

1. Groff, La Vigne, "Mapping an Opportunity Surface of Residential Burglary".  [doi:10.1177/0022427801038003003](http://journals.sagepub.com/doi/abs/10.1177/0022427801038003003).


### Related papers

1. Alex David Singleton, Seth Spielman & Chris Brunsdon (2016) "Establishing
a framework for Open Geographic Information science", International Journal of Geographical
Information Science, 30:8, 1507-1521, [DOI: 
10.1080/13658816.2015.1137579](http://www.tandfonline.com/doi/full/10.1080/13658816.2015.1137579)
   - A call to arms for using open source software and data sources, but most importantly, for producing _reproducible_ geographic information science.  Contains some interesting comments on synthetic data.
