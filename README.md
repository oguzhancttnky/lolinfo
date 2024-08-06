# lolinfo

lolinfo fetches data from mobalytics.gg gives informations about champion.

![Screenshot from 2024-08-06 11-42-01](https://github.com/user-attachments/assets/1b50757c-5d17-43aa-9fb8-2543f31ac1ab)


# Installation

Clone this repository
```
git clone https://github.com/oguzhancttnky/lolinfo.git
```
Navigate to folder
```
cd lolinfo
```
Now you can run lolinfo
```
pip install -r requirements.txt
python main.py
```
Or you can containerize it.
Firstly build the Docker image
```
docker build -t lolinfo .
```
Then run Docker container from the image named lolinfo 
```
sudo docker run -it lolinfo
```
