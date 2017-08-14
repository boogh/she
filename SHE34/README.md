

# SHE

SHE or Smart Heurisic Evaluation is a collaborative web application for supporting Heuristic Evaluation. The process of systematic development of user friendly interfaces or usability engineering involves constant evaluation of a system design through usability tests and inspection methods. Heuristic evaluation (HE) is one of the most important inspection methods in usability engineering, in which a number of usability experts evaluate the user interfaces based on a set of pre-defined principles or the so called "heuristics" and at the end, their findings will be merged in a summary report.

SHE is tool for supporting the whole process of heuristic evaluation. It is smart enough to recognize similarities between evaluations and recommend them as a potential merging candidate in the final report.
.It is built with [Python][0] using the [Django Web Framework][1].

###Running SHE 

To run SHE on your local machine follow these steps:

1) Cloning the source code from gitlab or github:

    `$ git clone https://erahnema@git.cs.upb.de/erahnema/she.git`
    
    Or alternatively from github: 

    `$ git clone https://github.com/boogh/she.git`

2) Creating a graphlab environment using Anaconda Python Environment (See [this installation guid][3])

  
    # Create a new conda environment with Python 2.7.x
   
    
     $ conda create -n gl-env python=2.7 anaconda=4.0.0
     
  
    # Activate the conda environment
    
     $ activate gl-env
     

    # Ensure pip is updated to the latest version
 
     $ conda update pip
     

    # Install licensed copy of GraphLab Create
  
    $ pip install --upgrade --no-cache-dir https://get.graphlab.com/GraphLab-
    Create/2.1/your registered email address here/your product key here/Graph
    Lab-Create-License.tar.gz
    
3) Installing the requirements of SHE and finally running SHE:

        $ pip install –r requirements.txt
        $ python manage.py makemigrations
        $ python manage.py migrate
        $ python manage.py runserver
        

####Note: 
In windows Django should be added to the path.


[0]: https://www.python.org/
[1]: https://www.djangoproject.com/
[3]: https://turi.com/download/install-graphlab-create-command-line.html
