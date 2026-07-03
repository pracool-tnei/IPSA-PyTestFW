Testing IPSA script is used for the purpose of basic testing IPSA files for every versions of its release.
BASIC TESTING I and BASIC TESTING III has been incorporated in the script at present.

Requirements:
1.  Enter the version of IPSA to be compared with as the BASE VERSION and the version of IPSA to compare as TEST VERSION.
2.  Provide the paths of file required for testing in the files list.
3.  Ensure that there is an existing folder Test Results/{BASE VERSION} with the files to be compared with for proper functioning of the script. If the folder doesn't exist, the user can create the said folder
    by commenting the following lines and run the script: 
    a.  Every function call of compareFiles()
    b.  GeneratePDF.generateGlobalPDF()
4.  Open IPSA (test version) run Testing IPSA script.

Limitations:
1.  The script at present runs each testing based on the file name and the contents saved in the file, This could be modified in the future to be more dynamic.

Created by:      Akshay V Menon
Modified by:     Ruben V Pulayath
Modified Date :  17/04/2026