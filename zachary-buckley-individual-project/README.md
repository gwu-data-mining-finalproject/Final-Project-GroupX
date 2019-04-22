# Individual Project Contents

The document describes the contents of my individual project folder.

## Code

The code contained in the Code folder are snapshots of the Code that was used in
constructing the paper, gui, and powerpoint presentation for our project, as I my
developed my portions or major contributions to the shared codebase.

### GUI Code

For the GUI, I developed a pattern we could use, starting with the [Demo.ui](Code/Demo.ui) file that was built using the designer file. The simple [genGUICode](Code/genGUICode) bash script was then used to generate [generated_gui.py](Code/generated_gui.py). Next I spent quite a bit of time working out how to get threaded operations to function in the pyQt GUI, and to my pleasant surprise it was fairly similar to the mechanisms used in java swing GUIs, which I've worked with before.
I ended up with [driver.py](Code/driver.py), which is responsible for launching the initializing the DEMO object that ultimately contains the runtime data structures for the GUI. The DEMO object is defined in [DEMO.py](Code/DEMO.py), and generally just contains the dataframe, and gui component objects. The wiring that really makes the GUI function is in [NetflixDataPanel.py](Code/NetflixDataPanel.py). The latest versions of these files, as they exist in the Group Project, can be found here:

* [Demo.ui](../Code/gui/Demo.ui)
* [genGUICode](../Code/gui/genGUICode)
* [generated_gui.py](../Code/gui/generated_gui.py)
* [driver.py](../driver.py)
* [NetflixDataPanel.py](../Code/gui/NetflixDataPanel.py)

### EDA

In building the slides and presentation it was necessary for us to build a number of plots and charts, I helped my group perform this task. Some of that effort was was captured in [Histograms.ipynb](Code/Histograms.ipynb). Largely this involved pulling in the reduced sample of data, and the full dataset (which does require a system with a decent amount of RAM.. mine has 16GB), and simply plotting various histograms.

Prior to that, we were exploring different aspects of the application somewhat independently, though never without some communication taking place. I had pursued the possibility of pulling the ratings data into a sparse matrix. Based on a lot of different attempts, and digging around the web. I was able to find a solution that utilizes the python array library to make better use of RAM, rapidly building multiple array's incrementally. And then utilizing numpy's fromBuffer function, and scipy's COO matrix type. This code is in [txt_to_sparse_ratings.py](Code/txt_to_sparse_ratings.py). *NOTE: this code was written early on in the project, and thus is potentially not compatible with its structure at this point.*

Another avenue I investigated for a bit, was the possibility of importing data from IMDB, though we ultimately decided against incorporating it in the final project due to the number of issues we still hadn't worked through, it was simply one too many things. My Code for that effort can be found in [IMDBImportResearch.ipynb](Code/IMDBImportResearch.ipynb). To my frustration, I actually did end up building up this file twice due to an unfortunately timed use of `git clean -dxf`.

### Preprocessing Code

To support the GUI software, I developed a function to unzip the original netflix data, which was ultimately fairly trivial. But also worked out a pattern for functions that would need to be ran by the gui... namely:

```python
def default_progress_handler(progress):
  print('progress happening:', progress)

def something_that_takes_time(arg1, arg2, progress_handler=default_progress_handler):
  #do things...
  return retVal
```

The code responsible for the decompression process is in [netflix_data.py](Code/netflix_data.py), which has been included in the final group code for the gui [here](../Code/processing/netflix_data.py). [netflix_data.py](Code/netflix_data.py) also contains the load_from_txt function that the gui utilizes for pulling all the netflix data into memory. I spent a lot of time getting that function running quickly, and ultimately used the same approach (modified) that I found for reading in the sparse matrix data quickly. The version of load_from_txt that we started with, was done by pedro, in [txt_to_csv.py](../pedro-uria-individual-project/Code/txt_to_csv.py).  

The group code responsible for reducing the dataframe being manipulated by the preprocessing gui is [downsample.py](../Code/preprocessing/downsample.py). I rearranged a version of these functions that pedro had built originally [downsample.py](../pedro-uria-individual-project/Code/downsample.py), ending up with [downsample.py](Code/downsample.py), which is pretty much the same version we're now using.

## Documents

Here you'll find a copy of the [final group project report](Individual-Final-Project-Report/Final-Group-Project-Report). For additional information on who did what portion of this report, please contact Aaron Gauthier, and he'll provide access to the google doc version control history. It didn't seem feasible to really figure out who worked on what part of this report as we all touched just about every section before pulling together the final version we're now using.
