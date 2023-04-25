<div align=center>

<!-- ![](https://img.shields.io/tokei/lines/github/wuzue/vibora?style=flat) -->
<!-- ![](https://img.shields.io/github/issues-raw/wuzue/vibora) -->
![](https://img.shields.io/github/issues-closed-raw/wuzue/vibora)
<!-- ![](https://img.shields.io/github/issues-pr-raw/wuzue/vibora) -->
![](https://img.shields.io/github/issues-pr-closed-raw/wuzue/vibora)
![](https://img.shields.io/badge/Python-3.10%2B-blue)

</div>

<div align=center>
  <img width='300px' src='docs/assets/realfang.png'/>
</div>

<h1 align=center>A PDF manipulation tool.</h1>

<h3 align=center> With just one line you can convert a .PDF file to .PNG, .PNG to .PDF, merge files, compress, encrypt and much more.</h3>

<hr>    

<h2>How to use it:</h2>

If you are using Windows, download Poppler and add it to PATH:
```
https://github.com/oschwartz10612/poppler-windows/releases/ 
```
Clone the repo to your machine:
```
git clone https://github.com/wuzue/vibora
```
Make sure to install the required dependencies. They are located in the ```requirements.txt``` file.
```
pip install -r requirements.txt
```
Now just run the ```main.py``` file to see what you can do with vibora:
```
python main.py help
```

*Python 3.10+ required.*

<hr>

<h2>What can vibora do?</h2>

* Convert PDF to PNG
* Convert PDF to TXT
* Convert TXT to PDF
* Extract images from a PDF file
* Compress PDF
* Merge PDF files
* Encrypt and Decrypt a PDF file
* Compare PDF files at a low level
* Convert a PDF file content into audio
* Redact sensitive information in a PDF file
* And more things. See all the features in *python main.py help*.