# CHANGELOG

PyPI Developer Tools `dtools` namespace projects

### 2025-05-22 - Rebuilt docs for all projects for next PyPI releases

- circular-array 3.15.0
- containers 1.0.0
- fp 2.0.0
- iterables 2.0.0
- queues 2.0.0
- splitends 0.29.0

### 2025-05-20 - Broke out dtools.fp.iterables to its own repo

- dtools.fp.iterables -> dtools.iterables
- GitHub repo: https://github.com/grscheller/dtools-iterables/

### 2025-05-12 - MayBe and Xor moved

- from dtools.fp
- to dtools.containers

### 2025-05-10 - Changed GitHub name of this repo
    
- GitHub repo name change
  - grscheller/dtools-docs -> grscheller/dtools-namespace-projects
  - will double as a project homepage as well as the document repo

Date:   Mon May 5 02:43:45 2025 -0600

### 2025-05-05 Added dtools.containers project

- added dtools.containers project and deprecated dtools.tuples
- dtools.tuples content moved to dtools.containers
  - actually dtools.tuples repo just renamed to dtools.containers
    - this allows older PyPI source code links to keep working
    - thought necessary since my Boring Math Library not updated yet

### 2025-04-24: Decided to change name back to dtools-docs
    
- a PyPI project named dtools already exists
- unfortunately, I missed this back in January

### 2025-04-24: Renamed repo from dtools-docs to just dtools
    
- morphing README.md into a project-wide Homepage
- created CHANGELOG.md file
- removed README.md links to deprecated dtools.datastructures project

### 2025-03-31: Updates for new dtools project   Mon Mar 31 16:19:46 2025 -0600

- adding infrastructure for dtools.tuples

### 2025-03-28: updated docs for all dtools projects

- ran linters and against all dtools namespace repos

### 2025-02-06: Standardized dtools and bm docs

- standardized Developer Tools and Boring Math project documentation

### 2025-01-17: Created this repo - dtools-docs

- created this repo for pdoc generated dtools project documentation
  - purpose to keep actual source code repos smaller
  - detailed documentation generated from source code docstrings
  - replaces grscheller-pypi-namespace-docs 
    - older repo still exits as a "zombie" project
      - to keep older PyPI document links working
- added development documentation infrastructure for all dtools repos
  - dtools.datastructures
  - dtools.fp
  - dtools.circular-array
- generated docs for first PyPI releases under dtools namespace
