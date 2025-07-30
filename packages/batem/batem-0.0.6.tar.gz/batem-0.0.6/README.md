# Setting up the teaching environment

Each question has a unique number so that you can use any kind of document to put your answers, providing the question numbers are mentioned. Don't wait for the end to test your way of collecting results. You can work directly in the notebook but be careful not to loose your responses (copy and export them regularly).

The lecture is designed as a tutorial to follow with an estimation of the needed time to solve each problem. It is composed of Jupyter notebooks, named notebookx_XXX.ipynb and example python files, located at the root folder. The core well-documented Python code is located in the _code__ and _ecommunity_ folders, but it's for curious people (it's not needed for solving the problems of the notebooks). Data like weather files (extension '.json'), thermal and physical properties (file named propertiesDB.xlsx) are located in the _data_ folder. When a file is generated, it will be located in the _result_ folder like physical parameters for simplified models (extension '.p'). All these folders can be reset thanks to the __"setup.ini" configuration file__.

Regarding your working environment, it is recommended to:
- Install the latest available version of Python (3.9 minimum but preferably 3.11) activating the checkbox "Install in the path of your operating system", either directly from the [Python distribution site](https://www.python.org/downloads/), or by using [Anaconda](https://www.anaconda.com/products/distribution), that embeds Python together with additional useful scientific librairies.
- Load and install the latest version of (Visual Studio code)[https://code.visualstudio.com] for your operating system and load from the VS studio extensions: Python from Microsoft and Jupyter from Microsoft.
- Go to the [git site of the building energy project](https://gricad-gitlab.univ-grenoble-alpes.fr/ploixs/batem) and download it as a zip file. Unzip and open with Visual Studio code. If the Internet connection is not tool slow, you can access a [MyMinder](https://bit.ly/3QbtIPK) site, where the code can be remote remotely.
- In the terminal of Visual Studio code, you can installed the modules dependencies using ```python3.X -m pip install -r requirements.txt```where x stands for the number of the Python version selected in Visual Studio code.
- Open the working folder with the unzipped files and double-click on the notebook you want. 
- Execute each cell following the proposed order.
  