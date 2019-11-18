library(zipcode)
library(tidyverse)
library(maps)
library(viridis)
library(ggthemes)
library(albersusa)#installed via github
#data
fm<-Export <- read_csv("~/Downloads/Export (1).csv")#the file we just downloaded
data(zipcode)
fm$zip<- clean.zipcodes(fm$zip)
#size by zip
fm.zip<-aggregate(data.frame(count=fm$FMID),list(zip=fm$zip,county=fm$County),length)
fm<- merge(fm.zip, zipcode, by='zip')