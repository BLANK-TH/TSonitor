Constants
=============
Constants is another configuration file that's a bit more complicated. Generally you shouldn't ever touch anything in
here unless instructed to or you know exactly what you're doing.

- *ttt*:
    - *regex*: :sup:`Named regex for each type of action listed`\
    - **log_header**: *Full line of the header indicating the start of TTT logs*
    - **log_separator**: *Full line of the footer/separator indicating the end of TTT logs*
    - *utility_weapon_names*: :sup:`List of weapon names that count as utility`\
- *jb*:
    - *regex*: :sup:`Named regex for each type of action listed`\
    - **log_header**: *List of all 3 lines that indicate the start of JB logs*
    - **log_separator**: *List of all 3 lines that indicate the end of JB logs*
    - *utility_weapon_names*: :sup:`Pairs of utility names and their corresponding weapon names`\
- *age*:
    - **regex**: *Named regex for each line in status*
    - **header**: *Full line of the header indicating the start of a status output*
    - **footer**: *Full line of the footer indicating the end of a status output*
- **error_threshold**: *Number of errors the program will attempt to recover from before exiting*
