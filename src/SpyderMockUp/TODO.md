# treeview

We need to move from an item-based item view to a model-based item-view.
Spyder 'owns' the 'treeView' object (as it is in charge of pane management)
this 'treeView' is *MODEL* based. A plugin (we thus) can register a *MODEL*
to the treeView, and interact with the model. This actually already takes 
care of the 'folding state' (I presume) ...

Spyder uses the following 2 libraries already :
    - [intervaltree (folding states)]
    - watchdog (to see if something changed in the project !!!)

For the time being we can stick to item based, and consentrate on the important
work, but upon integration with Spyder, we will need to do some work here !

If someone is in need of 'work', he can start figuring out how model based tree
views work :-)

# SpyderMockup document structure

We *ONLY* use icons from qtawesome (https://github.com/spyder-ide/qtawesome)
which includes the following :
    - Material Desing Icons (mdi) --> https://cdn.materialdesignicons.com/4.9.95/
    - Elusive Icons (ei) --> http://elusiveicons.com/icons/
    - Font Awesome
        (fa5)
        (fa5s) --> https://fontawesome.com/icons?d=gallery&s=solid&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.5.0,5.6.0,5.6.1,5.6.3,5.9.0&m=free
        (fa5b) --> https://fontawesome.com/icons?d=gallery&s=brands&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.5.0,5.6.0,5.6.1,5.6.3,5.9.0&m=free
        (fa) --> https://fontawesome.com/v4.7.0/icons/

We try to stick with the mdi icons for as long as it is workable!
(then the 'style' is consistent ;-)


In an ATE project, the structure under 'documentation' should reflect the structure under ~project/doc.

>>> next point only the icons as a visual representation, Spyder has the full implementation already

We recognize the following files (based on -last- extension) and those must be shown with the noted icon:

    .pdf                        mdi-file-pdf-outline   
    .doc / .docx / .odt         mdi-file-word-outline
    .xls / .xlsx / .ods         mdi-file-excel-outline
    .ppt / .pptx / .odp         mdi-file-powerpoint-outline
    .tex / .latex               mdi-file-outline + mdi-alpha-x    (la)tex
    .odf                        mdi-file-outline + mdi-exponent   formula
    .odg                        mdi-file-outline + mdi-draw       drawing
    .htm / .html                mdi-file-link-outline
    .png / .jpg /               mdi-file-image-outline            image
    .avi / .mp4                 mdi-file-video-outline            video
    .flac / .mid / .midi / .aac mdi-file-music-outline            audio
    .txt                        mdi-note-text-outline  
    .md                         mdi-file-outline + mdi-markdown
    .zip / .xz / .gz / .bz2     mdi-folder-zip-outline            compression
    
files that are not 'recognized' simply don't have an icon associated to them.


All folders under (and including) ~project/documentation have the following context menu:

    - 'Add file'               mdi-plus                           create an new (and empty) file with the desired extension.
                                                                  (no dialog, just make 'NewFile#.ext' in the current folder, then the user can rename it)
    - 'Import file'            mdi-file-download-outline          Copies -not-link- a file from anywhere on the file system to the current folder
                                                                  (use 'QtWidgets.QFileDialog.getExistingDirectory' & selectFileOnly or somehting like that)
    - 'Add folder'             mdi-folder-plus-outline            Adds a folder under the current folder.
                                                                  (no dialog, just make 'NewFoler#' in the current folder, then the user can rename it)
    - 'Import folder'          mid-folder-download-outline        Copies a folder from anywhere on the file system in the current folder
                                                                  (use 'QtWidgets.QFileDialog.getExistingDirectory' & 'QtWidgets.QFileDialog.ShowDirsOnly')
    - 'Rename'                 mdi-rename-box                     Renames the current folder (add a small dialog, beter yet, edit in the tree itself !!!)
      <separator>
    - 'Delete'                 mdi-delete-outline                 Deletes everything under the current folder ! (no confirmation dialog)
                                                                  Maybe the text 'Delete' can be made in RED ?!?

>>> following point is already available in Spyder, don't put too much effort in this   
                                                                  
All files under ~project/documentation have the folowing contet menu:
    
    - 'Edit'                   mdi-file-edit-outline              Opens the file in a new tab in QTextEdit
    - 'Rename'                 mdi-rename-box                     Renames the current file (add a small dialog, better yet, edit in the tree itself!!!)
      <separator>
    - 'Delete'                 mdi-delete-outline                 Deletes the current file ! (no confirmation dialog)
                                                                  Maybe the text 'Delete' can be made in RED ?!?
The ~project/documentation folder can not be deleted !
The ~project/documentation/standards folder can not be deleted !

# also

Under 'tests' and 'programs' (formerly 'flows'), the files are all python files, 
so there we need to have the following icons added to the tree:
    
    .py                       mdi-file-outline + mdi-language-python
    
all these files have the same context menu as above, thus :

    - 'Edit'                   mdi-file-edit-outline              Opens the file in a new tab in QTextEdit
    - 'Rename'                 mdi-rename-box                     Renames the current file (add a small dialog, better yet, edit in the tree itself!!!)
      <separator>
    - 'Delete'                 mdi-delete-outline                 Deletes the current file ! (no confirmation dialog)


    